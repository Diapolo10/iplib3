#! /usr/bin/env python3

from setuptools import setup, find_packages # type: ignore
from pathlib import Path

with open(Path(__file__).parent / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iplib3',
    version='0.1.3',
    description="A modern, object-oriented approach to IP addresses.",
    license="MIT License (MIT License)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Lari Liuhamo",
    author_email='lari.liuhamo+pypi@gmail.com',
    url='https://github.com/Diapolo10/iplib3',
    packages=find_packages(include=['iplib3', 'iplib3.*']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed',
    ],
    install_requires=[],
    setup_requires=['pytest-runner', 'flake8', 'setuptools', 'wheel'],
    tests_require=['pytest'],
)
