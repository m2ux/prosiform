"""Assert each catalogue is the set of codes the design declares for it.

The schema's catalogues are derived from the contract, not authored beside
it, so the check is the contract's own text: every code the design carries
under a prefix, taken from the branch and path the README's Design link
names, as the vocabulary check locates the same document. A diagnostic's
severity decides which catalogue its code comes from, and the design
prefixes an error code `E_` where it prefixes a warning code `W_`, so each
prefix is held to the catalogue of the severity that carries it. A code
the design adds fails this test until its catalogue carries it, and a code
in a catalogue the design does not name fails it too.
"""

import re

import pytest
from manifests import CATALOGUES, catalogue, severities
from vocabulary import design_reference, git_ref, git_show

PREFIXES = {"error": "E_", "warning": "W_"}


def design() -> str:
    branch, path = design_reference()
    return git_show(git_ref(branch), path)


def codes(prefix: str, text: str) -> set[str]:
    """Every code the text carries under one prefix."""
    return set(re.findall(rf"\b{prefix}[A-Z][A-Z0-9_]*\b", text))


@pytest.mark.parametrize(("severity", "prefix"), sorted(PREFIXES.items()))
def test_a_catalogue_is_the_codes_the_design_declares(
    severity: str, prefix: str
) -> None:
    assert catalogue(severity) == codes(prefix, design())


def test_every_severity_a_diagnostic_may_carry_has_a_catalogue() -> None:
    assert set(severities()) == set(CATALOGUES), (
        "a severity with no catalogue leaves its code closed over nothing"
    )
