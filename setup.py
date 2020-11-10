#! /usr/bin/env python3

from setuptools import setup, find_packages # type: ignore
from pathlib import Path

with open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iplib3',
    version='0.1.1',
    description="A modern, object-oriented approach to IP addresses.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Lari Liuhamo",
    author_email='lari.liuhamo+pypi@gmail.com',
    url='https://github.com/Diapolo10/iplib3',
    packages=find_packages(include=['iplib3', 'iplib3.*']),
    install_requires=[],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
)
