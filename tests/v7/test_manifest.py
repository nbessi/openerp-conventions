# -*- coding: utf-8 -*-
import unittest
from tests.base_test import ConventionCheckTest


class EmptyManifestChecker(ConventionCheckTest):

    _file_path = 'empty__openerp__.py'
    _file_name = '__openerp__.py'

    @unittest.expectedFailure
    def test_line_fail(self):
        """Ensure line check fail"""
        self.check_code('601', 2)

    @unittest.expectedFailure
    def test_code_fail(self):
        """Ensure code check fail"""
        self.check_code('401', 2)

    def test_missing_keys_error(self):
        """Test that missing mandatory key are detected"""
        mandatory_codes = ['O601', 'O602', 'O603']
        for code in mandatory_codes:
            self.check_code(code, 21)

class FaultManifestChecker(ConventionCheckTest):

    _file_path = 'faulty__openerp__.py'
    _file_name = '__openerp__.py'


    def test_O600(self):
        """Test code O600"""
        self.check_code('O600', 22)

    def test_O604(self):
        """Test code O604"""
        self.check_code('O604', 23)



if __name__ == '__main__':
    unittest.main()
