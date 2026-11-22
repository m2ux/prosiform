"""Read source files and declaration heads through verified directory walks.

`opened` supplies regular-file descriptors and `walked_directory`
records directory identities. The module requires the platform flags
named by `REQUIRED`.
"""

import errno
import os
import stat
from collections.abc import Callable
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
    """Open one segment with `flags`, classifying any failure through `refusal`."""
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
    """Return the directory identities verified by `walked_directory`."""
    observed: list[tuple[str, int, int]] = []
    os.close(walked_directory(root, path, observed))
    return tuple(observed)


def opened(
    root: Path, path: str, observed: list[tuple[str, int, int]] | None = None
) -> int:
    """Open a regular source after its `walked_directory` component walk.

    Absolute paths raise `Outside`; reserved final names raise `Absent`.
    `descend` opens the final name with `FILE` flags, and a nonregular
    descriptor raises `Absent`. Append the file identity to `observed`
    when supplied, and close every descriptor a refusal leaves open.
    """
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
    """Read a source through `opened`, at most its byte budget plus one byte.

    The extra byte detects overflow. A missing limit reads the whole file.
    """
    with os.fdopen(opened(root, path, observed), "rb") as handle:
        return handle.read() if limit is None else handle.read(limit + 1)


def read_head(
    root: Path,
    path: str,
    *,
    limit: int,
    ended: Callable[[int, bytes], bool],
    observed: list[tuple[str, int, int]] | None = None,
) -> bytes:
    """Read physical lines until `ended`, overflow, or end of file.

    `opened` owns the verified file access. `ended` receives each line's
    zero-based index and bytes; its first true answer ends the read.
    Apply the overflow-read bound `read_source` owns.
    """
    head = bytearray()
    with os.fdopen(opened(root, path, observed), "rb") as handle:
        index = 0
        while len(head) <= limit:
            line = handle.readline(limit + 1 - len(head))
            head += line
            if not line or ended(index, line):
                break
            index += 1
    return bytes(head)
