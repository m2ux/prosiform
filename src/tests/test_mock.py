"""Assert the substitution mapping redirects a reference where resolution happens.

Each case names one thing the mapping decides: which key a reference
matches, where the mapping is read relative to the source root, and that
a run given no mapping resolves what it resolved before. The order the
lookup cases are written in is what they are about — a key carrying a
fragment beats a key naming its document, and a document key covers
every fragment of it — because a lookup that answered the second first
would redirect a section to the wrong whole document.

The root exemption is the reason the parameter exists, so it is asked
from both directions: a substitute outside the writing source's root is
reached when the mapping names it, and the reference is still held to
the root when nothing does.
"""

import io
import json
import os
from pathlib import Path

import pytest

from prosiform.cli import main
from prosiform.closure import (
    UNSUBSTITUTED,
    OutsideRoot,
    Reference,
    Substitution,
    bundled,
    covers,
    identity,
    inside,
    withholding_target,
)
from prosiform.profile import is_markdown

SUBSTITUTE = Reference("stand-in.md", "stand-in.md", walk="stand-in.md")
SECTION = Reference("stand-in.md#one", "stand-in.md", "one", walk="stand-in.md")
WHOLE = Substitution({("rules.md", None): SUBSTITUTE})
FRAGMENTED = Substitution(
    {("rules.md", None): SUBSTITUTE, ("rules.md", "escalation"): SECTION}
)


def test_no_mapping_leaves_a_reference_naming_what_it_named() -> None:
    assert identity(inside("guide.md", "rules.md", "", UNSUBSTITUTED)) == "rules.md"


def test_a_document_key_names_the_substitute() -> None:
    assert identity(inside("guide.md", "rules.md", "", WHOLE)) == "stand-in.md"


def test_a_document_key_covers_every_fragment_of_its_document() -> None:
    found = inside("guide.md", "rules.md#escalation", "", WHOLE)
    assert (found.path, found.fragment) == ("stand-in.md", "escalation")


def test_a_fragment_key_takes_the_section_it_names() -> None:
    found = inside("guide.md", "rules.md#escalation", "", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", "one")


def test_a_fragment_key_leaves_another_section_of_the_document_alone() -> None:
    found = inside("guide.md", "rules.md#other", "", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", "other")


def test_a_whole_document_reference_takes_the_document_key() -> None:
    found = inside("guide.md", "rules.md", "", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", None)


def test_a_key_is_the_identity_a_reference_normalized_to() -> None:
    """Two spellings of one path name one key, so one mapping serves both."""
    mapped = Substitution({("docs/rules.md", None): Reference("s.md", "s.md")})
    assert inside("guide.md", "./docs/rules.md", "", mapped).path == "s.md"
    assert inside("docs/guide.md", "rules.md", "", mapped).path == "s.md"


def test_the_substitute_is_the_target_whole_and_the_text_stays_authored() -> None:
    found = inside("guide.md", "./rules.md", "", WHOLE)
    assert found.original == "./rules.md"
    assert (found.path, found.walk) == ("stand-in.md", "stand-in.md")
    assert is_markdown(found.path)


def test_a_substitute_outside_the_writing_source_root_is_reached() -> None:
    """The exemption is the case the parameter exists for."""
    mapped = Substitution({("docs/rules.md", None): Reference("../s.md", "../s.md")})
    assert inside("docs/guide.md", "rules.md", "docs", mapped).path == "../s.md"


def test_a_citation_outside_the_root_is_redirected_by_a_key() -> None:
    """A reference the root refuses can name a stand-in.

    Which is the case the parameter exists for: a substitute kept beside
    the tree under test is reached from a source whose root excludes it.
    """
    mapped = Substitution(
        {("notes.md", None): Reference("../stand-in.md", "../stand-in.md")}
    )
    found = inside("docs/guide.md", "../notes.md", "docs", mapped)
    assert found.path == "../stand-in.md"
    assert is_markdown(found.path)


def test_an_unmapped_citation_outside_the_root_is_still_refused() -> None:
    """The mapping names what an identity becomes; it never widens the root."""
    with pytest.raises(OutsideRoot):
        inside("docs/guide.md", "../notes.md", "docs")
    with pytest.raises(OutsideRoot):
        inside("docs/guide.md", "../notes.md", "docs", WHOLE)


def test_the_mapping_is_consulted_on_the_authored_identity_not_the_substitute() -> None:
    """A key is the identity the reference normalized to.

    The substitute is exempt from the writing source's root, so holding
    the substitute's path to `covers` — or refusing the authored path
    before asking the mapping — would refuse the case the parameter
    exists for.
    """
    mapped = Substitution(
        {("notes.md", None): Reference("../stand-in.md", "../stand-in.md")}
    )
    citation = inside("docs/guide.md", "../notes.md", "docs", mapped)
    assert not covers("docs", citation.path)
    assert citation.path == "../stand-in.md"


def test_only_the_authored_identity_is_matched_not_the_substitute_path() -> None:
    """A substitute that is also a key is read from disk rather than followed again."""
    mapped = Substitution(
        {
            ("notes.md", None): Reference("../stand-in.md", "../stand-in.md"),
            ("../stand-in.md", None): Reference("../other.md", "../other.md"),
        }
    )
    assert (
        inside("docs/guide.md", "../notes.md", "docs", mapped).path == "../stand-in.md"
    )


def test_an_external_reference_is_not_redirected() -> None:
    found = inside("guide.md", "https://example.test/rules.md", "", WHOLE)
    assert (found.external, found.path) == (True, "")


def test_the_two_halves_of_one_resolution_take_the_same_mapping() -> None:
    """`bundled` and `withholding_target` read one answer, so both agree."""
    assert bundled("guide.md", "rules.md", "the rules", "", WHOLE) is not None
    assert bundled("guide.md", "rules.md", "\u00ac the rules", "", WHOLE) is None
    assert withholding_target("guide.md", "rules.md", "\u00ac the rules", "", WHOLE)


def test_a_mapping_is_a_value_the_run_cannot_rewrite() -> None:
    with pytest.raises(TypeError):
        WHOLE.keys[("other.md", None)] = SUBSTITUTE  # type: ignore[index]


def invoke(cwd: Path, *arguments: str) -> tuple[int, str]:
    """One invocation from a directory, its status and the entry bundle it wrote."""
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(cwd)
        status = main([*arguments, "-o", str(cwd / "out")], out, err)
    finally:
        os.chdir(previous)
    folder = cwd / "out" / f"{Path(arguments[-1]).stem}.bundles"
    bundle = folder / f"{folder.name.removesuffix('.bundles')}.bundle.md"
    return status, bundle.read_text() if bundle.is_file() else ""


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A guide linking a document that holds a section, beside a stand-in."""
    (tmp_path / "out").mkdir()
    (tmp_path / "guide.md").write_text("# Guide\n\nSee [the rules](rules.md).\n")
    (tmp_path / "rules.md").write_text("# Rules\n\n## Escalation\n\nAsk.\n")
    (tmp_path / "stand-in.md").write_text("# Stand-in\n\nA stand-in.\n")
    return tmp_path


def test_a_run_given_no_mapping_publishes_the_document_the_link_names(
    tree: Path,
) -> None:
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Rules" in published
    assert "# Stand-in" not in published


def test_a_run_given_a_mapping_publishes_the_substitute(tree: Path) -> None:
    status, published = invoke(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 0
    assert "# Stand-in" in published
    assert "# Rules" not in published


def test_the_option_is_reached_by_its_long_form(tree: Path) -> None:
    status, published = invoke(tree, "--mock", "rules.md=stand-in.md", "guide.md")
    assert (status, "# Stand-in" in published) == (0, True)


def test_a_mapped_entry_derives_its_name_from_the_substitute(tree: Path) -> None:
    """The redirect is total, so the document the run opens is the one it names."""
    status, _published = invoke(tree, "-m", "guide.md=stand-in.md", "guide.md")
    assert status == 0
    assert (tree / "out" / "stand-in.bundles" / "stand-in.bundle.md").is_file()


def test_a_value_that_is_no_pair_is_invalid_usage(tree: Path) -> None:
    assert invoke(tree, "-m", "rules.md", "guide.md")[0] == 2


@pytest.mark.parametrize("value", ["=stand-in.md", "rules.md="])
def test_a_pair_carrying_no_side_is_invalid_usage(tree: Path, value: str) -> None:
    assert invoke(tree, "-m", value, "guide.md")[0] == 2


def test_a_mapping_before_d_does_not_hide_the_diagnostic_format(tree: Path) -> None:
    """The format is read before the grammar, so a value-taking option is walked."""
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(tree)
        status = main(
            [
                "-m",
                "rules.md=stand-in.md",
                "-d",
                "json",
                "-o",
                str(tree / "out"),
                "absent.md",
            ],
            out,
            err,
        )
    finally:
        os.chdir(previous)
    assert status == 1
    assert json.loads(err.getvalue())["code"] == "E_TARGET_NOT_FOUND"


def test_a_title_carrying_a_withheld_link_is_headed_by_the_text_it_emits(
    tree: Path,
) -> None:
    """A heading compared for coincidence is the text the emission publishes.

    The title's link names a document the tree lacks, so it is the mapping
    that makes its target exist and the mark that is dropped. A second
    document titled plainly reads the same once the mark is gone, which is
    what the run warns about.
    """
    (tree / "guide.md").write_text("# [\u00ac the rules](missing.md)\n\nSee.\n")
    (tree / "sibling.md").write_text("# the rules\n\nAlso.\n")
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(tree)
        status = main(
            [
                "-m",
                "missing.md=stand-in.md",
                "-d",
                "json",
                "guide.md",
                "sibling.md",
            ],
            out,
            err,
        )
    finally:
        os.chdir(previous)
    assert status == 0
    voices = [json.loads(line) for line in err.getvalue().splitlines() if line]
    assert [one["code"] for one in voices] == ["W_COINCIDENT_HEADING"]
    assert "read 'the rules'" in voices[0]["message"]
