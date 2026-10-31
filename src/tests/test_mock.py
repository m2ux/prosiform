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

The three shapes the mapping refuses are decided from one set of
identities, so each case is asked through the command line that carries
it: which pair of spellings a duplicate names, that a self-mock names the
entry its author wrote, and that a key carrying no document reaches the
usage failure rather than a document the option never named.
"""

import io
import json
import os
from pathlib import Path
from typing import Any

import pytest

from prosiform.cli import MOCK_UNUSED, main
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


def test_a_section_key_serves_no_other_section_of_its_document() -> None:
    """A key carrying a section redirects that section and nothing beside it."""
    mapped = Substitution({("rules.md", "escalation"): SECTION})
    found = inside("guide.md", "rules.md#other", "", mapped)
    assert identity(found) == "rules.md#other"
    assert mapped.unserved() == ("rules.md#escalation",)


def test_a_section_keys_substitute_section_is_the_one_the_run_reads() -> None:
    """The redirect replaces the reference, so the substitute's section is the whole."""
    advised = Reference("stand-in.md#advised", "stand-in.md", "advised")
    mapped = Substitution({("rules.md", "escalation"): advised})
    found = inside("guide.md", "rules.md#escalation", "", mapped)
    assert (found.path, found.fragment) == ("stand-in.md", "advised")


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


def test_one_key_serving_two_references_records_one_substitution() -> None:
    """A key names a target, so the two references it serves are one substitution."""
    mapped = Substitution({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", "", mapped, "guide.md:3")
    inside("guide.md", "rules.md#escalation", "", mapped, "guide.md:5")
    assert [one.resolved for one in mapped.redirects.targets()] == ["stand-in.md"]


def test_a_substitution_names_the_first_link_that_redirected_it() -> None:
    """The record keeps the position the run first met the substitution at."""
    mapped = Substitution({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", "", mapped, "guide.md:3")
    inside("guide.md", "rules.md", "", mapped, "guide.md:9")
    assert [one.origin for one in mapped.redirects.targets()] == ["guide.md:3"]


def test_a_stage_that_resolves_a_link_again_records_no_second_substitution() -> None:
    """Emission and candidate validation re-resolve a link and add nothing."""
    mapped = Substitution({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", "", mapped, "guide.md:3")
    bundled("guide.md", "rules.md", "the rules", "", mapped)
    assert len(mapped.redirects.targets()) == 1


def test_an_empty_mapping_records_neither_a_substitution_nor_an_unused_key() -> None:
    """Neither has a subject, so a run given no mapping states nothing."""
    assert UNSUBSTITUTED.redirects.targets() == ()
    assert UNSUBSTITUTED.unserved() == ()


def test_a_key_no_reference_named_is_unserved_and_keeps_its_authored_spelling() -> None:
    """The key states a fact about the invocation, in the caller's own spelling."""
    mapped = Substitution(
        {("docs/rules.md", None): SUBSTITUTE},
        {("docs/rules.md", None): "./docs/rules.md"},
    )
    inside("guide.md", "notes.md", "", mapped)
    assert mapped.unserved() == ("./docs/rules.md",)


def test_a_served_key_is_not_unserved() -> None:
    mapped = Substitution({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", "", mapped)
    assert mapped.unserved() == ()


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


def refused(cwd: Path, *arguments: str) -> tuple[int, list[dict[str, Any]]]:
    """One invocation from a directory, its status and the diagnostics it emitted."""
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(cwd)
        status = main(["-d", "json", *arguments], out, err)
    finally:
        os.chdir(previous)
    return status, [json.loads(line) for line in err.getvalue().splitlines() if line]


def test_two_spellings_of_one_key_are_refused_naming_both(tree: Path) -> None:
    """The message names the two options to edit, not the identity they share."""
    status, voices = refused(
        tree, "-m", "rules.md=stand-in.md", "-m", "./rules.md=guide.md", "guide.md"
    )
    assert status == 2
    assert [one["code"] for one in voices] == ["E_INVALID_USAGE"]
    assert "rules.md" in voices[0]["message"]
    assert "./rules.md" in voices[0]["message"]


def test_a_self_mock_is_refused(tree: Path) -> None:
    """A substitute naming its own key states no redirect at all."""
    status, voices = refused(tree, "-m", "rules.md=./rules.md", "guide.md")
    assert status == 2
    assert [one["code"] for one in voices] == ["E_INVALID_USAGE"]
    assert "one identity" in voices[0]["message"]


def test_a_key_carrying_no_document_is_refused(tree: Path) -> None:
    """A section alone names no document, so it is not resolved against one."""
    status, voices = refused(tree, "-m", "#escalation=stand-in.md", "guide.md")
    assert status == 2
    assert [one["code"] for one in voices] == ["E_INVALID_USAGE"]
    assert "#escalation" in voices[0]["message"]


def test_a_document_key_and_a_section_key_of_it_are_two_keys(tree: Path) -> None:
    """The identity a key names is its document and its section together."""
    status, published = invoke(
        tree,
        "-m",
        "rules.md=stand-in.md",
        "-m",
        "rules.md#escalation=guide.md",
        "guide.md",
    )
    assert status == 0
    assert "# Stand-in" in published


def test_a_mapping_shape_is_refused_before_any_source_is_read(tree: Path) -> None:
    """The refusals are decided from the mapping, so no absent entry masks one."""
    status, voices = refused(
        tree,
        "-m",
        "rules.md=stand-in.md",
        "-m",
        "./rules.md=guide.md",
        "absent.md",
    )
    assert status == 2
    assert [one["code"] for one in voices] == ["E_INVALID_USAGE"]


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
    assert [one["code"] for one in voices] == [
        "W_COINCIDENT_HEADING",
        "W_MOCK_SUBSTITUTED",
    ]
    assert "read 'the rules'" in voices[0]["message"]


def voices(cwd: Path, *arguments: str) -> tuple[int, list[dict[str, Any]]]:
    """One invocation from a directory, its status and its JSON diagnostics."""
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(cwd)
        status = main([*arguments, "-d", "json"], out, err)
    finally:
        os.chdir(previous)
    return status, [json.loads(line) for line in err.getvalue().splitlines() if line]


def test_a_substitution_warning_names_the_link_its_destination_and_the_substitute(
    tree: Path,
) -> None:
    """The three fields that tell one substitution from another."""
    status, said = voices(
        tree, "-m", "rules.md=stand-in.md", "-o", str(tree / "out"), "guide.md"
    )
    assert status == 0
    assert [one["code"] for one in said] == ["W_MOCK_SUBSTITUTED"]
    voice = said[0]
    assert voice["source"] == "rules.md"
    assert voice["resolved"] == "stand-in.md"
    assert voice["location"] == {"file": "guide.md", "line": 3, "column": 1}


def test_a_substitution_warning_states_the_identity_the_reference_would_have_named(
    tree: Path,
) -> None:
    """Two keys naming one stand-in are told apart only by what each replaces."""
    (tree / "sibling.md").write_text("# Sibling\n\nSee [other rules](other.md).\n")
    (tree / "other.md").write_text("# Other\n\nOther.\n")
    status, said = voices(
        tree,
        "-m",
        "rules.md=stand-in.md",
        "-m",
        "other.md=stand-in.md",
        "-o",
        str(tree / "out"),
        "guide.md",
        "sibling.md",
    )
    assert status == 0
    assert [one["code"] for one in said] == [
        "W_MOCK_SUBSTITUTED",
        "W_MOCK_SUBSTITUTED",
    ]
    assert ["'rules.md'" in said[0]["message"], "'other.md'" in said[1]["message"]] == [
        True,
        True,
    ]


def test_an_unused_key_warns_with_no_location_and_publishes(tree: Path) -> None:
    """A key that matched nothing states a fact about the invocation."""
    status, published = invoke(tree, "-m", "unrelated.md=stand-in.md", "guide.md")
    assert status == 0
    assert "# Rules" in published
    status, said = voices(
        tree, "-m", "unrelated.md=stand-in.md", "-o", str(tree / "out"), "guide.md"
    )
    assert status == 0
    assert [one["code"] for one in said] == ["W_MOCK_UNUSED"]
    assert said[0]["source"] == "unrelated.md"
    assert "location" not in said[0]


def test_a_served_key_warns_unused_for_nothing(tree: Path) -> None:
    """The complement of AC8: a mapping that matched states no unused key."""
    _status, said = voices(
        tree, "-m", "rules.md=stand-in.md", "-o", str(tree / "out"), "guide.md"
    )
    assert MOCK_UNUSED not in [one["code"] for one in said]


def test_a_check_run_reports_the_substitution_and_publishes_nothing(
    tree: Path,
) -> None:
    """The mapping applies under `-c`, which is how a mocked check runs in CI."""
    status, said = voices(
        tree, "-c", "-m", "rules.md=stand-in.md", "-o", str(tree / "out"), "guide.md"
    )
    assert status == 0
    assert [one["code"] for one in said] == ["W_MOCK_SUBSTITUTED"]
    assert said[0]["resolved"] == "stand-in.md"
    assert not (tree / "out" / "guide.bundles").exists()


def test_a_run_given_no_mapping_states_neither_warning(tree: Path) -> None:
    """An empty mapping raises neither, because neither has a subject."""
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert said == []


def test_a_section_key_leaves_the_rest_of_its_document_real(tree: Path) -> None:
    """One branch is redirected and the rest of its document compiles as it ships."""
    (tree / "guide.md").write_text(
        "# Guide\n\nRequire [the rules](rules.md) whole.\n\n"
        "Read [the escalation](rules.md#escalation) with it.\n"
    )
    (tree / "stand-in.md").write_text(
        "# Stand-in\n\n## Escalation\n\nAsk the stand-in.\n"
    )
    status, published = invoke(
        tree, "-m", "rules.md#escalation=stand-in.md", "guide.md"
    )
    assert status == 0
    assert "# Rules" in published
    assert "Ask the stand-in." in published
    assert "Ask.\n" in published


def test_a_document_key_and_a_section_key_of_it_both_serve_their_references(
    tree: Path,
) -> None:
    """The narrower key takes the section, and the wider one takes the document."""
    (tree / "guide.md").write_text(
        "# Guide\n\nRequire [the rules](rules.md) whole.\n\n"
        "Read [the escalation](rules.md#escalation) with it.\n"
    )
    (tree / "rules-copy.md").write_text("# Rules Copy\n\n## Escalation\n\nCopy.\n")
    (tree / "escalation-copy.md").write_text(
        "# Escalation Copy\n\n## Escalation\n\nEscalated.\n"
    )
    status, published = invoke(
        tree,
        "-m",
        "rules.md=rules-copy.md",
        "-m",
        "rules.md#escalation=escalation-copy.md",
        "guide.md",
    )
    assert status == 0
    assert (tree / "out" / "guide.bundles" / "guide.bundle.md").is_file()
    for substitute in ("# Rules Copy", "# Escalation Copy"):
        assert substitute in published
    assert "# Rules\n" not in published


def test_a_substitute_that_is_also_a_key_is_read_from_disk(tree: Path) -> None:
    """The mapping is applied once, so the second key is never followed."""
    (tree / "first.md").write_text("# First\n\nFirst.\n")
    (tree / "second.md").write_text("# Second\n\nSecond.\n")
    (tree / "third.md").write_text("# Third\n\nThird.\n")
    (tree / "guide.md").write_text("# Guide\n\nRequire [the first](first.md) whole.\n")
    status, said = voices(
        tree,
        "-m",
        "first.md=second.md",
        "-m",
        "second.md=third.md",
        "-o",
        str(tree / "out"),
        "guide.md",
    )
    assert status == 0
    assert [one["code"] for one in said] == ["W_MOCK_SUBSTITUTED", "W_MOCK_UNUSED"]
    assert said[0]["resolved"] == "second.md"
    assert said[1]["source"] == "second.md"
    _status, published = invoke(
        tree, "-m", "first.md=second.md", "-m", "second.md=third.md", "guide.md"
    )
    assert "# Second" in published
    assert "# Third" not in published


def grouped(cwd: Path, *arguments: str) -> tuple[int, str, list[dict[str, Any]]]:
    """One invocation from a directory, its status, entry bundle and diagnostics."""
    status, said = voices(cwd, *arguments, "-o", str(cwd / "out"))
    folder = cwd / "out" / f"{Path(arguments[-1]).stem}.bundles"
    bundle = folder / f"{folder.name.removesuffix('.bundles')}.bundle.md"
    return status, bundle.read_text() if bundle.is_file() else "", said


def group_tree(tmp_path: Path) -> Path:
    """A group of two documents, one link into it, and a substitute of its own."""
    (tmp_path / "out").mkdir()
    members = {
        "guide.md": (
            "---\nprosiform:\n  group: rules\n  group-depth: 2\n---\n"
            "The guide preamble, linking [the notes](notes.md) and "
            "[the rules](rules.md).\n\n## Scope\n\nThe guide's scope.\n"
        ),
        "notes.md": (
            "---\nprosiform:\n  group: rules\n  group-depth: 2\n---\n"
            "The notes preamble.\n\n## Scope\n\nThe notes' scope.\n"
        ),
        "rules.md": "# Rules\n\nEvery rule the tree under test holds.\n",
        "stand-in.md": (
            "---\nprosiform:\n  group: rules\n  group-depth: 2\n---\n"
            "The stand-in preamble.\n\n## Scope\n\nThe stand-in's scope.\n"
        ),
    }
    for name, text in members.items():
        (tmp_path / name).write_text(text)
    return tmp_path


def test_a_substitute_declaring_a_group_joins_it_under_its_own_member_heading(
    tmp_path: Path,
) -> None:
    """The substitute's group and depth decide its membership, not its key's."""
    tree = group_tree(tmp_path)
    status, published, _said = grouped(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 0
    assert published.startswith("# Rules\n")
    assert "### Stand In" in published
    assert published.count("The stand-in preamble.") == 1
    assert "Every rule the tree under test holds." not in published


def test_a_substitute_declaring_no_group_joins_no_group(tmp_path: Path) -> None:
    """No setting travels from the document the key named."""
    tree = group_tree(tmp_path)
    (tree / "plain.md").write_text("# Plain\n\nA plain stand-in.\n")
    status, published, _said = grouped(tree, "-m", "rules.md=plain.md", "guide.md")
    assert status == 0
    assert "# Plain" in published
    assert "### Plain" not in published


def test_the_group_a_substitute_declares_is_the_one_the_bundle_merges(
    tmp_path: Path,
) -> None:
    """The authored target's own group declaration contributes nothing."""
    tree = group_tree(tmp_path)
    (tree / "rules.md").write_text(
        "---\nprosiform:\n  group: authored\n  group-depth: 2\n---\n"
        "# Rules\n\nEvery rule the tree under test holds.\n"
    )
    status, published, _said = grouped(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 0
    assert published.startswith("# Rules\n")
    assert "# Authored" not in published


def test_a_group_depth_conflict_names_the_substitutes_own_declaration(
    tmp_path: Path,
) -> None:
    """The declaration that disagrees is the substitute's, at its own position."""
    tree = group_tree(tmp_path)
    (tree / "stand-in.md").write_text(
        "---\nprosiform:\n  group: rules\n  group-depth: 3\n---\n"
        "# Stand-in\n\nThe stand-in preamble.\n"
    )
    status, _published, said = grouped(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 1
    assert [one["code"] for one in said] == ["E_GROUP_DEPTH_CONFLICT"]
    assert said[0]["related"][0]["file"] == "stand-in.md"


def test_a_substitutes_metadata_failure_names_the_substitute(tmp_path: Path) -> None:
    """The substitute's own declaration is the one whose field is unpaired."""
    tree = group_tree(tmp_path)
    (tree / "stand-in.md").write_text(
        "---\nprosiform:\n  group: rules\n---\n# Stand-in\n\nStand-in.\n"
    )
    status, _published, said = grouped(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 1
    assert [one["code"] for one in said] == ["E_INVALID_CONVERSION_METADATA"]
    assert said[0]["location"]["file"] == "stand-in.md"
    assert said[0]["chain"] == ["guide.md", "stand-in.md"]


def test_a_substitute_reached_by_two_routes_joins_the_group_once(
    tmp_path: Path,
) -> None:
    """One source is one capture, so one membership, however many links name it."""
    tree = group_tree(tmp_path)
    (tree / "notes.md").write_text(
        "---\nprosiform:\n  group: rules\n  group-depth: 2\n---\n"
        "The notes preamble, linking [the rules](rules.md).\n\n"
        "## Scope\n\nThe notes' scope.\n"
    )
    status, published, _said = grouped(tree, "-m", "rules.md=stand-in.md", "guide.md")
    assert status == 0
    # One overview subsection and one variant heading name the one member.
    assert published.count("### Stand In") == 2
    assert published.count("The stand-in preamble.") == 1
    assert published.count("The stand-in's scope.") == 1


def rooted(tmp_path: Path) -> Path:
    """A guide linking a rule set, and a stand-in declaring its own root."""
    (tmp_path / "out").mkdir()
    (tmp_path / "guide.md").write_text("# Guide\n\nRequire [the rules](rules.md).\n")
    (tmp_path / "rules.md").write_text("# Rules\n\nEvery rule.\n")
    (tmp_path / "above.md").write_text("# Above\n\nAbove the stand-in root.\n")
    (tmp_path / "stand-in").mkdir()
    (tmp_path / "stand-in" / "entry.md").write_text(
        "---\nprosiform:\n  root: .\n---\n"
        "# Entry\n\nBeside [a detail](detail.md) and [above](../above.md).\n"
    )
    (tmp_path / "stand-in" / "detail.md").write_text("# Detail\n\nA detail.\n")
    return tmp_path


def test_a_substitutes_root_bounds_its_own_outgoing_links(tmp_path: Path) -> None:
    """A link inside the stand-in's root compiles; one above it stays a citation."""
    tree = rooted(tmp_path)
    status, published, _said = grouped(
        tree, "-m", "rules.md=stand-in/entry.md", "guide.md"
    )
    assert status == 0
    assert "Beside [a detail](#detail)" in published
    assert "[above](../above.md)" in published
    assert "# Above" not in published


def test_the_substitutes_root_is_read_from_its_own_bytes(tmp_path: Path) -> None:
    """The authored target's root is not the boundary its substitute is held to."""
    tree = rooted(tmp_path)
    (tree / "rules.md").write_text(
        "---\nprosiform:\n  root: ..\n---\n# Rules\n\nEvery rule.\n"
    )
    status, published, _said = grouped(
        tree, "-m", "rules.md=stand-in/entry.md", "guide.md"
    )
    assert status == 0
    assert "[above](../above.md)" in published
    assert "# Above" not in published


def test_a_substitute_above_the_working_directory_reads_its_own_settings(
    tmp_path: Path,
) -> None:
    """AC20's parent segment, read through the substitute's own bytes.

    A value carrying `..` names a substitute above the invocation working
    directory, and the group it joins and the root it declares are its
    own, resolved from the directory it sits in rather than from the tree
    the run started in.
    """
    tree = tmp_path / "tree"
    above = tmp_path / "above"
    tree.mkdir()
    above.mkdir()
    (tree / "guide.md").write_text(
        "---\nprosiform:\n  group: rules\n  group-depth: 2\n---\n"
        "The guide preamble, linking [the rules](rules.md).\n\n"
        "## Scope\n\nThe guide's scope.\n"
    )
    (tree / "rules.md").write_text("# Rules\n\nEvery rule.\n")
    (above / "entry.md").write_text(
        "---\nprosiform:\n  group: rules\n  group-depth: 2\n  root: .\n---\n"
        "The stand-in preamble, linking [its detail](detail.md) and "
        "[the guide](../tree/guide.md).\n\n"
        "## Scope\n\nThe stand-in's scope.\n"
    )
    (above / "detail.md").write_text("# Detail\n\nBeside the stand-in.\n")
    (tree / "out").mkdir()
    status, said = voices(
        tree, "-m", "rules.md=../above/entry.md", "-o", str(tree / "out"), "guide.md"
    )
    assert status == 0
    assert [one["code"] for one in said] == ["W_MOCK_SUBSTITUTED"]
    folder = tree / "out" / "guide.bundles"
    published = (folder / "guide.bundle.md").read_text()
    assert published.startswith("# Rules\n")
    assert "### Entry" in published
    assert "[its detail](#detail)" in published
    assert "Beside the stand-in." in published
    assert "[the guide](../tree/guide.md)" in published
