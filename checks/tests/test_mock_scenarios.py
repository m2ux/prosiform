"""Assert the scenario check reads a bundle the way it states.

The check holds a mocked bundle to four things: the run stated its substitution,
the artifact's heading is emitted once at the depth its front matter decides,
every byte outside that section is the unmocked bundle's, and inside the section
the stand-in's words stand where the artifact's did. Each reading is held here
to input it would be read wrongly: a section holding headings deeper than
itself, a heading the document repeats, a stand-in emitted as a document of its
own, a section carrying the artifact's prose beside the stand-in's, a stand-in
whose blocks the mode never reaches, and a tree a run wrote into.
"""

from pathlib import Path

import mock_scenarios
from mock_scenarios import Scenario, Stub

BASELINE = """\
# Artifacts

## Epic

The evidence required before starting an epic's work.

### Operations

#### Check Epic Prerequisites

The evidence required before starting an epic's work.

## Initiative
"""

PRODUCED = """\
# Artifacts

## Epic

### Operations

#### Check Epic Prerequisites

Placeholder for the prerequisite check a drafted epic states.

## Initiative
"""

STUB = """\
---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Epic

A stand-in title paragraph.

## Operations

### Check Epic Prerequisites

Placeholder for the prerequisite check a drafted epic states.

### Check Epic Completion

Placeholder for the completion check a drafted epic states.
"""

SCENARIO = Scenario(
    name="a scenario",
    stub=Stub("stand-in.md", STUB, "artifacts/epic.md"),
    heading="## Epic",
    member=True,
    command="Placeholder for the prerequisite check a drafted epic states.",
    avoided="The evidence required before starting an epic's work.",
)

CONVENTIONS = Scenario(
    name="a conventions scenario",
    stub=Stub("stand-in.md", "# Conventions\n\nRun `./fake-gh`.\n", "conventions.md"),
    heading="# Conventions",
    member=False,
    command="`./fake-gh`",
    avoided="uses its keyring login",
)


def test_a_section_ends_at_the_next_heading_of_its_own_level() -> None:
    found = mock_scenarios.section(BASELINE, "## Epic")
    assert found is not None
    start, end = found
    assert BASELINE[start:end].startswith("## Epic\n")
    assert "## Initiative" not in BASELINE[start:end]
    assert "#### Check Epic Prerequisites" in BASELINE[start:end]


def test_a_heading_the_document_repeats_is_located_at_its_first() -> None:
    found = mock_scenarios.section(BASELINE, "## Epic")
    assert found is not None
    assert found[0] == BASELINE.index("## Epic")


def test_a_heading_the_document_does_not_carry_is_absent() -> None:
    assert mock_scenarios.section(BASELINE, "## Protocol") is None


def test_a_heading_is_counted_by_the_marks_it_opens_with() -> None:
    assert mock_scenarios.depth("## Epic") == 2
    assert mock_scenarios.depth("# Artifacts") == 1
    assert mock_scenarios.depth("### Check Epic Prerequisites") == 3


def test_a_heading_repeated_in_the_bundle_is_counted_every_time() -> None:
    repeated = BASELINE + "\n## Epic\n"
    assert mock_scenarios.headings(repeated).count("## Epic") == 2


def test_a_paragraph_is_read_with_the_heading_above_it() -> None:
    found = mock_scenarios.placed(STUB)
    assert (
        "Check Epic Prerequisites",
        "Placeholder for the prerequisite check a drafted epic states.",
    ) in found


def test_a_paragraph_under_a_heading_is_titled_by_its_nearest_heading() -> None:
    found = mock_scenarios.placed(STUB)
    titles = [title for title, _ in found]
    assert "Check Epic Completion" in titles


def test_a_documents_front_matter_is_not_content() -> None:
    found = mock_scenarios.placed(STUB)
    assert all("prosiform" not in block for _, block in found)


def test_only_a_reached_heading_contributes_a_block() -> None:
    found = mock_scenarios.reachable(STUB, "## Epic", BASELINE, member=True)
    titles = [title for title, _ in found]
    assert "Check Epic Prerequisites" in titles
    assert "Check Epic Completion" not in titles


def test_a_member_contributes_no_title_paragraph() -> None:
    found = mock_scenarios.reachable(STUB, "## Epic", BASELINE, member=True)
    assert all(block != "A stand-in title paragraph." for _, block in found)


def test_a_document_emitted_as_a_title_keeps_its_own_paragraph() -> None:
    stub = "# Conventions\n\nRun `./fake-gh`.\n"
    found = mock_scenarios.reachable(stub, "# Conventions", "", member=False)
    assert found == [("Conventions", "Run `./fake-gh`.")]


def test_a_tree_is_fingerprinted_by_the_bytes_of_each_file(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("# Guide\n")
    first = mock_scenarios.fingerprint(tmp_path)
    (tmp_path / "guide.md").write_text("# Another guide\n")
    assert first != mock_scenarios.fingerprint(tmp_path)


def test_a_run_writing_into_the_tree_it_read_is_a_difference(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("# Guide\n")
    before = mock_scenarios.fingerprint(tmp_path)
    (tmp_path / "guide.bundles").mkdir()
    (tmp_path / "guide.bundles" / "guide.bundle.md").write_text("# Guide\n")
    differences = mock_scenarios.compare_tree(
        "a run", before, mock_scenarios.fingerprint(tmp_path)
    )
    assert len(differences) == 1
    assert any("written guide.bundles" in line for line in differences[0].detail)


def test_a_file_a_run_rewrote_is_a_difference(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("# Guide\n")
    before = mock_scenarios.fingerprint(tmp_path)
    (tmp_path / "guide.md").write_text("# Rewritten\n")
    differences = mock_scenarios.compare_tree(
        "a run", before, mock_scenarios.fingerprint(tmp_path)
    )
    assert any("changed guide.md" in line for line in differences[0].detail)


def test_a_tree_left_as_it_was_is_no_difference(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("# Guide\n")
    held = mock_scenarios.fingerprint(tmp_path)
    assert mock_scenarios.compare_tree("a run", held, held) == []


def test_a_member_heading_emitted_once_is_no_difference() -> None:
    assert mock_scenarios.compare_placement("a run", SCENARIO, PRODUCED, PRODUCED) == []


def test_a_document_emitted_at_the_groups_level_is_a_difference() -> None:
    produced = PRODUCED.replace("## Epic\n", "# Epic\n", 1)
    differences = mock_scenarios.compare_placement(
        "a run", SCENARIO, PRODUCED, produced
    )
    assert any("document of its own" in one.summary for one in differences)


def test_a_member_heading_emitted_twice_is_a_difference() -> None:
    produced = PRODUCED.replace("## Initiative", "## Epic\n\n## Initiative")
    differences = mock_scenarios.compare_placement(
        "a run", SCENARIO, PRODUCED, produced
    )
    assert any("2 times" in one.summary for one in differences)


def test_a_bundle_without_the_sections_heading_is_a_difference() -> None:
    differences = mock_scenarios.compare_placement(
        "a run", SCENARIO, "# Artifacts\n", "# Artifacts\n"
    )
    assert differences


def test_a_section_carrying_the_stand_ins_words_is_no_difference() -> None:
    assert mock_scenarios.compare_section("a run", SCENARIO, BASELINE, PRODUCED) == []


def test_a_section_withholding_the_stand_ins_words_is_a_difference() -> None:
    produced = PRODUCED.replace(
        "Placeholder for the prerequisite check a drafted epic states.", "Nothing."
    )
    differences = mock_scenarios.compare_section("a run", SCENARIO, BASELINE, produced)
    assert any("carries no" in one.summary for one in differences)


def test_a_section_carrying_the_artifacts_prose_is_a_difference() -> None:
    produced = PRODUCED.replace(
        "Placeholder for the prerequisite check a drafted epic states.",
        "The evidence required before starting an epic's work.",
    )
    differences = mock_scenarios.compare_section("a run", SCENARIO, BASELINE, produced)
    assert any("does not state" in one.summary for one in differences)


def test_a_difference_outside_the_section_is_placed_before_it() -> None:
    differences = mock_scenarios.compare_outside(
        "a run", SCENARIO, BASELINE, PRODUCED.replace("# Artifacts", "# Rules", 1)
    )
    assert differences
    assert "ahead of ## Epic" in differences[0].summary


def test_a_difference_after_the_section_is_placed_after_it() -> None:
    differences = mock_scenarios.compare_outside(
        "a run", SCENARIO, BASELINE, PRODUCED.replace("## Initiative", "## Another")
    )
    assert differences
    assert "after ## Epic" in differences[0].summary


def test_a_bundle_matching_outside_the_section_is_no_difference() -> None:
    assert mock_scenarios.compare_outside("a run", SCENARIO, BASELINE, PRODUCED) == []


def test_a_section_naming_the_stand_in_is_no_difference() -> None:
    produced = "# Conventions\n\nRun `./fake-gh`.\n"
    assert mock_scenarios.compare_instruction("a run", CONVENTIONS, produced) == []


def test_a_section_still_naming_the_tracker_is_a_difference() -> None:
    produced = "# Conventions\n\nRun `./fake-gh`, where `gh` uses its keyring login.\n"
    differences = mock_scenarios.compare_instruction("a run", CONVENTIONS, produced)
    assert differences
    assert any("stand-in exists to replace" in one.summary for one in differences)


def test_a_section_naming_no_stand_in_is_a_difference() -> None:
    differences = mock_scenarios.compare_instruction(
        "a run", CONVENTIONS, "# Conventions\n\nRun `gh`.\n"
    )
    assert differences
    assert any("./fake-gh" in one.summary for one in differences)


def test_the_shipped_scenarios_name_the_documents_they_stand_in_for() -> None:
    assert [
        (scenario.stub.key, scenario.heading) for scenario in mock_scenarios.SCENARIOS
    ] == [("artifacts/epic.md", "## Epic"), ("conventions.md", "# Conventions")]


def test_the_shipped_scenarios_are_named_and_distinct() -> None:
    names = [scenario.name for scenario in mock_scenarios.SCENARIOS]
    assert len(names) == len(set(names)) == 2


def test_a_stand_in_declares_the_group_its_artifact_joins() -> None:
    assert 'group: "artifacts"' in mock_scenarios.ARTIFACT_STUB
    assert "group-depth: 1" in mock_scenarios.ARTIFACT_STUB


def test_the_redirected_conventions_name_the_stand_in_and_not_the_tracker() -> None:
    stub = mock_scenarios.CONVENTIONS_STUB
    assert "./fake-gh" in stub
    assert "\n`gh` " not in stub
