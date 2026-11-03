"""Assert a link is a composition directive exactly where the design declares one.

A directive is a link whose text opens with the composition mark `↳` and a
space, alone or after the deferral mark; a link labelled with one Unicode
arrow is refused. Each case is written as Markdown and read through the
source reader, so the text a case judges is the text the parser produced:
an entity, an emphasis or a reference form arrives as the build reads it
rather than as a test spells it.

Deferral is read apart from recognition, so each deferred case is paired
with what the deferral alone states.
"""

import pytest

from prosiform.closure import (
    arrowed,
    conflicting,
    contradicting,
    deferred,
    deferring_dispatch,
    directive,
    gapped,
)
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
        "[⟶](a.md#out)",
        "[⤴](a.md#out)",
        "[➔](a.md#out)",
        "[⬅](a.md#out)",
        "[&rarr;](a.md#out)",
        "[&#x2192;](a.md#out)",
        "[&#8594;](a.md#out)",
        "[🡒](a.md#out)",
        "[&#x1F852;](a.md#out)",
        '[→](a.md#out "a title")',
        "[→]\n\n[→]: a.md#out",
        "[→][]\n\n[→]: a.md#out",
        "[→][out]\n\n[out]: a.md#out",
    ],
    ids=[
        "an arrow",
        "a supplemental arrows-a arrow",
        "a supplemental arrows-b arrow",
        "a dingbat arrow",
        "a miscellaneous symbols and arrows arrow",
        "a named entity",
        "a hexadecimal reference",
        "a decimal reference",
        "a supplementary arrow",
        "a supplementary arrow reference",
        "a titled link",
        "a shortcut reference",
        "a collapsed reference",
        "a full reference",
    ],
)
def test_a_label_of_one_arrow_is_an_arrow_label(written: str) -> None:
    label = first(written).label
    assert label is not None
    assert arrowed(label)


@pytest.mark.parametrize(
    "written",
    [
        "[A](a.md#out)",
        "[†](a.md#out)",
        "[‡](a.md#out)",
        "[&dagger;](a.md#out)",
        "[¹](a.md#out)",
        "[é](a.md#out)",
        "[𝔸](a.md#out)",
        "[&#x1D538;](a.md#out)",
        "[٣](a.md#out)",
        "[★](a.md#out)",
        "[⬒](a.md#out)",
        "[➤](a.md#out)",
        "[&#x1F80C;](a.md#out)",
        "[¬†](a.md#out)",
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
        "a footnote dagger",
        "a footnote double dagger",
        "a footnote dagger entity",
        "a superscript",
        "a precomposed letter",
        "a supplementary letter",
        "a supplementary letter reference",
        "a non-ascii digit",
        "a star",
        "a symbol of an arrows block named for no arrow",
        "a dingbat arrowhead",
        "an unassigned scalar of an arrows block",
        "the deferral mark against a footnote mark",
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
def test_a_label_that_is_not_one_plain_arrow_is_no_arrow_label(written: str) -> None:
    label = first(written).label
    assert label is None or not arrowed(label)


@pytest.mark.parametrize(
    "written",
    [
        "[↳ Inputs](a.md#out)",
        "[↳  Inputs](a.md#out)",
        '[↳ Inputs](a.md#out "a title")',
        "[↳ Inputs]\n\n[↳ Inputs]: a.md#out",
        "[↳ Inputs][]\n\n[↳ Inputs]: a.md#out",
        "[↳ Inputs][out]\n\n[out]: a.md#out",
        "[↳ *Inputs*](a.md#out)",
    ],
    ids=[
        "an inline link",
        "two blanks",
        "a titled link",
        "a shortcut reference",
        "a collapsed reference",
        "a full reference",
        "a formatted title",
    ],
)
def test_a_text_opening_with_the_composition_mark_is_a_directive(written: str) -> None:
    use = first(written)
    assert directive(use.opening)
    assert not deferred(use.opening)
    assert not gapped(use.opening)


@pytest.mark.parametrize(
    "written",
    [
        "[↳Inputs](a.md#out)",
        "[↳](a.md#out)",
        "[the ↳ Inputs](a.md#out)",
        "[*↳* Inputs](a.md#out)",
        "[`↳` Inputs](a.md#out)",
        "[¬ Inputs](a.md#out)",
        "[⇉ Inputs](a.md#out)",
        "[⫽ Inputs](a.md#out)",
        "[Inputs](a.md#out)",
    ],
    ids=[
        "a mark and no blank",
        "a lone mark",
        "a mark inside the text",
        "an emphasised mark",
        "a code span mark",
        "the deferral mark",
        "the dispatch mark",
        "the parallel mark",
        "no mark",
    ],
)
def test_a_text_not_opening_with_the_composition_mark_is_no_directive(
    written: str,
) -> None:
    assert not directive(first(written).opening)


@pytest.mark.parametrize(
    "written",
    [
        "![↳ Inputs](a.md#out)",
        "<https://example.com/↳>",
        "`[↳ Inputs](a.md#out)`",
    ],
    ids=["an image", "an autolink", "a link inside code"],
)
def test_a_use_written_as_no_link_is_no_directive(written: str) -> None:
    tokens = parse(written)
    found = [
        one
        for one in uses(tokens, list(regions(tokens)))
        if not one.resource and directive(one.opening)
    ]
    assert found == []


def test_bracketed_text_the_parser_leaves_unresolved_is_no_use() -> None:
    tokens = parse("[↳ Inputs] names no definition.\n")
    assert list(uses(tokens, list(regions(tokens)))) == []


@pytest.mark.parametrize(
    "written",
    ["[¬](a.md#out)", "[↳](a.md#out)", "[⇉](a.md#out)", "[⫽](a.md#out)"],
    ids=[
        "the deferral mark",
        "the composition mark",
        "the dispatch mark",
        "the parallel mark",
    ],
)
def test_a_lone_mark_is_no_directive_and_no_arrow_label(written: str) -> None:
    use = first(written)
    assert not directive(use.opening)
    assert use.label is not None
    assert not arrowed(use.label)


def test_the_deferral_mark_against_the_composition_mark_defers_a_directive() -> None:
    use = first("[¬↳ Inputs](a.md#out)")
    assert directive(use.opening)
    assert deferred(use.opening)
    assert not gapped(use.opening)
    assert not conflicting(use.opening)


def test_an_ordinary_deferred_label_is_a_deferral_and_no_directive() -> None:
    use = first("[¬ the rules](a.md#out)")
    assert deferred(use.opening)
    assert not directive(use.opening)
    assert not gapped(use.opening)


@pytest.mark.parametrize(
    "written",
    ["[¬ ↳ Inputs](a.md#out)", "[¬  ↳ Inputs](a.md#out)", "[↳ ¬ Inputs](a.md#out)"],
    ids=["one blank", "two blanks", "a deferral after the mark"],
)
def test_a_blank_between_two_marks_is_refused_and_no_directive(written: str) -> None:
    use = first(written)
    assert gapped(use.opening)
    assert not (directive(use.opening) and deferred(use.opening))


@pytest.mark.parametrize(
    "written",
    ["[¬¬](a.md#out)", "[¬↳](a.md#out)", "[¬ ↳](a.md#out)", "[¬→ ](a.md#out)"],
    ids=[
        "a doubled deferral mark",
        "the composition mark written against the deferral mark",
        "a deferred composition mark with no text",
        "a deferral written against an arrow and a blank",
    ],
)
def test_a_deferral_mark_beside_no_text_is_no_directive(written: str) -> None:
    use = first(written)
    assert not directive(use.opening)


@pytest.mark.parametrize(
    "written",
    ["[⇉↳ Inputs](a.md#out)", "[⫽↳ Inputs](a.md#out)", "[¬⇉↳ Inputs](a.md#out)"],
    ids=["a dispatch mark", "a parallel mark", "a deferred dispatch mark"],
)
def test_a_dispatch_mark_written_against_the_composition_mark_is_refused(
    written: str,
) -> None:
    use = first(written)
    assert contradicting(use.opening)
    assert conflicting(use.opening)
    assert not gapped(use.opening)


@pytest.mark.parametrize(
    "written",
    ["[¬⇉ the rules](a.md#out)", "[¬⫽ the rules](a.md#out)"],
    ids=["a dispatch", "a parallel dispatch"],
)
def test_the_deferral_mark_written_against_a_dispatch_mark_is_refused(
    written: str,
) -> None:
    use = first(written)
    assert deferring_dispatch(use.opening)
    assert conflicting(use.opening)
    assert not contradicting(use.opening)


@pytest.mark.parametrize(
    "written",
    [
        "[¬ →](a.md#out)",
        "[¬→](a.md#out)",
        "[⇉ →](a.md#out)",
        "[⫽→](a.md#out)",
        "[⇉&rarr;](a.md#out)",
        "[⇉🡒](a.md#out)",
    ],
    ids=[
        "a deferral and a blank",
        "a deferral",
        "a dispatch and a blank",
        "a parallel mark",
        "a dispatch mark and an entity",
        "a dispatch mark and a supplementary arrow",
    ],
)
def test_an_arrow_label_beside_marks_is_an_arrow_label_and_no_directive(
    written: str,
) -> None:
    use = first(written)
    assert use.label is not None
    assert arrowed(use.label)
    assert not directive(use.opening)
