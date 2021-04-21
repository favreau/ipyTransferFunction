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
import pathlib
import pkg_resources
from setuptools import find_packages, setup

BASEDIR = os.path.dirname(os.path.abspath(__file__))

def parse_reqs(reqs_file):
    ''' parse the requirements '''
    install_reqs = list()
    with pathlib.Path(reqs_file).open() as requirements_txt:
        install_reqs = [str(requirement)
                        for requirement
                        in pkg_resources.parse_requirements(requirements_txt)]
    return install_reqs


REQS = parse_reqs(os.path.join(BASEDIR, "requirements.txt"))

# read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    packages=find_packages(),
    install_requires=REQS,
    name='ipyTransferFunction',
    description='Transfer function editor for Blue Brain BioExplorer',
    url='https://github.com/favreau/ipyTransferFunction.git',
    author='Cyrille Favreau',
    author_email='cyrille.favreau@epfl.ch',
    license='GNU LGPL')
