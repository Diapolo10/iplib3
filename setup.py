#! /usr/bin/env python3

from setuptools import setup, find_packages # type: ignore
from pathlib import Path
import re


with open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(Path(__file__).parent / 'pyproject.toml', encoding='utf-8') as f:
    version = re.search(
        r"version = '(?P<version>.+?)'",
        f.read()
    ).groupdict().get('version')

setup(
    name='iplib3',
    version=version,
    description="A modern, object-oriented approach to IP addresses.",
    license="MIT License",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Lari Liuhamo",
    author_email='lari.liuhamo+pypi@gmail.com',

    url='https://github.com/Diapolo10/iplib3',
    project_urls={
        'Source code': 'https://github.com/Diapolo10/iplib3',
        'Tracker': 'https://github.com/Diapolo10/iplib3/issues',
    },

    packages=find_packages(include=['iplib3', 'iplib3.*']),
    keywords='network networking ip ipaddress address python3 pathlib',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed',
    ],

    install_requires=[],
    python_requires='>=3.6',
    setup_requires=['pytest-runner', 'flake8', 'setuptools', 'wheel'],
    tests_require=['pytest'],
)
