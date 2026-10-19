"""Assert the catalogue is the set of error codes the design declares.

The schema's catalogue is derived from the contract, not authored beside
it, so the check is the contract's own text: every `E_`-prefixed code the
design carries, taken from the branch and path the README's Design link
names, as the vocabulary check locates the same document. A code the
design adds fails this test until the catalogue carries it, and a code in
the catalogue the design does not name fails it too.
"""

import re

from manifests import catalogue
from vocabulary import design_reference, git_ref, git_show

ERROR_CODE = re.compile(r"\bE_[A-Z][A-Z0-9_]*\b")


def design() -> str:
    branch, path = design_reference()
    return git_show(git_ref(branch), path)


def test_the_catalogue_is_the_codes_the_design_declares() -> None:
    assert catalogue() == set(ERROR_CODE.findall(design()))
