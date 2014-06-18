# -*- coding: utf-8 -*-
import unittest
import os
import re
import sys
sys.path.insert(0, '.')

V7_TEST_DIR = 'tests.v7'


def collect_tests():
    # list files in directory tests/v7
    # inspired by flake8 source code
    names = os.listdir(V7_TEST_DIR.replace('.', os.path.sep))
    regex = re.compile("(?!_+)\w+\.py$")
    join = '.'.join
    # Make a list of the names like 'tests.vx.test_name'
    names = [join([V7_TEST_DIR, f[:-3]]) for f in names if regex.match(f)]
    # we load the testcases as module
    modules = [__import__(name, fromlist=[V7_TEST_DIR]) for name in names]
    suites = [unittest.TestLoader().loadTestsFromModule(m) for m in modules]
    suite = suites.pop()
    for s in suites:
        suite.addTests(s)
    print suite
    return suite

if __name__ == "__main__":
    suite = collect_tests()
    res = unittest.TextTestRunner(verbosity=1).run(suite)
    # If it was successful, we don't want to exit with code 1
    raise SystemExit(not res.wasSuccessful())
