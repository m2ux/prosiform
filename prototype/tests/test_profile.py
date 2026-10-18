"""Assert the parser supplies every clause of the declared profile.

`skill-markdown-v1` is CommonMark with pipe tables and double-tilde
strikethrough enabled, source task-list markers preserved as text,
typographic substitution disabled, and raw HTML recognized as a token of
its own so a run can refuse it. The build declares one parser because that
parser's `commonmark` preset supplies all five, and these tests hold the
pinned version to that claim.
"""

from importlib.metadata import version

from markdown_it import MarkdownIt

PARSER = "markdown-it-py"
PINNED_VERSION = "4.2.0"


def profile() -> MarkdownIt:
    """The parser configured as the declared profile."""
    return MarkdownIt("commonmark").enable(["table", "strikethrough"])


def test_parser_is_the_pinned_version() -> None:
    assert version(PARSER) == PINNED_VERSION


def test_pipe_tables_are_parsed() -> None:
    html = profile().render("| head | head |\n| --- | --- |\n| cell | cell |\n")
    assert "<table>" in html


def test_double_tilde_strikethrough_is_parsed() -> None:
    assert "<s>" in profile().render("~~struck~~\n")


def test_task_markers_stay_source_text() -> None:
    html = profile().render("- [ ] open\n- [x] done\n")
    assert "<input" not in html
    assert "[ ]" in html
    assert "[x]" in html


def test_typographic_substitution_is_off() -> None:
    html = profile().render('"quoted" -- dashed ...\n')
    assert "&quot;quoted&quot;" in html
    assert "--" in html
    assert "..." in html


def test_raw_html_is_a_token_of_its_own() -> None:
    assert [token.type for token in profile().parse("<div>raw</div>\n")] == [
        "html_block"
    ]
