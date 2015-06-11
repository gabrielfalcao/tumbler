#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <tumbler - flask bootstrapper>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ast
import os
from setuptools import setup, find_packages


class VersionFinder(ast.NodeVisitor):

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == 'version':
                self.version = node.value.s
        except:
            pass


def read_version():
    """Read version from sure/version.py without loading any files"""
    finder = VersionFinder()
    finder.visit(ast.parse(local_file('tumbler', '__init__.py')))
    return finder.version


local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f)).read()


install_requires = [
    'Flask==0.10.1',
    'Flask-Assets==0.10',
    'Jinja2==2.7.3',
    'MarkupSafe==0.23',
    'coloredlogs==1.0',
    'plant==0.1.1',
    'requests==2.5.1',
    'Flask-SQLAlchemy==2.0',
]


if __name__ == '__main__':
    setup(
        name='tumbler',
        version=read_version(),
        description=(
            'Tumbler is a simple layer that leverage flask with '
            'nice logs and automated settings management'
        ),
        author='Gabriel Falcao',
        author_email='gabriel@nacaolivre.org',
        include_package_data=True,
        url='http://github.com/gabrielfalcao/tumbler',
        packages=find_packages(exclude=['*tests*']),
        install_requires=install_requires,
        test_suite='nose.collector',
        entry_points={
            'console_scripts': ['tumbler = tumbler.cli:main'],
        },
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        ],
        package_data={
            'tumbler': ['requirements.txt'],
        },
    )
