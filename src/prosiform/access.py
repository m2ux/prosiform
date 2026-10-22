"""One source's bytes, read under the allowed root and through no symbolic link.

A path checked as a string and the path an open reaches are two different
paths. Every segment a reference writes can sit inside the root while the
file the open arrives at sits outside it, because a symbolic link below
the root is resolved by the open and by nothing before it. The read below
therefore descends the root-relative path one segment at a time, each
segment opened against the directory above it and none of them followed,
so the bytes it returns came from a file the root holds.

The root is canonicalized once, by the caller, and the walk starts at the
directory that canonicalization named. A link at or above the root is the
caller's own spelling of the root; a link below it is an alias this
module refuses whatever it points at, because a dependency base that
varied with which alias was discovered first would make a closure depend
on discovery order rather than on the documents it reaches.

The walk is the confinement, so it holds the root on its own terms: an
empty segment, a `.` and a `..` are each refused here rather than
descended, and the root-relative path a normalization produced carries
none of them. A regular file is the only thing the read returns; a
directory, a device and a socket each name no document.

Rooted, no-follow access is what the policy requires, so this module is
the environment it declares: a platform offering no `O_NOFOLLOW` and no
`O_DIRECTORY` fails at import rather than reading a source through a
check that weakened to a string comparison.
"""

import errno
import os
import stat
from pathlib import Path

SEPARATOR = "/"
RESERVED = ("", ".", "..")

REQUIRED = ("O_NOFOLLOW", "O_DIRECTORY", "O_CLOEXEC")
ABSENT = [flag for flag in REQUIRED if not hasattr(os, flag)]
if ABSENT:
    raise ImportError(
        f"rooted, no-follow source access needs {', '.join(ABSENT)}, which this "
        f"platform does not offer"
    )

ROOT = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY
FILE = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
DIRECTORY = FILE | os.O_DIRECTORY


class Unreadable(Exception):
    """A path the allowed root does not yield to a rooted, no-follow read.

    The message is the root-relative path the refusal is about, so a
    caller naming the reference it read states the refusal in one line.
    """


class Outside(Unreadable):
    """A path carrying a segment the walk cannot hold under the root."""


class Symlinked(Unreadable):
    """A path reaching a source through a symbolic link below the root."""


class Absent(Unreadable):
    """A path under the root naming no regular file."""


def refusal(parent: int, name: str, raised: OSError) -> BaseException:
    """What one refused segment is, read from the directory entry itself.

    The open is the safeguard and the entry is only how the refusal is
    named: a `lstat` says whether the segment the walk declined to follow
    is a link, which `O_NOFOLLOW` reports as the same error a directory
    loop does. A fault that is neither a link nor a missing entry is the
    operating system's, and it is raised as it arrived.
    """
    try:
        entry = os.lstat(name, dir_fd=parent)
    except OSError:
        return Absent(name)
    if stat.S_ISLNK(entry.st_mode):
        return Symlinked(name)
    if raised.errno in (errno.ENOENT, errno.ENOTDIR):
        return Absent(name)
    return raised


def descend(parent: int, name: str, flags: int) -> int:
    """One segment opened against the directory above it, following no link."""
    try:
        return os.open(name, flags, dir_fd=parent)
    except OSError as raised:
        raise refusal(parent, name, raised) from raised


def opened(root: Path, path: str) -> int:
    """One source's open descriptor, reached by descending from the allowed root.

    The path is root-relative and spelled with forward slashes, which is
    what a normalized reference carries. The caller owns the descriptor
    this returns and closes it; a walk that refuses a segment closes
    everything it opened and raises instead.
    """
    walked = path.split(SEPARATOR)
    if any(segment in RESERVED for segment in walked):
        raise Outside(path)
    held = os.open(root, ROOT)
    try:
        for name in walked[:-1]:
            below = descend(held, name, DIRECTORY)
            os.close(held)
            held = below
        file = descend(held, walked[-1], FILE)
    except BaseException:
        os.close(held)
        raise
    os.close(held)
    try:
        if not stat.S_ISREG(os.fstat(file).st_mode):
            raise Absent(path)
    except BaseException:
        os.close(file)
        raise
    return file


def read_source(root: Path, path: str) -> bytes:
    """One source's bytes, read by descending its path from the allowed root."""
    with os.fdopen(opened(root, path), "rb") as handle:
        return handle.read()
