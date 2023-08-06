from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

LOGGER_BASE_NAME = "libscout"
INDENT = {x: " "*x for x in range(1, 10)}
FILE_EXT_LIB_PROFILE = "pylibv3"

HF = sha256

@dataclass
class LibScoutConfig:
    config_file_path: str = "./config/LibScoutConfig.toml"
    log_config_path: str = "./config/logging.ini"
    path_to_android: str | None = None

    no_partial_matching: bool = False
    lib_usage_analysis: bool = False
    verbose_profiles: bool = False # generate lib profiles with TRACE + PubOnly

    lib_dep_analysis: bool = False

    profiles_dir: str = "./profiles"

# These packages are excluded by default
FW_TYPES = ("android", "java", "dalvik", "kotlin", "androidx", "kotlinx")