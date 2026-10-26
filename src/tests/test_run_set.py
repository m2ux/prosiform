"""Assert a run-set target holds one bulleted list whose every item is a call.

Each case parses one target under the profile and reads its shape, with a
call being any link whose destination ends in a Markdown suffix, standing
in for the resolution a run performs from the target's own document.
"""

import pytest

from prosiform.profile import parse
from prosiform.run_set import EMPTY, UNLINKED, Stray, stray
from prosiform.source import regions


def calls(destination: str) -> bool:
    """Whether one destination names a Markdown document."""
    return destination.partition("#")[0].endswith(".md")


def shape(text: str) -> Stray | None:
    """The stray construct a whole-document target carries, if any."""
    tokens = parse(text)
    return stray(tokens, tuple(regions(tokens)), calls)


def test_a_bulleted_list_of_calls_below_the_heading_is_a_run_set() -> None:
    assert shape("# Reviews\n\n- [A](a.md)\n- Run [B](b.md#b) then report.\n") is None


def test_a_list_with_no_heading_above_it_is_a_run_set() -> None:
    assert shape("- [A](a.md)\n") is None


def test_nested_bulleted_items_each_carrying_a_call_are_a_run_set() -> None:
    text = "# R\n\n- [A](a.md)\n  - [B](b.md)\n    - [C](c.md)\n- [D](d.md)\n"
    assert shape(text) is None


def test_a_loose_item_of_two_paragraphs_carrying_a_call_is_a_run_set() -> None:
    assert shape("# R\n\n- [A](a.md)\n\n  Then report.\n\n- [B](b.md)\n") is None


@pytest.mark.parametrize(
    ("text", "held", "line"),
    [
        ("# R\n", EMPTY, None),
        ("# R\n\nProse.\n\n- [A](a.md)\n", "a paragraph", 3),
        ("# R\n\n1. [A](a.md)\n", "a numbered list", 3),
        ("# R\n\n- [A](a.md)\n\n```text\nx\n```\n", "a code block", 5),
        ("# R\n\n- [A](a.md)\n\n## More\n", "a heading", 5),
        ("# R\n\n- [A](a.md)\n\n* [B](b.md)\n", "a further bulleted list", 5),
        ("# R\n\n- [A](a.md)\n- Nothing.\n", UNLINKED, 4),
        ("# R\n\n- Group\n  - [A](a.md)\n", UNLINKED, 3),
        ("# R\n\n- [A](a.md)\n  1. [B](b.md)\n", "a numbered list", 4),
        ("# R\n\n- [A](a.md)\n  > [B](b.md)\n", "a block quote", 4),
        ("# R\n\n- ![A](a.png)\n", UNLINKED, 3),
        ("# R\n\n- [A](a.txt)\n", UNLINKED, 3),
    ],
)
def test_anything_but_calls_in_one_bulleted_list_is_stray(
    text: str, held: str, line: int | None
) -> None:
    assert shape(text) == Stray(held, line)
