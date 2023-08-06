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
import pathlib
import timeit
import pprint
import lief

from enum import Enum
from functools import reduce

from LibScout.config import INDENT, LOGGER_BASE_NAME
from LibScout.hashtree import HashTree, HashTreeNode
from LibScout.profile import (
    Profile,
    ProfileCache,
    LibProfile,
    AppStats,
    HashTreeMatch,
    ProfileMatch,
    get_unique_profiles,
    get_app_profile,
)
from LibScout.pkg import PackageTree, to_packages, to_path
from LibScout.files import extract_dex_files

logger = logging.getLogger(LOGGER_BASE_NAME)

MIN_PARTIAL_SCORE = 0.7
MIN_CLASS_SCORE = 0.33


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2
    UNRELATED = 3


def get_relationship(package_name: str, next_pn: str) -> Relationship:
    pn1_depth = package_name.count(".") + 1
    pn2_depth = next_pn.count(".") + 1

    if package_name.startswith(next_pn) and pn1_depth > pn2_depth:
        return Relationship.PARENT
    elif next_pn.startswith(package_name) and pn2_depth > pn1_depth:
        return Relationship.CHILD
    elif package_name == next_pn:
        return Relationship.SIBLING

    return Relationship.UNRELATED


def compute_sim_score(lib_node: HashTreeNode, app_node: HashTreeNode) -> float:
    # if they have not the exact same class e.g. PackageNode vs ClassNode, simScore is 0f
    if lib_node.node_type != app_node.node_type:
        return 0.0

    # if hashes are equal return 1f
    if lib_node.hash_value == app_node.hash_value:
        return 1.0

    # calculate partial score
    matched = list(filter(lambda x: x in app_node, lib_node.children))
    return float(len(matched)) / float(len(lib_node))


class LibMatcher:
    cache: ProfileCache
    stats: AppStats

    def __init__(
        self,
        cache: ProfileCache,
        fwpt: PackageTree = None,
        collect_lib_usage: bool = False,
        excluded: set[str] = None,
        ambiguous: set[str] = None,
        no_partial_matching: bool = False,
        min_partial_score: int = MIN_PARTIAL_SCORE,
        min_class_score: int = MIN_CLASS_SCORE,
        htree_options: dict = None,
        **options,
    ) -> None:
        self.cache = cache
        self.stats = None
        self.ambiguous = ambiguous or set()
        self.excluded = excluded or set()
        self.collext_lib_usage = collect_lib_usage

        # options
        self.no_partial_matching = no_partial_matching
        self.min_partial_score = min_partial_score
        self.min_class_score = min_class_score
        self.htree_options = htree_options or {}
        self.tmp_dir = options.get("tmp_dir", None)
        self.cleanup = options.get("cleanup", False)

        # :meta: private
        self._fwpt = fwpt  # framework package tree
        self._unique_libs = {}

    @property
    def framework_pt(self) -> PackageTree:
        return self._fwpt

    @property
    def unique_libraries(self) -> dict[str, str]:
        return self._unique_libs

    def identify_libs(self, file_path: str) -> AppStats:
        self.stats = AppStats(file_path)
        path = pathlib.Path(file_path)
        start = timeit.default_timer()
        logger.info("Processing app: %s", path.name)

        self.unique_libraries.update(get_unique_profiles(self.cache))
        logger.info(
            "Found %d unique libraries in %d library profiles",
            len(self.unique_libraries),
            len(self.cache),
        )

        # load all dex files
        logger.info("Load DEX files using LIEF:")
        dex_files = []
        time = timeit.default_timer()
        for file_path in extract_dex_files(file_path, self.tmp_dir):
            dex_files.append(lief.DEX.parse(file_path))
            logger.debug("%s- Parsed %s", INDENT[4], file_path)

        logger.info(
            "%s=> Imported %d DEX files (in %2fs)",
            INDENT[4],
            len(dex_files),
            (timeit.default_timer() - time),
        )
        # generate app package tree and hash trees
        app_profile = get_app_profile(
            dex_files, self.framework_pt, self.excluded, **self.htree_options
        )
        self.stats.profile = app_profile
        # fast scan (heuristic) - check if lib root package is in app
        logger.info("=== Scan for libraries in root packages (heuristic) ===")
        for lib_profile in self.cache:
            if lib_profile is None:
                continue # ignore errors, maybe log them

            # check if library root package is present in app (for validation purposes)
            root_package = lib_profile.package_tree.get_root_package(self.excluded)

            # In some edge case the automatic root package extraction gives us a generic
            # package that could match multiple different libraries. In these cases it is
            # better to ignore them instead of getting a lot of false matches
            if not root_package or root_package in self.ambiguous:
                continue

            in_tree = root_package in app_profile.package_tree
            if in_tree and lib_profile.name not in self.stats.package_only_matches: # ???
                self.stats.package_only_matches[lib_profile.name] = root_package
                logger.info(
                    "%s- Found lib root package %s (%s)",
                    INDENT[4],
                    root_package,
                    lib_profile.name,
                )

        logger.info("")
        # check app against all loaded profiles (exact + partial matching)
        pm_start = timeit.default_timer()
        results = []
        logger.info("=== Match profiles ===")
        for profile in self.cache:
            # check if this is the most current library version
            profile.is_deprecated = (
                self.unique_libraries.get(profile.name) > profile.version
            )

            # compute similarity scores for each hash tree
            pm = self.partial_match_for_trees(app_profile, profile)
            results.append(pm)

            # do we have a one-to-one copy of the library?
            if pm.is_full_match():
                logger.debug("%s- All configs match!", INDENT[4])
                logger.debug(
                    "%s- Re-Obfuscated library? - %s", INDENT[4], pm.is_lib_obfuscated()
                )
                logger.debug("")

        logger.info(
            "%s>> Profile matching done (%2fs)",
            INDENT[4],
            (timeit.default_timer() - pm_start),
        )
        self.stats.matches = results
        self.show_results()

        # run library API usage analysis for full matches only
        if self.collext_lib_usage:
            pass  # maybe leave that out

        logger.info("")
        self.stats.processing_time = timeit.default_timer() - start
        logger.info("App processing time: %2f", self.stats.processing_time)
        return self.stats

    def partial_match_for_trees(
        self, app_profile: Profile, lib_profile: LibProfile
    ) -> ProfileMatch:
        pmatch = ProfileMatch(lib_profile)
        logger.debug("Partial match of lib: %s", lib_profile.name)

        # check if library root package is present in app (for validation purposes)
        root_pkg = lib_profile.package_tree.get_root_package(self.excluded)
        pmatch.lib_root_present = root_pkg and root_pkg in app_profile.package_tree
        logger.debug(
            "%sLibrary root package %s is %s present in app!",
            INDENT[4],
            root_pkg,
            "" if pmatch.lib_root_present else "not",
        )

        # calculate scores for each hash tree
        for hash_tree in app_profile.hash_trees:
            self.partial_match(pmatch, hash_tree, lib_profile)

        return pmatch

    def partial_match(
        self, pmatch: ProfileMatch, app_tree: HashTree, lib_profile: LibProfile
    ) -> None:
        # Multi-step approach to compute the similarity score between a given library
        # and an application. We first check for a full match by comparing the package
        # hashes of the library with the ones from the application. If there is no full
        # match we compute a candidate list for each app package, compute partitions
        # (potential root packages) and determine the maximum over all partitions.
        tree = lib_profile.hash_trees[0]  # assume there is only one tree
        htmatch = HashTreeMatch()
        logger.debug(
            "%s- Partial match for config: %s", INDENT[4], app_tree.get_config()
        )

        if not tree:
            logger.error(
                "Could not find library HashTree for config: %s", app_tree.get_config()
            )

        # step 0. shortcut - check if library fully matches by comparing the package hashes
        logger.debug("%s# Step 0: Check if lib packages fully match", INDENT[3])
        if app_tree.root.children == tree.root.children and len(tree.root) > 0:
            # We can use the comparison operator as we've implemented __eq__ in HashTreeNode
            logger.debug(
                "%s-> All package hashes (%d) of library match!",
                INDENT[3],
                len(tree.root),
            )

            lib_nodes = set(tree.root.children)
            htmatch.score = 1.0  # full match
            htmatch.nodes = [
                x for x in app_tree.root.children if x in lib_nodes
            ]  # We actually don't need that

            pmatch.results.append(htmatch)
            return

        # we do not perform partial matching for libs that have multiple lib root packages
        lib_root_pkg = lib_profile.package_tree.get_root_package(self.excluded)
        logger.debug("%s# Step 0.5: Check root package: %s", INDENT[8], lib_root_pkg)
        if not lib_root_pkg:
            logger.debug(
                "%s-> No partial matching performed due to multiple lib root packages",
                INDENT[3],
            )
            htmatch.score = -1.0
            pmatch.results.append(htmatch)
            return

        # Step 1. compute candidate list
        # Candidate list of each library package sorted by similarity score, i.e.
        #   lp1 ∶ ap1 (0.95), ap2 (0.84), ap3 (0.75)
        #   lp3 ∶ ap6 (0.91), ap4 (0.60)
        #   lp2 ∶ ap7 (0.85), ap9 (0.82)
        logger.debug("%s# Step 1: Compute candidate list", INDENT[3])
        time = timeit.default_timer()

        candidates: dict[HashTreeNode, list] = {}
        for lp in tree.root.children:
            clist = []  # candicate list for lp

            # Filter application packages that start with declared manifest app package name
            # TODO: unfortunately, most app packages do only partially match the manifest package
            #       name. This means to match more app packages we would have to test partially
            #       (but: this could lead to false positives if we have libs from the same developer)
            # REVISIT: removed additional manifest package check
            for ap in app_tree.root.children:
                score = compute_sim_score(lp, ap)
                if score > self.min_class_score:
                    clist.append((ap, score))

            clist.sort(key=lambda x: x[1])
            candidates[lp] = clist

        # sort tree map by highest candidate values
        def sort_candidates(key: str) -> float:
            clist = candidates[key]
            if len(clist) == 0:
                return -1

            return clist[0][1]  # return sim score

        sorted_clist: list[HashTreeNode] = list(sorted(candidates, key=sort_candidates))
        logger.debug(
            "%sSorted candidate list (%2fs)", INDENT[3], (timeit.default_timer() - time)
        )

        # Step 2. get potential root packages -- partitions  (skip package name of apk)
        # Note: This will _not_ work if app developer manually renamed the library
        # packages (e.g. prefixed lib packages with app package)
        logger.debug("%s# Step 2: Determine partitions", INDENT[8])
        time = timeit.default_timer()
        lib_root_depth = lib_root_pkg.count(".") + 1

        # retrieve potential app root packages of depth libPDepth
        app_root_packages = set()
        for ap in app_tree.root.children:
            packages = to_packages(ap.value, include_class=True)
            if len(packages) - 1 < lib_root_depth:
                # getSubPackageOfDepth()
                app_root_packages.add(to_path(*packages[:lib_root_depth]))

        logger.debug(
            "%s# Partitions(%d): %s",
            INDENT[3],
            len(app_root_packages),
            pprint.pformat(app_root_packages, compact=True),
        )
        # Filter candidates by lib root package
        app_root_packages = list(
            filter(lambda x: x.startswith(lib_root_pkg), app_root_packages)
        )
        logger.debug(
            "%s# Unique Partitions(%d): %s",
            INDENT[3],
            len(app_root_packages),
            pprint.pformat(app_root_packages, compact=True),
        )
        logger.debug(
            "%s- Step 2 processing time: %2f",
            INDENT[4],
            (timeit.default_timer() - time),
        )

        # step 3. compute maximum score for each partition (including selected app packages)
        # A score is a mapping of root package -> pair < score, nodes with individual package scores >
        logger.debug("%s# Step 3: Partition scores", INDENT[8])
        # pre-compute library package relationships
        relationships: list[Relationship] = []
        for i in range(len(sorted_clist) - 1):
            relationships.append(
                get_relationship(sorted_clist[i].value, sorted_clist[i + 1].value)
            )

        scores: dict[str, tuple[float, list[tuple[HashTreeNode, float]]]] = {}
        for root_pkg in app_root_packages:
            time = timeit.default_timer()
            # part_sim_score := sim_score, list[matched nodes]
            part_sim_score = self.compute_partition_sim_score(
                root_pkg, sorted_clist, candidates, relationships
            )
            if part_sim_score[1]:
                logger.debug(
                    "%s-> Partition: %s, sim score: %2f",
                    INDENT[4],
                    root_pkg,
                    part_sim_score[0],
                )
                scores[root_pkg] = part_sim_score
            logger.debug(
                "%s- Processing time: %2f", INDENT[5], (timeit.default_timer() - time)
            )

        # step 4. chose overall maximum (with a minimum threshold of @MIN_PARTIAL_MATCHING_SCORE)
        logger.debug("%s# Step 4: Compute overall maximum score", INDENT[8])
        if len(scores) == 0:
            logger.debug("No partial matching for %s\n", repr(pmatch.lib_profile))
            # update results
            htmatch.score = 0.0
            pmatch.results.append(htmatch)
        else:
            logger.debug(
                "%s%d results for partial matching of lib %s (%s)",
                INDENT[3],
                len(scores),
                repr(pmatch.lib_profile),
                app_tree.get_config(),
            )
            # get best score over partitions
            highest_score, package = self.get_highest_score(scores)
            logger.debug(
                "%s=> Maximum partial matching score: %2f (partition: %s)\n",
                INDENT[4],
                highest_score,
                package,
            )

            htmatch.root_package = package
            htmatch.score = highest_score
            htmatch.nodes = list(map(lambda x: x[0], scores[package]))
            pmatch.results.append(htmatch)

    def get_highest_score(self, scores: dict[str, tuple]) -> tuple[str, float]:
        highest_score = 0
        root_package = None
        for root in scores:
            score = scores[root][1]
            logger.debug("%s- RootPackage: %s, score: %2f", INDENT[4], root, score)
            if score > highest_score:
                highest_score = score
                root_package = root

        return root_package, highest_score

    def compute_partition_sim_score(
        self,
        root_pkg: str,
        clist: list[HashTreeNode],
        candidates: dict,
        relationships: list[Relationship],
    ) -> tuple | None:
        logger.debug("%s- Calculate sim score for partitions: %s", INDENT[3], root_pkg)

        def filter_candidates(x: tuple[HashTreeNode, float]):
            # check if candidate package starts with root package and has the same package depth
            return (
                x[0].value.startswith(root_pkg)
                and x[0].value.count(".") + 1 == root_pkg.count(".") + 1
            )

        # create view on candidate list (filter app packages that do not start
        # with rootPackage and app packages that have a different depth as the
        # lib package)
        count = 0
        candidate_list = []
        for package_candidate in clist:
            matched = list(filter(filter_candidates, candidates[package_candidate]))
            if len(matched) > 0:
                count += 1
                candidate_list.append(matched)  # note that we don't use extend()

        # stop if less than half of lib packages have no candidate
        if count / len(candidate_list) < 0.5:
            logger.debug(
                "%sOnly %d / %d lib packages for partition: %s have candidates [SKIP]",
                INDENT[4],
                count,
                len(candidate_list),
                root_pkg,
            )
            return None

        # test all combinations and retrieve maximum
        return self.get_best_match(candidate_list, relationships)

    def get_best_match(
        self, clist: list[list], lib_relationships: list[Relationship]
    ) -> tuple | None:
        # keep track of the size of candidate arrays for each lib
        # Example cList:
        #    lp1 ∶ ap1 (0.95), ap2 (0.84), ap3 (0.75)
        #    lp3 ∶ ap6 (0.91), ap4 (0.60)
        #    lp2 ∶ ap7 (0.85), ap9 (0.82)
        # => size array [3,2,2]
        # Discover the size of each inner array and populate sizeArray.
        sizes = [len(x) for x in clist]

        # keep track of the index of each inner String array which will be used
        # to make the next combination (access pattern)
        counters = [0] * len(clist)

        # Calculate the total number of combinations possible, here: 3*2*2 = 12
        total = reduce(lambda count, l: (count or 1) * (len(l) or 1), clist, 0)

        # stop if we have too many combinations
        if total > 65536:
            logger.debug(
                "%s[GetBestMatch] more that 2^16 combinations (%d) - [SKIP]",
                INDENT[4],
                total,
            )
            return None
        else:
            logger.debug("%s- Testing %d combinations!", INDENT[4], total)

        # only consider solutions that are better than the min matching score
        highest_score = self.min_partial_score
        best_match = None
        for i in range(total, 0, -1):
            # calculate sim score for current combination (set in counterArray)
            score = 0.0
            for candidates in clist:  # can be optimized
                score += (
                    0 if len(candidates) == 0 else candidates[counters[i]][1]
                )  # score value

            sim_score = score / len(clist)
            # if we have a new highscore, perform structural matching (package relationships) to
            # verify correctness of the solution
            if sim_score > highest_score:
                current = []
                for i in range(len(clist) - 1):
                    # don't use empty candidates
                    if len(clist[i]) == 0 and len(clist[i + 1]) == 0:
                        continue

                    node1, node_score = clist[i][counters[i]]
                    node2, _ = clist[i + 1][counters[i + 1]]
                    relationship = get_relationship(node1.value, node2.value)
                    if lib_relationships[i] != relationship:
                        current = None
                        break
                    else:
                        current.append((node1, node_score))

                if current is not None:
                    highest_score = sim_score
                    best_match = current
                    last_elements = clist[-1]
                    if len(last_elements) != 0:  # add last element (if existing)
                        best_match.append(last_elements[counters[-1]])

                    logger.debug(
                        "%s- Found new highscore: %d at position %s",
                        INDENT[4],
                        int(highest_score),
                        str(counters),
                    )

            # Increment the counterArray so that the next combination is taken on the next
            # iteration of this loop.
            for i in range(len(clist) - 1, 0, -1):
                if counters[i] + 1 < sizes[i]:
                    counters[i] += 1
                    # None of the indices of higher significance need to be
                    # incremented, so jump out of this for loop at this point.
                    break

                # The index at this position is at its max value, so zero it
                # and continue this loop to increment the index which is more
                # significant than this one.
                counters[i] = 0

        return highest_score, best_match

    def show_results(self) -> None:
        logger.info("")
        logger.info("=== Report ===")
        logger.info("- Full library matches:")

        # Step1: print libs for which all configs match
        pass
