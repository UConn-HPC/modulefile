# Released into the Public Domain:
# https://creativecommons.org/publicdomain/zero/1.0/legalcode

"""Generate environmental modulefile from prefix directory."""

from __future__ import print_function
import argparse
from collections import OrderedDict
import logging
import os
import sys

import jinja2 as j2


# Map of environmental variables to prepend, depending on directory found.
ENV_DIRS = OrderedDict({
    'PATH': ['bin'],
    'CPATH': ['include'],
    'LD_LIBRARY_PATH': ['lib', 'lib32', 'lib64'],
    'PKG_CONFIG_PATH': ['pkgconfig'],
    'MANPATH': ['man', 'share/man'],
    'INFOPATH': ['info', 'share/info'],
})


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(prog=__name__, description=__doc__)
    parser.add_argument('prefix',
                        help='installation path containing application',
                        type=str)
    parser.add_argument('--pkg_name',
                        help=('package name '
                              '(default: second-last prefix directory)'),
                        type=str)
    parser.add_argument('--pkg_version',
                        help=('package version '
                              '(default: last prefix directory)'),
                        type=str)
    parser.add_argument('--env',
                        help=('environmental variable key=value pair. '
                              'Can be specified multiple times. '
                              'ex. --env LICENSE_FILE=/path/to/license'),
                        type=str, action='append')
    parser.add_argument('--verbosity',
                        help=('verbosity (default: %(default)s)'),
                        default='debug', choices=['warn', 'info', 'debug'])
    args = parser.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.verbosity.upper()),
                        format='%(levelname)-6s %(message)s')
    error = False
    dirs = os.path.normpath(args.prefix).split(os.sep)
    if not os.path.isabs(args.prefix):
        sys.stderr.write('Error: Prefix must be an absolute path')
        error = True
    if len(dirs[1:]) < 2 and \
       (args.pkg_name is None or args.pkg_version is None):
        sys.stderr.write(('Error: Prefix is too short to '
                          'infer package name and version'))
        error = True
    if error:
        parser.print_help()
        sys.exit(2)
    if args.pkg_name is None:
        args.pkg_name = dirs[-2]
        logging.info('Inferred package name from prefix as: %s',
                     args.pkg_name)
    if args.pkg_version is None:
        args.pkg_version = dirs[-1]
        logging.info('Inferred package version from prefix as: %s',
                     args.pkg_version)
    return args


def cli(argv=None):
    """Entrypoint to */bin/modulefile executable."""
    args = parse_args(argv)
    paths = discover_paths(args.prefix)
    contents = modulefile(args.prefix, [args.pkg_name, args.pkg_version],
                          paths=paths)
    print(contents)


def discover_paths(prefix):
    """Return paths."""
    paths = OrderedDict()
    for env, top_dirs in ENV_DIRS.items():
        for top_dir in top_dirs:
            path = os.path.join(prefix, top_dir)
            if os.path.exists(path):
                if env in paths.keys():
                    paths[env].append(path)
                else:
                    paths[env] = [path]
    return paths


def modulefile(prefix, pkg, deps=None, paths=None, envs=None):
    """Return modulefile string."""
    env = j2.Environment(loader=j2.PackageLoader('modulefile'))
    template = env.get_template('modulefile.j2')
    if paths is not None:
        for env, dirs in paths.items():
            paths[env] = ':'.join(dirs)
    output = template.render(
        prefix=prefix,
        pkg=pkg,
        deps=deps,
        paths=paths,
        envs=envs,
    )
    logging.debug('Generated modulefile:\n%s', output)
    return output
