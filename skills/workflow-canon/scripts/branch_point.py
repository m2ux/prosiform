"""Find a corpus tree's branch point, and check it out beside the tree.

The branch point is the nearest of the merge-bases of the tree's HEAD with origin/workflows and with
each origin/iNN/workflows integration branch: the one with the fewest commits between it and HEAD.
A branch cut from an initiative's integration branch measures against that branch, and every other
branch against origin/workflows. The remote-tracking refs are read as they stand; nothing is fetched.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

INTEGRATION = re.compile(r'^refs/remotes/origin/(?:workflows|i\d\d/workflows)$')


class BranchPointError(Exception):
    """The branch point cannot be found or checked out; the message says why."""


def git(tree: Path, *args: str) -> str | None:
    """A git command's trimmed stdout in tree, or None when it fails."""
    run = subprocess.run(['git', *args], cwd=tree, capture_output=True, text=True)
    return run.stdout.strip() if run.returncode == 0 else None


def integration_refs(tree: Path) -> list[str]:
    listing = git(tree, 'for-each-ref', '--format=%(refname)', 'refs/remotes/origin/') or ''
    return sorted(ref for ref in listing.splitlines() if INTEGRATION.match(ref))


def branch_point(tree: Path) -> tuple[str, str]:
    """The nearest integration ref's short name and its merge-base with HEAD."""
    refs = integration_refs(tree)
    if not refs:
        raise BranchPointError(f'{tree} has no origin/workflows or origin/iNN/workflows ref')
    candidates = []
    for ref in refs:
        base = git(tree, 'merge-base', 'HEAD', ref)
        if base:
            distance = int(git(tree, 'rev-list', '--count', f'{base}..HEAD') or 0)
            candidates.append((distance, ref, base))
    if not candidates:
        raise BranchPointError(f'HEAD of {tree} has no merge-base with {", ".join(refs)}')
    _, ref, base = min(candidates)
    return ref.removeprefix('refs/remotes/'), base


def populated_submodules(tree: Path) -> list[str]:
    """Paths of tree's submodules whose files are on disk.

    `git submodule status` marks an uninitialised submodule with a leading `-`; every other
    state has a working tree.
    """
    listing = git(tree, 'submodule', 'status') or ''
    paths = []
    for line in listing.splitlines():
        if not line or line.startswith('-'):
            continue
        fields = line[1:].split()
        if len(fields) >= 2:
            paths.append(fields[1])
    return paths


def _remove_worktrees(worktrees: list[tuple[Path, Path]]) -> None:
    for repository, path in worktrees:
        subprocess.run(['git', 'worktree', 'remove', '--force', str(path)], cwd=repository,
                       capture_output=True)


def _fill_submodules(source: Path, target: Path) -> list[tuple[Path, Path]]:
    """Give target the submodules source has, each at the commit target records.

    A guard reads a corpus as a filesystem, so a target missing a submodule the source carries
    holds a smaller corpus, and every guard that reads the missing files reports the difference
    as the edit's doing. The commit comes from target, so a pointer bump between the two stands.

    Returns each (submodule repository, worktree) pair for removal.
    """
    filled: list[tuple[Path, Path]] = []
    for path in populated_submodules(source):
        commit = git(target, 'rev-parse', f'HEAD:{path}')
        if commit is None:
            continue
        destination = target / path
        if destination.is_dir() and not any(destination.iterdir()):
            destination.rmdir()
        run = subprocess.run(
            ['git', 'worktree', 'add', '--detach', '--quiet', str(destination), commit],
            cwd=source / path, capture_output=True, text=True)
        if run.returncode != 0:
            _remove_worktrees(filled)
            raise BranchPointError(
                f'could not check out submodule {path} at {commit[:12]}: {run.stderr.strip()}')
        filled.append((source / path, destination))
    return filled


@contextmanager
def checked_out(tree: Path, commit: str) -> Iterator[Path]:
    """A detached worktree of tree's repository at commit, removed on exit.

    Submodules tree carries are filled in at the commits that worktree records, so both sides of
    a comparison hold the same corpus roots.
    """
    holder = Path(tempfile.mkdtemp(prefix='workflow-canon-base-'))
    path = holder / 'tree'
    added = subprocess.run(['git', 'worktree', 'add', '--detach', '--quiet', str(path), commit],
                           cwd=tree, capture_output=True, text=True)
    submodules: list[tuple[Path, Path]] = []
    try:
        if added.returncode != 0:
            raise BranchPointError(f'could not check out {commit[:12]}: {added.stderr.strip()}')
        submodules = _fill_submodules(tree, path)
        yield path
    finally:
        _remove_worktrees(submodules)
        if added.returncode == 0:
            subprocess.run(['git', 'worktree', 'remove', '--force', str(path)], cwd=tree,
                           capture_output=True)
        shutil.rmtree(holder, ignore_errors=True)
