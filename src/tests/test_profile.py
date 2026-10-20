"""Assert the build's configured parser supplies every clause of the profile.

`skill-markdown-v1` is CommonMark with pipe tables and double-tilde
strikethrough enabled, source task-list markers preserved as text,
typographic substitution disabled, and raw HTML recognized as a token of
its own so a run can refuse it. Each clause here names the configuration
that enforces it, so a parser version or a preset that stopped supplying
one fails against the profile rather than against a description of it.

The recognition clause carries both its directions. A construct naming a
dependency or a section fails; the prose, the code span and the escape
that resemble one pass untouched. A rule only ever observed firing is a
rule whose other half nobody tested.
"""

from importlib.metadata import version

import pytest

from prosiform.limits import NESTING
from prosiform.profile import is_markdown, parse, parser, refusals

PARSER = "markdown-it-py"
PINNED_VERSION = "4.2.0"

LINK_OPEN = "link_open"


def render(text: str) -> str:
    """One source rendered by the parser the profile configures."""
    return str(parser(NESTING.default).render(text))


def links(text: str) -> list[str]:
    """Every link the profile's parse carries, as its destination."""
    found: list[str] = []
    for token in parse(text):
        for child in token.children or []:
            if child.type == LINK_OPEN:
                found.append(str(child.attrGet("href")))
    return found


def messages(text: str) -> list[str]:
    """Every refusal the profile returns for one source."""
    return [refusal.message for refusal in refusals(parse(text))]


def test_parser_is_the_pinned_version() -> None:
    assert version(PARSER) == PINNED_VERSION


def test_pipe_tables_are_parsed() -> None:
    html = render("| head | head |\n| --- | --- |\n| cell | cell |\n")
    assert "<table>" in html


def test_double_tilde_strikethrough_is_parsed() -> None:
    assert "<s>" in render("~~struck~~\n")


def test_task_markers_stay_source_text() -> None:
    html = render("- [ ] open\n- [x] done\n- [X] done\n")
    assert "<input" not in html
    assert "[ ]" in html
    assert "[x]" in html
    assert "[X]" in html


def test_typographic_substitution_is_off() -> None:
    html = render('"quoted" -- dashed ... (c)\n')
    assert "&quot;quoted&quot;" in html
    assert "--" in html
    assert "..." in html
    assert "(c)" in html


def test_raw_html_is_a_token_of_its_own() -> None:
    assert [token.type for token in parse("<div>raw</div>\n")] == ["html_block"]


@pytest.mark.parametrize("marker", ["[x]", "[X]"])
def test_a_definition_cannot_turn_a_task_marker_into_a_link(marker: str) -> None:
    source = f"- {marker} done\n\n{marker}: page.md\n"
    assert links(source) == []
    assert marker in parse(source)[3].content


def test_a_bracketed_label_that_is_no_task_marker_still_resolves() -> None:
    assert links("A [x] in prose.\n\n[x]: page.md\n") == ["page.md"]
    assert links("- text and [x] after it\n\n[x]: page.md\n") == ["page.md"]


@pytest.mark.parametrize(
    "name",
    ["guide.md", "guide.markdown", "GUIDE.MD", "docs/Guide.Markdown"],
)
def test_a_markdown_suffix_is_classified_case_insensitively(name: str) -> None:
    assert is_markdown(name)


@pytest.mark.parametrize("name", ["guide.txt", "guide.mdx", "guide", "guide.md.bak"])
def test_a_suffix_outside_the_profile_is_not_markdown(name: str) -> None:
    assert not is_markdown(name)


@pytest.mark.parametrize(
    "source",
    [
        "<div>raw</div>\n",
        "a paragraph carrying <span>raw</span> markup\n",
        "<!-- a comment -->\n",
        "See [[page]] for the procedure.\n",
        "![[page]]\n",
        "A claim[^1] needing support.\n",
        "[^1]: the note\n",
        "## Title {#custom-id}\n",
        "| head |\n| --- |\n| [[page]] |\n",
        "> See [[page]] for the procedure.\n",
    ],
)
def test_a_recognized_construct_is_refused(source: str) -> None:
    assert len(messages(source)) == 1


@pytest.mark.parametrize(
    "source",
    [
        "A code span naming `[[page]]` is prose about a wiki link.\n",
        "An escaped \\[\\[page\\]\\] is literal text.\n",
        "A paragraph mentioning {#custom-id} names no section.\n",
        "## Title with {#custom-id} in the middle of it\n",
        "```\n[[page]]\n<div>raw</div>\n[^1]: the note\n```\n",
        "    [[page]]\n",
        "A regular expression `[^abc]` matches one character.\n",
        "An autolink <https://example.com> is a link, not markup.\n",
        "A [link](page.md) and an ![image](logo.png).\n",
        "- [ ] open\n- [x] done\n",
    ],
)
def test_prose_resembling_a_construct_passes_untouched(source: str) -> None:
    assert messages(source) == []


def test_a_refusal_names_the_line_and_the_spelling_it_found() -> None:
    found = list(refusals(parse("# Guide\n\nSee [[page]] here.\n")))
    assert len(found) == 1
    assert found[0].line == 3
    assert found[0].reference == "[[page]]"
