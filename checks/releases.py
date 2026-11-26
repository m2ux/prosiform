#!/usr/bin/env python3
"""Assert the release tags naming the commit under test state what its build reports.

The versioning policy, `docs/versioning.md`, tags a release as one commit
carrying a contract tag, `contract/vX.Y.Z`, and a build tag, `python/vX.Y.Z`
for the build `src/` holds. Each tag is written by hand beside a version the
build declares elsewhere, so this check holds the tags naming the
repository's HEAD to the build, as `check` states, and exits nonzero on any
fault.

A commit carrying no release tag passes, so the check constrains a release
and leaves every other commit alone; a checkout that fetched no tags reads
none. The build is the one `PROSIFORM_BUILD` names, read through the
invocation check's `reported`, so a build tag with no build configured fails
rather than passing unread.
"""

import re
import subprocess
import sys
from pathlib import Path

from documents import ROOT
from invocation import VERSION, Unreadable, reported
from runner import BuildNotConfigured

BUILD_TAG = "python"
CONTRACT_TAG = "contract"

RELEASE = re.compile(rf"^({BUILD_TAG}|{CONTRACT_TAG})/(.*)$")
NUMBER = re.compile(r"^v([0-9]+)\.([0-9]+)\.([0-9]+)$")
REPORTED = re.compile(r"(\S+)\s+\([^()\s]+\)\s*$")

Number = tuple[str, str, str]


def tags_at_head(repository: Path) -> list[str]:
    """Every tag `git tag --points-at HEAD` lists for the repository.

    An annotated tag is listed by the commit it names.
    """
    result = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=repository,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def reported_version() -> str:
    """The version the build under test reports: the word before its profile."""
    line = reported(VERSION).strip()
    found = REPORTED.search(line)
    if not found:
        raise Unreadable(
            f"the build reported {line!r} for {VERSION}, which names no version "
            "beside a profile"
        )
    return found.group(1)


def check(repository: Path) -> tuple[list[str], list[str]]:
    """What holds and what fails among the release tags naming HEAD.

    - **A release tag.** A tag under `python/` or `contract/`; a tag under
      any other prefix names something other than a release and is passed
      over. A release tag whose name is not `vX.Y.Z` states no version and
      fails.
    - **A build tag.** Its version is the version the build under test
      reports, because a build tag asserts what the build reports.
    - **A contract tag beside a build tag.** Its major and minor are the
      build tag's, since a build's major and minor are the contract revision
      it implements. A contract tag alone is a revision tagged in its own
      right and is compared with nothing.

    The build runs only when a build tag names HEAD. Raises
    `BuildNotConfigured` or `Unreadable` when it does and the build's version
    cannot be read.
    """
    passed: list[str] = []
    failures: list[str] = []
    numbers: dict[str, list[tuple[str, Number]]] = {BUILD_TAG: [], CONTRACT_TAG: []}
    for tag in tags_at_head(repository):
        release = RELEASE.match(tag)
        if not release:
            continue
        spelled = NUMBER.match(release.group(2))
        if not spelled:
            failures.append(f"{tag}: a release tag names its version as vX.Y.Z")
            continue
        major, minor, patch = spelled.groups()
        numbers[release.group(1)].append((tag, (major, minor, patch)))

    if not numbers[BUILD_TAG]:
        for contract, _ in numbers[CONTRACT_TAG]:
            passed.append(f"ok   {contract} — a contract revision tagged alone")
        return passed, failures

    version = reported_version()
    for tag, number in numbers[BUILD_TAG]:
        tagged = ".".join(number)
        if tagged == version:
            passed.append(f"ok   {tag} — the build reports {version}")
        else:
            failures.append(f"{tag}: the build reports {version}, not {tagged}")
        for contract, revision in numbers[CONTRACT_TAG]:
            if revision[:2] == number[:2]:
                passed.append(f"ok   {tag} — implements {contract}")
            else:
                failures.append(
                    f"{tag}: implements contract revision {'.'.join(number[:2])}, "
                    f"and {contract} beside it names {'.'.join(revision[:2])}"
                )
    return passed, failures


def main() -> int:
    try:
        passed, failures = check(ROOT)
    except (BuildNotConfigured, Unreadable) as unread:
        print(f"releases check: {unread}", file=sys.stderr)
        return 1

    for line in passed:
        print(line)
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(
            f"\nreleases check: {len(failures)} release tag fault(s)", file=sys.stderr
        )
        return 1
    if not passed:
        print("releases check: no release tag names HEAD")
        return 0
    print(
        f"\nreleases check: {len(passed)} statement(s) of the release tags "
        "naming HEAD, each held to the build"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
