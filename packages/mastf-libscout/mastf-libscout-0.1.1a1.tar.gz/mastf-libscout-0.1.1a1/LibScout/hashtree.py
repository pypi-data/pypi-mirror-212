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

import hashlib
import re
import logging
import lief

from LibScout.pkg.tree import PackageTree
from LibScout.pkg.utils import normalize_name, get_package_name
from LibScout import ch
from LibScout.config import LOGGER_BASE_NAME, HF

METHOD_NODE = "MN"
CLASS_NODE = "CN"
PACKAGE_NODE = "PN"

logger = logging.getLogger(LOGGER_BASE_NAME)


class HashTreeNode:
    hash_value: str
    children: list["HashTreeNode"]
    node_type: str
    value: str  # class_name, method signature or package_name

    def __init__(self, hash_value: str | bytes, value: str, node_type: str) -> None:
        self.children = []
        self.value = value
        self.node_type = node_type
        self.hash_value = None
        if isinstance(hash_value, str):
            self.hash_value = hash_value
        elif isinstance(hash_value, bytes):
            self.hash_value = HF(hash_value).hexdigest()

        if not self.hash_value:
            raise ValueError("Invalid hash configuration")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, HashTreeNode):
            return False
        return __value.hash_value == self.hash_value

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __len__(self) -> int:
        return len(self.children)

    def __str__(self) -> str:
        return self.hash_value

    def __hash__(self) -> int:
        return hash(self.hash_value)

    def __repr__(self) -> str:
        return f"<{self.node_type} value='{self.value}'>"

    def __contains__(self, node: "HashTreeNode") -> bool:
        return node in self.children

    def __getstate__(self) -> object:
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)


INNER_CLASS_PATTERN = re.compile(r"^.+\$\d+$")

# @deprecated
def generate_hash_tree(
    dex: lief.DEX.File, fwpt: PackageTree = None, **options
) -> HashTree:
    tree = HashTree(**options)
    tree.load({x.fullname: x for x in dex.classes}, fwpt)
    return tree


class HashTree:
    root: HashTreeNode

    def __init__(
        self,
        access_flags: int = 0,
        keep_packages: bool = True,
        keep_classes: bool = False,
        keep_methods: bool = False,
        prune_classes: bool = False,
        prune_methods: bool = True,
    ) -> None:
        self.root = None
        self.access_flags = access_flags
        self.keep_packages = keep_packages
        self.keep_classes = keep_classes
        self.keep_methods = keep_methods
        self.prune_classes = prune_classes
        self.prune_methods = prune_methods
        # :meta: private
        self._class_hashes = 0
        self._method_hashes = 0

    def __str__(self) -> str:
        return self.root.hash_value

    def __repr__(self) -> str:
        return f"<HashTree {self.get_config()}>"

    def load(self, dex: dict[str, lief.DEX.Class], framework_tree: PackageTree) -> None:
        self._debug("Generate HashTree...")
        class_hashes = 0  # will be logged
        method_hashes = 0

        # create map package name -> set of clazzNodes
        package_map = {}
        for class_name in dex:
            class_def = dex[class_name]
            if not ch.is_app_class(class_def, framework_tree):
                continue

            name = normalize_name(class_name)
            # create mathod node objects
            method_nodes = []
            for method in class_def.methods:
                node = self.new_method_node(method, dex, framework_tree)
                if node is not None:
                    method_nodes.append(node)

            # normalize - skip classes with no methods
            if len(method_nodes) == 0:
                # self._debug(">> no methods found for class: %s", name, indent=" " * 4)
                continue

            method_nodes.sort(key=lambda node: node.hash_value)
            # update stats
            method_hashes += len(method_nodes)
            class_hashes += 1

            class_node = HashTreeNode(HashTree.get_hash(method_nodes), name, CLASS_NODE)
            if not self.prune_methods:
                class_node.children.extend(method_nodes)
            else:
                del method_nodes

            pkg_name = get_package_name(class_def.fullname, is_internal=True)
            if pkg_name not in package_map:
                package_map[pkg_name] = []

            package_map[pkg_name].append(class_node)

        for value in package_map:
            package_map[value].sort(key=lambda x: x.hash_value)

        package_nodes = []
        for package_name in sorted(package_map):
            class_nodes: list[HashTreeNode] = package_map[package_name]
            pkg_node = HashTreeNode(
                HashTree.get_hash(class_nodes),
                value=package_name if self.keep_packages else "",
                node_type=PACKAGE_NODE
            )
            if not self.prune_classes:
                pkg_node.children.extend(class_nodes)

            package_nodes.append(pkg_node)

        package_nodes.sort(key=lambda x: x.hash_value)
        self.root = HashTreeNode(HashTree.get_hash(package_nodes), None, None)
        self.root.children.extend(package_nodes)
        self._class_hashes = class_hashes
        self._method_hashes = method_hashes

        self._debug(
            "- Generated %d package hashes.", len(package_nodes), indent=" " * 4
        )
        self._debug("- Generated %d class hashes.", class_hashes, indent=" " * 4)
        self._debug("- Generated %d method hashes.", method_hashes, indent=" " * 4)
        self._debug("=> Library Hash: %s", self.root.hash_value, indent=" " * 4)

    @staticmethod
    def get_hash(nodes: list[HashTreeNode]) -> str:
        hasher = HF()
        for node in nodes:
            hasher.update(node.hash_value.encode())
        return hasher.hexdigest()

    def new_method_node(
        self, method: lief.DEX.Method, vm: dict[str, lief.DEX.Class], tree: PackageTree
    ) -> HashTreeNode | None:

        if self.access_flags != 0 and method.has(self.access_flags):
            return

        if not ch.is_app_method(method):
            return

        signature = ch.get_method_signature(method) #if self.keep_methods else ""
        descriptor = ch.get_fuzzy_descriptor(method, vm, tree)
        if not descriptor:
            return  # TODO: Raise exception
        return HashTreeNode(descriptor.encode(), signature, METHOD_NODE)

    @property
    def class_count(self) -> int:
        return self._class_hashes

    @property
    def method_count(self) -> int:
        return self._method_hashes

    @property
    def package_count(self) -> int:
        return len(self.root)

    def _debug(self, msg: str, *args, indent: str = None) -> None:
        if indent:
            msg = f"{indent}{msg}"
        logger.debug(msg, *args)

    def get_config(self) -> str:
        keep_config = []
        if self.keep_packages:
            keep_config.append(PACKAGE_NODE)
        if self.keep_classes:
            keep_config.append(CLASS_NODE)
        if self.keep_methods:
            keep_config.append("MSIG")

        prune_config = []
        if self.prune_classes:
            prune_config.append(CLASS_NODE)
        if self.prune_methods:
            prune_config.append("MSIG")

        return (
            f"{HF} | Flags: {self.access_flags:#x} | Keep: {'/'.join(keep_config)} "
            f"| Prune: {'/'.join(prune_config)}"
        )
