from __future__ import annotations

import os
import logging
import timeit
import pathlib
import lief

from LibScout.profile import ProfileCache, LibProfile
from LibScout.config import LOGGER_BASE_NAME, INDENT
from LibScout.files import (
    extract_aar_classes,
    convert_jar_classes,
    FILE_EXT_AAR,
    FILE_EXT_DEX,
    FILE_EXT_JAR,
    DX_MIN_SDK_VERSION
)

from LibScout.pkg import PackageTree, generate_package_tree
from LibScout.hashtree import generate_hash_tree

logger = logging.getLogger(LOGGER_BASE_NAME)


class LibProfiler:
    cache: ProfileCache

    def __init__(
        self,
        cache: ProfileCache,
        framework_pt: PackageTree = None,
        tmp_dir: str = None,
        excluded: set[str] = None,
        jar2dex_path: str = None,
        cleanup: bool = True,
        min_sdk_version=DX_MIN_SDK_VERSION,
        htree_options: dict = None,
    ) -> None:
        self.cache = cache
        self.framework_pt = framework_pt
        self._profile = None
        # options
        self.tmp_dir = tmp_dir
        self.excluded = excluded
        self.jar2dex_path = jar2dex_path
        self.cleanup = cleanup
        self.htree_options = htree_options or {}
        self.min_sdk_version = min_sdk_version

    def extract_fingerprints(self, lib_data_path: str, lib_path: str) -> LibProfile:
        start = timeit.default_timer()
        # read library description
        self._profile = self.cache.load_profile_data(lib_data_path)

        logger.info("Processing library: %s", self.lib_profile.name)
        logger.info("Library Description:")
        for line in str(self.lib_profile.comment).splitlines():
            logger.info("%s%s", INDENT[2], line)

        path = pathlib.Path(lib_path)
        if path.suffix == FILE_EXT_AAR:
            lib_path = extract_aar_classes(lib_path, self.tmp_dir)

        if not lib_path.endswith((FILE_EXT_DEX, FILE_EXT_JAR)):
            raise ValueError(f"Expected a .jar or .dex file - got {lib_path}")

        if lib_path.endswith(FILE_EXT_JAR):
            logger.info("Convert .class files of %s into single DEX file", lib_path)
            time = timeit.default_timer()
            dex_path = convert_jar_classes(lib_path, self.tmp_dir, self.jar2dex_path, self.min_sdk_version)
        else:
            dex_path = lib_path

        dex = lief.DEX.parse(dex_path)
        logger.info(
            "%s- DEX file created and parsed (%2fs)",
            INDENT[4],
            (timeit.default_timer() - time),
        )
        logger.info(
            "%s- Generate PackageTree of lib: %s", INDENT[4], self.lib_profile.name
        )
        time = timeit.default_timer()
        tree = generate_package_tree(dex, self.excluded)
        # maybe print stats
        if not tree.get_root_package(self.excluded):
            logger.warning("%s- Library contains multiple root packages!", INDENT[4])

        hash_tree = generate_hash_tree(dex, self.framework_pt, **self.htree_options)
        logger.info(
            "Generated HashTree and PackageTree (in %2fs)",
            (timeit.default_timer() - time),
        )
        self.lib_profile.package_tree = tree
        self.lib_profile.hash_trees = [hash_tree]

        if self.cleanup:
            # cleanup tmp files if library input was an .aar file
            if path.suffix == ".aar":
                os.remove(str(lib_path))
                logger.debug("[CLEAN] Jar removed at %s", str(lib_path))

            os.remove(dex_path)
            logger.debug("[CLEAN] Dex file removed at %s", dex_path)

        logger.info("")
        logger.info("Processing time: %2fs", (timeit.default_timer() - start))
        return self.lib_profile

    @property
    def lib_profile(self) -> LibProfile:
        return self._profile
