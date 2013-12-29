# -*- coding: utf-8 -*-
"""OpenERP community addons standard plugin for flake8"""
import re

try:
    import ast
    from ast import NodeVisitor
except ImportError:
    from flake8.util import ast
    from ast import NodeVisitor


__version__ = '0.0.1'

# To improve manage spaces
INVALID_MODEL_CLASS = ['osv', 'osv.osv']
INVALID_TRANSIENT_CLASS = ['osv_memory']
MODEL_NAMES = ['Model', 'TransientModel', 'AbstractModel', 'BaseModel']

INVALID_CLASS_NAME = re.compile(r'([A-Z][a-z0-9]+)+')


class BaseCheckerMeta(type):
    """Base checker type
    This will automatically register an instance of any checker subclass
    into self._cheks. This will be used by OpenERPConventionsChecker
    to run all checkers. A checker must have a visit(root_node) function
    implemented.

    Checker have to be split by topic like class, manifest, init file etc.

    Code is inpired from pep8-naming extention

    """
    def __init__(self, class_name, bases, namespace):
        self.errors = []
        try:
            self._checks.append(self())
        except AttributeError:
            self._checks = []

BaseChecker = BaseCheckerMeta('BaseChecker',
                              (object,),
                              {'__doc__': "Base classfor conventions checks."})


class OpenERPConventionsChecker(object):
    """Check OpenERP conventions

    It will call the function 'visit(root_node)' f all checker instances
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


class OpenERPModelChecker(BaseChecker, ast.NodeVisitor):
    """ast.NodeVisitor subclass that check root ast.node.
    It checks class validity

    Please take look at ast.Node visitor for more information
    about visit/visitor behavior

    """

    invalid_name = INVALID_CLASS_NAME.match

    O701 = 'osv.osv is deprecated, please use orm.Model'
    O702 = 'osv.osv_memory is deprecated, please use orm.TransientModel'
    O703 = 'orm.Model class name should NOT use CapWords conventiont'

    def make_error_tuple(self, code, node):
        """Make an error tuple used by flake8

        Uses input code to find corressponding property lookup

        :param code: string of code number must be set as propety
        :param node: ast node source of error

        :returns: (line number, col, text, type)

        """
        code_text = '%s %s' % (code, getattr(self, code))
        return (node.lineno, node.col_offset, code_text, type(self))

    def check_model_type(self, node):
        """Check if deprecated osv.osv is used"""
        faulty = [x for x in node.bases if getattr(x, 'attr', None)
                  in INVALID_MODEL_CLASS]
        for fault in faulty:
            self.errors.append(self.make_error_tuple('O701', node))

    def check_model_transient_type(self, node):
        """Check if deprecated osv.osv_memory is used"""
        faulty = [x for x in node.bases if getattr(x, 'attr', None)
                  in INVALID_TRANSIENT_CLASS]
        for fault in faulty:
            self.errors.append(self.make_error_tuple('O702', node))

    def check_model_name(self, node):
        """Check is Model name follows conventions"""
        if any(x for x in node.bases if getattr(x, 'attr', None) in MODEL_NAMES):
            if self.invalid_name(node.name):
                self.errors.append(self.make_error_tuple('O703', node))

    def visit_ClassDef(self, node):
        """Visits and validate orm.Model definition"""
        self.check_model_type(node)
        self.check_model_transient_type(node)
        self.check_model_name(node)
