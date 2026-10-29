"""Assert `make check` names the authoring check ahead of the corpus.

A rule break in a file a usage-example fixture reaches alters that fixture's
bundle, so a corpus run over the broken tree fails on the bytes that moved and
names the bundle rather than the file and the rule. The authoring check reads
the example alone and needs no build, so its position ahead of the corpus is
what makes the rule the verdict a broken tree meets first. The repository's
own `Makefile` is held to that order here, and the reading is held to a
Makefile written for this test.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MAKEFILE = ROOT / "Makefile"

CHECK = re.compile(r"^check\s*:[ \t]*([^\n#]*)$", re.MULTILINE)


def prerequisites(text: str) -> list[str]:
    """The targets `check` names, in the order it names them."""
    found = CHECK.search(text)
    assert found is not None, "the Makefile declares no check target"
    return found.group(1).split()


def test_the_makefile_names_authoring_ahead_of_corpus() -> None:
    order = prerequisites(MAKEFILE.read_text())
    assert "authoring" in order, "check names no authoring target"
    assert "corpus" in order, "check names no corpus target"
    assert order.index("authoring") < order.index("corpus"), (
        "check names corpus ahead of authoring, so a rule break in a "
        "fixture-reached file is reported as a bundle byte difference"
    )


def test_the_reading_keeps_the_order_the_rule_names_are_written_in() -> None:
    text = "check: lint authoring corpus test\n\ncorpus:\n\tpython3 checks/corpus.py\n"
    assert prerequisites(text) == ["lint", "authoring", "corpus", "test"]
    reversed_text = "check: lint corpus authoring\n"
    order = prerequisites(reversed_text)
    assert order.index("corpus") < order.index("authoring")
