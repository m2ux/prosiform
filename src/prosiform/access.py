"""Bounded source capture through verified no-follow directory walks."""

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
        return Absent(name) if raised.errno in (errno.ENOENT, errno.ENOTDIR) else raised
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


def walked_directory(
    root: Path, path: str, observed: list[tuple[str, int, int]]
) -> int:
    """Walk relative components before normalization and retain directory identity."""
    if path.startswith("/"):
        raise Outside(path)
    held = os.open(root, DIRECTORY)
    current = str(root)
    info = os.fstat(held)
    observed.append((current, info.st_dev, info.st_ino))
    try:
        for name in path.split("/"):
            if name in ("", "."):
                continue
            below = descend(held, name, DIRECTORY)
            os.close(held)
            held = below
            current = os.path.normpath(os.path.join(current, name))
            info = os.fstat(held)
            observed.append((current, info.st_dev, info.st_ino))
        return held
    except BaseException:
        os.close(held)
        raise


def directory(root: Path, path: str) -> tuple[tuple[str, int, int], ...]:
    """Verify every component of a directory declaration without following links."""
    observed: list[tuple[str, int, int]] = []
    os.close(walked_directory(root, path, observed))
    return tuple(observed)


def opened(
    root: Path, path: str, observed: list[tuple[str, int, int]] | None = None
) -> int:
    """Open one regular source after verifying its authored component walk."""
    if path.startswith("/"):
        raise Outside(path)
    identities = [] if observed is None else observed
    parent, _, name = path.rpartition("/")
    if name in RESERVED:
        raise Absent(path)
    held = walked_directory(root, parent, identities)
    try:
        file = descend(held, name, FILE)
    finally:
        os.close(held)
    try:
        info = os.fstat(file)
        if not stat.S_ISREG(info.st_mode):
            raise Absent(path)
        identities.append(
            (os.path.normpath(str(root / path)), info.st_dev, info.st_ino)
        )
    except BaseException:
        os.close(file)
        raise
    return file


def read_source(
    root: Path,
    path: str,
    *,
    limit: int | None = None,
    observed: list[tuple[str, int, int]] | None = None,
) -> bytes:
    """Read at most the supplied byte budget plus one byte to detect overflow."""
    with os.fdopen(opened(root, path, observed), "rb") as handle:
        return handle.read() if limit is None else handle.read(limit + 1)
