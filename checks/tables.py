#!/usr/bin/env python3
"""Assert the README tables name what the project declares and nothing else.

Two enumerations are written in one place and documented in another, so each
is compared with its source in both directions. A declared item no table names
leaves a reader unaware of it; a table row no declaration backs sends a reader
after something the project does not have.

- A table whose header carries a cell `Command` enumerates commands. Each of
  its rows names one target, written `make <target>`, and the set compared is
  every rule the `Makefile` declares. Nothing is excluded, so a target that
  does work is documented or this check fails. The names beginning with a dot
  are make's own directives rather than commands, and are not rules.
- A table whose header carries a cell `Declared` enumerates the project's
  declarations, with the version it pins in the `Value` cell beside it. The
  set compared is `requires-python`, which a table writes as `Python`, with
  `[project] dependencies` and the `dev` dependency group of
  `prototype/pyproject.toml`. A name is compared as the packaging ecosystem
  compares one, case-folded with its separators run together, and reported as
  the table writes it.

A table is located by its header and a document by git, so a table moved
within a README, and the README a new tree brings with it, are both read
without this check being edited.

A row that names a declared item under another version is one fault, not two:
the item is documented, and what it is documented as is wrong.
"""

import re
import sys
import tomllib

from documents import ROOT, readmes, tables

MAKEFILE = ROOT / "Makefile"
PYPROJECT = ROOT / "prototype" / "pyproject.toml"
PYTHON = "Python"

RULE = re.compile(r"^([A-Za-z0-9_][A-Za-z0-9_.-]*)\s*:(?:[^=]|$)", re.MULTILINE)
MAKE_COMMAND = re.compile(r"^make\s+([A-Za-z0-9_.-]+)$")
REQUIREMENT = re.compile(r"^([A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?)\s*(.*)$")
MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def plain(cell: str) -> str:
    """A cell reduced to its text: a link to its label, a code span to its code."""
    return MARKDOWN_LINK.sub(r"\1", cell).replace("`", "").strip()


def key(name: str) -> str:
    """A package name as the packaging ecosystem compares one."""
    return re.sub(r"[-_.]+", "-", name).lower()


def targets() -> set[str]:
    """Every target the Makefile declares."""
    return {match.group(1) for match in RULE.finditer(MAKEFILE.read_text())}


def declarations() -> dict[str, str]:
    """Each declaration of the project definition, to the version it pins."""
    project = tomllib.loads(PYPROJECT.read_text())
    declared = {PYTHON: project["project"]["requires-python"]}
    requirements = list(project["project"].get("dependencies", []))
    requirements += list(project.get("dependency-groups", {}).get("dev", []))
    for requirement in requirements:
        match = REQUIREMENT.match(requirement.strip())
        if match is not None:
            declared[match.group(1)] = match.group(2).strip()
    return declared


Match = tuple[str | None, str | None]


def match_command(document: str, record: dict[str, str], declared: set[str]) -> Match:
    """The target one Command row names, or the reason it names none."""
    command = plain(record.get("Command", ""))
    found = MAKE_COMMAND.match(command)
    if found is None:
        return None, f"{document}: a Command row reads '{command}' and names no command"
    target = found.group(1)
    if target not in declared:
        return None, (
            f"{document}: make {target} — the table names it and the Makefile "
            f"declares no such target"
        )
    return target, None


def match_declaration(
    document: str, record: dict[str, str], declared: dict[str, tuple[str, str]]
) -> Match:
    """The declaration one Declared row names, or the reason it names none."""
    item = plain(record.get("Declared", ""))
    if key(item) not in declared:
        return None, (
            f"{document}: {item} — the table names it and prototype/pyproject.toml "
            f"declares no such dependency"
        )
    name, version = declared[key(item)]
    stated = plain(record.get("Value", ""))
    if stated != version:
        return key(item), (
            f"{document}: {name} — the table names '{stated}' and "
            f"prototype/pyproject.toml declares '{version}'"
        )
    return key(item), None


def main() -> int:
    declared_targets = targets()
    declared_items = {
        key(name): (name, version) for name, version in declarations().items()
    }

    failures: list[str] = []
    named_targets: set[str] = set()
    named_items: set[str] = set()

    for path in readmes():
        document = path.relative_to(ROOT).as_posix()
        for table in tables(path.read_text()):
            if "Command" in table.headers:
                for record in table.records():
                    target, failure = match_command(document, record, declared_targets)
                    if target is None:
                        failures.append(str(failure))
                        continue
                    named_targets.add(target)
                    print(f"ok   command     make {target} — {document}")
            if "Declared" not in table.headers:
                continue
            if "Value" not in table.headers:
                failures.append(f"{document}: a Declared table carries no Value column")
                continue
            for record in table.records():
                item, failure = match_declaration(document, record, declared_items)
                if item is not None:
                    named_items.add(item)
                if failure is not None:
                    failures.append(failure)
                elif item is not None:
                    print(f"ok   declared    {declared_items[item][0]} — {document}")

    for target in sorted(declared_targets - named_targets):
        failures.append(
            f"make {target} — the Makefile declares it and no command table names it"
        )
    for item in sorted(set(declared_items) - named_items):
        failures.append(
            f"{declared_items[item][0]} — prototype/pyproject.toml declares it and "
            f"no declaration table names it"
        )

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\ntable check: {len(failures)} table fault(s)", file=sys.stderr)
        return 1
    print(
        f"\ntable check: {len(declared_targets)} command(s) and "
        f"{len(declared_items)} declaration(s), each declared by the project "
        f"and named by a table"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
