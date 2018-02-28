#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Cyrille Favreau <cyrille.favreau@gmail.ch>
#
# This file is part of ipyTransferFunction
# <https://github.com/favreau/ipyTransferFunction>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""setup.py"""
import os
import re

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession
from optparse import Option

BASEDIR = os.path.dirname(os.path.abspath(__file__))

version_file = 'version.py'
version_line = open(version_file, "rt").read()
version_regexp = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(version_regexp, version_line, re.M)
if mo:
    version_str = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in %s.' % (version_file,))


def parse_reqs(reqs_file):
    ''' parse the requirements '''
    options = Option('--workaround')
    options.skip_requirements_regex = None
    options.isolated_mode = True
    install_reqs = parse_requirements(reqs_file, options=options, session=PipSession())
    return [str(ir.req) for ir in install_reqs]


REQS = parse_reqs(os.path.join(BASEDIR, "requirements.txt"))
EXTRA_REQS_PREFIX = 'requirements_'
EXTRA_REQS = {}
for file_name in os.listdir(BASEDIR):
    if not file_name.startswith(EXTRA_REQS_PREFIX):
        continue
    base_name = os.path.basename(file_name)
    (extra, _) = os.path.splitext(base_name)
    extra = extra[len(EXTRA_REQS_PREFIX):]
    EXTRA_REQS[extra] = parse_reqs(file_name)

exec(open('version.py').read())
setup(name='ipyTransferFunction',
      version=version_str,
      description='Transfer function editor for Jupyter notebook',
      packages=['ipyTransferFunction'],
      url='https://github.com/favreau/ipyTransferFunction.git',
      author='Cyrille Favreau',
      author_email='cyrille.favreau@gmail.com',
      license='GNU LGPL',
      install_requires=REQS,
      extras_require=EXTRA_REQS,)
