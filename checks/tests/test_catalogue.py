"""Assert each catalogue is the design's codes, and that fixtures state them.

The schema's catalogues are derived from the contract, not authored beside
it, so the check is the contract's own text: every code the design carries
under a prefix, taken from the branch and path the README's Design link
names, as the vocabulary check locates the same document. A diagnostic's
severity decides which catalogue its code comes from, and the design
prefixes an error code `E_` where it prefixes a warning code `W_`, so each
prefix is held to the catalogue of the severity that carries it. A code
the design adds fails this test until its catalogue carries it, and a code
in a catalogue the design does not name fails it too.

A warning accompanies a successful run, so a warning code is a statement
about what such a run writes to standard error, and the corpus is where
that statement is made. Every code the warning catalogue holds is
therefore declared by a fixture: a warning the design declares and no
manifest carries is a claim no run of the corpus exercises.
"""

import re

import pytest
from manifests import CATALOGUES, catalogue, declared_codes, severities
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


def test_every_warning_the_design_declares_is_declared_by_a_fixture() -> None:
    unstated = catalogue("warning") - declared_codes("warning")
    assert not unstated, (
        f"no fixture declares {', '.join(sorted(unstated))}, so the corpus "
        "states nothing about the run that warning accompanies"
    )


def test_every_severity_a_diagnostic_may_carry_has_a_catalogue() -> None:
    assert set(severities()) == set(CATALOGUES), (
        "a severity with no catalogue leaves its code closed over nothing"
    )
