# -*- coding: utf-8 -*-
import unittest
from tests.base_test import ConventionCheckTest


class ManifestChecker(ConventionCheckTest):

    _file_path = 'empty__openerp__.py'
    _file_name = '__openerp__.py'

    @unittest.expectedFailure
    def test_line_fail(self):
        self.check_code('601', 2)

    @unittest.expectedFailure
    def test_code_fail(self):
        self.check_code('401', 2)

    def test_missing_keys_error(self):
        mandatory_codes = ['O601', 'O602', 'O603']
        for code in mandatory_codes:
            self.check_code(code, 21)



if __name__ == '__main__':
    unittest.main()
