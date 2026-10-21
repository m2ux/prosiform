"""Assert the names a merged group writes and the membership a rule decides.

The corpus declares what a grouped run publishes. These are the cases
beneath it: the slug a group is headed by, the name a member's overview
subsection carries, the members the `Overview` section carries a
subsection for, the run of a path a variant heading is shortened to, and
the rule that decides which group a document belongs to.
"""

from collections.abc import Mapping

import pytest

from prosiform.bundle import Group
from prosiform.cli import membership
from prosiform.grouping import (
    member_heading,
    merged,
    prepared,
    qualifiers,
    states,
    titled,
)
from prosiform.profile import parse
from prosiform.provenance import MEMBER_OVERVIEW, Generated
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


@pytest.mark.parametrize(
    ("path", "named", "expected"),
    [
        ("artifacts/epic-issue-body.md", "artifacts", "Epic Issue Body"),
        ("modes/plan-mode.md", "modes", "Plan"),
        ("modes/review-mode.md", "modes", "Review"),
        ("modes/mode.md", "modes", "Mode"),
        ("notes/bare.md", "notes", "Bare"),
    ],
)
def test_a_member_is_named_by_its_stem_less_what_the_group_states(
    path: str, named: str, expected: str
) -> None:
    assert member_heading(path, named) == expected


def test_one_segment_distinguishes_documents_in_one_directory() -> None:
    assert qualifiers(["modes/plan-mode.md", "modes/review-mode.md"]) == {
        "modes/plan-mode.md": "Plan Mode",
        "modes/review-mode.md": "Review Mode",
    }


def test_a_shared_stem_takes_the_segments_that_tell_the_paths_apart() -> None:
    assert qualifiers(["guides/alpha/notes.md", "guides/beta/notes.md"]) == {
        "guides/alpha/notes.md": "Alpha Notes",
        "guides/beta/notes.md": "Beta Notes",
    }


def test_the_segments_every_path_shares_are_dropped_before_the_run_is_measured() -> (
    None
):
    assert qualifiers(["a/b/one.md", "a/b/c/one.md"]) == {
        "a/b/one.md": "One",
        "a/b/c/one.md": "C One",
    }


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("modes/plan-mode.md", "modes"),
        ("guides/alpha/notes.md", "guides"),
        ("entry.md", None),
        ("other/note.md", None),
    ],
)
def test_a_document_belongs_to_the_group_its_deepest_named_directory_heads(
    path: str, expected: str | None
) -> None:
    assert membership(path, {"modes": 2, "guides": 2}) == expected


def test_the_deepest_named_directory_decides_between_two_rules() -> None:
    assert membership("artifacts/modes/one.md", {"artifacts": 2, "modes": 3}) == "modes"


def test_a_member_the_group_emits_nothing_else_from_takes_an_overview_subsection() -> (
    None
):
    one = group_of(
        "notes",
        2,
        {
            "notes/bare.md": "# Bare\n",
            "notes/kept.md": "# Kept\n\n## Findings\n\nHeld.\n",
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
    one = group_of("notes", 2, {"notes/bare.md": "# Bare\n\n## Findings\n\nHeld.\n"})
    assert one.parts == ("# Notes", "## Findings\n", "Held.\n")
