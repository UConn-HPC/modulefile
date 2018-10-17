# Released into the Public Domain:
# https://creativecommons.org/publicdomain/zero/1.0/legalcode

"""Generate environmental modulefile from prefix directory."""

import sys
# Prefer setuptools over distutils.
from setuptools import find_packages, setup


# Boilerplate for pytest-runner suggested by pypi page.
NEEDS_PYTEST = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
# Also add pytest itself because it is a runtime dependency of pytest-runner.
PYTEST_RUNNER = ['pytest-runner', 'pytest'] if NEEDS_PYTEST else []

setup(
    # Essentials.
    name='modulefile',
    version='0.1.dev0',
    description=__doc__,

    # Non-metadata.
    entry_points={
        'console_scripts': [
            'modulefile=modulefile:cli'
        ],
    },
    install_requires=[
        'enum34',
        'jinja2',               # Template for modulefile.
    ],
    packages=find_packages(exclude=['test']),
    package_data={'modulefile': ['templates/*.j2']},
    include_package_data=True,
    setup_requires=PYTEST_RUNNER,
    tests_require=[
        'pytest',               # Powerful test suite.
        'pytest-cov',           # coverage.py wrapper.
        'pytest-pylint',        # pylint wrapper.
        'pytest-yamltree',      # Easily create directory trees.
        'six',                  # Python 2 and 3 compatibility.
    ],

    # Metadata.
    author='Pariksheet Nanda',
    author_email='pariksheet.nanda@uconn.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Tcl',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: System Administration',
        'Topic :: Utilities',
    ],
    url='https://github.com/UConn-HPC/modulefile',
)
