""" Version utility (partly from django project)
"""
import datetime
import functools
import subprocess
import typing
import os


def get_version(*, version: typing.Tuple[int, int, int], final: bool):
    """Return a PEP 440-compliant version number."""
    assert len(version) == 3

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases

    main = get_main_version(version)

    sub = ''
    if not final:
        git_changeset = get_git_changeset()
        assert git_changeset
        if git_changeset:
            sub = '.dev%s' % git_changeset

    return main + sub


def get_main_version(version):
    """Return main version (X.Y[.Z])."""
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


@functools.lru_cache()
def get_git_changeset():
    """Return a numeric identifier of the latest git changeset.
    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    # Repository may not be found if __file__ is undefined, e.g. in a frozen
    # module.
    if '__file__' not in globals():
        return None

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.run(
        'git log --pretty=format:%ct --quiet -1 HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=repo_dir, universal_newlines=True,
        check=True
    )
    timestamp = git_log.stdout
    timezone = datetime.timezone.utc
    try:
        timestamp = datetime.datetime.fromtimestamp(int(timestamp), tz=timezone)
    except ValueError:
        return None

    return timestamp.strftime('%Y%m%d%H%M%S')
