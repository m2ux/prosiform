"""Assert the names a merged group writes for explicit members.

The corpus declares what a grouped run publishes. These are the cases
beneath it: the slug a group is headed by, the name a member's
subsection carries, the members a group carries a subsection for and
where those subsections sit, the run of a path a variant heading is
shortened to, and where a group a linked file declares stands in the
result its parent merges.
"""

import json
import re
from collections.abc import Mapping
from contextlib import chdir
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from prosiform.bundle import Group
from prosiform.cli import main
from prosiform.grouping import (
    member_headings,
    merged,
    prepared,
    states,
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
            prepared(
                path, parse(text), lines(text), {}, None, None, depth, conversions={}
            )
            for path, text in sorted(documents.items())
        ],
    )


@pytest.mark.parametrize(
    ("named", "expected"),
    [
        ("modes", "Modes"),
        ("epic-issue-body", "Epic-Issue-Body"),
        ("plan_mode", "Plan_Mode"),
        ("SKILL", "SKILL"),
        ("two words", "Two Words"),
    ],
)
def test_a_group_is_headed_by_its_name_in_title_case(named: str, expected: str) -> None:
    one = group_of(named, 2, {"g/one.md": "## Findings\n\nHeld.\n"})
    assert one.headings[0] == expected


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
        "artifacts/epic-issue-body.md": "Epic-Issue-Body",
        "artifacts/bare.md": "Bare",
    }


def test_members_of_one_stem_take_the_segments_that_tell_them_apart() -> None:
    assert member_headings(
        ["guides/alpha/notes.md", "guides/beta/notes.md"], "guides"
    ) == {
        "guides/alpha/notes.md": "Alpha/Notes",
        "guides/beta/notes.md": "Beta/Notes",
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
            ["A/Plan", "B/Plan"],
        ),
        (["g/a/notes.md", "g/b/Notes.md"], "g", ["A/Notes", "B/Notes"]),
        (["g/a/one-two.md", "g/b/one_two.md"], "g", ["One-Two", "One_Two"]),
        (["modes/plan.md", "modes/plan-mode.md"], "modes", ["Plan", "Plan-Mode"]),
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
        "guides/alpha/notes.md": "Alpha/Notes",
        "guides/beta/notes.md": "Beta/Notes",
    }


def test_the_segments_every_path_shares_are_dropped_before_the_run_is_measured() -> (
    None
):
    assert member_headings(["a/b/one.md", "a/b/c/one.md"], "b") == {
        "a/b/one.md": "One",
        "a/b/c/one.md": "C/One",
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
        "## Bare",
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
        "## Bare",
        "## Findings\n",
        "Held.\n",
    )


def test_members_holding_only_a_first_heading_take_no_overview() -> None:
    one = group_of(
        "notes",
        2,
        {
            "notes/bare.md": "# Bare\n\n## Findings\n\nHeld.\n",
            "notes/kept.md": "# Kept\n\n## Findings\n\nKept too.\n",
        },
    )
    assert "Overview" not in one.headings
    assert one.headings[:3] == ("Notes", "Bare", "Kept")


def test_a_member_carrying_content_above_the_depth_takes_the_overview() -> None:
    one = group_of(
        "notes",
        2,
        {
            "notes/bare.md": "# Bare\n\n## Findings\n\nHeld.\n",
            "notes/kept.md": "Read this first.\n\n## Findings\n\nKept too.\n",
        },
    )
    assert one.parts[:5] == (
        "# Notes",
        "## Overview",
        "### Bare",
        "### Kept",
        "Read this first.\n",
    )


@pytest.mark.parametrize("named", ["-", "_", "- _", "--"])
def test_a_member_whose_name_carries_no_word_takes_its_path_text(named: str) -> None:
    path = f"rules/{named}.md"
    names = member_headings([path, "rules/kept.md"], "rules")
    assert names == {path: f"Rules/{named}.md", "rules/kept.md": "Kept"}


def test_a_titled_parent_s_whole_document_reference_reaches_its_title() -> None:
    for depth, title in ((1, "Guide"), (2, "Guide"), (3, "Guide")):
        documents = {
            "rules/guide.md": "# Guide\n\nOpens.\n\n## Steps\n\n### Detail\n\nOne.\n",
            "rules/other.md": "# Other\n\n## Steps\n\nTwo.\n",
        }
        one = merged(
            "rules",
            depth,
            [
                prepared(
                    path,
                    parse(text),
                    lines(text),
                    {},
                    None,
                    None,
                    depth,
                    keep_title=path == "rules/guide.md",
                    conversions={},
                )
                for path, text in sorted(documents.items())
            ],
            "rules/guide.md",
        )
        assert answering(one, "rules/guide.md") == title, depth


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
            ["B/Notes", "C/Other"],
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


DECLARED = "---\nprosiform: {}\n---\n"


def paired(group: str, depth: int) -> str:
    """Frontmatter whose default preset pairs its document with one group."""
    return f"---\nprosiform:\n  default:\n    group: {{{group}: {depth}}}\n---\n"


def composed(
    root: Path, documents: Mapping[str, str], entry: str = "guide.md"
) -> tuple[int, str, list[dict[str, object]]]:
    """One run over a tree: its exit status, its entry bundle and its diagnostics."""
    for path, text in documents.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    out, err = StringIO(), StringIO()
    with TemporaryDirectory() as folder, chdir(root):
        status = main(["-o", folder, "-d", "json", "--entry", entry], out, err)
        written = sorted(Path(folder).glob("*.bundles/*.bundle.md"))
        bundle = written[0].read_text() if written else ""
    diagnostics = [json.loads(line) for line in err.getvalue().splitlines() if line]
    return status, bundle, diagnostics


def outline(bundle: str) -> list[str]:
    """Every heading line a bundle carries, in bundle order.

    The `§ Instructions` heading and the line beneath it are the run's own
    structure rather than a document's, so an outline of what the documents
    contribute leaves them out.
    """
    held = re.findall(r"^#+ .+$", bundle, re.MULTILINE)
    return [one for one in held if one != "# \u00a7 Instructions"]


def test_a_nested_group_moves_every_heading_down_one_level_per_division() -> None:
    documents = {
        "g/one.md": "Above.\n\n## Findings\n\nOne.\n",
        "g/two.md": "## Findings\n\nTwo.\n",
    }
    top = group_of("notes", 2, documents)
    nested = merged(
        "notes",
        2,
        [
            prepared(path, parse(text), lines(text), {}, None, None, 2, conversions={})
            for path, text in sorted(documents.items())
        ],
        at=3,
    )
    assert nested.level == 3
    assert [one.level for one in nested.record.headings] == [
        one.level + 2 for one in top.record.headings
    ]
    assert nested.headings == top.headings


def test_a_file_s_pair_places_its_own_sections(tmp_path: Path) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": paired("modes", 2)
            + "# Guide\n\nRead [the rules](rules.md).\n\n## Procedure\n\nGuide.\n",
            "rules.md": paired("rules", 2) + "# Rules\n\n## Procedure\n\nRules.\n",
        },
    )
    assert status == 0
    assert outline(bundle) == [
        "# Guide",
        "## Procedure",
        "## Rules",
        "### Rules",
        "### Procedure",
    ]
    assert bundle.index("Guide.") < bundle.index("## Rules") < bundle.index("Rules.")


def test_a_parent_s_pair_leaves_the_sections_it_links_alone(tmp_path: Path) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": paired("modes", 2)
            + "# Guide\n\nRead [the rules](rules.md).\n\n## Procedure\n\nGuide.\n",
            "rules.md": DECLARED + "# Rules\n\n## Procedure\n\nRules.\n",
        },
    )
    assert status == 0
    assert outline(bundle) == ["# Guide", "## Procedure", "# Rules", "## Procedure"]


def test_a_linked_file_is_composed_before_its_parent_merges_it(
    tmp_path: Path,
) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": DECLARED + "# Guide\n\nFollow [the steps](steps.md).\n",
            "steps.md": paired("steps", 2)
            + "# Steps\n\n## Run\n\nRun, then [check](checks.md).\n",
            "checks.md": paired("checks", 2) + "# Checks\n\n## Verify\n\nVerify.\n",
        },
    )
    assert status == 0
    assert outline(bundle) == [
        "# Guide",
        "## Steps",
        "### Steps",
        "### Run",
        "### Checks",
        "#### Checks",
        "#### Verify",
    ]


def test_an_intermediate_group_nests_inside_its_parent(tmp_path: Path) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": paired("guides", 2)
            + "# Guide\n\nRead [notes](notes.md) and [plain](plain.md).\n\n"
            "## Procedure\n\nWalk.\n",
            "notes.md": paired("notes", 2)
            + "# Notes\n\n## Findings\n\nHeld, as [extra](extra.md) says.\n",
            "plain.md": DECLARED + "# Plain\n\nPlain.\n",
            "extra.md": DECLARED + "# Extra\n\nExtra.\n",
        },
    )
    assert status == 0
    assert outline(bundle) == [
        "# Guide",
        "## Procedure",
        "## Notes",
        "### Notes",
        "### Findings",
        "# Plain",
        "# Extra",
    ]


def test_a_group_placed_by_a_document_in_two_groups_nests_in_the_first(
    tmp_path: Path,
) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": DECLARED
            + (
                '# Guide\n\n## Checks\n\nSee [rules](rules.md "checks").\n\n'
                '## Draft\n\nSee [rules](rules.md "draft").\n'
            ),
            "rules.md": "---\nprosiform:\n  Checks:\n    group: {reviews: 1}\n"
            "  Draft:\n    group: {drafts: 1}\n---\n"
            "# Rules\n\nTo [the leaf](leaf.md).\n",
            "leaf.md": paired("leaves", 2) + "# Leaf\n\n## Payload\n\nLeaf.\n",
        },
    )
    assert status == 0
    assert outline(bundle) == [
        "# Guide",
        "## Checks",
        "## Draft",
        "## Reviews",
        "### Rules",
        "### Leaves",
        "#### Leaf",
        "#### Payload",
        "## Drafts",
        "### Rules",
    ]
    assert bundle.count("Leaf.") == 1


def test_a_nested_heading_pushed_beyond_h6_fails(tmp_path: Path) -> None:
    status, bundle, diagnostics = composed(
        tmp_path,
        {
            "guide.md": DECLARED + "# Guide\n\nRead [deep](deep.md).\n",
            "deep.md": paired("deep", 1)
            + "# Deep\n\n## Two\n\n### Three\n\n#### Four\n\n##### Five\n\nDeep.\n",
        },
    )
    assert status == 1
    assert bundle == ""
    assert [one["code"] for one in diagnostics] == ["E_HEADING_DEPTH_OVERFLOW"]


def test_a_link_a_file_does_not_bundle_stays_its_content(tmp_path: Path) -> None:
    status, bundle, _ = composed(
        tmp_path,
        {
            "guide.md": DECLARED + "# Guide\n\nRead [the notes](notes.md).\n",
            "notes.md": paired("notes", 2) + "# Notes\n\n## Findings\n\n"
            "See [the draft](draft.md) and [the web](https://example.com/page).\n",
            "draft.md": "# Draft\n\nUndeclared.\n",
        },
    )
    assert status == 0
    assert (
        "### Findings\n\nSee [the draft](draft.md) and "
        "[the web](https://example.com/page).\n"
    ) in bundle
    assert "Undeclared." not in bundle
    assert outline(bundle) == ["# Guide", "## Notes", "### Notes", "### Findings"]
