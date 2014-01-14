# -*- coding: utf-8 -*-
"""Provide base checkers metaclass"""


class BaseCheckerMeta(type):
    """Base checker type
    This will automatically register an instance of any checker subclass
    into self._checks. This will be used by OpenERPConventionsChecker
    to run all checkers. A checker must have a visit(root_node) function
    implemented.

    Checker have to be split by topic like class, manifest, init file etc.

    Code is inspired from pep8-naming extension

    """
    def __init__(self, class_name, bases, namespace):
        self.errors = []
        self.filename = None
        try:
            self._checks.append(self())
        except AttributeError:
            self._checks = []


class BaseChecker(object):
    "Base class for conventions checks."
    __metaclass__ = BaseCheckerMeta

    def set_filename(self, filename):
        self.filename = filename
