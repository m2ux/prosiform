"""Assert a link is a composition directive exactly where the design declares one.

A directive is a link whose label, read as plain text once entities are
decoded and the deferral mark set aside, is one Unicode scalar above
U+007F that is no whitespace, control or format scalar. Each case is
written as Markdown and read through the source reader, so the label a
case judges is the label the parser produced: an entity, an emphasis or
a reference form arrives as the build reads it rather than as a test
spells it.

Deferral is read apart from recognition, so each deferred case is
paired with what the deferral alone states.
"""

import pytest

from prosiform.closure import deferred, directive, dispatched, gapped
from prosiform.profile import parse
from prosiform.source import Use, regions, uses


def first(text: str) -> Use:
    """The first reference use one document carries."""
    tokens = parse(text)
    return next(uses(tokens, list(regions(tokens))))


@pytest.mark.parametrize(
    "written",
    [
        "[→](a.md#out)",
        "[é](a.md#out)",
        "[&rarr;](a.md#out)",
        "[&#x2192;](a.md#out)",
        "[&#8594;](a.md#out)",
        "[𝔸](a.md#out)",
        "[&#x1D538;](a.md#out)",
        '[→](a.md#out "a title")',
        "[→]\n\n[→]: a.md#out",
        "[→][]\n\n[→]: a.md#out",
        "[→][out]\n\n[out]: a.md#out",
    ],
    ids=[
        "an arrow",
        "a precomposed letter",
        "a named entity",
        "a hexadecimal reference",
        "a decimal reference",
        "a supplementary scalar",
        "a supplementary scalar reference",
        "a titled link",
        "a shortcut reference",
        "a collapsed reference",
        "a full reference",
    ],
)
def test_a_label_of_one_scalar_above_ascii_is_a_directive(written: str) -> None:
    assert directive(first(written).label)


@pytest.mark.parametrize(
    "written",
    [
        "[A](a.md#out)",
        "[&amp;](a.md#out)",
        "[\\*](a.md#out)",
        "[ → ](a.md#out)",
        "[→ ](a.md#out)",
        "[ →](a.md#out)",
        "[*→*](a.md#out)",
        "[**→**](a.md#out)",
        "[`→`](a.md#out)",
        "[~~→~~](a.md#out)",
        "[→\\\n](a.md#out)",
        "[<b>→</b>](a.md#out)",
        "[![→](p.png)](a.md#out)",
        "[↓↑](a.md#out)",
        "[é](a.md#out)",
        "[☺️](a.md#out)",
        "[👩‍💻](a.md#out)",
        "[🇬🇧](a.md#out)",
        "[x][→]\n\n[→]: a.md#out",
        "[ ](a.md#out)",
        "[&nbsp;](a.md#out)",
        "[　](a.md#out)",
        "[\x85](a.md#out)",
        "[​](a.md#out)",
        "[&#xAD;](a.md#out)",
        "[&#xFEFF;](a.md#out)",
    ],
    ids=[
        "an ascii letter",
        "an entity decoding to ascii",
        "an escaped ascii mark",
        "a scalar between spaces",
        "a trailing space",
        "a leading space",
        "an emphasis",
        "a strong emphasis",
        "a code span",
        "a strikethrough",
        "a hard line break",
        "raw html",
        "an image inside the label",
        "two scalars",
        "a combining sequence",
        "a variation selector sequence",
        "a joined emoji",
        "a flag of two scalars",
        "a full reference whose own text is ascii",
        "a no-break space",
        "a no-break space entity",
        "an ideographic space",
        "a next-line control",
        "a zero-width space",
        "a soft hyphen",
        "a byte order mark",
    ],
)
def test_a_label_that_is_not_one_plain_scalar_is_no_directive(written: str) -> None:
    assert not directive(first(written).label)


@pytest.mark.parametrize(
    "written",
    [
        "![→](a.md#out)",
        "<https://example.com/→>",
        "`[→](a.md#out)`",
    ],
    ids=["an image", "an autolink", "a link inside code"],
)
def test_a_use_written_no_label_is_no_directive(written: str) -> None:
    tokens = parse(written)
    assert not any(directive(one.label) for one in uses(tokens, list(regions(tokens))))


def test_bracketed_text_the_parser_leaves_unresolved_is_no_use() -> None:
    tokens = parse("[→] names no definition.\n")
    assert list(uses(tokens, list(regions(tokens)))) == []


@pytest.mark.parametrize(
    "written",
    ["[¬](a.md#out)", "[↳](a.md#out)", "[⇉](a.md#out)", "[⫽](a.md#out)"],
    ids=[
        "the deferral mark",
        "the inline mark",
        "the dispatch mark",
        "the parallel mark",
    ],
)
def test_a_lone_operator_or_convention_mark_is_no_directive(written: str) -> None:
    assert not directive(first(written).label)


@pytest.mark.parametrize(
    "written",
    ["[¬→](a.md#out)", "[¬&rarr;](a.md#out)", "[¬𝔸](a.md#out)"],
    ids=["an arrow", "an entity", "a supplementary scalar"],
)
def test_a_glyph_the_deferral_mark_is_written_against_is_a_deferred_directive(
    written: str,
) -> None:
    use = first(written)
    assert directive(use.label)
    assert deferred(use.opening)
    assert not gapped(use.opening, use.label)


def test_an_ordinary_deferred_label_is_a_deferral_and_no_directive() -> None:
    use = first("[¬ the rules](a.md#out)")
    assert deferred(use.opening)
    assert not directive(use.label)
    assert not gapped(use.opening, use.label)


def test_an_immediate_glyph_is_a_directive_and_no_deferral() -> None:
    use = first("[→](a.md#out)")
    assert directive(use.label)
    assert not deferred(use.opening)


@pytest.mark.parametrize(
    "written",
    [
        "[¬ →](a.md#out)",
        "[¬  →](a.md#out)",
        "[¬ &rarr;](a.md#out)",
        "[⇉ →](a.md#out)",
        "[⫽ →](a.md#out)",
        "[¬⇉ →](a.md#out)",
    ],
    ids=[
        "a deferral and one blank",
        "a deferral and two blanks",
        "a deferral and an entity",
        "a dispatch",
        "a parallel dispatch",
        "a deferred dispatch",
    ],
)
def test_a_blank_between_a_mark_and_a_glyph_is_refused_and_no_directive(
    written: str,
) -> None:
    use = first(written)
    assert gapped(use.opening, use.label)
    assert not directive(use.label)


@pytest.mark.parametrize(
    "written",
    ["[¬¬](a.md#out)", "[¬↳](a.md#out)", "[¬ ↳](a.md#out)", "[¬→ ](a.md#out)"],
    ids=[
        "a doubled deferral mark",
        "an inline mark written against the deferral mark",
        "a deferred inline mark",
        "a deferred glyph and a trailing space",
    ],
)
def test_a_deferral_mark_beside_no_qualifying_label_is_no_directive(
    written: str,
) -> None:
    use = first(written)
    assert not directive(use.label)
    assert not gapped(use.opening, use.label)


@pytest.mark.parametrize(
    "written",
    ["[⇉→](a.md#out)", "[⫽→](a.md#out)", "[ ¬→](a.md#out)"],
    ids=[
        "a dispatch mark written against a glyph",
        "a parallel mark written against a glyph",
        "a deferred glyph after a blank",
    ],
)
def test_a_mark_written_against_a_glyph_it_cannot_defer_is_text(written: str) -> None:
    use = first(written)
    assert not directive(use.label)
    assert not deferred(use.opening)
    assert not dispatched(use.opening)
