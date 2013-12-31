# -*- coding: utf-8 -*-
"""Provide base checkers metaclass"""


class BaseCheckerMeta(type):
    """Base checker type
    This will automatically register an instance of any checker subclass
    into self._cheks. This will be used by OpenERPConventionsChecker
    to run all checkers. A checker must have a visit(root_node) function
    implemented.

    Checker have to be split by topic like class, manifest, init file etc.

    Code is inspired from pep8-naming extention

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
