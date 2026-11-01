"""Assert `make check` names every guard that reads the example ahead of every
target that bundles it.

Two kinds of target read the example tree. A guard reads it directly and needs
no build: `make steps` reads every procedure's step headings, and
`make authoring` reads the authoring rules by file and line. A bundling target
runs the build over it: `make test` copies the example and compiles each of its
modes, and `make corpus` does so through the usage-example fixtures.

A rule break in a document the guards read alters the bundle a bundling target
compares, so a bundling target running first reports the bytes that moved, or
the target-not-found code the moved link produces, where the guard names the
file and the rule. The repository's own `Makefile` is held to that order here,
and the reading is held to a Makefile written for this test.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MAKEFILE = ROOT / "Makefile"

CHECK = re.compile(r"^check\s*:[ \t]*([^\n#]*)$", re.MULTILINE)

GUARDS = ("steps", "authoring")
BUNDLING = ("test", "corpus")

MASKED = {
    "steps": "a broken step convention is reported as the bundle bytes that moved",
    "authoring": (
        "a broken authoring rule is reported as a bundle byte difference or a "
        "target-not-found code"
    ),
}


def prerequisites(text: str) -> list[str]:
    """The targets `check` names, in the order it names them."""
    found = CHECK.search(text)
    assert found is not None, "the Makefile declares no check target"
    return found.group(1).split()


def test_the_makefile_names_every_guard_ahead_of_every_bundling_target() -> None:
    order = prerequisites(MAKEFILE.read_text())
    for target in (*GUARDS, *BUNDLING):
        assert target in order, f"check names no {target} target"
    for guard in GUARDS:
        for target in BUNDLING:
            assert order.index(guard) < order.index(target), (
                f"check names {target} ahead of {guard}, so {MASKED[guard]}"
            )


def test_the_reading_keeps_the_order_the_rule_names_are_written_in() -> None:
    text = (
        "check: lint steps authoring test corpus\n"
        "\n"
        "corpus:\n"
        "\tpython3 checks/corpus.py\n"
    )
    assert prerequisites(text) == ["lint", "steps", "authoring", "test", "corpus"]
    reversed_text = "check: lint corpus test authoring steps\n"
    order = prerequisites(reversed_text)
    assert order.index("corpus") < order.index("steps")
    assert order.index("test") < order.index("authoring")
