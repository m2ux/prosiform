#!/usr/bin/env python3
"""Assert the documented invocation is the invocation the command offers.

A caller reads the repository's documentation and writes a command line
from it. Documentation and command are written in two places, so each is
compared with the other in both directions: an option the command offers
and no table names is one a caller never learns of, and a table row the
command does not offer is a command line that fails for whoever follows
it.

The command's own help output is the comparison's one side, read from
the build under test rather than from this repository's source. The
build is named by configuration — `PROSIFORM_BUILD` holds its command
line, as it does for the corpus — so nothing here imports a package,
names a module or names a language, and the documentation binds every
implementation of the contract rather than the first one.

Four things are compared:

- **Every argument.** A table whose header carries a cell `Option`
  enumerates them. Each row's `Option` cell is one argument as the help
  writes its invocation, and the `Effect` cell beside it is that
  argument's own help text, reproduced word for word. A default is part
  of that text, so a default that moves is a row that no longer matches.
- **Every exit status.** A table whose header carries a cell `Exit`
  enumerates them, each row's `Meaning` reproducing the status's own
  line from the help output.
- **The profile identifier.** The command reports it beside its version,
  and the documented invocation names it.
- **The statements the contract requires of the documented invocation.**
  That a failed run stops the work, that reading the sources instead is
  unsupported, and which platforms the build supports. These are prose
  rather than a surface the command exposes, so each is held to the
  sentence that states it; the check keeps the statement from being
  dropped, and the review that lands it is what holds it true.

Tables are located by their headers and required statements are checked
throughout the invocation guide.

Whitespace is the one difference a comparison forgives: the help output
wraps its descriptions to a terminal width and a table cell is one line,
so runs of whitespace collapse to a single space on both sides.
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass

from documents import ROOT, plain, rows
from runner import BUILD, BuildNotConfigured, build_under_test

INVOCATION = ROOT / "invocation.md"
WIDTH = "80"

HELP = "-h"
VERSION = "-v"

OPTION = "Option"
EFFECT = "Effect"
EXIT = "Exit"
MEANING = "Meaning"

ARGUMENTS = ("positional arguments", "options")
STATUSES = "exit statuses"

HEADING = re.compile(r"^(\S[^:]*):\s*$")
ENTRY = re.compile(r"^ {2}(\S.*?)\s*$")
CONTINUATION = re.compile(r"^ {4,}(\S.*?)\s*$")
COLUMN = re.compile(r"\s{2,}")
STATUS = re.compile(r"^ {2}([0-9]+)\s{2,}(\S.*?)\s*$")
PROFILE = re.compile(r"\(([^()\s]+)\)\s*$")

STATEMENTS = (
    ("a failed run stops the work", "A failed run publishes nothing"),
    (
        "reading the sources instead is unsupported",
        "reading the sources itself is unsupported",
    ),
    ("which platforms are supported", "The supported environment is POSIX"),
    (
        "the support rests on no-follow access",
        "rests on rooted, no-follow source access",
    ),
)


class Unreadable(Exception):
    """Something the comparison needs that the run could not read."""


@dataclass(frozen=True)
class Argument:
    """One argument of the command: its invocation and its own help text."""

    invocation: str
    effect: str


def flat(text: str) -> str:
    """One line of text, its runs of whitespace collapsed to single spaces."""
    return " ".join(text.split())


def reported(*arguments: str) -> str:
    """What the build under test writes to standard output for one invocation."""
    command = build_under_test() + list(arguments)
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
        env={**os.environ, "COLUMNS": WIDTH},
    )
    if result.returncode != 0:
        raise Unreadable(
            f"{' '.join(command)} exited {result.returncode}\n{result.stderr.strip()}"
        )
    return result.stdout


def documented_arguments(text: str) -> list[Argument]:
    """Every argument the command's help output describes, in the order listed."""
    found: list[Argument] = []
    section = ""
    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading is not None:
            section = heading.group(1)
            continue
        if section not in ARGUMENTS:
            continue
        trailing = CONTINUATION.match(line)
        if trailing is not None and found:
            last = found[-1]
            found[-1] = Argument(
                last.invocation, flat(f"{last.effect} {trailing.group(1)}")
            )
            continue
        entry = ENTRY.match(line)
        if entry is None:
            continue
        columns = COLUMN.split(entry.group(1), maxsplit=1)
        invocation = columns[0]
        effect = columns[1] if len(columns) > 1 else ""
        found.append(Argument(flat(invocation), flat(effect)))
    return found


def documented_statuses(text: str) -> list[tuple[str, str]]:
    """Every exit status the command's help output names, with its meaning."""
    found: list[tuple[str, str]] = []
    section = ""
    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading is not None:
            section = heading.group(1)
            continue
        if section != STATUSES:
            continue
        status = STATUS.match(line)
        if status is not None:
            found.append((status.group(1), flat(status.group(2))))
    return found


def profile(version: str) -> str:
    """The profile identifier the command reports beside its version."""
    found = PROFILE.search(version.strip())
    if found is None:
        raise Unreadable(
            f"the command reported {version.strip()!r} for {VERSION}, which "
            f"names no profile identifier"
        )
    return found.group(1)


def compare(
    kind: str,
    offered: dict[str, str],
    stated: list[tuple[str, str]],
) -> tuple[list[str], list[str]]:
    """One surface's documentation against what the command offers."""
    passed: list[str] = []
    failures: list[str] = []
    named: set[str] = set()
    for name, meaning in stated:
        if name not in offered:
            failures.append(
                f"invocation.md: {name} — a table names this {kind} and the command "
                f"offers no such {kind}"
            )
            continue
        named.add(name)
        if meaning != offered[name]:
            failures.append(
                f"invocation.md: {name} — the table reads {meaning!r} and the "
                f"command's help reads {offered[name]!r}"
            )
            continue
        passed.append(f"ok   {kind:<11} {name}")
    for name in offered:
        if name not in named:
            failures.append(
                f"{name} — the command offers this {kind} and no table names it"
            )
    return passed, failures


def check() -> tuple[list[str], list[str]]:
    """Every comparison the documented invocation is held to."""
    text = INVOCATION.read_text()

    usage = reported(HELP)
    arguments = documented_arguments(usage)
    if not arguments:
        raise Unreadable(f"the command's {HELP} output describes no argument")
    statuses = documented_statuses(usage)
    if not statuses:
        raise Unreadable(f"the command's {HELP} output names no exit status")

    passed, failures = compare(
        "option",
        {argument.invocation: argument.effect for argument in arguments},
        [
            (plain(record.get(OPTION, "")), plain(record.get(EFFECT, "")))
            for record in rows(text, OPTION)
        ],
    )
    status_passed, status_failures = compare(
        "status",
        dict(statuses),
        [
            (plain(record.get(EXIT, "")), plain(record.get(MEANING, "")))
            for record in rows(text, EXIT)
        ],
    )
    passed += status_passed
    failures += status_failures

    identifier = profile(reported(VERSION))
    if identifier in text:
        passed.append(f"ok   profile     {identifier}")
    else:
        failures.append(
            f"invocation.md: the command reports the profile {identifier} and the "
            "invocation guide names it nowhere"
        )

    for states, sentence in STATEMENTS:
        if sentence in text:
            passed.append(f"ok   statement   {states}")
        else:
            failures.append(
                f"invocation.md: the guide does not state {states}; it "
                f"is stated by the sentence reading {sentence!r}"
            )
    return passed, failures


def main() -> int:
    try:
        passed, failures = check()
    except BuildNotConfigured as absent:
        print(f"invocation check: {absent}", file=sys.stderr)
        return 1
    except Unreadable as unreadable:
        print(f"invocation check: {unreadable}", file=sys.stderr)
        return 1

    for line in passed:
        print(line)
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(
            f"\ninvocation check: {len(failures)} documentation fault(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"\ninvocation check: {len(passed)} statement(s) of the documented "
        f"invocation, each held to the build {BUILD} names"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
