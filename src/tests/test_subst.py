"""Assert a `subst` pair redirects a reference where resolution happens.

Each case names one thing a pair decides: which key a reference matches,
which document's links it reaches, and that a document stating no pair
resolves what it names. The order the lookup cases are written in is what
they are about — a key carrying a fragment beats a key naming its
document, and a document key covers every fragment of it — because a
lookup that answered the second first would redirect a section to the
wrong whole document.

The run cases state each pair in the `default` preset of the document
whose link it redirects, which is the one channel a substitution has.
"""

import io
import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from test_cli import linked, opening

from prosiform.bundle import shown_text
from prosiform.candidate import carried, intended
from prosiform.cli import SUBST_UNUSED, main
from prosiform.closure import (
    DECLARING,
    UNSUBSTITUTED,
    Reference,
    Substitution,
    bundled,
    identity,
    inside,
    withholding_target,
)
from prosiform.limits import NESTING
from prosiform.profile import is_markdown, parse
from prosiform.source import regions

DECLARED = "---\nprosiform: {}\n---\n"
BUDGET = NESTING.default

Pairs = Mapping[tuple[str, str | None], Reference]


def writing(pairs: Pairs, *documents: str) -> Substitution:
    """A run's mapping in which each document named states the pairs given."""
    return Substitution().governed(
        {document: pairs for document in documents or ("guide.md",)}
    )


SUBSTITUTE = Reference("stand-in.md", "stand-in.md", walk="stand-in.md")
SECTION = Reference("stand-in.md#one", "stand-in.md", "one", walk="stand-in.md")
WHOLE = writing({("rules.md", None): SUBSTITUTE})
FRAGMENTED = writing(
    {("rules.md", None): SUBSTITUTE, ("rules.md", "escalation"): SECTION}
)


def test_no_pair_leaves_a_reference_naming_what_it_named() -> None:
    assert identity(inside("guide.md", "rules.md", UNSUBSTITUTED)) == "rules.md"


def test_a_document_key_names_the_substitute() -> None:
    assert identity(inside("guide.md", "rules.md", WHOLE)) == "stand-in.md"


def test_a_document_key_covers_every_fragment_of_its_document() -> None:
    found = inside("guide.md", "rules.md#escalation", WHOLE)
    assert (found.path, found.fragment) == ("stand-in.md", "escalation")


def test_a_fragment_key_takes_the_section_it_names() -> None:
    found = inside("guide.md", "rules.md#escalation", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", "one")


def test_a_fragment_key_leaves_another_section_of_the_document_alone() -> None:
    found = inside("guide.md", "rules.md#other", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", "other")


def test_a_section_key_serves_no_other_section_of_its_document() -> None:
    """A key carrying a section redirects that section and nothing beside it."""
    mapped = writing({("rules.md", "escalation"): SECTION})
    found = inside("guide.md", "rules.md#other", mapped)
    assert identity(found) == "rules.md#other"
    assert not mapped.redirects.served(
        ("guide.md", ("rules.md", "escalation")), SECTION
    )


def test_a_section_keys_substitute_section_is_the_one_the_run_reads() -> None:
    """The redirect replaces the reference, so the substitute's section is the whole."""
    advised = Reference("stand-in.md#advised", "stand-in.md", "advised")
    mapped = writing({("rules.md", "escalation"): advised})
    found = inside("guide.md", "rules.md#escalation", mapped)
    assert (found.path, found.fragment) == ("stand-in.md", "advised")


def test_a_whole_document_reference_takes_the_document_key() -> None:
    found = inside("guide.md", "rules.md", FRAGMENTED)
    assert (found.path, found.fragment) == ("stand-in.md", None)


def test_a_key_is_the_identity_a_reference_normalized_to() -> None:
    """Two spellings of one path name one key, so one pair serves both."""
    mapped = writing(
        {("docs/rules.md", None): Reference("s.md", "s.md")},
        "guide.md",
        "docs/guide.md",
    )
    assert inside("guide.md", "./docs/rules.md", mapped).path == "s.md"
    assert inside("docs/guide.md", "rules.md", mapped).path == "s.md"


def test_the_substitute_is_the_target_whole_and_the_text_stays_authored() -> None:
    found = inside("guide.md", "./rules.md", WHOLE)
    assert found.original == "./rules.md"
    assert (found.path, found.walk) == ("stand-in.md", "stand-in.md")
    assert is_markdown(found.path)


def test_a_substitute_above_the_working_directory_is_reached() -> None:
    """A key decides what an identity names, wherever its substitute sits."""
    mapped = writing(
        {("docs/rules.md", None): Reference("../s.md", "../s.md")}, "docs/guide.md"
    )
    assert inside("docs/guide.md", "rules.md", mapped).path == "../s.md"


def test_a_path_above_the_working_directory_is_redirected_by_a_key() -> None:
    """A pair is asked of an identity above the working directory too."""
    mapped = writing({("../notes.md", None): Reference("stand-in.md", "stand-in.md")})
    found = inside("guide.md", "../notes.md", mapped)
    assert found.path == "stand-in.md"
    assert is_markdown(found.path)


def test_an_unmapped_path_above_the_working_directory_names_itself() -> None:
    """A path no pair holds a key for names the document it normalized to."""
    assert inside("guide.md", "../notes.md").path == "../notes.md"
    assert inside("guide.md", "../notes.md", WHOLE).path == "../notes.md"


def test_a_pair_is_consulted_on_the_authored_identity_not_the_substitute() -> None:
    """A key is the identity the reference normalized to, never the substitute's."""
    mapped = writing(
        {("notes.md", None): Reference("../stand-in.md", "../stand-in.md")},
        "docs/guide.md",
    )
    assert inside("docs/guide.md", "../notes.md", mapped).path == "../stand-in.md"


def test_only_the_authored_identity_is_matched_not_the_substitute_path() -> None:
    """A substitute that is also a key is read from disk rather than followed again."""
    mapped = writing(
        {
            ("notes.md", None): Reference("../stand-in.md", "../stand-in.md"),
            ("../stand-in.md", None): Reference("../other.md", "../other.md"),
        },
        "docs/guide.md",
    )
    assert inside("docs/guide.md", "../notes.md", mapped).path == "../stand-in.md"


def test_an_external_reference_is_not_redirected() -> None:
    found = inside("guide.md", "https://example.test/rules.md", WHOLE)
    assert (found.external, found.path) == (True, "")


def test_the_two_halves_of_one_resolution_take_the_same_mapping() -> None:
    """`bundled` and `withholding_target` read one answer, so both agree."""
    assert bundled("guide.md", "rules.md", "the rules", DECLARING, WHOLE) is not None
    assert bundled("guide.md", "rules.md", "¬ the rules", DECLARING, WHOLE) is None
    assert withholding_target("guide.md", "rules.md", "¬ the rules", DECLARING, WHOLE)


def test_a_mapping_is_a_value_the_run_cannot_rewrite() -> None:
    with pytest.raises(TypeError):
        WHOLE.documents["guide.md"][("other.md", None)] = SUBSTITUTE  # type: ignore[index]


def test_one_key_serving_two_references_records_one_substitution() -> None:
    """A key names a target, so the two references it serves are one substitution."""
    mapped = writing({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", mapped, "guide.md:3")
    inside("guide.md", "rules.md#escalation", mapped, "guide.md:5")
    assert [one.resolved for one in mapped.redirects.targets()] == ["stand-in.md"]


def test_a_substitution_names_the_first_link_that_redirected_it() -> None:
    """The record keeps the position the run first met the substitution at."""
    mapped = writing({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", mapped, "guide.md:3")
    inside("guide.md", "rules.md", mapped, "guide.md:9")
    assert [one.origin for one in mapped.redirects.targets()] == ["guide.md:3"]


def test_a_stage_that_resolves_a_link_again_records_no_second_substitution() -> None:
    """Emission and candidate validation re-resolve a link and add nothing."""
    mapped = writing({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "rules.md", mapped, "guide.md:3")
    bundled("guide.md", "rules.md", "the rules", DECLARING, mapped)
    assert len(mapped.redirects.targets()) == 1


def test_a_mapping_stating_no_pair_records_no_substitution() -> None:
    """A run whose documents state no pair has no subject for either warning."""
    inside("guide.md", "rules.md", UNSUBSTITUTED, "guide.md:3")
    assert UNSUBSTITUTED.redirects.targets() == ()


def test_a_pair_is_served_by_a_reference_its_document_writes() -> None:
    mapped = writing({("rules.md", None): SUBSTITUTE})
    inside("guide.md", "notes.md", mapped)
    assert not mapped.redirects.served(("guide.md", ("rules.md", None)), SUBSTITUTE)
    inside("guide.md", "rules.md", mapped)
    assert mapped.redirects.served(("guide.md", ("rules.md", None)), SUBSTITUTE)


def stating(document: Path, subst: str) -> None:
    """One document whose `default` preset states the `subst` list given."""
    text = document.read_text()
    if text.startswith(DECLARED):
        text = (
            f"---\nprosiform:\n  default:\n    subst: {subst}\n---\n"
            + text[len(DECLARED) :]
        )
    else:
        text = text.replace("  default:\n", f"  default:\n    subst: {subst}\n", 1)
    document.write_text(text)


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
    (tmp_path / "guide.md").write_text(
        DECLARED + "# Guide\n\nSee [the rules](rules.md).\n"
    )
    (tmp_path / "rules.md").write_text(DECLARED + "# Rules\n\n## Escalation\n\nAsk.\n")
    (tmp_path / "stand-in.md").write_text(DECLARED + "# Stand-in\n\nA stand-in.\n")
    return tmp_path


def test_a_document_stating_no_pair_publishes_the_document_the_link_names(
    tree: Path,
) -> None:
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Rules" in published
    assert "# Stand-in" not in published


def test_a_pair_publishes_the_substitute(tree: Path) -> None:
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Stand-in" in published
    assert "# Rules" not in published


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


def test_a_document_key_naming_an_absent_document_keeps_its_shape(tree: Path) -> None:
    """A document key's absence is refused as every other absent target is."""
    (tree / "guide.md").write_text(
        DECLARED + "# Guide\n\nRun [\u21c9 the rules](absent.md).\n"
    )
    _status, said = refused(tree, "-o", str(tree / "out"), "guide.md")
    assert [one["code"] for one in said] == ["E_TARGET_NOT_FOUND"]
    assert said[0]["reference"] == "absent.md"
    assert "subst" not in said[0]["message"]
    assert "resolved" not in said[0]


def test_a_document_key_and_a_section_key_of_it_are_two_keys(tree: Path) -> None:
    """The identity a key names is its document and its section together."""
    stating(
        tree / "guide.md", "[{rules.md: stand-in.md}, {rules.md#escalation: guide.md}]"
    )
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Stand-in" in published


def test_a_title_carrying_a_withheld_link_is_headed_by_the_text_it_emits(
    tree: Path,
) -> None:
    """A heading compared for coincidence is the text the emission publishes.

    The title's link names a document the tree lacks, so it is the pair
    that makes its target exist and the mark that is dropped. A second
    document titled plainly reads the same once the mark is gone, which is
    what the run warns about.
    """
    (tree / "guide.md").write_text(
        DECLARED + "# [\u00ac the rules](missing.md)\n\nSee.\n"
    )
    (tree / "sibling.md").write_text(DECLARED + "# the rules\n\nAlso.\n")
    stating(tree / "guide.md", "[{missing.md: stand-in.md}]")
    out, err = io.StringIO(), io.StringIO()
    previous = Path.cwd()
    try:
        os.chdir(tree)
        status = main(
            ["-d", "json", linked(tree, "guide.md", "sibling.md")],
            out,
            err,
        )
    finally:
        os.chdir(previous)
    assert status == 0
    voices = [json.loads(line) for line in err.getvalue().splitlines() if line]
    assert [one["code"] for one in voices] == [
        "W_COINCIDENT_HEADING",
        "W_SUBST_USED",
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
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    voice = said[0]
    assert voice["source"] == "rules.md"
    assert voice["resolved"] == "stand-in.md"
    assert voice["location"] == {"file": "guide.md", "line": 8, "column": 1}


def test_a_substitution_warning_states_the_identity_the_reference_would_have_named(
    tree: Path,
) -> None:
    """Two keys naming one stand-in are told apart only by what each replaces."""
    (tree / "sibling.md").write_text(
        DECLARED + "# Sibling\n\nSee [other rules](other.md).\n"
    )
    (tree / "other.md").write_text("# Other\n\nOther.\n")
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    stating(tree / "sibling.md", "[{other.md: stand-in.md}]")
    status, said = voices(
        tree, "-o", str(tree / "out"), linked(tree, "guide.md", "sibling.md")
    )
    assert status == 0
    assert [one["code"] for one in said] == [
        "W_SUBST_USED",
        "W_SUBST_USED",
    ]
    assert ["'rules.md'" in said[0]["message"], "'other.md'" in said[1]["message"]] == [
        True,
        True,
    ]


def test_an_unused_key_warns_with_no_location_and_publishes(tree: Path) -> None:
    """A pair no link named has no link to point at."""
    stating(tree / "guide.md", "[{unrelated.md: stand-in.md}]")
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Rules" in published
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_UNUSED"]
    assert said[0]["source"] == "unrelated.md"
    assert "location" not in said[0]


def test_a_served_key_warns_unused_for_nothing(tree: Path) -> None:
    """A pair a link named states no unused pair."""
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    _status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert SUBST_UNUSED not in [one["code"] for one in said]


def test_a_check_run_reports_the_substitution_and_publishes_nothing(
    tree: Path,
) -> None:
    """A pair applies under `-c`, which is how a substituted check runs in CI."""
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    assert said[0]["resolved"] == "stand-in.md"
    assert not (tree / "out" / "guide.bundles").exists()


def test_a_run_stating_no_pair_states_neither_warning(tree: Path) -> None:
    """A run whose documents state no pair raises neither: neither has a subject."""
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert said == []


def test_a_section_key_leaves_the_rest_of_its_document_real(tree: Path) -> None:
    """One branch is redirected and the rest of its document compiles as it ships."""
    (tree / "guide.md").write_text(
        DECLARED + "# Guide\n\nRequire [the rules](rules.md) whole.\n\n"
        "Read [the escalation](rules.md#escalation) with it.\n"
    )
    (tree / "stand-in.md").write_text(
        DECLARED + "# Stand-in\n\n## Escalation\n\nAsk the stand-in.\n"
    )
    stating(tree / "guide.md", "[{rules.md#escalation: stand-in.md}]")
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Rules" in published
    assert "Ask the stand-in." in published
    assert "Ask.\n" in published


def test_a_document_key_and_a_section_key_of_it_both_serve_their_references(
    tree: Path,
) -> None:
    """The narrower key takes the section, and the wider one takes the document."""
    (tree / "guide.md").write_text(
        DECLARED + "# Guide\n\nRequire [the rules](rules.md) whole.\n\n"
        "Read [the escalation](rules.md#escalation) with it.\n"
    )
    (tree / "rules-copy.md").write_text(
        DECLARED + "# Rules Copy\n\n## Escalation\n\nCopy.\n"
    )
    (tree / "escalation-copy.md").write_text(
        DECLARED + "# Escalation Copy\n\n## Escalation\n\nEscalated.\n"
    )
    stating(
        tree / "guide.md",
        "[{rules.md: rules-copy.md}, {rules.md#escalation: escalation-copy.md}]",
    )
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert (tree / "out" / "guide.bundles" / "guide.bundle.md").is_file()
    for substitute in ("# Rules Copy", "# Escalation Copy"):
        assert substitute in published
    assert "# Rules\n" not in published


def test_a_substitute_that_is_also_a_key_is_read_from_disk(tree: Path) -> None:
    """A pair is applied once, so the second key is never followed."""
    (tree / "first.md").write_text(DECLARED + "# First\n\nFirst.\n")
    (tree / "second.md").write_text(DECLARED + "# Second\n\nSecond.\n")
    (tree / "third.md").write_text(DECLARED + "# Third\n\nThird.\n")
    (tree / "guide.md").write_text(
        DECLARED + "# Guide\n\nRequire [the first](first.md) whole.\n"
    )
    stating(tree / "guide.md", "[{first.md: second.md}, {second.md: third.md}]")
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED", "W_SUBST_UNUSED"]
    assert said[0]["resolved"] == "second.md"
    assert said[1]["source"] == "second.md"
    _status, published = invoke(tree, "guide.md")
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
            "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
            "The guide preamble, linking [the notes](notes.md) and "
            "[the rules](rules.md).\n\n## Scope\n\nThe guide's scope.\n"
        ),
        "notes.md": (
            "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
            "The notes preamble.\n\n## Scope\n\nThe notes' scope.\n"
        ),
        "rules.md": "# Rules\n\nEvery rule the tree under test holds.\n",
        "stand-in.md": (
            "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
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
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, published, _said = grouped(tree, "guide.md")
    assert status == 0
    assert published.startswith(f"{opening('Rules')}# Rules\n")
    assert "### Stand-In" in published
    assert published.count("The stand-in preamble.") == 1
    assert "Every rule the tree under test holds." not in published


def test_a_substitute_declaring_no_group_joins_no_group(tmp_path: Path) -> None:
    """No setting travels from the document the key named."""
    tree = group_tree(tmp_path)
    (tree / "plain.md").write_text(DECLARED + "# Plain\n\nA plain stand-in.\n")
    stating(tree / "guide.md", "[{rules.md: plain.md}]")
    status, published, _said = grouped(tree, "guide.md")
    assert status == 0
    assert "# Plain" in published
    assert "### Plain" not in published


def test_the_group_a_substitute_declares_is_the_one_the_bundle_merges(
    tmp_path: Path,
) -> None:
    """The authored target's own group declaration contributes nothing."""
    tree = group_tree(tmp_path)
    (tree / "rules.md").write_text(
        "---\nprosiform:\n  default:\n    group: {authored: 2}\n---\n"
        "# Rules\n\nEvery rule the tree under test holds.\n"
    )
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, published, _said = grouped(tree, "guide.md")
    assert status == 0
    assert published.startswith(f"{opening('Rules')}# Rules\n")
    assert "# Authored" not in published


def test_a_group_conflict_names_the_substitutes_own_declaration(
    tmp_path: Path,
) -> None:
    """The declaration that disagrees is the substitute's, at its own position."""
    tree = group_tree(tmp_path)
    (tree / "stand-in.md").write_text(
        "---\nprosiform:\n  default:\n    group: {rules: 3}\n---\n"
        "# Stand-in\n\nThe stand-in preamble.\n"
    )
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, _published, said = grouped(tree, "guide.md")
    assert status == 1
    assert [one["code"] for one in said] == ["E_GROUP_CONFLICT"]
    assert said[0]["related"][0]["file"] == "stand-in.md"


def test_a_substitutes_metadata_failure_names_the_substitute(tmp_path: Path) -> None:
    """The substitute's own declaration is the one whose field is refused."""
    tree = group_tree(tmp_path)
    (tree / "stand-in.md").write_text(
        "---\nprosiform:\n  default:\n    group: rules\n---\n# Stand-in\n\nStand-in.\n"
    )
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, _published, said = grouped(tree, "guide.md")
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
        "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
        "The notes preamble, linking [the rules](rules.md).\n\n"
        "## Scope\n\nThe notes' scope.\n"
    )
    stating(tree / "notes.md", "[{rules.md: stand-in.md}]")
    stating(tree / "guide.md", "[{rules.md: stand-in.md}]")
    status, published, _said = grouped(tree, "guide.md")
    assert status == 0
    # One overview subsection and one variant heading name the one member.
    assert published.count("### Stand-In") == 2
    assert published.count("The stand-in preamble.") == 1
    assert published.count("The stand-in's scope.") == 1


def test_a_substitute_above_the_working_directory_reads_its_own_settings(
    tmp_path: Path,
) -> None:
    """AC20's parent segment, read through the substitute's own bytes.

    An alternative carrying `..` names a substitute above the invocation working
    directory, and the group it joins is its own. Its links resolve from
    the directory it sits in, and a link beside it naming a document that
    declares nothing is carried as its author wrote it.
    """
    tree = tmp_path / "tree"
    above = tmp_path / "above"
    tree.mkdir()
    above.mkdir()
    (tree / "guide.md").write_text(
        "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
        "The guide preamble, linking [the rules](rules.md).\n\n"
        "## Scope\n\nThe guide's scope.\n"
    )
    (tree / "rules.md").write_text("# Rules\n\nEvery rule.\n")
    (above / "entry.md").write_text(
        "---\nprosiform:\n  default:\n    group: {rules: 2}\n---\n"
        "The stand-in preamble, linking [its detail](detail.md).\n\n"
        "## Scope\n\nThe stand-in's scope.\n"
    )
    (above / "detail.md").write_text("# Detail\n\nBeside the stand-in.\n")
    (tree / "out").mkdir()
    stating(tree / "guide.md", "[{rules.md: ../above/entry.md}]")
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    folder = tree / "out" / "guide.bundles"
    published = (folder / "guide.bundle.md").read_text()
    assert published.startswith(f"{opening('Rules')}# Rules\n")
    assert "### Entry" in published
    assert "[its detail](detail.md)" in published
    assert "Beside the stand-in." not in published


def withheld_tree(tmp_path: Path) -> Path:
    """A guide deferring one section, beside a stand-in holding a different one."""
    (tmp_path / "out").mkdir()
    (tmp_path / "guide.md").write_text(
        DECLARED
        + "# Guide\n\nDefer [\u00ac the rules](rules.md#escalation) to a later run.\n"
    )
    (tmp_path / "rules.md").write_text(
        DECLARED + "# Rules\n\nEvery rule the tree under test holds.\n\n"
        "## Escalation\n\nAsk the maintainer.\n"
    )
    (tmp_path / "stand-in.md").write_text(
        DECLARED
        + "# Stand-in\n\nOne section, redirected.\n\n## Answers\n\nAsk the stand-in.\n"
    )
    return tmp_path


def test_a_deferred_target_is_redirected_to_the_substitute(tmp_path: Path) -> None:
    """AC4: the destination a deferral publishes is the substitute's own path.

    A deferral compiles nothing here, so the substitute contributes no
    content and no heading: what moves is the destination the later run
    follows.
    """
    tree = withheld_tree(tmp_path)
    stating(tree / "guide.md", "[{rules.md#escalation: stand-in.md#answers}]")
    status, published, said = grouped(tree, "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    assert "[the rules](stand-in.md#answers)" in published
    assert "Every rule the tree under test holds." not in published
    assert "Ask the stand-in." not in published
    assert "# Stand-in" not in published


def test_a_deferred_destination_publishes_the_section_the_substitution_names(
    tmp_path: Path,
) -> None:
    """The resolved fragment is published, so a later run finds the section it names.

    A key carrying a section redirects the section with the document. The
    run has confirmed the substitute carries it, so publishing the
    authored fragment instead would name a section that need not exist
    and a later run following the bundle would refuse.
    """
    tree = withheld_tree(tmp_path)
    the_run = tree / "out" / "guide.bundles" / "guide.bundle.md"
    stating(tree / "guide.md", "[{rules.md#escalation: stand-in.md#answers}]")
    assert grouped(tree, "guide.md")[0] == 0
    assert "[the rules](stand-in.md#answers)" in the_run.read_text()
    (tree / "later.md").write_text(
        DECLARED + "# Later\n\nFollow [the rules](stand-in.md#answers).\n"
    )
    assert invoke(tree, "later.md")[0] == 0
    (tree / "later.md").write_text(
        DECLARED + "# Later\n\nFollow [the rules](stand-in.md#escalation).\n"
    )
    assert invoke(tree, "later.md")[0] == 1


def test_a_deferred_targets_heading_is_confirmed_of_the_substitute(
    tmp_path: Path,
) -> None:
    """The document the run confirms is the one the later run reads."""
    tree = withheld_tree(tmp_path)
    stating(tree / "guide.md", "[{rules.md#escalation: stand-in.md#elsewhere}]")
    status, said = voices(tree, "-o", str(tree / "out"), "guide.md")
    assert status == 1
    assert [one["code"] for one in said] == ["E_TARGET_NOT_FOUND"]
    assert said[0]["resolved"] == "stand-in.md"


def test_a_dispatched_target_is_redirected_and_its_bundle_compiled(
    tmp_path: Path,
) -> None:
    """A dispatch compiles the bundle of the substitute, not of the target."""
    (tmp_path / "out").mkdir()
    (tmp_path / "guide.md").write_text(
        DECLARED + "# Guide\n\n## Steps\n\nApply [\u21c9 the rules](rules.md).\n"
    )
    (tmp_path / "rules.md").write_text(
        DECLARED + "# Rules\n\nEvery rule the tree holds.\n"
    )
    (tmp_path / "stand-in.md").write_text(
        DECLARED + "# Stand-in\n\nEvery rule the stand-in holds.\n"
    )
    stating(tmp_path / "guide.md", "[{rules.md: stand-in.md}]")
    status, said = voices(tmp_path, "-o", str(tmp_path / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    folder = tmp_path / "out" / "guide.bundles"
    assert (folder / "stand-in.bundle.md").is_file()
    assert not (folder / "rules.bundle.md").exists()
    published = (folder / "guide.bundle.md").read_text()
    assert "(stand-in.bundle.md)" in published
    assert (
        (folder / "stand-in.bundle.md")
        .read_text()
        .startswith(f"{opening('Stand-in')}# Stand-in\n")
    )


def test_a_parallel_dispatched_target_is_redirected_and_listed_once(
    tmp_path: Path,
) -> None:
    """The set a parallel mark publishes lists the substitute's bundle."""
    (tmp_path / "out").mkdir()
    (tmp_path / "guide.md").write_text(
        DECLARED
        + "# Guide\n\n## Steps\n\nRun [\u2afd the rules](rules.md) beside the rest.\n"
    )
    (tmp_path / "rules.md").write_text(
        DECLARED + "# Rules\n\nEvery rule the tree holds.\n"
    )
    (tmp_path / "stand-in.md").write_text(
        DECLARED + "# Stand-in\n\nEvery rule the stand-in holds.\n"
    )
    stating(tmp_path / "guide.md", "[{rules.md: stand-in.md}]")
    status, said = voices(tmp_path, "-o", str(tmp_path / "out"), "guide.md")
    assert status == 0
    assert [one["code"] for one in said] == ["W_SUBST_USED"]
    folder = tmp_path / "out" / "guide.bundles"
    assert (folder / "stand-in.bundle.md").is_file()
    listed = (folder / "guide.bundle.md").read_text()
    assert "[\u21c9 the rules](stand-in.bundle.md)" in listed


def test_the_candidate_comparison_reads_the_same_substitute() -> None:
    """A substituted bundle's expected destination is the one the bundle published.

    The comparison resolves each withheld link again, so a run whose
    published destination came from a pair while the comparison
    resolved without it would report the destination as one the bundle
    invented. Both answers are read from one mapping here.
    """
    text = "# Guide\n\nDefer [\u00ac the rules](rules.md#escalation) to a later run.\n"
    tokens = parse(text, BUDGET, {})
    span = next(one for one in regions(tokens) if one.type == "paragraph_open")
    mapped = writing(
        {
            ("rules.md", "escalation"): Reference(
                "stand-in.md#answers", "stand-in.md", "answers", walk="stand-in.md"
            )
        }
    )
    found = [
        intended(
            "guide.md",
            one,
            at,
            children,
            {},
            DECLARING,
            None,
            mapped,
        )
        for children, at, one in carried(tokens, span)
    ]
    assert [one.destination for one in found] == ["stand-in.md#answers"]
    unmapped = [
        intended("guide.md", one, at, children, {}, DECLARING, None, UNSUBSTITUTED)
        for children, at, one in carried(tokens, span)
    ]
    assert [one.destination for one in unmapped] == ["rules.md#escalation"]


GOVERNED = Substitution().governed({"guide.md": {("rules.md", None): SUBSTITUTE}})


def test_a_documents_pair_redirects_the_links_that_document_writes() -> None:
    assert identity(inside("guide.md", "rules.md", GOVERNED)) == "stand-in.md"


def test_a_documents_pair_leaves_another_documents_links_alone() -> None:
    assert identity(inside("notes.md", "rules.md", GOVERNED)) == "rules.md"


def test_a_documents_pair_records_to_the_runs_record() -> None:
    mapped = Substitution()
    governed = mapped.governed({"guide.md": {("rules.md", None): SUBSTITUTE}})
    inside("guide.md", "rules.md", governed, "guide.md:6")
    assert [one.resolved for one in mapped.redirects.targets()] == ["stand-in.md"]
    assert mapped.redirects.served(("guide.md", ("rules.md", None)), SUBSTITUTE)


def test_reading_what_a_heading_shows_records_no_substitution() -> None:
    """The heading-text path decides what a heading shows and serves no key."""
    mapped = writing({("rules.md", None): SUBSTITUTE})
    tokens = parse("# Guide\n\n## [\u00ac Rules](rules.md)\n", BUDGET)
    shown = shown_text("guide.md", tokens, DECLARING, mapped, conversions={})
    assert list(shown.values()) == ["Guide", "Rules"]
    assert mapped.redirects.targets() == ()
    assert not mapped.redirects.served(("guide.md", ("rules.md", None)), SUBSTITUTE)


def test_an_unrecorded_mapping_answers_as_the_mapping_does() -> None:
    mapped = writing({("rules.md", None): SUBSTITUTE})
    quiet = mapped.unrecorded().writing("guide.md")
    assert quiet.redirect(Reference("rules.md", "rules.md"), "guide.md:3").path == (
        "stand-in.md"
    )
    assert mapped.redirects.targets() == ()
    assert not mapped.redirects.served(("guide.md", ("rules.md", None)), SUBSTITUTE)


def presetted(tree: Path, presets: str) -> None:
    """The tree's guide, declaring the presets given as its prosiform mapping."""
    (tree / "guide.md").write_text(
        f"---\nprosiform:\n{presets}---\n"
        "# Guide\n\n## Keep\n\nSee [the rules](rules.md).\n"
    )


def test_a_default_pair_publishes_the_substitute_and_states_it(tree: Path) -> None:
    presetted(tree, "  default:\n    subst: [{rules.md: stand-in.md}]\n")
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Stand-in" in published
    assert "# Rules" not in published
    _status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert [(one["code"], one["source"], one["resolved"]) for one in said] == [
        ("W_SUBST_USED", "rules.md", "stand-in.md")
    ]


def test_a_selected_presets_pair_holds_over_defaults(tree: Path) -> None:
    (tree / "other.md").write_text(DECLARED + "# Other\n\nOther.\n")
    (tree / "entry.md").write_text(
        DECLARED + '# Entry\n\n## Keep\n\n[guide](guide.md "Keep")\n'
    )
    presetted(
        tree,
        "  default:\n    subst: [{rules.md: other.md}]\n"
        "  Keep:\n    subst: [{rules.md: stand-in.md}]\n",
    )
    status, published = invoke(tree, "entry.md")
    assert status == 0
    assert "# Stand-in" in published
    assert "# Other" not in published


def test_a_document_under_no_subst_compiles_its_links_as_authored(
    tree: Path,
) -> None:
    presetted(tree, "  default:\n    group: {guides: 1}\n")
    status, published = invoke(tree, "guide.md")
    assert status == 0
    assert "# Rules" in published
    assert "# Stand-in" not in published


def test_a_pair_no_link_names_warns_unused_naming_its_document(tree: Path) -> None:
    presetted(tree, "  default:\n    subst: [{unrelated.md: stand-in.md}]\n")
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [(one["code"], one["source"]) for one in said] == [
        ("W_SUBST_UNUSED", "unrelated.md")
    ]
    assert "prosiform.default in 'guide.md'" in said[0]["message"]
    assert "location" not in said[0]


def test_a_pair_reached_only_by_a_heading_outside_the_selection_is_unused(
    tree: Path,
) -> None:
    """A heading the run did not select compiles nothing, so its link uses no pair."""
    (tree / "guide.md").write_text(
        "---\nprosiform:\n  default:\n    subst: [{rules.md: stand-in.md}]\n---\n"
        "# Guide\n\n## Keep\n\nFollow the guide.\n\n## [\u00ac Rules](rules.md)\n\n"
        "Read the rules.\n"
    )
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md#keep")
    assert status == 0
    assert [(one["code"], one["source"]) for one in said] == [
        ("W_SUBST_UNUSED", "rules.md")
    ]


def test_two_tag_selections_selecting_disagreeing_pairs_are_refused(tree: Path) -> None:
    (tree / "other.md").write_text(DECLARED + "# Other\n\nOther.\n")
    (tree / "entry.md").write_text(
        DECLARED + '# Entry\n\n## Plan\n\n[guide](guide.md "Plan")\n\n'
        '## Review\n\n[guide](guide.md "Review")\n'
    )
    presetted(
        tree,
        "  Plan:\n    subst: [{rules.md: other.md}]\n"
        "  Review:\n    subst: [{rules.md: stand-in.md}]\n",
    )
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "entry.md")
    assert status == 2
    assert [one["code"] for one in said] == ["E_INVALID_USAGE"]
    assert "prosiform.Plan.subst and prosiform.Review.subst" in said[0]["message"]


def test_a_pair_whose_alternative_names_no_markdown_document_is_refused(
    tree: Path,
) -> None:
    presetted(tree, "  default:\n    subst: [{rules.md: notes.txt}]\n")
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert status == 2
    assert [one["code"] for one in said] == ["E_INVALID_USAGE"]
    assert "names no Markdown document" in said[0]["message"]


def test_a_preset_pair_reads_the_same_from_any_working_directory(
    tmp_path: Path,
) -> None:
    """Both sides resolve from the declaring file, so the run's start plays no part."""
    (tmp_path / "out").mkdir()
    (tmp_path / "modes").mkdir()
    (tmp_path / "modes" / "plan.md").write_text(
        "---\nprosiform:\n  default:\n    subst: [{../rules.md: ../stand-in.md}]\n"
        "---\n# Plan\n\n## Keep\n\nSee [the rules](../rules.md).\n"
    )
    (tmp_path / "rules.md").write_text(DECLARED + "# Rules\n\nThe rules.\n")
    (tmp_path / "stand-in.md").write_text(DECLARED + "# Stand-in\n\nA stand-in.\n")
    (tmp_path / "modes" / "out").mkdir()
    assert invoke(tmp_path / "modes", "plan.md")[0] == 0
    assert invoke(tmp_path, "modes/plan.md")[0] == 0
    from_modes = tmp_path / "modes" / "out" / "plan.bundles" / "plan.bundle.md"
    from_root = tmp_path / "out" / "modes_plan.bundles" / "modes_plan.bundle.md"
    assert from_root.read_text() == from_modes.read_text()
    assert "# Stand-in" in from_root.read_text()
    assert "# Rules" not in from_root.read_text()


def test_a_substitutes_fragment_only_link_names_its_own_section() -> None:
    """The substitute writes no pair, so its section link resolves where it stands."""
    mapped = Substitution().governed(
        {"guide.md": {("rules.md", None): SUBSTITUTE, ("stand-in.md", None): SECTION}}
    )
    assert identity(inside("stand-in.md", "#part", mapped)) == "stand-in.md#part"
    assert identity(inside("guide.md", "stand-in.md", mapped)) == "stand-in.md#one"


def test_two_documents_declaring_one_key_are_two_pairs(tree: Path) -> None:
    """A pair is its document's, so the one no link of its document used warns."""
    pair = "---\nprosiform:\n  default:\n    subst: [{rules.md: stand-in.md}]\n---\n"
    (tree / "guide.md").write_text(
        DECLARED + "# Guide\n\nSee [one](one.md) and [two](two.md).\n"
    )
    (tree / "one.md").write_text(pair + "# One\n\nSee [the rules](rules.md).\n")
    (tree / "two.md").write_text(pair + "# Two\n\nNo link.\n")
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert status == 0
    assert [(one["code"], one["source"]) for one in said] == [
        ("W_SUBST_USED", "rules.md"),
        ("W_SUBST_UNUSED", "rules.md"),
    ]
    assert "in 'two.md'" in said[1]["message"]


def test_a_folder_side_is_refused_naming_the_entry(tree: Path) -> None:
    """A pair names one document or one section, so a separator ending a side fails."""
    presetted(tree, "  default:\n    subst: [{rules/: stubs/}]\n")
    status, said = voices(tree, "-c", "-o", str(tree / "out"), "guide.md")
    assert status == 1
    assert [one["code"] for one in said] == ["E_INVALID_CONVERSION_METADATA"]
    assert "prosiform.default.subst[0] side 'rules/'" in said[0]["message"]
