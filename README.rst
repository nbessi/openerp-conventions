OpenERP Conventions
========================

Check the OpenERP community addons conventions.

This module provides a plugin for ``flake8``, the Python code checker.


Installation (unreleased)
-------------------------

You can install, upgrade, ``openerp-conventions`` with these commands::

  $ git clone git@github.com:nbessi/openerp-conventions.git
  $ cd openerp-conventions
  $ path_to_python2 setup.py develop
  (If you do not use a Python virtual env, it may require root permission)


Plugin for Flake8
-----------------

When both ``flake8`` and ``openerp-conventions`` are installed, the plugin is
available in ``flake8``::

  $ flake8 --version
  2.1.0 (pep8: 1.4.6, OpenERP convention: 0.0.1, pyflakes: 0.7.3, mccabe: 0.2.1)

By default the plugin is enabled.

These error codes are emitted:

+------+-------------------------------------------------------------+
| code | sample message                                              |
+======+=============================================================+
| O600 |Warning unknow manifest key                                  |
+------+-------------------------------------------------------------+
| O601 | Manifest "name" key is missing                              |
+------+-------------------------------------------------------------+
| O602 | Manifest "description" key is missing                       |
+------+-------------------------------------------------------------+
| O603 | Manifest "licence" key is missing                           |
+------+-------------------------------------------------------------+
| O604 | Manifest licence should be AGPL-3                           |
+------+-------------------------------------------------------------+
| O701 | osv.osv is deprecated, please use orm.Model                 |
+------+-------------------------------------------------------------+
| O702 | osv.osv_memory is deprecated, please use orm.TransientModel |
+------+-------------------------------------------------------------+
| O703 | orm.Model class name should NOT use CapWords convention     |
+------+-------------------------------------------------------------+


Changes
-------

0.x - unreleased
````````````````
