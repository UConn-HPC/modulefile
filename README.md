# modulefile

[![Build Status](https://travis-ci.org/UConn-HPC/modulefile.svg?branch=master)](https://travis-ci.org/UConn-HPC/modulefile)
[![Coverage](https://codecov.io/gh/UConn-HPC/modulefile/graphs/badge.svg)](https://codecov.io/gh/UConn-HPC/modulefile)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

Search prefix directory of installed software and generate
[environmental modules](https://en.wikipedia.org/wiki/Environment_Modules_(software))
modulefile.

# Installation

```bash
git clone https://github.com/UConn-HPC/modulefile
pip install --user --upgrade --editable modulefile/
```

Make sure that `~/.local/bin` or similar is in your path per
[PEP 370](https://www.python.org/dev/peps/pep-0370/).

# Usage

``` bash
modulefile /path/to/my/app/1.0 > /path/to/my/modulefile/dir/app/1.0
```

# Tests

Virtual environments and tests are orchestrated using `tox`.  Install
`tox` using `pip`:

    pip install --user tox

Run all tests using:

    tox

Debug failing tests:

    tox -- --pdb

If you add dependencies and get import errors, you need to recreate
the tox environment:

    tox --recreate

When you edit the files, you're likely going to create lots of linter
errors caught by the tox unit tests if your text editor doesn't have
interactive error reporting.  If you use Emacs, you can configure it
for python development by installing
[elpy](https://github.com/jorgenschaefer/elpy).
