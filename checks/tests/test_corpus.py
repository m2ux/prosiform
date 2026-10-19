"""Assert every fixture the corpus holds is a fixture the schema describes.

A fixture is a directory holding a manifest. Each one is validated against
`fixtures/manifest.schema.json`, and each path its manifest names is
required to exist, so a malformed fixture fails as a fixture rather than
as a bundling.
"""

from pathlib import Path

import pytest
from manifests import (
    CORPUS,
    MANIFEST_NAME,
    errors,
    fixtures,
    identity,
    missing_files,
    read,
)

FIXTURES = fixtures()


def test_the_corpus_holds_a_fixture() -> None:
    assert FIXTURES, f"no directory under {CORPUS} holds a {MANIFEST_NAME}"


@pytest.mark.parametrize("fixture", FIXTURES, ids=identity)
def test_a_fixture_manifest_matches_the_schema(fixture: Path) -> None:
    manifest = read(fixture / MANIFEST_NAME)
    assert errors(manifest) == []
    assert missing_files(fixture, manifest) == []
