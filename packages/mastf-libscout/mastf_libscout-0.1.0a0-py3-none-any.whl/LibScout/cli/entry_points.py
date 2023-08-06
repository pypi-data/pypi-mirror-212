# All libscout entry points

import sys
import os
import argparse
import pathlib
import logging

from LibScout.cli import main
from LibScout.profile.caches import get_cache, PickleCache
from LibScout.core.matcher import MIN_CLASS_SCORE, MIN_PARTIAL_SCORE
from LibScout.core.robot import DEFAULT_SKIP_VERSIONS
from LibScout.files import DX_MIN_SDK_VERSION



def init_logging(args: argparse.Namespace) -> logging.Logger:
    # Setup logging: use pre-defined file or just set the logging level
    if os.path.exists(args.log_config):
        try:
            logging.basicConfig(filename=args.log_config, force=True, encoding="utf-8")
        except Exception as err:
            raise err
    else:
        log_levels = {
            0: logging.ERROR,
            1: logging.WARNING,
            2: logging.INFO,
            3: logging.DEBUG,
        }

        basic_log_level = min(3, max(0, args.verbose))
        logging.basicConfig(level=log_levels[basic_log_level])

    return logging.getLogger(main.LOGGER_BASE_NAME)


def get_htree_options(args) -> dict:
    options_dict = {}

    for option in args.htree:
        name, value = option.split(":")

        if name == "KP":  # TODO: rewrite
            options_dict["keep_packages"] = value.lower() == "true"
        elif name == "KC":
            options_dict["keep_classes"] = value.lower() == "true"
        elif name == "KM":
            options_dict["keep_methods"] = value.lower() == "true"
        elif name == "PC":
            options_dict["prune_classes"] = value.lower() == "true"
        elif name == "PM":
            options_dict["prune_methods"] = value.lower() == "true"
        elif name == "AC":
            options_dict["access_flags"] = int(value)

    return options_dict


def run_profile_library(args: argparse.Namespace, logger: logging.Logger) -> None:
    if not args.cache:
        cache = PickleCache()
    else:
        cache = get_cache(args.cache)

    main.profile_library(
        file_path=args.path,
        lib_data_path=args.library_data,
        android_jar=args.android_jar,  # or config.android_jar
        cache=cache,
        dest_path=args.output,
        force_overwrite=args.force,
        tmp_dir=args.tmp_dir,
        j2d_path=args.j2d_path,
        cleanup=args.cleanup,
        min_sdk_version=args.dx_min_sdkv,
        htree_options=get_htree_options(args),
    )


def run_identify_libs(args: argparse.Namespace, logger: logging.Logger) -> None:
    if not args.cache:
        cache = PickleCache()
    else:
        cache = get_cache(args.cache)

    main.identify_libraries(
        files=args.path,
        android_jar=args.android_jar,
        profiles_path=args.profiles,
        cache=cache,
        dest_path=args.output,
        excluded=set(["de", "com", "org"]),
        htree_options=get_htree_options(args),
        parallel=args.parallel,
        force_overwrite=args.force,
        min_class_score=args.min_cls_score,
        min_partial_score=args.min_partial_score,
        analyze_api=args.analyze_api,
    )

def run_robot(args: argparse.Namespace, logger: logging.Logger) -> None:
    if (
        args.skip
        and os.path.exists(args.skip)
        and not os.path.isdir(args.skip)
    ):
        with open(args.skip, "r", encoding="utf-8") as fp:
            args.skip = fp.readlines()

    main.fetch_libraries(
        lib_files=args.path,
        local_repo=args.local_repo,
        skip_dev_versions=not args.with_dev,
        skip_keywords=args.skip or DEFAULT_SKIP_VERSIONS
    )


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    # Global options
    parser.add_argument(
        "-v",
        required=False,
        action="count",
        default=0,
        dest="verbose",
        help="Specifies the verbosity (use -vvv for more verbose output).",
    )
    parser.add_argument(
        "--log-config",
        required=False,
        default="logging.ini",
        help="File path to the logging configuration file.",
    )

    # Hash-Tree options
    parser.add_argument(
        "--htree",
        default=[],
        action="append",
        required=False,
        help=(
            "HashTree options: e.g. --htree KP:True AC:0 PC:True (available options: "
            "KC - keep classes, KP - keep packages, KM - keep meethods, "
            "PC - prune classes, PM - prune methods, AC - access flags as integer)"
        ),
    )

    sub_parsers = parser.add_subparsers(help="sub-commands:")

    # --- Profile parser ---
    profile_parser = sub_parsers.add_parser(
        name="profile",
        help="This module generates unique library fingerprints from original lib SDKs (.jar and .aar files supported).",
    )
    profile_parser.add_argument("path", help="File path to the library JAR/AAR file")
    profile_parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=None,
        help="Destination directory for the binary profile (optional - default './profiles')",
    )
    profile_parser.add_argument(
        "-a",
        "--android-jar",
        required=False,
        default=None,
        help="Path to the latest android.jar file",
    )
    profile_parser.add_argument(
        "-x",
        "--library-data",
        required=True,
        help="XML or JSON file storing the library base data.",
    )
    profile_parser.add_argument(
        "-C",
        "--cache",
        required=False,
        default=None,
        help="The LibProfileCache to use for import and export of profiles.",
    )
    profile_parser.add_argument(
        "-f",
        "--force",
        required=False,
        action="store_true",
        default=False,
        help="Forces LibScout to delete any existing profile files.",
    )
    profile_parser.add_argument(
        "--tmp-dir",
        required=False,
        default=None,
        help="Specify a custom temporary directory (default is os-specific).",
    )
    profile_parser.add_argument(
        "--j2d-path",
        required=False,
        default=None,
        help="Custom d2j-jar2dex path to use when compiling library classes.",
    )
    profile_parser.add_argument(
        "--cleanup",
        required=False,
        action="store_true",
        default=True,
        help="Specifies whether to remove temporary generated files afterwards (default: True)",
    )
    profile_parser.add_argument(
        "--dx-min-sdkv",
        required=False,
        default=DX_MIN_SDK_VERSION,
        help="Specifies the minimum SDK version used to generate DEX files.",
    )
    profile_parser.set_defaults(fn=run_profile_library)

    # --- Matcher parser ---
    matcher_parser = sub_parsers.add_parser(
        "match", help="Tries to identify libraries in one ore more APK files"
    )
    matcher_parser.add_argument(
        "path",
        help="File path(s) APK file(s) that should be scanned.",
        metavar="PATHS",
        action="append",
    )
    matcher_parser.add_argument(
        "-a",
        "--android-jar",
        required=True,
        default=None,
        help="Path to the (latest) android.jar file",
    )
    matcher_parser.add_argument(
        "-p",
        "--profiles",
        required=True,
        default=False,
        help="Forces LibScout to delete any existing profile files.",
    )
    matcher_parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=None,
        help="Destination path for the JSON report (optional)",
    )
    matcher_parser.add_argument(
        "-C",
        "--cache",
        required=False,
        default=None,
        help="The LibProfileCache to use for import and export of profiles.",
    )
    matcher_parser.add_argument(
        "-f",
        "--force",
        required=False,
        action="store_true",
        default=False,
        help="Forces LibScout to delete any existing JSON reports files.",
    )
    matcher_parser.add_argument(
        "--parallel",
        required=False,
        action="store_true",
        default=False,
        help="Forces LibScout to run the identifying process on multiple threads.",
    )
    matcher_parser.add_argument(
        "--analyze-api",
        required=False,
        action="store_true",
        default=False,
        help="Analyzes API usage of the scanned APK file.",
    )
    matcher_parser.add_argument(
        "--no-partial-matching",
        required=False,
        action="store_true",
        default=False,
        help="Disables partial matching and reduces the runtime of LibScout.",
    )
    matcher_parser.add_argument(
        "--min-cls-score",
        required=False,
        type=float,
        default=MIN_CLASS_SCORE,
        help="Specifies the minimum class score (relative amount of classes - float).",
    )
    matcher_parser.add_argument(
        "--min-partial-score",
        required=False,
        type=float,
        default=MIN_PARTIAL_SCORE,
        help="The minimum partial score to accept partial matches.",
    )
    matcher_parser.add_argument(
        "-E",
        "--excluded",
        required=False,
        default=None,
        help="Path to a file storing excluded package names for root packages.",
    )
    matcher_parser.set_defaults(fn=run_identify_libs)

    # --- Robot parser ---
    robot_parser = sub_parsers.add_parser("robot", help="Tries to download SDK files.")
    robot_parser.add_argument(
        "path",
        metavar="PATHS",
        nargs="+",
        help="One or more library-specs (JSON files)",
    )
    robot_parser.add_argument(
        "-R",
        "--local-repo",
        required=False,
        default=None,
        help="The root directory where to store library files.",
    )
    robot_parser.add_argument(
        "--with-dev",
        required=False,
        default=False,
        action="store_true",
        help="Downloads all versions (including -alpha, -beta).",
    )
    robot_parser.add_argument(
        "--skip",
        required=False,
        default=None,
        help="Path to a file storing exclusion keywords.",
    )
    robot_parser.set_defaults(fn=run_robot)
    return parser


def run_from_comand_line(*cmd):
    parser = setup_parser()
    args = parser.parse_args(cmd if cmd else None)

    # maybe load config files
    logger = init_logging(args)
    if "fn" not in args or not args.fn:
        logger.error("Invalid options - expected an operation mode!")
        return

    args.fn(args, logger)


if __name__ == "__main__":
    run_from_comand_line()
