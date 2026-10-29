#!/usr/bin/env python3
"""Validate the findings ledger, the runs it records and the exposure set.

The ledger is `ledger/` at the repository root. Each entry is one TOML file
under `ledger/entries/`, validated against `ledger/entry.schema.json`; each
bundling run is one TOML file under `ledger/runs/`, validated against
`ledger/run.schema.json`; the exposure set is `ledger/exposure.toml`,
validated against `ledger/exposure.schema.json`. The schemas are JSON Schema
documents read through `jsonschema`, the reading the fixture manifests take,
so a parsed TOML document validates directly. They are read through one
registry, because a run record names its sources with the shapes the
exposure set declares rather than with a second spelling of them.

A run record's identity is its file's name without the extension, which is
what an entry citing the run carries, so an entry citing a run the ledger
does not hold is a failure.

The exposure set's example half names every mode entry of the worked
example: a mode file under `example/work-planner/modes/` that no declared
command names is a failure, as is a command naming an entry that does not
exist. The run records are then counted against the declared set, and the
count is reported rather than held: the set is a target the stage works
toward, so a declared source no run has bundled yet is not a failure. An
empty ledger with a valid exposure set passes.
"""

import json
import sys
import tomllib
from collections.abc import Mapping
from functools import cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent

LEDGER = ROOT / "ledger"
ENTRIES = LEDGER / "entries"
RUNS = LEDGER / "runs"
ENTRY_SCHEMA = LEDGER / "entry.schema.json"
RUN_SCHEMA = LEDGER / "run.schema.json"
EXPOSURE = LEDGER / "exposure.toml"
EXPOSURE_SCHEMA = LEDGER / "exposure.schema.json"
EXAMPLE_MODES = ROOT / "example" / "work-planner" / "modes"

SCHEMAS = (ENTRY_SCHEMA, EXPOSURE_SCHEMA, RUN_SCHEMA)


def load_schema(path: Path) -> dict[str, Any]:
    """One JSON Schema document."""
    with path.open("rb") as handle:
        document: dict[str, Any] = json.load(handle)
    return document


@cache
def schema_registry() -> Registry[bool | Mapping[str, Any]]:
    """The ledger's schemas, each addressable by its own identifier.

    A run record names its sources by reference to the shapes the exposure
    set declares, so both documents are loaded for one validation.
    """
    registry: Registry[bool | Mapping[str, Any]] = Registry()
    for path in SCHEMAS:
        document = load_schema(path)
        registry = registry.with_resource(
            document["$id"], Resource.from_contents(document)
        )
    return registry


def read(path: Path) -> dict[str, Any]:
    """One TOML document, parsed."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Every way the document departs from the schema, each naming its field."""
    validator = Draft202012Validator(schema, registry=schema_registry())
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '(root)'}: "
        f"{error.message}"
        for error in sorted(validator.iter_errors(document), key=str)
    ]


def entry_errors(entry: dict[str, Any]) -> list[str]:
    """Every way one ledger entry departs from the entry schema."""
    return schema_errors(entry, load_schema(ENTRY_SCHEMA))


def run_errors(run: dict[str, Any]) -> list[str]:
    """Every way one run record departs from the run schema."""
    return schema_errors(run, load_schema(RUN_SCHEMA))


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


def run_files(runs: Path = RUNS) -> list[Path]:
    """Every run record in the ledger, in path order."""
    return sorted(runs.glob("*.toml")) if runs.is_dir() else []


def source_keys(record: dict[str, Any]) -> set[tuple[str, ...]]:
    """The sources one record names, each reduced to a comparable key."""
    keys: set[tuple[str, ...]] = {
        ("example", item["cwd"], item["command"]) for item in record.get("example", [])
    }
    for item in record.get("workspace", []):
        keys.add(("workspace", item["repository"], item["branch"], item["path"]))
    return keys


def declared_keys(declaration: dict[str, Any]) -> set[tuple[str, ...]]:
    """The sources the exposure set declares, each reduced to the same key."""
    return source_keys(declaration)


def exposed(
    runs: list[dict[str, Any]], declaration: dict[str, Any]
) -> set[tuple[str, ...]]:
    """The declared sources some run names, so exposure is read off the records.

    A run naming a source the set does not declare contributes no key: the
    set is what the stage is measured against, and bundling a source outside
    it says nothing about the sources inside it.
    """
    named: set[tuple[str, ...]] = set()
    for run in runs:
        named.update(source_keys(run))
    return named & declared_keys(declaration)


def check(
    entries: Path = ENTRIES,
    runs: Path = RUNS,
    exposure: Path = EXPOSURE,
    modes: Path = EXAMPLE_MODES,
    root: Path = ROOT,
) -> list[str]:
    """Every failure the ledger, its runs and its exposure set carry."""
    failures = [
        f"{exposure.name}: {error}"
        for error in exposure_errors(read(exposure), modes, root)
    ]
    identities: set[str] = set()
    for path in run_files(runs):
        try:
            record = read(path)
        except tomllib.TOMLDecodeError as error:
            failures.append(f"runs/{path.name}: not TOML: {error}")
            continue
        errors = run_errors(record)
        if not errors:
            identities.add(path.stem)
        failures.extend(f"runs/{path.name}: {error}" for error in errors)
    for path in entry_files(entries):
        try:
            entry = read(path)
        except tomllib.TOMLDecodeError as error:
            failures.append(f"{path.name}: not TOML: {error}")
            continue
        failures.extend(f"{path.name}: {error}" for error in entry_errors(entry))
        cited = entry.get("run")
        if isinstance(cited, str) and cited not in identities:
            failures.append(
                f"{path.name}: cites run {cited!r}, which ledger/runs/ does not hold"
            )
    return failures


def main() -> int:
    failures = check()
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\nledger check: {len(failures)} failure(s)", file=sys.stderr)
        return 1
    declared = declared_keys(read(EXPOSURE))
    reached = exposed([read(path) for path in run_files()], read(EXPOSURE))
    print(
        f"ledger check: {len(entry_files())} entry file(s), "
        f"{len(run_files())} run record(s) and the exposure set match their schemas"
    )
    print(f"exposure: {len(reached)} of {len(declared)} declared source(s) bundled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
