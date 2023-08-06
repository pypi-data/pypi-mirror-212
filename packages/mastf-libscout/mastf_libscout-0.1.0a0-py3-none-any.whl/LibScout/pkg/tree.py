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

import zipfile
import lief

from typing import Iterable
from logging import getLogger

from LibScout.config import LOGGER_BASE_NAME, FW_TYPES
from LibScout.pkg.utils import to_packages, to_path

__all__ = [
    "Node",
    "from_list",
    "generate_package_tree",
    "get_framework_pt",
    "PackageTree",
]

logger = getLogger(LOGGER_BASE_NAME)

DEFAULT_CHARSET = ("|___ ", "|--- ", "|   ")


class Node:
    """Represents a node in a tree-like structure.

    :param name: The name associated with the node.
    """

    name: str
    """The node's name"""

    class_count: int
    """The amount of classes in this node."""

    children: list["Node"]
    """A list storing all children"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.class_count = 0
        self.children = []

    def __eq__(self, __value: object) -> bool:
        """Compares the node with another object for equality.

        >>> Node("foo") == Node("bar")
        False

        :param __value: The object to compare.
        :return: True if the objects are equal, False otherwise.
        :meta: public
        """
        if not isinstance(__value, Node):
            return super().__eq__(__value)

        node: Node = __value
        return self.name == node.name

    def __ne__(self, __value: object) -> bool:
        """Compares the node with another object for inequality.

        >>> Node("foo") != Node("bar")
        True

        :param __value: The object to compare.
        :return: True if the objects are not equal, False otherwise.
        :meta: public
        """
        return not self.__eq__(__value)

    def __str__(self) -> str:
        """Returns the node's name.

        :return: The string representation of the node.
        :meta: public
        """
        # candidate: toString()
        return self.name

    def __repr__(self) -> str:
        """Returns a string representation of the node for debugging purposes.

        :return: The string representation of the node.
        :meta: public
        """
        return f"<{self.__class__.__name__} name='{self.name}'>"

    def __len__(self) -> int:
        """Returns the number of child nodes.

        :return: The number of child nodes.
        :meta: public
        """
        return len(self.children)

    def __getstate__(self) -> object:
        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        self.__dict__.update(state)

    def has_classes(self) -> bool:
        """Checks if the node has associated classes.

        :return: True if the node has associated classes, False otherwise.
        """
        # candidate: hasClasses()
        return self.class_count != 0

    @property
    def is_leaf(self) -> bool:
        """Checks if the node is a leaf node (has no children).

        :return: True if the node is a leaf node, False otherwise.
        """
        # candidate: isLeaf()
        return len(self.children) == 0

    def show(
        self,
        prefix: str = None,
        is_tail: bool = False,
        charset: list[str] = DEFAULT_CHARSET,
        include_class_count: bool = False,
    ) -> None:
        """Displays the node and its children in a tree-like format.

        Example output of Google-Gson package tree:

        .. code-block:: text

            INFO:libscout:|--- com (0)
            INFO:libscout:|   |___ google (0)
            INFO:libscout:|       |___ gson (40)
            INFO:libscout:|           |--- reflect (1)
            INFO:libscout:|           |--- annotations (5)
            INFO:libscout:|           |--- internal (52)
            INFO:libscout:|           |   |___ bind (69)
            INFO:libscout:|           |       |___ util (1)
            INFO:libscout:|           |___ stream (6)

        :param prefix: The prefix string to be added before the node's name (used
                       for indentation).
        :param is_tail: A flag indicating if the node is a tail node (last child
                        of its parent).
        :param charset: A list of characters used for tree drawing.
        :param include_class_count: A flag indicating if the class count should be
                                    included in the display.
        """
        if not prefix:
            prefix = ""

        logger.info(
            "%s%s%s (%s)",
            prefix,
            charset[0] if is_tail else charset[1],
            self.name,
            self.class_count if include_class_count else "-",
        )

        for i, child in enumerate(self.children):
            new_prefix = "".join([prefix, " " * 4 if is_tail else charset[2]])
            child.show(
                new_prefix,
                is_tail=i == len(self) - 1,
                charset=charset,
                include_class_count=include_class_count,
            )


def from_list(elements: list[str | lief.DEX.Class]) -> PackageTree:
    """
    Create a PackageTree from a list of elements.

    :param elements: List of elements that can be either strings representing full class names or lief.DEX.Class objects.
    :type elements: list[str | lief.DEX.Class]
    :return: The created PackageTree.
    :rtype: PackageTree
    """
    tree = PackageTree()
    for element in elements:
        if isinstance(element, str):
            tree.add(full_class_name=element, cn_internal=True)
        elif isinstance(element, lief.DEX.Class):
            tree.add(full_class_name=element.pretty_name, cn_internal=False)
    return tree


def generate_package_tree(dex: lief.DEX.File, excluded: set[str] = None) -> PackageTree:
    """
    Generate a PackageTree from a lief.DEX.File.

    :param dex: The lief.DEX.File object representing the DEX file.
    :type dex: lief.DEX.File
    :param excluded: Optional set of excluded package names.
    :type excluded: set[str], optional
    :return: The generated PackageTree.
    :rtype: PackageTree
    """
    logger.info("=== PackageTree ===")
    tree = PackageTree()
    tree.load(dex, excluded)
    tree.show(include_class_count=True)

    logger.debug("")
    logger.debug("Package names (included classes):")
    packages = tree.get_packages()
    for package in packages:
        logger.debug("%s%s (%d)", " " * 4, package, packages[package])

    logger.info("")
    return tree


def get_framework_pt(android_jar: str, excluded: set[str] = None) -> PackageTree:
    """
    Get the PackageTree for the Android framework from an Android JAR file.

    :param android_jar: The path to the Android JAR file.
    :type android_jar: str
    :param excluded: Optional set of excluded package names.
    :type excluded: set[str], optional
    :return: The PackageTree for the Android framework.
    :rtype: PackageTree
    """
    tree = PackageTree()
    with zipfile.ZipFile(android_jar) as jar:
        names = filter(lambda x: x.endswith(".class"), jar.namelist())
    tree.load(names, excluded)
    return tree


class PackageTree:
    """Represents a package tree that organizes classes into a hierarchical structure.

    Usage Examples
    ~~~~~~~~~~~~~~

    .. code-block:: python
        :linenos:

        # Create a new PackageTree
        tree = PackageTree()

        # Load classes from a DEX file
        dex = dvm.DalvikVMFormat(dex_file_path)
        tree.load(dex)

        # Add classes manually
        tree.add(full_class_name="com.example.package1.ClassA")
        tree.add(package=["com", "example", "package2"], incl_class=True)

        # Check if a class exists in the tree
        if "com.example.package1.ClassA" in tree:
            print("ClassA exists in the package tree")

        # Get the root package
        root_package = tree.get_root_package()
        print("Root Package:", root_package)

        # Display the package tree structure
        tree.show(include_class_count=True)

        # Get the total number of classes in the tree
        total_classes = tree.app_classes
        print("Total classes:", total_classes)

        # Get the number of non-empty packages
        non_empty_packages = tree.non_empty_packages
        print("Non-empty packages:", non_empty_packages)

    :param dex: Optional DalvikVMFormat object representing the DEX file. If
                provided, the tree will be loaded with the classes from the
                DEX file.
    """

    root: Node
    """The root node of this tree"""

    def __init__(self, dex: lief.DEX.File = None) -> None:
        self.root = Node("root")
        if dex is not None:
            self.load(dex)

    def __contains__(self, full_class_name: str) -> bool:
        """
        Checks if a given full class name exists in the package tree.

        :param full_class_name: The full class name to search for.
        :return: True if the class name exists in the tree, False otherwise.
        :meta: public
        """
        return self.search(full_class_name, recursive=True) is not None

    def __repr__(self) -> str:
        """
        Returns a string representation of the PackageTree for debugging purposes.

        :return: The string representation of the PackageTree.
        :meta: public
        """
        return f"<PackageTree root='{self.get_root_package()}'>"

    def load(
        self, names_or_dex: lief.DEX.File | Iterable[str], excluded: set[str] = None
    ) -> None:
        excluded = excluded or set()
        if not isinstance(names_or_dex, (lief.DEX.File, Iterable)):
            raise TypeError(
                "Expected DalvikVMFormat or Iterable[str] - got %s" % type(names_or_dex)
            )

        class_list = names_or_dex
        if isinstance(names_or_dex, lief.DEX.File):
            class_list = [x.pretty_name for x in names_or_dex.classes if x.source_filename]

        for class_def in class_list:
            packages = to_packages(class_def, include_class=False, is_internal=True)
            if to_path(*packages) in excluded:
                continue

            self.add(package=packages)

    def search(
        self, name: str, node: Node = None, recursive: bool = False
    ) -> Node | None:
        """Searches for a node with a given name in the package tree.

        :param name: The name to search for.
        :param node: The starting node for the search. If not provided, the search
                     starts from the root node.
        :param recursive: Flag indicating whether to perform a recursive search
                          through child nodes.
        :return: The found Node object if the name exists in the tree, None otherwise.
        """
        current = node or self.root
        if not recursive:
            nodes = list(filter(lambda x: x.name == name, current.children))
            if len(nodes) == 0:
                return None

            return nodes[0]  # only first result

        packages = to_packages(name, True)
        for package_name in packages:
            current = self.search(package_name, node=current)
            if not current:
                return None

        return current

    def add(
        self,
        full_class_name: str = None,
        package: list[str] = None,
        cn_internal: bool = False,
        incl_class: bool = False,
    ) -> None:
        """Adds a class to the package tree.

        :param full_class_name: The full class name to be added. If not provided,
                                the package argument must be given.
        :param package: The package hierarchy of the class. If not provided, it
                        will be derived from the full_class_name.
        :param cn_internal: Flag indicating whether the class name is internal.
        :param incl_class: Flag indicating whether to include the class name in
                           the package hierarchy.
        """
        if not full_class_name and package is None:
            return

        if package is None and full_class_name:
            package = to_packages(full_class_name, incl_class, cn_internal)

        current = self.root
        if len(package) == 0:
            current.class_count += 1
        else:
            for i, name in enumerate(package):
                node = self.search(name, node=current)
                if node is not None:
                    current = node
                else:
                    next_node = Node(name)
                    current.children.append(next_node)
                    current = next_node

                if i == len(package) - 1:
                    current.class_count += 1

    def get_packages(
        self, path: str = "", node: Node = None, dump_all: bool = False
    ) -> dict[str, int]:
        """Retrieves the packages and their class counts in the package tree.

        :param path: The current path in the package hierarchy.
        :param node: The starting node for retrieving packages. If not provided,
                     the retrieval starts from the root node.
        :param dump_all: Flag indicating whether to include all packages,
                         regardless of class count.
        :return: A dictionary containing the packages as keys and their respective
                 class counts as values.
        """
        result = {}
        node = node if node is not None else self.root
        if node.has_classes() or dump_all:
            full_path = to_path(path, node.name)
            result[full_path] = node.class_count

        if not node.is_leaf:
            for child in node.children:
                next_path = to_path(path, "" if node.name == "root" else node.name)
                result.update(self.get_packages(next_path, child, dump_all))

        return result

    def get_root_package(self, excluded: set[str] = None) -> str | None:
        """
        Retrieves the root package of the package tree.

        :param excluded: A set of package names to be excluded from the root
                         package determination.
        :return: The root package name, or None if the tree is empty or the root
                 package cannot be determined.
        """
        excluded = excluded or set()
        excluded.update(FW_TYPES) # always exclude them
        current = self.root
        domains = []

        # This is another heuristic to determine the proper root package in presence of another lib dependency
        # whose package name differs at depth 1 or at depth 2 if depth 1 is some common namespace
        if len(current) > 1 or (
            len(current) == 1 and current.children[0].name in excluded
        ):
            if len(current) == 1:
                current = current.children[0]
                domains.append(current.name)

            depth = 0
            count = 0
            for i, node in enumerate(current.children):
                # determine the largest subtree in terms of packages
                node_count = len(self.get_packages("", node, True))
                if node_count > count:
                    depth = i
                    count = node_count

            current = current.children[depth]
            domains.append(current.name)
            if current.has_classes():
                return ".".join(domains) if len(domains) > 0 else None

        while len(current) == 1:
            current = current.children[0]
            domains.append(str(current))
            if current.has_classes():
                break

        # disallow incomplete root packages of depth 1 that start with common namespace
        if len(domains) == 1 and domains[0] in excluded:
            return None

        return ".".join(domains) if len(domains) > 0 else None

    def show(
        self, include_class_count: bool = False, excluded: set[str] = None
    ) -> None:
        """
        Displays the package tree structure in a hierarchical format.

        :param include_class_count: Flag indicating whether to include the class
                                    count for each package.
        """
        root_package = self.get_root_package(excluded)
        logger.info("Root Package: %s", root_package or "- none -")

        if len(self.root) == 1 and not self.root.has_classes():
            self.root.children[0].show(include_class_count=include_class_count)
        else:
            self.root.show(include_class_count=include_class_count)

    @property
    def app_classes(self) -> int:
        """
        Returns the total number of classes in the package tree.

        :return: The number of classes in the tree.
        """
        return sum(self.get_packages().values())

    @property
    def non_empty_packages(self) -> int:
        """
        Returns the number of non-empty packages in the package tree.

        :return: The number of non-empty packages.
        """
        return len(self.get_packages())
