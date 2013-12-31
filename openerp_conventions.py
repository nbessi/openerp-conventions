# -*- coding: utf-8 -*-
"""OpenERP community addons standard plugin for flake8"""
from __future__ import absolute_import

import common_checker
from common_checker.base_checker import BaseChecker

# When OpenERP version 8 API will be frozen
# We wille be able to do version toggle here
import v7

__version__ = '0.0.1'


class OpenERPConventionsChecker(object):
    """Check OpenERP conventions

    It will call the function 'visit(root_node)' for all checker instances
    registered in BaseCheckerMeta

    """

    name = 'OpenERP convention'

    version = __version__

    def __init__(self, tree, filename):
        """Constructor

        :param tree: root ast.node of current module
        :param filename: current module filename
        """
        self.tree = tree if tree else ()
        self.filename = filename
        self.checks = BaseChecker._checks


    def run(self):
        """Run the checks"""
        return self.check_tree(self.tree)

    def check_tree(self, tree_root):
        """Apply all checks registered in BaseCheckerMeta on root ast.node

        :param tree_root: Root ast node of the namespace

        :returns: yeld list of errors codes

        """
        for check in self.checks:
            check.visit(tree_root)
            for error in check.errors:
                yield error
