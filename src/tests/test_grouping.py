"""Assert the names a merged group writes for explicit members.

The corpus declares what a grouped run publishes. These are the cases
beneath it: the slug a group is headed by, the name a member's
subsection carries, the members a group carries a subsection for and
where those subsections sit, the run of a path a variant heading is
shortened to.
"""

from collections.abc import Mapping

import pytest

from prosiform.bundle import Group
from prosiform.grouping import (
    member_headings,
    merged,
    prepared,
    states,
    titled,
)
from prosiform.profile import parse
from prosiform.provenance import MEMBER_OVERVIEW, VARIANT_HEADING, Generated
from prosiform.source import lines


def group_of(named: str, depth: int, documents: Mapping[str, str]) -> Group:
    """One merged group, from the slug it is headed by and the sources it merges."""
    return merged(
        named,
        depth,
        [
            prepared(path, parse(text), lines(text), {}, None, None, depth)
            for path, text in sorted(documents.items())
        ],
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("modes", "Modes"),
        ("epic-issue-body", "Epic Issue Body"),
        ("plan_mode", "Plan Mode"),
        ("SKILL", "SKILL"),
        ("two words", "Two Words"),
    ],
)
def test_a_name_is_emitted_in_title_case(text: str, expected: str) -> None:
    assert titled(text) == expected


@pytest.mark.parametrize(
    ("heading", "word", "expected"),
    [
        ("modes", "mode", True),
        ("modes", "Mode", True),
        ("mode", "mode", True),
        ("modes", "plan", False),
        ("artifacts", "body", False),
    ],
)
def test_a_group_heading_states_the_kind_its_members_are(
    heading: str, word: str, expected: bool
) -> None:
    assert states(heading, word) is expected


def test_a_member_is_named_by_its_stem_less_what_the_group_states() -> None:
    assert member_headings(
        ["modes/plan-mode.md", "modes/review-mode.md", "modes/mode.md"], "modes"
    ) == {
        "modes/plan-mode.md": "Plan",
        "modes/review-mode.md": "Review",
        "modes/mode.md": "Mode",
    }
    assert member_headings(
        ["artifacts/epic-issue-body.md", "artifacts/bare.md"], "artifacts"
    ) == {
        "artifacts/epic-issue-body.md": "Epic Issue Body",
        "artifacts/bare.md": "Bare",
    }


def test_members_of_one_stem_take_the_segments_that_tell_them_apart() -> None:
    assert member_headings(
        ["guides/alpha/notes.md", "guides/beta/notes.md"], "guides"
    ) == {
        "guides/alpha/notes.md": "Alpha Notes",
        "guides/beta/notes.md": "Beta Notes",
    }


def test_a_member_a_stem_distinguishes_is_named_by_that_stem_alone() -> None:
    assert member_headings(
        ["guides/alpha/notes.md", "guides/beta/summary.md"], "guides"
    ) == {
        "guides/alpha/notes.md": "Notes",
        "guides/beta/summary.md": "Summary",
    }


@pytest.mark.parametrize(
    ("paths", "named", "expected"),
    [
        (
            ["modes/a/plan.md", "modes/b/plan-mode.md"],
            "modes",
            ["A Plan", "B Plan"],
        ),
        (["g/a/notes.md", "g/b/Notes.md"], "g", ["A Notes", "B Notes"]),
        (["g/a/one-two.md", "g/b/one_two.md"], "g", ["A One Two", "B One Two"]),
        (["modes/plan.md", "modes/plan-mode.md"], "modes", ["Plan", "Plan Mode"]),
    ],
)
def test_final_member_names_distinguish_after_formatting(
    paths: list[str], named: str, expected: list[str]
) -> None:
    assert list(member_headings(paths, named).values()) == expected


def test_one_segment_distinguishes_documents_in_one_directory() -> None:
    assert member_headings(["modes/plan-mode.md", "modes/review-mode.md"], "modes") == {
        "modes/plan-mode.md": "Plan",
        "modes/review-mode.md": "Review",
    }


def test_a_shared_stem_takes_the_segments_that_tell_the_paths_apart() -> None:
    assert member_headings(
        ["guides/alpha/notes.md", "guides/beta/notes.md"], "guides"
    ) == {
        "guides/alpha/notes.md": "Alpha Notes",
        "guides/beta/notes.md": "Beta Notes",
    }


def test_the_segments_every_path_shares_are_dropped_before_the_run_is_measured() -> (
    None
):
    assert member_headings(["a/b/one.md", "a/b/c/one.md"], "b") == {
        "a/b/one.md": "One",
        "a/b/c/one.md": "C One",
    }


def test_a_member_the_group_emits_nothing_else_from_takes_a_subsection() -> None:
    one = group_of(
        "notes",
        2,
        {
            "notes/bare.md": "# Bare\n",
            "notes/kept.md": "## Findings\n\nHeld.\n",
        },
    )
    assert one.parts == (
        "# Notes",
        "## Overview",
        "### Bare",
        "## Findings\n",
        "Held.\n",
    )


def test_such_a_subsection_answers_the_whole_document_and_the_title_it_absorbed() -> (
    None
):
    one = group_of("notes", 2, {"notes/bare.md": "# Bare\n"})
    answered = [
        heading.answers
        for heading in one.record.headings
        if isinstance(heading, Generated) and heading.kind == MEMBER_OVERVIEW
    ]
    assert answered == [(("notes/bare.md", None), ("notes/bare.md", "bare"))]


def test_a_member_whose_content_sits_at_the_grouping_depth_takes_no_subsection() -> (
    None
):
    one = group_of("notes", 2, {"notes/bare.md": "## Findings\n\nHeld.\n"})
    assert one.parts == ("# Notes", "## Findings\n", "Held.\n")


def test_a_member_whose_title_the_subsection_absorbs_takes_one() -> None:
    one = group_of("notes", 2, {"notes/bare.md": "# Bare\n\n## Findings\n\nHeld.\n"})
    assert one.parts == (
        "# Notes",
        "## Overview",
        "### Bare",
        "## Findings\n",
        "Held.\n",
    )


def test_a_group_emitting_no_merged_section_carries_no_overview() -> None:
    one = group_of(
        "rules",
        1,
        {
            "rules/agents.md": "Name the harness.\n",
            "rules/common.md": "Keep paragraphs short.\n",
        },
    )
    assert one.parts == (
        "# Rules",
        "## Agents",
        "Name the harness.\n",
        "## Common",
        "Keep paragraphs short.\n",
    )


def answering(one: Group, path: str) -> str:
    """The text of the heading a whole-document reference to one member reaches."""
    return next(
        heading.text
        for heading in one.record.headings
        if (path, None) in heading.answers
    )


def test_two_members_contributing_one_heading_text_reach_two_destinations() -> None:
    one = group_of(
        "rules",
        2,
        {
            "rules/agents.md": "## Style\n\nName the harness.\n",
            "rules/common.md": "## Style\n\nKeep paragraphs short.\n",
        },
    )
    assert answering(one, "rules/agents.md") == "Agents"
    assert answering(one, "rules/common.md") == "Common"


def test_a_heading_text_one_member_carries_is_that_member_s_destination() -> None:
    one = group_of(
        "rules",
        2,
        {
            "rules/agents.md": "## Style\n\nName the harness.\n",
            "rules/limits.md": "## Budgets\n\nStay inside the budget.\n",
        },
    )
    assert answering(one, "rules/agents.md") == "Style"
    assert answering(one, "rules/limits.md") == "Budgets"


def test_no_two_members_of_one_group_reach_one_destination() -> None:
    documents = {
        "rules/agents.md": "## Style\n\nName the harness.\n",
        "rules/common.md": "Read this first.\n\n## Style\n\nKeep paragraphs short.\n",
        "rules/limits.md": "## Budgets\n\nStay inside the budget.\n",
        "rules/notes.md": "- Jot it down.\n",
    }
    one = group_of("rules", 2, documents)
    reached = [
        at
        for at, heading in enumerate(one.record.headings)
        for path in documents
        if (path, None) in heading.answers
    ]
    assert len(reached) == len(documents)
    assert len(set(reached)) == len(documents)


def reaching(one: Group, path: str, fragment: str) -> list[str]:
    """The text of each heading a reference to one member's section reaches."""
    return [
        heading.text
        for heading in one.record.headings
        if (path, fragment) in heading.answers
    ]


def test_a_reference_into_a_shared_section_reaches_its_document_s_variant() -> None:
    one = group_of(
        "rules",
        2,
        {
            "rules/agents.md": "## Style\n\nName the harness.\n",
            "rules/common.md": "## Style\n\nKeep paragraphs short.\n",
        },
    )
    assert reaching(one, "rules/agents.md", "style") == ["Agents"]
    assert reaching(one, "rules/common.md", "style") == ["Common"]


def test_a_reference_into_a_section_one_member_carries_reaches_its_heading() -> None:
    one = group_of("rules", 2, {"rules/agents.md": "## Style\n\nName the harness.\n"})
    assert reaching(one, "rules/agents.md", "style") == ["Style"]


@pytest.mark.parametrize("preamble", ["", "Read this first.\n\n"])
@pytest.mark.parametrize("first", ["Body.\n", "### Draft\n\nBody.\n", ""])
@pytest.mark.parametrize("second", ["### Draft\n\nOther body.\n", ""])
def test_every_pooled_contributor_has_its_own_heading_and_destination(
    preamble: str, first: str, second: str
) -> None:
    one = group_of(
        "rules",
        2,
        {
            "rules/agents.md": preamble + "## Style\n\n" + first,
            "rules/common.md": preamble + "## Style\n\n" + second,
        },
    )
    variants = [
        heading.text
        for heading in one.record.headings
        if isinstance(heading, Generated) and heading.kind == VARIANT_HEADING
    ]
    assert variants == ["Agents", "Common"]
    assert answering(one, "rules/agents.md") == "Agents"
    assert answering(one, "rules/common.md") == "Common"


def test_a_sole_contributor_keeps_its_subheading_arrangement() -> None:
    one = group_of("rules", 2, {"rules/agents.md": "## Style\n\n### Draft\n\nBody.\n"})
    assert one.parts == ("# Rules", "## Style\n", "### Draft\n", "Body.\n")


@pytest.mark.parametrize(
    ("named", "documents", "expected"),
    [
        (
            "g",
            {
                "g/a/notes.md": "First.\n\n## Alone\n\nOnly.\n",
                "g/b/notes.md": "Second.\n\n## Findings\n\nSecond finding.\n",
                "g/c/other.md": "Third.\n\n## Findings\n\nThird finding.\n",
            },
            ["B Notes", "C Other"],
        ),
        (
            "modes",
            {
                "modes/plan-mode.md": "First.\n\n## Procedure\n\nPlan.\n",
                "modes/review-mode.md": "Second.\n\n## Procedure\n\nReview.\n",
            },
            ["Plan", "Review"],
        ),
    ],
)
def test_variant_names_match_the_overview_across_the_whole_group(
    named: str, documents: Mapping[str, str], expected: list[str]
) -> None:
    one = group_of(named, 2, documents)
    overview = {
        heading.answers[0][0]: heading.text
        for heading in one.record.headings
        if isinstance(heading, Generated) and heading.kind == MEMBER_OVERVIEW
    }
    variants = [
        heading
        for heading in one.record.headings
        if isinstance(heading, Generated) and heading.kind == VARIANT_HEADING
    ]
    assert [heading.text for heading in variants] == expected
    assert all(heading.text == overview[heading.answers[0][0]] for heading in variants)
