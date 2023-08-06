
from LibScout.hashtree import HashTreeNode
from LibScout.pkg import PackageTree, to_packages
from LibScout.profile import LibProfile

__all__ = [
    "HashTreeMatch",
    "compare_package_nodes",
    "ProfileMatch",
]

from typing import List

class HashTreeMatch:
    """Represents a match between two hash trees."""

    def __init__(self) -> None:
        self.nodes: List[HashTreeNode] = []  # List of matching hash tree nodes
        self.score: float = 0.0  # Match score, ranging from 0.0 to 1.0 (-1 is invalid)
        self.root_package: str | None = None  # Root package of the match, if known

    def is_full_match(self) -> bool:
        """
        Check if the match is a full match (score = 1.0).

        :return: True if the match is a full match, False otherwise.
        :rtype: bool
        """
        return self.score == 1.0

    def is_partial_match(self) -> bool:
        """
        Check if the match is a partial match (0 < score < 1).

        :return: True if the match is a partial match, False otherwise.
        :rtype: bool
        """
        return 0 < self.score < 1

    def __str__(self) -> str:
        """
        Return a string representation of the HashTreeMatch object.

        :return: String representation of the HashTreeMatch.
        :rtype: str
        """
        return f"<HTreeMatch score={self.score}>"


def compare_package_nodes(tree_nodes: List[HashTreeNode], matching_nodes: List[HashTreeNode]) -> bool:
    """
    Compare two lists of hash tree nodes for equality.

    :param tree_nodes: The list of hash tree nodes from the original tree.
    :type tree_nodes: List[HashTreeNode]
    :param matching_nodes: The list of hash tree nodes from the matching tree.
    :type matching_nodes: List[HashTreeNode]
    :return: True if the lists are equal, False otherwise.
    :rtype: bool
    """
    tree_nodes.sort(key=lambda x: x.value)
    matching_nodes.sort(key=lambda x: x.value)

    for i in range(min(len(tree_nodes), len(matching_nodes))):
        if tree_nodes[i] != matching_nodes[i]:
            return False
    return True



class ProfileMatch:
    """
    Represents a match between a library profile and an app profile.
    """

    def __init__(self, profile: LibProfile) -> None:
        self.lib_profile: LibProfile = profile  # The library profile
        self.lib_methods: set[str] = set()  # Set of normalized library method signatures used
        self.lib_root_present: bool = False  # Flag indicating if the library root is present in the app profile
        self.matched_package_tree: PackageTree = None  # The matched package tree
        self.results: List[HashTreeMatch] = []  # List of hash tree matches

    def is_full_match(self) -> bool:
        """
        Check if the match is a full match.

        :return: True if the match is a full match, False otherwise.
        :rtype: bool
        """
        return len(self.results) > 0 and all(map(lambda x: x.is_full_match(), self.results))

    def has_one_match(self) -> bool:
        """
        Check if the match has at least one full match.

        :return: True if the match has at least one full match, False otherwise.
        :rtype: bool
        """
        return len(self.results) > 0 and any(map(lambda x: x.is_full_match(), self.results))

    def is_partial_match(self) -> bool:
        """
        Check if the match is a partial match.

        :return: True if the match is a partial match, False otherwise.
        :rtype: bool
        """
        if self.has_one_match():
            return False
        return any(map(lambda x: x.is_partial_match(), self.results))

    def sort_matches(self) -> None:
        """
        Sort the hash tree matches based on their scores.
        """
        self.results.sort(key=lambda x: x.score)

    @property
    def best_match(self) -> HashTreeMatch:
        """
        Get the best hash tree match.

        :return: The best hash tree match.
        :rtype: HashTreeMatch
        """
        self.sort_matches()
        return self.results[0]

    def is_lib_obfuscated(self) -> bool:
        """
        Check if the library is obfuscated.

        :return: True if the library is obfuscated, False otherwise.
        :rtype: bool
        """
        for htree_match in self.results:
            if htree_match.is_full_match():
                trees = self.lib_profile.hash_trees
                for tree in trees:
                    if not compare_package_nodes(tree.root.children, htree_match.nodes):
                        return True
        return False

    def get_matched_package_tree(self) -> PackageTree | None:
        """
        Get the matched package tree.

        :return: The matched package tree if the match is a full match, None otherwise.
        :rtype: PackageTree | None
        """
        if not self.is_full_match():
            return None
        if not self.matched_package_tree:
            for htree_match in self.results:
                if htree_match.is_full_match():
                    nodes = map(lambda x: to_packages(x.name, True, True), htree_match.nodes)
                    self.matched_package_tree = PackageTree()
                    for node in nodes:
                        self.matched_package_tree.add(package=node)
                    break
        return self.matched_package_tree

    def show(self) -> None:
        """
        Display the profile match.
        """
        # TODO
        pass