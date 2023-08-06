from __future__ import annotations

import os
import re
import logging
import pathlib
import timeit
import json

from concurrent.futures import ThreadPoolExecutor

from LibScout.pkg import get_framework_pt
from LibScout.config import LOGGER_BASE_NAME, FILE_EXT_LIB_PROFILE

from LibScout.config import INDENT
from LibScout.profile import ProfileCache, PickleCache, export_app_stats
from LibScout.files import DX_MIN_SDK_VERSION
from LibScout.core.profiler import LibProfiler
from LibScout.core.matcher import LibMatcher, MIN_CLASS_SCORE, MIN_PARTIAL_SCORE
from LibScout.core.robot import LibRobot

logger = logging.getLogger(LOGGER_BASE_NAME)


def profile_library(
    file_path: str,
    lib_data_path: str,
    android_jar: str,
    cache: ProfileCache,
    dest_path: str = None,
    force_overwrite: bool = False,
    tmp_dir: str = None,
    j2d_path: str = None,
    cleanup: bool = False,
    min_sdk_version: int = DX_MIN_SDK_VERSION,
    excluded: set[str] | str = None,
    htree_options: dict = None,
) -> None:
    # 1. Prepare framework tree
    fw_tree = get_framework_pt(android_jar, excluded)

    # 2. Create profiler instance
    profiler = LibProfiler(
        cache=cache,
        framework_pt=fw_tree,
        tmp_dir=tmp_dir,
        excluded=excluded,
        jar2dex_path=j2d_path,
        cleanup=cleanup,
        min_sdk_version=min_sdk_version,
        htree_options=htree_options,
    )

    profile = profiler.extract_fingerprints(lib_data_path, file_path)
    clean_name = re.sub(r"\s+", "-", profile.name).replace("::", "__")
    if not dest_path:
        target_path = pathlib.Path("./profiles")
        target_path.mkdir(exist_ok=True, parents=True)
        dest_path = str(target_path)

    target_path = pathlib.Path(dest_path)
    if not target_path.is_dir():
        logger.warning("Moving destination to parent directory of %s", dest_path)
        target_path = target_path.parent

    if profile.version not in clean_name:
        clean_name = f"{clean_name}_{profile.version}"

    # Storing files under: profiles/{category}/{name}_{version}.pylib3
    target_path = target_path / profile.category
    target_path.mkdir(parents=True, exist_ok=True)
    dest_path = str(target_path / f"{clean_name}.{FILE_EXT_LIB_PROFILE}")
    logger.info("Saving %s to %s", profile, dest_path)
    if os.path.exists(dest_path) and not force_overwrite:
        logger.error(
            "File at destination path %s already exists (use --force to overwrite)",
            dest_path,
        )
        return

    cache.save_profile(profile, dest_path)


def _run_libmatch(
    matcher: LibMatcher,
    apk_file_path: str,
    dest_path: str = None,
    force: bool = False,
) -> None:
    # 7. identify libraries
    stats = matcher.identify_libs(apk_file_path)

    # 8. save collected stats
    destination = pathlib.Path(dest_path if dest_path else "temp.json")
    if destination.exists() and not force:
        logger.warning("Destination path at %s already exists - [SKIP]", destination)

    result = export_app_stats(stats, matcher.excluded)
    with open(str(destination), "w") as fp:
        json.dump(result, fp, indent=4)

    logger.info("Finished LibMatch operation on %s!", apk_file_path)


def identify_libraries(
    files: list[str],
    android_jar: str,
    profiles_path: str,
    cache: ProfileCache = None,
    dest_path: str = None,
    excluded: set[str] = None,
    amiguous: set[str] = None,
    htree_options: dict = None,
    **options,
) -> None:
    start = timeit.default_timer()
    # 1. Prepare framework tree
    fw_tree = get_framework_pt(android_jar, excluded=excluded)

    # 2. load profiles if we have a PickleCache
    if not cache:
        cache = PickleCache()

    if isinstance(cache, PickleCache):
        logger.info("Load library profiles: (from %s)", profiles_path)
        time = timeit.default_timer()
        for profile_file in pathlib.Path(profiles_path).rglob(
            f"*.{FILE_EXT_LIB_PROFILE}"
        ):
            cache.import_profile(profile_file)

        logger.info(
            "%s=> Imported %d library profiles (in %2fs)",
            INDENT[4],
            len(cache),
            timeit.default_timer() - time,
        )

    if len(cache) == 0:
        logger.warning("No library profiles loaded - quitting...")
        return

    # 3. Create executor if necessary
    executor = None
    if options.get("parallel", False):
        executor = ThreadPoolExecutor(thread_name_prefix="LibScout::Worker")

    # :options:
    force_overwrite = options.get("force_overwrite", False)
    analyze_api = options.get("analyze_api", False)
    no_partial = options.get("no_partial_matching", False)
    min_class_score = options.get("min_class_score", MIN_CLASS_SCORE)
    min_partial_score = options.get("min_partial_score", MIN_PARTIAL_SCORE)

    for apk_file_path in files:
        apk_path = pathlib.Path(apk_file_path)
        # Ignore invalid files
        if not apk_path.exists() or apk_path.is_dir():
            logger.warning("APK file not found at %s - [SKIP]", apk_file_path)
            continue

        # 4. Create matcher instance
        matcher = LibMatcher(
            cache=cache,
            fwpt=fw_tree,
            collect_lib_usage=analyze_api,
            excluded=excluded,
            ambiguous=amiguous,
            no_partial_matching=no_partial,
            min_class_score=min_class_score,
            min_partial_score=min_partial_score,
            htree_options=htree_options,
        )

        # 5. Run LibMatcher
        if executor is not None:
            executor.submit(
                _run_libmatch, matcher, apk_file_path, dest_path, force_overwrite
            )
        else:
            _run_libmatch(matcher, apk_file_path, dest_path, force_overwrite)

    if executor is not None:
        executor.shutdown(wait=True)
    logger.info("Global processing time: %2fs", timeit.default_timer() - start)


def fetch_libraries(
    lib_files: list[str],
    local_repo: str = None,
    skip_dev_versions: bool = True,
    skip_keywords: list[str] = None,
) -> None:
    robot = LibRobot(
        local_repo=local_repo,
        skip_dev=skip_dev_versions,
        skip_keywords=set(skip_keywords or []),
    )
    for file_path in lib_files:
        logger.info("+ Start download of lib-spec: %s", file_path)
        start = timeit.default_timer()
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            logger.warning("%s! Could not validate file at %s", INDENT[2], file_path)
            continue

        robot.run(file_path)
        logger.info("=> Finished download (in %2fs)", timeit.default_timer() - start)
