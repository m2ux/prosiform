#!/usr/bin/env python3
"""Validate the findings ledger and the exposure set it declares.

The ledger is `ledger/` at the repository root. Each entry is one TOML file
under `ledger/entries/`, validated against `ledger/entry.schema.json`; the
exposure set is `ledger/exposure.toml`, validated against
`ledger/exposure.schema.json`. Both schemas are JSON Schema documents read
through `jsonschema`, the reading the fixture manifests take, so a parsed
TOML document validates directly.

The exposure set's example half names every mode entry of the worked
example: a mode file under `example/work-planner/modes/` that no declared
command names is a failure, as is a command naming an entry that does not
exist. An empty ledger with a valid exposure set passes.
"""

import json
import sys
import tomllib
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent

LEDGER = ROOT / "ledger"
ENTRIES = LEDGER / "entries"
ENTRY_SCHEMA = LEDGER / "entry.schema.json"
EXPOSURE = LEDGER / "exposure.toml"
EXPOSURE_SCHEMA = LEDGER / "exposure.schema.json"
EXAMPLE_MODES = ROOT / "example" / "work-planner" / "modes"


def load_schema(path: Path) -> dict[str, Any]:
    """One JSON Schema document."""
    with path.open("rb") as handle:
        document: dict[str, Any] = json.load(handle)
    return document


def read(path: Path) -> dict[str, Any]:
    """One TOML document, parsed."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Every way the document departs from the schema, each naming its field."""
    validator = Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '(root)'}: "
        f"{error.message}"
        for error in sorted(validator.iter_errors(document), key=str)
    ]


def entry_errors(entry: dict[str, Any]) -> list[str]:
    """Every way one ledger entry departs from the entry schema."""
    return schema_errors(entry, load_schema(ENTRY_SCHEMA))


def exposure_errors(
    declaration: dict[str, Any], modes: Path = EXAMPLE_MODES, root: Path = ROOT
) -> list[str]:
    """Every way the exposure set departs from its schema or the example.

    The schema holds both halves present. The example half is then held to
    the mode files the worked example carries, so a mode added later is
    declared where it is added.
    """
    errors = schema_errors(declaration, load_schema(EXPOSURE_SCHEMA))
    if errors:
        return errors
    declared = set()
    for index, item in enumerate(declaration["example"]):
        entry = (root / item["cwd"] / item["command"].split(" ", 1)[1]).resolve()
        if not entry.is_file():
            errors.append(f"example.{index}: {item['command']} names no file")
        declared.add(entry)
    for mode in sorted(modes.glob("*.md")):
        if mode.resolve() not in declared:
            errors.append(
                f"example: {mode.relative_to(root).as_posix()} is a mode entry "
                "no command names"
            )
    return errors


def entry_files(entries: Path = ENTRIES) -> list[Path]:
    """Every entry file in the ledger, in path order."""
    return sorted(entries.glob("*.toml")) if entries.is_dir() else []


def check(
    entries: Path = ENTRIES,
    exposure: Path = EXPOSURE,
    modes: Path = EXAMPLE_MODES,
    root: Path = ROOT,
) -> list[str]:
    """Every failure the ledger and its exposure set carry, each naming its file."""
    failures = [
        f"{exposure.name}: {error}"
        for error in exposure_errors(read(exposure), modes, root)
    ]
    for path in entry_files(entries):
        try:
            entry = read(path)
        except tomllib.TOMLDecodeError as error:
            failures.append(f"{path.name}: not TOML: {error}")
            continue
        failures.extend(f"{path.name}: {error}" for error in entry_errors(entry))
    return failures


def main() -> int:
    failures = check()
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\nledger check: {len(failures)} failure(s)", file=sys.stderr)
        return 1
    print(
        f"ledger check: {len(entry_files())} entry file(s) and the exposure set "
        "match their schemas"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
