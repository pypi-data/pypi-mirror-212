# -*- coding: utf-8 -*-
# Copyright 2023 tkwant authors.
#
# This file is part of tkwant.  It is subject to the license terms in the file
# LICENSE.rst found in the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/license.html.
# A list of tkwant authors can be found in
# the file AUTHORS.rst at the top-level directory of this distribution and at
# https://tkwant.kwant-project.org/doc/stable/pre/authors.html.
"""tkwant, a Python package for time-resolved quantum transport."""

import os

from ._common import TKWANT_VERSION
from ._common import TkwantDeprecationWarning
from . import _logging as logging

__all__ = ['TkwantDeprecationWarning', 'logging']

for module in ('system', 'leads', 'onebody', 'manybody', 'mpi',
               'greenfunctions', 'special', 'interaction'):
    exec('from . import {0}'.format(module))
    __all__.append(module)


del module  # remove cruft from namespace

# set version attribute
__version__ = TKWANT_VERSION


def test(args=None):
    """Run tkwant's unit tests.
       Optional command line **args** can be provided as a list of strings."""
    import pytest
    command = [os.path.dirname(os.path.realpath(__file__))]
    if args:
        command += args
    return pytest.main(command)
