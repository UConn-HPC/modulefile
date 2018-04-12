# Released into the Public Domain:
# https://creativecommons.org/publicdomain/zero/1.0/legalcode

"""Unit tests for modulefile."""

import pytest
import six

from modulefile import ENV_DIRS, cli, discover_paths, modulefile, parse_args


# modulefile
def test_modulefile_creates_string():
    contents = modulefile('/opt/myapp/1.0', ['myapp', '1.0'])
    assert isinstance(contents, six.string_types)


# cli
def test_cli_prints_modulefile(capsys):
    contents = modulefile('/opt/myapp/1.0', ['myapp', '1.0'])
    cli(['/opt/myapp/1.0'])
    stdout, _ = capsys.readouterr()
    assert stdout.rstrip() == contents


# parse_args
def test_parse_args_missing_prefix_raises_error():
    assert pytest.raises(SystemExit, parse_args, [''])


def test_parse_args_short_prefix_raises_error():
    assert pytest.raises(SystemExit, parse_args, ['/opt'])


def test_parse_args_relative_prefix_raises_error():
    assert pytest.raises(SystemExit, parse_args, ['opt/myapp/1.0'])


def test_parse_args_no_env_separator_raises_error():
    assert pytest.raises(SystemExit, parse_args,
                         ['/opt/myapp/1.0', '--env', 'BAR_baz'])


def test_parse_args_only_with_prefix():
    args = parse_args(['/opt/myapp/1.0'])
    assert args.prefix == '/opt/myapp/1.0'


def test_parse_args_with_envs():
    args = parse_args(['/opt/myapp/1.0',
                       '--env', 'FOO=bar',
                       '--env', 'BAR=baz'])
    assert args.env == ['FOO=bar', 'BAR=baz']


def test_parse_args_with_deps():
    args = parse_args(['/opt/myapp/1.0',
                       '--dep', 'gcc/5',
                       '--dep', 'netcdf/4'])
    assert args.dep == ['gcc/5', 'netcdf/4']


# discover_paths
def test_discover_paths_finds_all_directories(tmpdir):
    paths = discover_paths('/nonexistant/path')
    assert not paths
    tmpdir.yaml_create('''
    bin: {}
    info: {}
    man: {}
    share:
        info: {}
        man: {}
    include: {}
    lib:
        pkgconfig: {}
    lib32:
        pkgconfig: {}
    lib64:
        pkgconfig: {}
    ''')
    paths = discover_paths(str(tmpdir))
    assert paths

    def check_paths(env, dirs):
        """Check that path exists."""
        paths_ = [str(tmpdir.join(top_dir)) for top_dir in dirs]
        assert set(paths[env]) == set(paths_)

    for env, dirs in ENV_DIRS.items():
        check_paths(env, dirs)
