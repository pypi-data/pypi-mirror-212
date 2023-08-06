from __future__ import annotations
import io

import sys
import os
import io
import pickle
import json

from xml.dom import minidom
from typing import Iterator

from LibScout.profile import LibProfile, ProfileCache
from LibScout.profile.base import LibProfile

__all__ = ["PickleCache"]


def get_cache(fmt: str) -> ProfileCache:
    class_name, *args = fmt.split(":")
    mod = sys.modules[__name__]

    if not hasattr(mod, class_name):
        raise NotImplementedError(
            f"Could not find requested client type: '{class_name}' in module "
            "LibScout.profile.caches - Make sure the class name matches the code."
        )

    positional = []
    keyword_args = {}
    for argument in args:
        if "=" in argument:
            key, value = argument.split("=")
            keyword_args[key] = value
        else:
            positional.append(argument)

    cache_type = getattr(mod, class_name)
    if not issubclass(cache_type, ProfileCache):
        raise TypeError(f"Expected a subclass of ProfileCache - got {cache_type}")

    return cache_type(*positional, **keyword_args)


KEY_NAME = "name"
KEY_CATEGORY = "category"
KEY_VERSION = "version"
KEY_RELEASE_DATE = "releasedate"  #: optional
KEY_COMMENT = "comment"  #: optional


class PickleCache(ProfileCache):
    profiles: list[LibProfile]

    def __init__(self, profiles: list[LibProfile] = None) -> None:
        super().__init__()
        self.profiles = profiles or []

    def import_profile(self, storage: str | io.IOBase) -> LibProfile:
        if isinstance(storage, io.IOBase):
            profile = pickle.load(storage)

        with open(storage, "rb") as libfp:
            profile = pickle.load(libfp)

        self.profiles.append(profile)
        return profile

    def save_profile(self, profile: LibProfile, dest: str | io.IOBase) -> bool:
        if not isinstance(dest, (str, io.IOBase)):
            raise TypeError(f"Invalid destination type: {type(dest).__name__}")

        if isinstance(dest, io.IOBase):
            pickle.dump(profile, dest, protocol=pickle.HIGHEST_PROTOCOL)
            return True

        if os.path.isdir(dest):
            return False

        with open(dest, "wb") as storage:
            pickle.dump(profile, storage)
        return True

    def load_profile_data(self, buf: dict | io.IOBase | str) -> LibProfile:
        # JSON and xml files should be accepted
        if isinstance(buf, dict):  # direct creation
            return LibProfile(
                package_tree=None,
                hash_trees=None,
                name=buf[KEY_NAME],  # not optional
                category=buf[KEY_CATEGORY],
                version=buf[KEY_VERSION],
                release_date=buf.get(KEY_RELEASE_DATE, ""),  # optional
                comment=buf.get(KEY_COMMENT, ""),
            )

        elif isinstance(buf, str):
            if buf.endswith(".json"):
                with open(buf, "rb") as docfp:
                    return self.load_profile_data(json.load(docfp))
            elif buf.endswith(".xml"):
                return self._xml_data(minidom.parse(buf))
            else:
                raise NotImplementedError(f"Invalid filename: {buf}")

        elif isinstance(buf, io.IOBase):
            return self.load_profile_data(json.load(buf))

        raise TypeError(f"Unsupported type: {type(buf).__name__}")

    def _xml_data(self, root: minidom.Document) -> LibProfile:
        return LibProfile(
            package_tree=None,
            hash_trees=None,
            name=self._get_xml_value(root, KEY_NAME),
            category=self._get_xml_value(root, KEY_CATEGORY),
            version=self._get_xml_value(root, KEY_VERSION),
            release_date=self._get_xml_value(root, KEY_RELEASE_DATE, optional=True),
            comment=self._get_xml_value(root, KEY_COMMENT, optional=True),
        )

    def _get_xml_value(self, element: minidom.Element, key: str, optional=False) -> str:
        node = element.getElementsByTagName(key)
        if len(node) == 0 and not optional:
            raise SyntaxError(f"Expected a <{key}> node")
        elif len(node) == 0 and optional:
            return ""

        value_node = node[0].childNodes
        if len(value_node) == 0:
            return ""
        return str(value_node[0].nodeValue).strip()

    def __len__(self) -> int:
        return len(self.profiles)

    def __iter__(self) -> Iterator[LibProfile]:
        return iter(self.profiles)


class LazyPickleCache(PickleCache):
    profile_meta: list[str]

    def __init__(self, profiles: list[LibProfile] = None) -> None:
        super().__init__(profiles)
        self.profile_meta = []
        self.profiles.clear()

    def import_profile(self, storage: str) -> LibProfile:
        if not isinstance(storage, str):
            raise TypeError("Only paths are allowed to be added to a LazyCache!")

        if storage not in self.profile_meta:
            self.profile_meta.append(storage)
        return None

    def __len__(self) -> int:
        return len(self.profile_meta)

    def __iter__(self) -> Iterator[LibProfile]:
        for storage in self.profile_meta:
            profile = super().import_profile(storage)
            self.profiles.clear()
            yield profile
