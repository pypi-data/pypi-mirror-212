# Copyright (c) 2015-2017  Erik Derr [derr@cs.uni-saarland.de]
# Copyright (c) 2023 MatrixEditor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import logging
import io
import timeit
import lief
import pathlib

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Iterator, Iterable

from LibScout.config import LOGGER_BASE_NAME
from LibScout.pkg.tree import PackageTree
from LibScout.hashtree import generate_hash_tree, HashTree

logger = logging.getLogger(LOGGER_BASE_NAME)

__all__ = [
    "Profile",
    "LibProfile",
    "get_unique_profiles",
    "ProfileCache",
    "AppStats",
    "get_app_profile",
    "export_app_stats",
]


@dataclass
class Profile:
    """
    Represents a profile containing a package tree and hash trees.

    :param package_tree: The package tree associated with the profile.
    :type package_tree: PackageTree
    :param hash_trees: List of hash trees associated with the profile.
    :type hash_trees: list[HashTree]
    """

    package_tree: PackageTree
    hash_trees: list[HashTree]


@dataclass
class LibProfile(Profile):
    """
    Represents a library profile extending the base Profile class.

    :param name: The name of the library.
    :type name: str
    :param category: The category of the library.
    :type category: str
    :param version: The version of the library.
    :type version: str
    :param release_date: The release date of the library.
    :type release_date: str
    :param comment: Optional comment about the library.
    :type comment: str | None
    :param is_deprecated: Flag indicating if the library is deprecated. Defaults to False.
    :type is_deprecated: bool
    """

    name: str
    category: str
    version: str
    release_date: str
    comment: str | None = None
    is_deprecated: bool = False

    def __str__(self) -> str:
        """
        Returns a string representation of the library profile.

        :return: String representation of the library profile.
        :rtype: str
        """
        return f"{self.name} ({self.version})"

    def __repr__(self) -> str:
        """
        Returns a string representation of the library profile for debugging purposes.

        :return: String representation of the library profile.
        :rtype: str
        """
        return f"<LibProfile[{self.name}] version='{self.version}'>"


@dataclass
class AppStats:
    """Represents statistics related to an application.

    :param file_path: The file path of the application.
    :type file_path: str
    :param is_multidex: Flag indicating if the application uses multidex. Defaults to False.
    :type is_multidex: bool
    :param profile: The profile associated with the application. Defaults to None.
    :type profile: Profile | None
    :param matches: List of matches associated with the application. Defaults to an empty list.
    :type matches: list
    :param package_only_matches: Dictionary of package-only matches associated with the application.
        The keys represent the package names and the values represent the match descriptions.
        Defaults to an empty dictionary.
    :type package_only_matches: dict[str, str]
    :param processing_time: The processing time of the application in seconds. Defaults to 0.0.
    :type processing_time: float
    """

    file_path: str
    is_multidex: bool = False
    profile: Profile | None = None
    matches: list = field(default_factory=list)
    package_only_matches: dict[str, str] = field(default_factory=dict)
    processing_time: float = 0.0


def get_unique_profiles(profiles: Iterable[LibProfile]) -> dict[str, str]:
    """
    Get a dictionary of unique library profiles based on their names.

    If multiple profiles with the same name exist, only the one with the highest version
    number will be included in the result.

    :param profiles: Iterable of library profiles.
    :type profiles: Iterable[LibProfile]
    :return: Dictionary of unique library profiles with names as keys and highest versions as values.
    :rtype: dict[str, str]
    """
    result = {}
    for profile in profiles:
        if profile.name not in result:
            result[profile.name] = profile.version
        else:
            if result[profile.name] < profile.version:
                result[profile.name] = profile.version

    return result


def get_app_profile(
    dex_files: Iterable[lief.DEX.File],
    framework_tree: PackageTree = None,
    excluded: set[str] = None,
    **options,
) -> Profile:
    """
    Generate the profile of an application based on its DEX files.

    This function generates the package tree and hash trees for the application.

    :param dex_files: Iterable of DEX files representing the application.
    :type dex_files: Iterable[lief.DEX.File]
    :param framework_tree: Optional framework package tree. Defaults to None.
    :type framework_tree: Optional[PackageTree]
    :param excluded: Set of packages to exclude from the package tree. Defaults to None.
    :type excluded: Optional[Set[str]]
    :param options: Additional options for generating the hash trees.
    :return: Profile containing the package tree and hash trees of the application.
    :rtype: Profile
    """
    # Generate the app package tree
    package_tree = PackageTree()
    hash_trees = []
    start = timeit.default_timer()
    for dex in dex_files:
        package_tree.load(dex, excluded)
        hash_trees.append(generate_hash_tree(dex, framework_tree, **options))

    logger.info("- Generated app PackageTree (in %2fs)", timeit.default_timer() - start)
    logger.info("")
    package_tree.show(include_class_count=True, excluded=excluded)

    logger.info("- Generated app hash trees (in %2fs)", timeit.default_timer() - start)
    logger.info("")
    return Profile(package_tree, hash_trees)


class ProfileCache(ABC):
    """
    Abstract base class for a profile cache.
    """

    @abstractmethod
    def import_profile(self, storage: str | io.IOBase) -> LibProfile:
        """
        Import a profile from the given storage.

        :param storage: The storage from which to import the profile.
        :type storage: str or io.IOBase
        :return: The imported profile.
        :rtype: LibProfile
        """
        pass

    @abstractmethod
    def save_profile(self, profile: LibProfile, dest: str | io.IOBase) -> bool:
        """
        Save a profile to the specified destination.

        :param profile: The profile to save.
        :type profile: LibProfile
        :param dest: The destination where the profile will be saved.
        :type dest: str or io.IOBase
        :return: True if the profile was successfully saved, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def load_profile_data(self, buf: object | io.IOBase | str) -> LibProfile:
        """
        Load profile data from the given buffer.

        :param buf: The buffer from which to load the profile data.
        :type buf: object or io.IOBase or str
        :return: The loaded profile.
        :rtype: LibProfile
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[LibProfile]:
        """
        Iterate over the profiles in the cache.

        :return: An iterator over the profiles in the cache.
        :rtype: Iterator[LibProfile]
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """
        Get the number of profiles in the cache.

        :return: The number of profiles in the cache.
        :rtype: int
        """
        pass


def export_profile_match(pm, excluded: set[str] = None) -> dict:
    return {
        "lib_name": pm.lib_profile.name,
        "lib_version": pm.lib_profile.version,
        "is_original_package": not pm.is_lib_obfuscated(),
        "is_root_package": ""
        if not pm.get_matched_package_tree()
        else pm.get_matched_package_tree().get_root_package(excluded),
        "score": pm.best_match.score,
        "comment": pm.lib_profile.comment,
    }


def export_app_stats(stats: AppStats, excluded: set[str] = None) -> dict:
    ptree = stats.profile.package_tree
    pkg_only = {}
    matches = []

    libs_matched = set()
    exported_matches = {}
    for profile_match in stats.matches:
        if profile_match.best_match and profile_match.best_match.score > 0:
            lib_name = profile_match.lib_profile.name
            if lib_name not in exported_matches:
                # initialize list and add pm
                exported_matches[lib_name] = [profile_match]
            else:
                match_list = exported_matches[lib_name]
                # check if we have to add this pm to existing list
                if (
                    match_list[0].best_match
                    and match_list[0].best_match.score < profile_match.best_match.score
                ):
                    # replace list
                    match_list.clear()
                    match_list.append(profile_match)
                elif (
                    match_list[0].best_match
                    and match_list[0].best_match.score == profile_match.best_match.score
                ):
                    # add to existing list
                    match_list.append(profile_match)
            libs_matched.add(lib_name)

    # save the PM's that are to be exported
    for lib_name in exported_matches:
        for pm in exported_matches[lib_name]:
            matches.append(export_profile_match(pm, excluded))

    # save all library names that did not match via profiles but via root package name
    for pkg in stats.package_only_matches:
        if pkg not in libs_matched:
            pkg_only[pkg] = stats.package_only_matches[pkg]

    return {
        "app_info": {
            # REVISIT: maybe use androguard to extract other information as well
            "file_name": pathlib.Path(stats.file_path).name,
            "is_multidex": stats.is_multidex,
        },
        "stats": {
            "package_count": ptree.non_empty_packages,
            "class_count": ptree.app_classes,
            "processing_time": stats.processing_time,
        },
        "matches[package_only]": pkg_only,
        "matches": matches,
    }
