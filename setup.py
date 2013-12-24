#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import distutils
import re
from os.path import join, abspath, dirname
__version__ = re.search(
    "__version__\s*=\s*'(.*)'",
    open(join(dirname(abspath(__file__)), 'promarsh/__init__.py')).read(),
    re.M).group(1)


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name).read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            requirements.append(re.sub(r'\s*-f\s+.*#egg=(.*)-([0-9]+\.[0-9.]*)(.*)$', r'\1==\2\3', line))
        else:
            requirements.append(line)
            return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
            return dependency_links


class PyTest(distutils.core.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        import unittest
        setup_file = sys.modules['__main__'].__file__
        setup_dir = os.path.abspath(os.path.dirname(setup_file))
        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover(setup_dir)
        test_runner.run(test_suite)


distutils.core.setup(
    name='promarsh',
    version=__version__,
    description='Protocol description packet',
    long_description=open("README.md").read(),
    author='Justin Wong',
    author_email='justin.w.xd@gmail.com',
    license="BSD",
    platforms=["Linux"],
    url='https://github.com/bigeagle/promarsh',
    packages=['promarsh'],
    package_dir={'promarsh': 'promarsh'},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2.6",
    ],
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt'),
    cmdclass={'test': PyTest},
)
