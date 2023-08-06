import sys
import re
import json
import pathlib
import logging
import urllib3
import shutil

from xml.etree import ElementTree
from LibScout.config import LOGGER_BASE_NAME, INDENT
from LibScout.files import FILE_EXT_AAR, FILE_EXT_JAR

logger = logging.getLogger(LOGGER_BASE_NAME)

# --- Constants ---

DEFAULT_LIB_FILE_NAME = "library.xml"
DEFAULT_SKIP_VERSIONS = ["-alpha", "-prealpha", "-beta", "-rc", "-dev", "-snapshot"]

DEFAULT_JCENTER_URL = "https://jcenter.bintray.com"


class LibRobot:
    def __init__(
        self,
        local_repo: str = None,
        skip_dev: bool = True,
        skip_keywords: set[str] = None,
    ) -> None:
        self.skip_dev = skip_dev
        self.skip_keywords = skip_keywords or DEFAULT_SKIP_VERSIONS
        self.local_repo = local_repo or "my-lib-repo"
        self._pool_manager = urllib3.PoolManager(timeout=1000.0)

    @property
    def local_dir(self) -> pathlib.Path:
        return pathlib.Path(self.local_repo)

    @property
    def manager(self) -> urllib3.PoolManager:
        return self._pool_manager

    def run(self, data: str | dict) -> None:
        logger.info("- Storing libraries to %s", self.local_dir)
        if isinstance(data, str):
            with open(data, "rb") as fp:
                data = json.load(fp)

        logger.info(
            "- Updating libraries%s",
            ":" if not self.skip_dev else "(skip dev versions):",
        )
        for lib_def in data["libraries"]:
            repo = lib_def.get("repo", None)
            if not repo:
                logger.warning(
                    "Skip library: %s (No repository defined)!", lib_def["name"]
                )
                continue

            self.fetch_library(
                lib_def["name"],
                lib_def["category"],
                lib_def.get("comment"),
                repo,
                lib_def["groupid"],
                lib_def["artifactid"],
            )

    def fetch_library(
        self,
        name: str,
        category: str,
        comment: str,
        url: str,
        group_id: str,
        artifact_id: str,
    ) -> None:
        # replace all blanks with dash
        name = re.sub(r"\s+", "-", name)
        logger.info(
            "%s# Check library %s [%s] (g:'%s', a:'%s')",
            INDENT[3],
            name,
            category,
            group_id,
            artifact_id,
        )

        local_lib_dir = self.local_dir / category / name.replace("::", "__")
        local_lib_dir.mkdir(parents=True, exist_ok=True)

        # Assemble base URL and retrieve meta data
        try:
            if url == "jcenter":
                url = DEFAULT_JCENTER_URL

            url = url.removesuffix("/")
            meta_url = f"{url}/{group_id.replace('.', '/')}/{artifact_id.replace('.', '/')}/maven-metadata.xml"

            response = self.manager.request("GET", meta_url, timeout=2000)
            data = ElementTree.fromstring(response.data) # TODO: maybe change
        except urllib3.exceptions.TimeoutError as err:
            logger.error("%s! TimeoutError: %s", INDENT[3], str(err))
            return

        except Exception as err:
            logger.exception("%s! Error during parsing: %s", INDENT[3], str(err))
            return

        # retrieve available versions
        versions = []
        for version_def in data.find("versioning"):
            for version_item in version_def.iter("version"):
                if not self.skip_dev or not any(
                    x in version_item.text.strip().lower() for x in self.skip_keywords
                ):
                    versions.append(version_item.text.strip())

        logger.info(
            "%s- Retrieved meta-data for %d versions:", INDENT[4], len(versions)
        )

        versions.sort()
        update_count = 0
        if len(versions) > 0:
            for version in versions:
                # skip lib version if already existing
                if not (self.local_dir / version / DEFAULT_LIB_FILE_NAME).exists():
                    update_count += 1
                    target_dir = local_lib_dir / version
                    target_file_type = FILE_EXT_AAR[1:]

                    result = self.download_file(
                        target_dir,
                        url,
                        group_id,
                        artifact_id,
                        version,
                        target_file_type,
                    )
                    if result == 1:
                        target_file_type = FILE_EXT_JAR[1:]
                        result = self.download_file(
                            target_dir,
                            url,
                            group_id,
                            artifact_id,
                            version,
                            target_file_type,
                        )

                    if result == 0:
                        logger.info(
                            "%s- Update version: %s, type: %s, target: %s",
                            INDENT[7],
                            version,
                            target_file_type,
                            target_dir,
                        )
                        target_file = target_dir / DEFAULT_LIB_FILE_NAME
                        self.write_description(
                            target_file, name, category, version, comment
                        )

        if update_count == 0:
            logger.info("%s-> All versions are up-to-date!", INDENT[6])
        else:
            logger.info("%s=> Downloaded %s updates!", INDENT[6], update_count)

    def download_file(
        self,
        target_dir: pathlib.Path,
        url: str,
        group_id: str,
        artifact_id: str,
        version: str,
        file_type: str,
    ) -> int:
        target_dir.mkdir(parents=True, exist_ok=True)

        # assemble download URL
        url_artifact_id = artifact_id.replace(".", "/")
        url_group_id = group_id.replace(".", "/")

        if url == "mvn-central":
            repo_url = "https://search.maven.org/remotecontent?filepath="
            target_file = f"{url_artifact_id}-{version}.{file_type}"
        else:
            repo_url = url
            target_file = f"{url_artifact_id}-{version}.{file_type}"

        dest_file = target_dir / target_file
        if dest_file.exists():
            return 0 # maybe log that

        # retrieve and save file
        repo_url = repo_url.removesuffix("/")
        url = f"{repo_url}/{url_group_id}/{url_artifact_id}/{version}/{target_file}"


        try:
            with open(dest_file, "wb") as fp:
                response = self.manager.request("GET", url, preload_content=False)
                if response.status == 404:
                    return 1

                shutil.copyfileobj(response, fp)
                response.release_conn()
                return 0
        except urllib3.exceptions.HTTPError as err:
            if file_type != FILE_EXT_AAR:
                logger.error(
                    "%s! HTTPError while retrieving %s file: %s",
                    INDENT[4],
                    file_type,
                    str(err),
                )
            return 1
        except Exception as err:
            logger.exception("%s! Download failed: %s", INDENT[4], str(err))
            return 1

    def write_description(
        self, target: pathlib.Path, name: str, category: str, version: str, comment: str
    ) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)

        with open(str(target), "w", encoding="utf-8") as descfp:
            descfp.write(DEFAULT_LIB_DESC_TEMPLATE % (name, category, version, comment))


DEFAULT_LIB_DESC_TEMPLATE = """<?xml version="1.0"?>
<library>
	<!-- library name, e.g. "Google Admob" -->
	<name>%s</name>

	<!-- category, any of "Advertising", "Analytics", "Android", "Cloud", "SocialMedia", "Utilities" -->
	<category>%s</category>

	<!-- optional: version string, e.g. "4.0.4" -->
	<version>%s</version>

	<!-- optional: date (format: dd.MM.yyyy  example: 21.05.2017) -->
	<releasedate></releasedate>

	<!-- optional: comment -->
	<comment>%s</comment>
</library>
"""
