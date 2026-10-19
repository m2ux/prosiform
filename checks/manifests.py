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


@cache
def schema() -> dict[str, Any]:
    """The corpus manifest schema."""
    with SCHEMA.open("rb") as handle:
        document: dict[str, Any] = json.load(handle)
    return document


def catalogue() -> set[str]:
    """The error codes a manifest may name."""
    codes: list[str] = schema()["$defs"]["errorCode"]["enum"]
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


def missing_files(fixture: Path, manifest: dict[str, Any]) -> list[str]:
    """Every path the manifest names that the fixture does not hold.

    The schema states a path's shape; whether the fixture carries what the
    path names is a fact about the directory.
    """
    missing = []
    root = manifest.get("invocation", {}).get("root")
    if isinstance(root, str) and not (fixture / root).is_dir():
        missing.append(f"invocation.root: {root} is not a directory")
    stdout = manifest.get("expected", {}).get("stdout")
    if isinstance(stdout, str) and not (fixture / stdout).is_file():
        missing.append(f"expected.stdout: {stdout} is not a file")
    return missing


def fixtures(corpus: Path = CORPUS) -> list[Path]:
    """Every fixture directory in the corpus, in path order.

    A fixture is any directory holding a manifest, so a family is a
    directory and a fixture's identity is its path under the corpus.
    """
    return sorted(path.parent for path in corpus.rglob(MANIFEST_NAME))
