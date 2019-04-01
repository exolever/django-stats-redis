#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages


def get_version(*file_paths):
    """Retrieves the version from ratings/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("stats", "__init__.py")

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-stats-redis',
    version=version,
    description='Manage stats with Redis within mixin for Django models',
    long_description=readme + '\n\n' + history,
    author='marfyl',
    author_email='marfyl.dev@gmail.com',
    url='https://github.com/exolever/django-stats',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django-appconf', 'redis'],
    license="MIT",
    zip_safe=False,
    keywords=['python', 'django', 'stats', 'redis'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
