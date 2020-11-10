from setuptools import setup, find_packages # type: ignore

setup(
    name='iplib3',
    version='0.1.0',
    description="A modern, object-oriented approach to IP addresses.",
    author="Lari Liuhamo",
    author_email='lari.liuhamo+pypi@gmail.com',
    url='https://github.com/Diapolo10/iplib',
    packages=find_packages(include=['iplib3', 'iplib3.*']),
    install_requires=[],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
)
