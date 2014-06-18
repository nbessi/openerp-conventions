# -*- coding: utf-8 -*-
"""OpenERP addons manifest aka __openerp__.py checker"""
import os
import sys
import unittest
from openerp_conventions import OpenERPConventionsChecker
try:
    import ast
except ImportError:
    from flake8.util import ast


def load_tests(loader, tests, pattern):
    return tests


class ConventionCheckTest(unittest.TestCase):
    """Root test class that initalize checker for given file"""

    _file_name = None
    _file_path = None

    def init_tree(self):
        # There should be a better solution do not hesitate to PL :)
        subclass_path = sys.modules[self.__class__.__module__].__file__
        subclass_base_dir = os.path.dirname(subclass_path)
        path = os.path.join(os.path.abspath(subclass_base_dir),
                            'testsuite', self._file_path)
        source = file(path).read()
        return ast.parse(source)

    def setUp(self):
        assert self._file_name and self._file_path
        tree = self.init_tree()
        self.checker = OpenERPConventionsChecker(tree, self._file_name)
        self.checks = [x for x in self.checker.check_tree(tree)]
        self.mapping = {}
        for check in self.checks:
            code = check[2].split(' ')[0]
            vals = {'message': check[2],
                    'line': check[0],
                    'col': check[1]}
            self.mapping[code] = vals

    def check_code(self, code, linenb, col=None):

        self.assertIn(code, self.mapping,
                      msg='Code %s not found in checks' % code)
        check = self.mapping[code]
        self.assertEqual(linenb, check['line'],
                         msg='Wrong line expected %s got %s' % (check['line'],
                                                                linenb))
        if col:
            self.assertEqual(col, check['col'],
                             msg='Wrong col expected %s got %s' % (check['col'],
                                                                   col))
