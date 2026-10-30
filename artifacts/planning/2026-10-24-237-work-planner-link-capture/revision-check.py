"""Run a named instrument at one merged revision in a throwaway checkout.

Usage:
  python3 revision-check.py --project <checkout> --revision <sha-or-branch> -- <command> [args...]
      [--keep]

The checkout is created detached, the command runs at its top level with the revision's own files,
and the checkout is removed afterwards unless --keep is given. Exit status is the command's.

The skill requires a criterion to be verified in a checkout of the merged revision it is verifying,
and states that a checkout being edited is not that revision. A named branch is a moving reference
rather than a revision, so it is resolved to its current commit first and the command runs at that
commit. git also refuses one commit in two worktrees, so the checkout is detached rather than
placed on the branch.

A run that fails still removes its checkout, so a repeated verification leaves nothing behind.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def git(project: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(['git', *args], cwd=project, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--keep', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = [a for a in args.command if a != '--']
    if not command:
        sys.exit('no command supplied after --')

    resolved = git(args.project, 'rev-parse', '--verify', f'{args.revision}^{{commit}}')
    if resolved.returncode != 0:
        sys.exit(f'revision not found: {args.revision}')
    commit = resolved.stdout.strip()

    root = Path(tempfile.mkdtemp(prefix='revision-check-'))
    tree = root / commit[:8]
    added = git(args.project, 'worktree', 'add', '--detach', str(tree), commit)
    if added.returncode != 0:
        sys.exit(f'worktree add failed: {added.stderr.strip()}')
    try:
        print(json.dumps({'revision': commit, 'checkout': str(tree)}))
        return subprocess.run(command, cwd=tree).returncode
    finally:
        if args.keep:
            print(f'kept: {tree}')
        else:
            git(args.project, 'worktree', 'remove', '--force', str(tree))
            git(args.project, 'worktree', 'prune')
            os.rmdir(root)


if __name__ == '__main__':
    sys.exit(main())
