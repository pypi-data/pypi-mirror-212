from __future__ import annotations

import pathlib
import tempfile
import zipfile
import subprocess
import sys

FILE_EXT_AAR = ".aar"
FILE_EXT_JAR = ".jar"
FILE_EXT_DEX = ".dex"

DX_MIN_SDK_VERSION = 26


def extract_aar_classes(aar_path: str, tmp_dir: str = None) -> str:
    """
    Extracts the classes.jar file from an AAR (Android Archive) file.

    :param aar_path: Path to the AAR file.
    :param tmp_dir: Optional. Path to the temporary directory for extraction. If not provided,
                    the system default temporary directory will be used.
    :return: Path to the extracted classes.jar file.
    :raises FileNotFoundError: If the AAR file or temporary directory is not found.
    """

    path = pathlib.Path(aar_path)
    if not path.exists():
        raise FileNotFoundError(f"AAR file not found at {aar_path}")

    tmp_dir = pathlib.Path(tmp_dir or tempfile.gettempdir())
    if not tmp_dir.exists():
        raise FileNotFoundError(f"Temp-Directory not found at {tmp_dir}")

    destination = str(tmp_dir / "classes.jar")
    with zipfile.ZipFile(aar_path) as zfile:
        zfile.extract("classes.jar", str(tmp_dir))

    return destination


def extract_dex_files(apk_path: str, tmp_dir: str = None) -> list[str]:
    """
    Extracts DEX (Dalvik Executable) files from an APK (Android Application Package) file.

    :param apk_path: Path to the APK file.
    :param tmp_dir: Optional. Path to the temporary directory for extraction. If not provided,
                    the system default temporary directory will be used.
    :return: List of paths to the extracted DEX files.
    :raises FileNotFoundError: If the APK file or temporary directory is not found.
    """

    path = pathlib.Path(apk_path)
    if not path.exists():
        raise FileNotFoundError(f"APK file not found at {apk_path}")

    tmp_dir = pathlib.Path(tmp_dir or tempfile.gettempdir())
    if not tmp_dir.exists():
        raise FileNotFoundError(f"Temp-Directory not found at {tmp_dir}")

    result = []
    with zipfile.ZipFile(apk_path) as zfile:
        for file_name in zfile.namelist():
            if file_name.endswith(FILE_EXT_DEX):
                destination = pathlib.Path(tmp_dir) / file_name
                if not destination.exists():
                    zfile.extract(file_name, str(tmp_dir))
                result.append(str(destination))

    return result


def convert_jar_classes(
    jar_path: str,
    tmp_dir: str = None,
    d2j_invoke_path: str = None,
    min_sdk_version: int = DX_MIN_SDK_VERSION,
) -> str:
    """
    Converts Java class files in a JAR (Java Archive) file to DEX (Dalvik Executable) format.

    :param jar_path: Path to the JAR file.
    :param tmp_dir: Optional. Path to the temporary directory for extraction. If not provided,
                    the system default temporary directory will be used.
    :param d2j_invoke_path: Optional. Path to the d2j_invoke script/executable for conversion.
                            If not provided, it will be assumed as "d2j_invoke.bat" on Windows
                            and "d2j_invoke.sh" on other platforms.
    :param min_sdk_version: Minimum SDK version for the generated DEX file. Default is 26.
    :return: Path to the converted DEX file.
    :raises FileNotFoundError: If the JAR file or temporary directory is not found.
    :raises RuntimeError: If the conversion process fails.
    """

    path = pathlib.Path(jar_path)
    if not path.exists():
        raise FileNotFoundError(f"JAR file not found at {jar_path}")

    tmp_dir = pathlib.Path(tmp_dir or tempfile.gettempdir())
    if not tmp_dir.exists():
        raise FileNotFoundError(f"Temp-Directory not found at {tmp_dir}")

    destination = str(tmp_dir / f"{path.stem}.dex")
    d2j_invoke_path = d2j_invoke_path or "d2j_invoke.%s" % (
        "bat" if "win" in sys.platform else "sh"
    )
    try:
        cmd = (
            f'{str(pathlib.Path(d2j_invoke_path))} com.android.dx.command.Main --dex --output="{destination}" '
            f"--no-strict --min-sdk-version={min_sdk_version} {str(path)}"
        )
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        return destination
    except subprocess.CalledProcessError as err:
        raise RuntimeError(err.stdout.decode()) from err
