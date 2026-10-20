"""Assert the rewrite: where a marked link sits, and what the bundle writes there.

The corpus declares what a run publishes. These are the cases beneath
it: the extents a code span masks, the spans one marked link occupies,
the text the mark leaves behind, and the refusal a link the emission
cannot edit raises.
"""

import pytest
from markdown_it.token import Token

from prosiform.profile import parse
from prosiform.rewrite import (
    Unrewritable,
    code_spans,
    destinations,
    rewritten,
    sites,
    unmarked,
)
from prosiform.source import INLINE


def inline_of(text: str) -> Token:
    """The first inline token one source carries."""
    return next(token for token in parse(text) if token.type == INLINE)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("plain text", []),
        ("a `span` here", [(2, 8)]),
        ("a ``span with ` inside`` here", [(2, 24)]),
        ("one `a` two `b`", [(4, 7), (12, 15)]),
        ("an unclosed `run of text", []),
        (r"an escaped \`backtick\` pair", []),
    ],
)
def test_code_spans_are_the_extents_the_profile_reads(
    text: str, expected: list[tuple[int, int]]
) -> None:
    assert code_spans(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("[¬ rules](rules.md)", [((1, 8), (10, 18))]),
        ("[¬rules](rules.md)", [((1, 7), (9, 17))]),
        ("[rules](rules.md)", []),
        ("`[¬ rules](rules.md)`", []),
        ("![¬ picture](plan.png)", []),
        (r"\[¬ rules](rules.md)", []),
        ('[¬ rules](rules.md "A title")', [((1, 8), (10, 18))]),
        ("[¬ rules](<rules.md>)", [((1, 8), (10, 20))]),
        ("[¬ a](a.md) and [¬ b](b.md)", [((1, 4), (6, 10)), ((17, 20), (22, 26))]),
    ],
)
def test_sites_are_the_marked_links_the_text_carries(
    text: str, expected: list[tuple[tuple[int, int], tuple[int, int]]]
) -> None:
    assert [(one.label, one.target) for one in sites(text)] == expected


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("¬ the rules", "the rules"),
        ("¬the rules", "the rules"),
        ("¬\tthe rules", "the rules"),
        ("the rules", "the rules"),
        ("¬", ""),
    ],
)
def test_the_mark_leaves_the_text_that_followed_it(label: str, expected: str) -> None:
    assert unmarked(label) == expected


@pytest.mark.parametrize(
    ("text", "assigned", "expected"),
    [
        ("[¬ rules](rules.md)", ["rules"], "[rules](#rules)"),
        ("[¬rules](rules.md#a)", ["a"], "[rules](#a)"),
        (
            '[¬ rules](rules.md "A title")',
            ["rules"],
            '[rules](#rules "A title")',
        ),
        (
            "A `[¬ draft](draft.md)` example beside [¬ rules](rules.md).",
            ["rules"],
            "A `[¬ draft](draft.md)` example beside [rules](#rules).",
        ),
        (
            "[¬ a](a.md) and [¬ b](b.md)",
            ["a", "b"],
            "[a](#a) and [b](#b)",
        ),
        ("nothing to rewrite", [], "nothing to rewrite"),
    ],
)
def test_a_marked_link_is_written_to_its_destination(
    text: str, assigned: list[str], expected: str
) -> None:
    assert rewritten(text, assigned) == expected


def test_a_link_the_emission_cannot_edit_is_refused() -> None:
    with pytest.raises(Unrewritable):
        rewritten("`[¬ rules](rules.md)`", ["rules"])


def test_a_rewrite_writes_no_line_break_into_the_text() -> None:
    text = "The procedure requires\n[¬ the shared rules](rules.md) whole.\n"
    assert rewritten(text, ["rules"]).count("\n") == text.count("\n")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("The procedure requires [¬ rules](rules.md).", ["rules.md"]),
        ("The procedure cites [rules](rules.md).", []),
        ("A fragment [¬ alpha](#alpha) of its own.", ["#alpha"]),
        ("An example `[¬ draft](draft.md)` of one.", []),
    ],
)
def test_the_parser_names_each_marked_link_a_token_carries(
    text: str, expected: list[str]
) -> None:
    assert destinations(inline_of(text)) == expected
