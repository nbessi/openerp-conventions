# -*- coding: utf-8 -*-
"""OpenERP addons manifest aka __openerp__.py checker"""
import os
try:
    import ast
    from ast import NodeVisitor
except ImportError:
    from flake8.util import ast
    from ast import NodeVisitor

from common_checker.base_checker import BaseChecker

AGPL = 'AGPL-3'

ALLOWED_KEYS = ['name', 'version', 'author',
                'maintainer', 'category', 'complexity',
                'depends', 'description', 'website, st',
                'installable', 'auto_install',
                'license', 'application',
                'images', 'icon', 'web',
                'js', 'css', 'qweb']


class OpenERPManifestChecker(BaseChecker, ast.NodeVisitor):
    """ast.NodeVisitor subclass that check root ast.node.
    It checks class validity

    Please take look at ast.Node visitor for more information
    about visit/visitor behavior

    """
    O600 = 'Warning unknown Manifest key'
    O601 = 'Manifest "name" key is missing'
    O602 = 'Manifest "description" key is missing'
    O603 = 'Manifest "license" key is missing'
    O604 = 'Manifest license should be %s' % AGPL
    O605 = 'Manifest author key is missing'
    O606 = 'Manifest version key is missing'
    O607 = 'Manifest version is incorrect'
    O608 = 'Manifest website key is missing'
    O609 = 'Manifest init key is deprecated use data'
    O610 = 'Manifest update key is deprecated use data'
    O611 = 'Manifest application key is missing'
    O612 = 'Manifest complexity key is missing'
    O613 = ('Manifest complexity key is invalid it should be'
            ' easy, normal, or expert')
    O614 = 'Manifest data key is missing'
    O615 = 'Manifest data key should be a list'
    O616 = 'Manifest depends key should be a list'
    O617 = 'Manifest installable key is set to False'
    O618 = 'Manifest installable key should be a boolean'
    O619 = 'Manifest is not a valid RST'

    def make_error_tuple(self, code, node):
        """Make an error tuple used by flake8

        Uses input code to find corressponding property lookup

        :param code: string of code number must be set as propety
        :param node: ast node source of error

        :returns: (line number, col, text, type)

        """
        code_text = '%s %s' % (code, getattr(self, code))
        return (node.lineno, node.col_offset, code_text, type(self))

    def generic_visit(self, node):
        """Refer to Python ast NodeVisitor documentation"""
        # We have also to be compatible with editor mode that
        # create temp
        # TODO find a better way to ensure that is a manifest file
        if '__openerp__' in os.path.basename(self.filename):
            return ast.NodeVisitor.generic_visit(self, node)

    def make_dict(self, node):
        """Transforms node to real Python dict

        :param node: ast.node representing a dict

        :returns: a evaluated dict

        """
        res = ast.literal_eval(node)
        if not isinstance(res, dict):
            raise ValueError('Manifest node is not a dict')
        return res

    def ensure_key(self, node, manifest_dict, keyname, code):
        """Check if key is present"""
        if keyname not in manifest_dict:
            self.errors.append(self.make_error_tuple(code, node))

    def check_allowed_keys(self, node, manifest_dict):
        """Ensure code 600

        Check if manifest dict has a unknown key

        """
        for key in manifest_dict:
            if key not in ALLOWED_KEYS:
                faulty_node = next(x for x in node.keys
                                   if ast.literal_eval(x) == key)
                self.errors.append(self.make_error_tuple('O600', faulty_node))

    def get_nodes_from_key(self, dict_node, lk_key):
        index = 0
        for key in dict_node.keys:
            if ast.literal_eval(key) == lk_key:
                return (key, dict_node.values[index])
            index += 1
        return None, None

    def check_license_value(self, node, manifest_dict):
        """Check if license is AGPL, if it exists"""
        # Default to AGPL since, we don't need to
        # report a bad license if it doesn't exist
        # instead it will be reported by 0603
        if manifest_dict.get('license', AGPL) != AGPL:
            key, val = self.get_nodes_from_key(node, 'license')
            self.errors.append(self.make_error_tuple('O604', val))

    def visit_Dict(self, node):
        """Visits and validate orm.Model definition"""
        manifest_dict = self.make_dict(node)
        self.check_allowed_keys(node, manifest_dict)
        self.ensure_key(node, manifest_dict, 'name', 'O601')
        self.ensure_key(node, manifest_dict, 'description', 'O602')
        self.ensure_key(node, manifest_dict, 'license', 'O603')
        self.check_license_value(node, manifest_dict)
