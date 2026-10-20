#!/usr/bin/env python3
"""Read and validate a fixture manifest against the corpus schema.

A fixture is a directory under `fixtures/` holding `manifest.toml`, the
source tree that manifest names and the bytes it expects back. The manifest
is the whole declaration, and `fixtures/manifest.schema.json` is the shape
it must take: a JSON Schema document, so the schema is data both builds
read rather than code one of them owns.

TOML's value model is a subset of JSON's, so a parsed manifest validates
directly. Reading needs the standard library and `jsonschema`, which the
locked development group carries.
"""

import json
import tomllib
from functools import cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent

CORPUS = ROOT / "fixtures"
SCHEMA = CORPUS / "manifest.schema.json"
MANIFEST_NAME = "manifest.toml"

CATALOGUES = {"error": "errorCode", "warning": "warningCode"}

ROOT_NOT_FOUND = "E_ROOT_NOT_FOUND"


@cache
def schema() -> dict[str, Any]:
    """The corpus manifest schema."""
    with SCHEMA.open("rb") as handle:
        document: dict[str, Any] = json.load(handle)
    return document


def severities() -> list[str]:
    """The severities a diagnostic may carry, in the order the schema lists them."""
    declared: list[str] = schema()["$defs"]["diagnostic"]["properties"]["severity"][
        "enum"
    ]
    return declared


def catalogue(severity: str) -> set[str]:
    """The codes a diagnostic of one severity may name.

    A diagnostic is named by its severity and its code together, so the
    severity selects the catalogue: an error decides a failing run and a
    warning accompanies a successful one.
    """
    codes: list[str] = schema()["$defs"][CATALOGUES[severity]]["enum"]
    return set(codes)


def read(manifest_path: Path) -> dict[str, Any]:
    """One manifest, parsed."""
    with manifest_path.open("rb") as handle:
        manifest: dict[str, Any] = tomllib.load(handle)
    return manifest


def errors(manifest: dict[str, Any]) -> list[str]:
    """Every way the manifest departs from the schema, each naming its field."""
    validator = Draft202012Validator(schema())
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '(root)'}: "
        f"{error.message}"
        for error in validator.iter_errors(manifest)
    ]


def absent_root(manifest: dict[str, Any]) -> bool:
    """Whether the manifest declares a run that cannot find its allowed root.

    `E_ROOT_NOT_FOUND` is the contract's name for that outcome, so a
    manifest expecting it has declared that `invocation.root` names no
    directory. The declaration is the diagnostic itself, which is why no
    field beside the root repeats it.
    """
    declared = manifest.get("expected", {}).get("diagnostics", [])
    return any(
        isinstance(diagnostic, dict) and diagnostic.get("code") == ROOT_NOT_FOUND
        for diagnostic in declared
    )


def missing_files(fixture: Path, manifest: dict[str, Any]) -> list[str]:
    """Every path the manifest names that the fixture does not hold.

    The schema states a path's shape; whether the fixture carries what the
    path names is a fact about the directory. A fixture declaring that the
    run cannot find its allowed source root is the one that names a root
    it does not hold, and `present_files` holds it to that.
    """
    missing = []
    root = manifest.get("invocation", {}).get("root")
    if (
        isinstance(root, str)
        and not absent_root(manifest)
        and not (fixture / root).is_dir()
    ):
        missing.append(f"invocation.root: {root} is not a directory")
    stdout = manifest.get("expected", {}).get("stdout")
    if isinstance(stdout, str) and not (fixture / stdout).is_file():
        missing.append(f"expected.stdout: {stdout} is not a file")
    return missing


def present_files(fixture: Path, manifest: dict[str, Any]) -> list[str]:
    """Every path the manifest declares absent that the fixture already holds.

    A declaration the directory contradicts before the run says nothing
    about the run, so it is a defect in the fixture rather than a
    difference the run produced. A fixture declaring that the run cannot
    find its allowed source root declares that root absent, so a fixture
    holding it is refused the same way.
    """
    declared = manifest.get("expected", {}).get("absent", [])
    present = [
        f"expected.absent: {name} is a path the fixture holds"
        for name in declared
        if isinstance(name, str) and (fixture / name).exists()
    ]
    root = manifest.get("invocation", {}).get("root")
    if isinstance(root, str) and absent_root(manifest) and (fixture / root).exists():
        present.append(f"invocation.root: {root} is a path the fixture holds")
    return present


def identity(fixture: Path, corpus: Path = CORPUS) -> str:
    """A fixture's identity: its path under the corpus.

    A directory outside the corpus is identified by its absolute path, so
    a fixture written for one run still names itself.
    """
    resolved = fixture.resolve()
    try:
        return resolved.relative_to(corpus.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def fixtures(corpus: Path = CORPUS) -> list[Path]:
    """Every fixture directory in the corpus, in path order.

    A fixture is any directory holding a manifest, so a family is a
    directory and a fixture's identity is its path under the corpus.
    """
    return sorted(path.parent for path in corpus.rglob(MANIFEST_NAME))


def declared_codes(severity: str, corpus: Path = CORPUS) -> set[str]:
    """Every code the corpus's fixtures declare at one severity.

    A fixture states a diagnostic by naming its severity and its code
    together, so the codes the corpus reaches are read from the manifests
    that carry them rather than from a list held beside the corpus. A
    fixture added anywhere is counted by being a fixture.

    A fixture awaiting later work declares its diagnostics like any
    other: the expectation is the corpus's the moment the manifest
    carries it, whatever the build under test currently produces.
    """
    return {
        diagnostic["code"]
        for fixture in fixtures(corpus)
        for diagnostic in read(fixture / MANIFEST_NAME)
        .get("expected", {})
        .get("diagnostics", [])
        if diagnostic.get("severity") == severity
    }
