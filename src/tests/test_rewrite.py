"""Assert source-local reference interpretation: what the bundle writes where.

The corpus declares what a run publishes. These are the cases beneath
it: the extents a code span masks, the definition environment a source
declares, the uses that environment resolves, the inline form a
reference-style use is published as, the bytes a deferred link keeps,
the line each published entry answers to, and the refusal content the
emission cannot edit raises.
"""

from typing import Any

import pytest
from markdown_it.token import Token

from prosiform.profile import REFERENCES, parse
from prosiform.rewrite import (
    Definition,
    Unrewritable,
    code_spans,
    definitions,
    destinations,
    rewritten,
    uses,
)
from prosiform.source import INLINE, lines


def read(text: str) -> tuple[Token, dict[str, Definition]]:
    """The first inline token one source carries, and the definitions it declares."""
    environment: dict[str, Any] = {}
    tokens = parse(text, env=environment)
    inline = next(token for token in tokens if token.type == INLINE)
    return inline, definitions(environment.get(REFERENCES, {}), lines(text))


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
        ("[rules](rules.md)", [((1, 6), (8, 16))]),
        ("`[¬ rules](rules.md)`", []),
        ("![picture](plan.png)", [((2, 9), (11, 19))]),
        (r"\[¬ rules](rules.md)", []),
        ('[¬ rules](rules.md "A title")', [((1, 8), (10, 18))]),
        ("[¬ rules](<rules.md>)", [((1, 8), (10, 20))]),
        ("[¬ a](a.md) and [¬ b](b.md)", [((1, 4), (6, 10)), ((17, 20), (22, 26))]),
    ],
)
def test_an_inline_use_is_the_spans_the_text_carries(
    text: str, expected: list[tuple[tuple[int, int], tuple[int, int]]]
) -> None:
    assert [(one.label, one.target) for one in uses(text, {})] == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("[rules]: rules.md\n", {"RULES": ("rules.md", "", (0, 1))}),
        (
            '[rules]: rules.md "The Rules"\n',
            {"RULES": ("rules.md", '"The Rules"', (0, 1))},
        ),
        ("[a b]: <my doc.md>\n", {"A B": ("<my doc.md>", "", (0, 1))}),
        ("> [q]: q.md\n", {"Q": ("q.md", "", (0, 1))}),
        ("[rules]: rules.md", {"RULES": ("rules.md", "", (0, 1))}),
    ],
)
def test_a_definition_is_read_as_its_source_spelled_it(
    text: str, expected: dict[str, tuple[str, str, tuple[int, int]]]
) -> None:
    environment: dict[str, Any] = {}
    parse(text, env=environment)
    found = definitions(environment.get(REFERENCES, {}), lines(text))
    assert {
        label: (one.destination, one.title, one.lines) for label, one in found.items()
    } == expected


@pytest.mark.parametrize(
    ("text", "assigned", "expected"),
    [
        ("[rules](rules.md)", ["#rules"], "[rules](#rules)"),
        ("[¬ rules](../rules.md)", ["topic/rules.md"], "[¬ rules](topic/rules.md)"),
        ("[¬rules](rules.md#a)", [None], "[¬rules](rules.md#a)"),
        (
            '[rules](rules.md "A title")',
            ["#rules"],
            '[rules](#rules "A title")',
        ),
        (
            "A `[draft](draft.md)` example beside [rules](rules.md).",
            ["#rules"],
            "A `[draft](draft.md)` example beside [rules](#rules).",
        ),
        (
            "[a](a.md) and [b](b.md)",
            ["#a", "#b"],
            "[a](#a) and [b](#b)",
        ),
        ("[rules](../rules.md)", [None], "[rules](../rules.md)"),
        ("[¬ rules](../rules.md)", [None], "[¬ rules](../rules.md)"),
        ("nothing to rewrite", [], "nothing to rewrite"),
    ],
)
def test_a_compiled_link_is_written_to_its_destination(
    text: str, assigned: list[str | None], expected: str
) -> None:
    assert "".join(rewritten(lines(text), inline_of(text), assigned, {})) == expected


@pytest.mark.parametrize(
    ("body", "definition", "assigned", "expected"),
    [
        (
            "A [full][rules] use.",
            "[rules]: rules.md\n",
            [None],
            "A [full](rules.md) use.",
        ),
        (
            "A [rules][] use.",
            "[rules]: rules.md\n",
            [None],
            "A [rules](rules.md) use.",
        ),
        ("A [rules] use.", "[rules]: rules.md\n", [None], "A [rules](rules.md) use."),
        (
            "A [full][rules] use.",
            '[rules]: rules.md "The Rules"\n',
            [None],
            'A [full](rules.md "The Rules") use.',
        ),
        (
            "A [¬ full][rules] use.",
            '[rules]: rules.md "The Rules"\n',
            [None],
            'A [¬ full](rules.md "The Rules") use.',
        ),
        (
            "A ![diagram][plan] use.",
            "[plan]: pics/plan.png\n",
            [],
            "A ![diagram](pics/plan.png) use.",
        ),
        (
            "A [RULES][] use spelled another way.",
            "[rules]: rules.md\n",
            [None],
            "A [RULES](rules.md) use spelled another way.",
        ),
        (
            "A [literal] bracket.",
            "[other]: other.md\n",
            [],
            "A [literal] bracket.",
        ),
        (
            "An example `[rules]` of one.",
            "[rules]: rules.md\n",
            [],
            "An example `[rules]` of one.",
        ),
        (
            "An escaped \\[rules] bracket.",
            "[rules]: rules.md\n",
            [],
            "An escaped \\[rules] bracket.",
        ),
        (
            "A [link ![diagram][plan] inside][rules] use.",
            "[rules]: rules.md\n[plan]: pics/plan.png\n",
            [None],
            "A [link ![diagram](pics/plan.png) inside](rules.md) use.",
        ),
    ],
)
def test_a_resolved_reference_style_use_is_published_inline(
    body: str, definition: str, assigned: list[str | None], expected: str
) -> None:
    inline, defined = read(f"{body}\n\n{definition}")
    assert "".join(rewritten(lines(body), inline, assigned, defined)) == expected


def test_a_definition_of_one_source_resolves_no_other_source_brackets() -> None:
    text = "A [runner] bracket."
    inline, defined = read(f"{text}\n")
    assert defined == {}
    assert "".join(rewritten(lines(text), inline, [], defined)) == text


def test_a_task_marker_a_definition_spells_is_no_use() -> None:
    text = "- [x] done\n\n[x]: page.md\n"
    environment: dict[str, Any] = {}
    tokens = parse(text, env=environment)
    defined = definitions(environment.get(REFERENCES, {}), lines(text))
    inline = next(token for token in tokens if token.type == INLINE)
    assert rewritten(["- [x] done\n"], inline, [], defined) == ["- [x] done\n"]


def test_a_link_the_emission_cannot_edit_is_refused() -> None:
    text = "`[¬ rules](rules.md)`"
    with pytest.raises(Unrewritable):
        rewritten(lines(text), inline_of(text), ["#rules"], {})


def test_a_rewrite_reports_one_entry_for_each_line_it_was_given() -> None:
    text = "The procedure requires\n[the shared rules](rules.md) whole.\n"
    written = rewritten(lines(text), inline_of(text), ["#rules"], {})
    assert written == [
        "The procedure requires\n",
        "[the shared rules](#rules) whole.\n",
    ]


def test_a_definition_spelled_across_two_lines_is_published_as_authored() -> None:
    body = "A [full][rules] use.\n"
    definition = '[rules]:\n  rules.md\n  "The Rules,\nwritten out"\n'
    inline, defined = read(f"{body}\n{definition}")
    assert rewritten(lines(body), inline, [None], defined) == [
        'A [full](rules.md "The Rules,\nwritten out") use.\n'
    ]


def test_a_compiled_use_of_such_a_definition_takes_its_assigned_destination() -> None:
    body = "A [full][rules] use.\n"
    definition = '[rules]:\n  rules.md\n  "The Rules,\nwritten out"\n'
    inline, defined = read(f"{body}\n{definition}")
    assert rewritten(lines(body), inline, ["#rules"], defined) == [
        'A [full](#rules "The Rules,\nwritten out") use.\n'
    ]


def test_a_line_break_a_replacement_swallows_ends_the_entry_that_held_it() -> None:
    body = "A [full][\nrules] use.\n"
    definition = "[rules]: rules.md\n"
    inline, defined = read(f"{body}\n{definition}")
    written = rewritten(lines(body), inline, [None], defined)
    assert len(written) == 2
    assert "".join(written) == "A [full](rules.md) use.\n"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("The procedure requires [rules](rules.md).", [("rules.md", "rules")]),
        ("The procedure defers [¬ rules](rules.md).", [("rules.md", "¬ rules")]),
        ("A fragment [alpha](#alpha) of its own.", [("#alpha", "alpha")]),
        ("An example `[draft](draft.md)` of one.", []),
        ("A picture ![of it](plan.png) names no link.", []),
    ],
)
def test_the_parser_names_each_link_a_token_carries(
    text: str, expected: list[tuple[str, str]]
) -> None:
    assert destinations(inline_of(text)) == expected
