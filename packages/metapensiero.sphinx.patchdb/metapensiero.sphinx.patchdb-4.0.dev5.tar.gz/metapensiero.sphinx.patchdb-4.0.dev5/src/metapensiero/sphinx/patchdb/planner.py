# -*- coding: utf-8 -*-
# :Project:   PatchDB — Execution planner
# :Created:   ven 12 mag 2023, 17:04:06
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2023 Lele Gaifax
#

from collections import defaultdict
from graphlib import TopologicalSorter
import logging

from .patch import DependencyError


logger = logging.getLogger(__name__)


class ExecutionPlanner:
    """
    Iterator over a set of patches, taking into account their relative order.
    """

    def __init__(self, manager, context):
        self.manager = manager
        self.context = context
        self.patches = self._collectPatches()
        self.constraints = self._computeConstraints()

    def _collectPatches(self):
        manager = self.manager
        context = self.context

        patches = set()
        by_pid = dict()

        logger.debug("Collecting patches...")
        for patch in manager.db.values():
            patch.adjustUnspecifiedRevisions(manager, context)

            applicable, reason = patch.isApplicable(context)
            if applicable:
                patches.add(patch)
                by_pid[patch.patchid] = patch
            else:
                logger.debug(' - ignoring "%s": %s', patch, reason)

        drop = set()
        for patch in patches:
            if patch.is_migration:
                for pid, prev in patch.depends:
                    crev = context[pid]
                    if crev is not None and prev < context[pid]:
                        logger.debug(' - ignoring "%s",'
                                     ' depends on "%s@%d" but it is already at %d',
                                     patch, pid, prev, context[pid])
                        drop.add(patch)
                        break

                if patch in drop:
                    continue

                for pid, prev in patch.drops:
                    if context[pid] is None:
                        logger.debug(' - ignoring "%s", drops "%s" but it is already gone',
                                     patch, pid)
                        drop.add(patch)
                        break

                if patch in drop:
                    continue


                for pid, prev in patch.brings:
                    other = by_pid.get(pid)
                    if other is not None:
                        logger.debug(' - ignoring "%s", brought by "%s"', other, patch)
                        drop.add(other)

        return patches - drop

    def _computeConstraints(self):
        patches = self.patches
        if not patches:
            return None

        manager = self.manager
        context = self.context

        logger.debug("Building constraints graph between %d patches...", len(patches))

        # Reverse index between a given patch and the one that brings it
        brings = {}

        # Reverse index between a given patch and those that depend on it
        depends = defaultdict(set)

        # Dependency graph for the toposort
        constraints = defaultdict(set)

        for patch in patches:
            if patch.is_placeholder:
                # This is a "placeholder" patch and it has not been applied yet
                logger.critical("%s has not been applied yet", patch)
                raise DependencyError('%s has not been applied yet' % patch)

            # Consider always-first and always-last patches
            if patch.always:
                before = patch.always == 'first'
                logger.debug(' - "%s" shall be executed %s all the others',
                             patch, "before" if before else "after")
                for other in patches:
                    if other is not patch and other.always != patch.always:
                        if before:
                            constraints[other].add(patch)
                        else:
                            constraints[patch].add(other)

            # Ensure this patch gets executed after the ones it depends on, and take note
            # about the patches that depend on this
            for oid, orev in patch.depends:
                crev = context[oid]
                assert crev is None or crev <= orev
                if crev != orev:
                    other = manager[oid]
                    if other in patches:
                        logger.debug(' - "%s" shall be executed after "%s"', patch, other)
                        constraints[patch].add(other)
                    depends[(oid, orev)].add(patch)

            # Ensure this patch gets executed before the ones it preceeds
            for oid, orev in patch.preceeds:
                crev = context[oid]
                assert crev is None or crev >= orev
                if crev != orev:
                    other = manager[oid]
                    if other in patches:
                        logger.debug(' - "%s" shall be executed after "%s"', other, patch)
                        constraints[other].add(patch)

            # Take note about the patches brought by this one
            for oid, orev in patch.brings:
                if (oid, orev) in brings:
                    raise DependencyError('Multiple patches bring to "%s@%s": "%s" and "%s"',
                                          oid, orev, patch, brings[(oid, orev)])
                crev = context[oid]
                assert crev is None or crev <= orev
                brings[(oid, orev)] = patch

        # Add further constraints between patch dependencies and the one that brings them
        for p in depends:
            for patch in depends[p]:
                for d in patch.depends:
                    if d in brings:
                        other = brings[d]
                        logger.debug(' - %s" shall be executed after "%s"', patch, other)
                        constraints[patch].add(other)

        return constraints

    def __len__(self):
        return len(self.patches)

    def __iter__(self):
        if self.constraints:
            return TopologicalSorter(self.constraints).static_order()
        else:
            return iter(self.patches)
