"""Assert the bundle's structure: its file groups and how they join.

The corpus declares what a run publishes. These are the cases beneath
it: the heading one path generates, the escaping that keeps that heading
literal, the regions a selection carries into a group, the headings a
partial selection needs above it, and the two decisions a group makes
about its own headings, and the Prosiform section a dispatching bundle
opens with.
"""

import json
import re
from collections.abc import Mapping
from contextlib import chdir
from io import StringIO
from pathlib import Path

import pytest

from prosiform.bundle import (
    MAX_LEVEL,
    Group,
    Overflow,
    absorbed,
    assemble,
    escaped,
    group,
    heading_text,
    openings,
    rewrite,
    title_cased,
)
from prosiform.cli import INPUT_FAILURE, SUCCESS, main
from prosiform.dispatch import (
    DISPATCH_PROTOCOL,
    HEADING_COLLISION,
    PARALLEL_PROTOCOL,
)
from prosiform.profile import parse
from prosiform.provenance import STRUCTURAL_ANCESTOR, Origin
from prosiform.source import Selection, lines, regions, section


def grouped(path: str, text: str) -> Group:
    """One file group, from the path that names it and the source it carries."""
    return group(path, parse(text), lines(text))


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("guide", "Guide"),
        ("docs/note", "Docs/Note"),
        ("docs/sub/note", "Docs/Sub/Note"),
        ("my-note", "My-Note"),
        ("docs/field-notes", "Docs/Field-Notes"),
        ("plan_mode", "Plan_Mode"),
        ("two words", "Two Words"),
        ("Already Titled", "Already Titled"),
        ("GUIDE", "GUIDE"),
        ("notes.v2", "Notes.v2"),
        ("café-münster", "Café-Münster"),
    ],
)
def test_a_generated_heading_capitalizes_each_word_and_keeps_every_separator(
    text: str, expected: str
) -> None:
    assert title_cased(text) == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("guide.md", "Guide"),
        ("guide.markdown", "Guide"),
        ("GUIDE.MARKDOWN", "GUIDE"),
        ("docs/note.md", "Docs/Note"),
        ("docs/sub/note.md", "Docs/Sub/Note"),
        ("notes.v2.md", "Notes.v2"),
        ("guide", "Guide"),
    ],
)
def test_a_file_heading_is_the_path_without_its_markdown_suffix(
    path: str, expected: str
) -> None:
    assert heading_text(path) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("guide", "guide"),
        ("docs/note", "docs/note"),
        ("plan_[v2]", "plan\\_\\[v2\\]"),
        ("a*b", "a\\*b"),
        ("a`b", "a\\`b"),
        ("a<b>c", "a\\<b\\>c"),
        ("a&b", "a\\&b"),
        ("a~b", "a\\~b"),
        ("a!b", "a\\!b"),
        ("a\\b", "a\\\\b"),
        ("a#b", "a\\#b"),
        ("note-1.v2 (final)", "note-1.v2 (final)"),
    ],
)
def test_a_path_is_escaped_as_literal_heading_text(text: str, expected: str) -> None:
    assert escaped(text) == expected


def test_an_escaped_path_opens_no_construct() -> None:
    heading = f"# {escaped('plan_[v2](x)')}\n"
    tokens = parse(heading)
    children = tokens[1].children or []
    assert [child.type for child in children] == ["text"]
    assert children[0].content == "plan_[v2](x)"


def test_an_escaped_path_closes_no_heading() -> None:
    """A number sign ending a path is heading text, not a closing sequence."""
    heading = f"# {escaped('notes/draft #')}\n"
    tokens = parse(heading)
    children = tokens[1].children or []
    assert [child.type for child in children] == ["text"]
    assert children[0].content == "notes/draft #"


def test_a_path_ending_in_a_number_sign_keeps_it_in_its_file_heading() -> None:
    one = grouped("notes/draft #.md", "A document whose path ends in a number sign.\n")
    assert one.text.splitlines()[0] == "# Notes/Draft \\#"
    assert one.headings[0] == "Notes/Draft #"


def test_a_group_opens_on_its_file_heading() -> None:
    assert grouped("docs/note.md", "Body.\n").text == "# Docs/Note\n\nBody.\n"


def test_the_file_heading_absorbs_the_document_s_title() -> None:
    carried = grouped("guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    assert carried.text == "# Guide\n\n## Run\n\nDo it.\n"
    assert carried.headings == ("Guide", "Run")


@pytest.mark.parametrize("name", ["My Note", "my-note", "MY NOTE"])
def test_a_name_is_slugged_as_the_title_it_is_compared_with_is(name: str) -> None:
    assert absorbed(parse("# My Note\n"), name) is not None


def test_a_name_slugging_elsewhere_absorbs_no_title() -> None:
    assert absorbed(parse("# Docs\n"), "note") is None


def test_a_file_heading_carries_the_title_and_not_the_path() -> None:
    carried = grouped("docs/my-note.md", "# My Note\n\n## Run\n")
    assert carried.text == "# My Note\n\n## Run\n"


def test_an_absorbed_group_keeps_its_source_heading_levels() -> None:
    text = "# Guide\n\n## Run\n\n### Detail\n"
    assert grouped("guide.md", text).text == "# Guide\n\n## Run\n\n### Detail\n"


def test_a_title_the_path_does_not_name_heads_the_group() -> None:
    carried = grouped("guide.md", "# Another Name\n\n## Run\n")
    assert carried.text == "# Another Name\n\n## Run\n"
    assert carried.headings == ("Another Name", "Run")


def test_a_title_heads_the_group_as_literal_text() -> None:
    carried = grouped("guide.md", "# The *marked* [guide](https://example.com)\n")
    assert carried.text == "# The marked guide\n"
    assert carried.headings == ("The marked guide",)


def test_a_second_h1_leaves_the_title_unabsorbed() -> None:
    text = "# Guide\n\nOne.\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# Guide\n\n## Guide\n\nOne.\n\n## Guide\n"


def test_an_h1_that_is_not_the_first_heading_leaves_the_title_unabsorbed() -> None:
    text = "## Run\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# Guide\n\n### Run\n\n## Guide\n"


def test_a_container_nested_title_is_not_absorbed() -> None:
    assert absorbed(parse("> # Guide\n"), "guide") is None


def test_a_document_carrying_no_heading_keeps_its_file_heading_alone() -> None:
    assert grouped("guide.md", "Body only.\n").text == "# Guide\n\nBody only.\n"


def test_a_preamble_sits_after_the_file_heading_and_before_the_first_heading() -> None:
    text = "# Guide\n\nLead text.\n\n## Run\n"
    assert grouped("guide.md", text).text == "# Guide\n\nLead text.\n\n## Run\n"


def test_a_blank_line_above_the_first_region_is_not_carried() -> None:
    assert grouped("guide.md", "\n\n# Guide\n\nBody.\n").text == "# Guide\n\nBody.\n"


def test_a_removed_reference_definition_leaves_no_blank_line_behind_it() -> None:
    text = "# Guide\n\n- [x] done\n\n[x]: page.md\n"
    assert grouped("guide.md", text).text == "# Guide\n\n- [x] done\n"


def test_an_unused_reference_definition_is_removed_with_the_used_ones() -> None:
    text = "# Guide\n\nBody.\n\n[a]: one.md\n[b]: two.md\n"
    assert grouped("guide.md", text).text == "# Guide\n\nBody.\n"


@pytest.mark.parametrize(
    "written",
    [
        " ---",
        "---  ",
        '+++\ntitle = "Guide"\n+++',
        "    <span>raw</span>",
        "```text\n[[page]]\n```",
        "> quoted\n> more",
        "- one\n\n- two",
    ],
)
def test_a_region_carries_the_bytes_its_source_wrote(written: str) -> None:
    carried = grouped("guide.md", f"# Guide\n\n{written}\n")
    assert carried.text == f"# Guide\n\n{written}\n"


def test_a_region_ends_with_the_newline_its_source_spelled() -> None:
    text = "# Guide\r\n\r\nOne line.\r\n\r\n- one\r\n- two\r\n"
    assert grouped("guide.md", text).text == (
        "# Guide\n\nOne line.\r\n\n- one\r\n- two\r\n"
    )


def test_a_last_line_carrying_no_terminator_ends_with_the_bundles_own() -> None:
    assert grouped("guide.md", "# Guide\r\n\r\nOne line.").text == (
        "# Guide\n\nOne line.\n"
    )


def test_a_bundle_closes_with_the_newline_its_final_part_carries() -> None:
    bundled = assemble([grouped("guide.md", "# Guide\r\n\r\nBody.\r\n")])
    assert bundled == "# Guide\n\nBody.\r\n"


def test_the_separation_between_two_regions_is_one_blank_line() -> None:
    text = "# Guide\n\nOne.\n\n\n\n\nTwo.\n"
    assert grouped("guide.md", text).text == "# Guide\n\nOne.\n\nTwo.\n"


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("> ## Quoted", "> ### Quoted"),
        ("> > ## Quoted", "> > ### Quoted"),
        ("- item\n\n  ## Listed", "- item\n\n  ### Listed"),
        ("1. item\n\n   ## Listed", "1. item\n\n   ### Listed"),
    ],
)
def test_a_heading_a_container_carries_is_shifted_where_it_sits(
    written: str, expected: str
) -> None:
    carried = grouped("guide.md", f"## Lead\n\n{written}\n")
    assert carried.text == f"# Guide\n\n### Lead\n\n{expected}\n"


def test_a_heading_a_container_carries_is_one_the_group_emits() -> None:
    carried = grouped("guide.md", "# Guide\n\n> ## Quoted\n>\n> Inside.\n\n## Run\n")
    assert carried.headings == ("Guide", "Quoted", "Run")


def test_a_heading_a_code_example_holds_is_no_heading_the_group_emits() -> None:
    carried = grouped("guide.md", "# Guide\n\n> ```\n> ## Not A Heading\n> ```\n")
    assert carried.headings == ("Guide",)


def test_a_container_keeps_the_heading_like_text_a_code_example_holds() -> None:
    written = "> ```markdown\n> ## Not A Heading\n> ```"
    carried = grouped("guide.md", f"## Lead\n\n{written}\n")
    assert carried.text == f"# Guide\n\n### Lead\n\n{written}\n"


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("Run\n===", "## Run"),
        ("Run\n---", "### Run"),
        ("Run the *marked* `one`\n---", "### Run the *marked* `one`"),
        ("Run\nand stop\n---", "### Run and stop"),
        ("> Quoted\n> ---", "> ### Quoted"),
    ],
)
def test_a_shifted_group_emits_a_setext_heading_as_atx(
    written: str, expected: str
) -> None:
    carried = grouped("guide.md", f"## Lead\n\n{written}\n")
    assert carried.text == f"# Guide\n\n### Lead\n\n{expected}\n"


def test_a_group_that_shifts_by_nothing_leaves_a_setext_heading_alone() -> None:
    carried = grouped("guide.md", "# Guide\n\nRun\n---\n")
    assert carried.text == "# Guide\n\nRun\n---\n"


def test_a_converted_heading_keeps_a_number_sign_run_ending_its_text() -> None:
    carried = grouped("guide.md", "## Lead\n\nSharp #\n---\n")
    assert carried.text == "# Guide\n\n### Lead\n\n### Sharp \\#\n"


def test_a_converted_heading_shows_the_text_its_source_lines_carried() -> None:
    carried = grouped("guide.md", "## Lead\n\nRun\nand stop\n---\n")
    assert carried.headings == ("Guide", "Lead", "Run and stop")


def test_a_shift_beyond_the_sixth_level_for_a_nested_heading_is_an_overflow() -> None:
    text = "## Lead\n\n> ###### Deep\n"
    with pytest.raises(Overflow) as refused:
        grouped("guide.md", text)
    assert refused.value.heading == "Deep"
    assert refused.value.level == MAX_LEVEL + 1


def test_a_shift_beyond_the_sixth_level_is_an_overflow() -> None:
    text = "## Lead\n\n###### Deep\n"
    with pytest.raises(Overflow) as refused:
        grouped("guide.md", text)
    assert refused.value.heading == "Deep"
    assert refused.value.level == MAX_LEVEL + 1


def test_an_absorbed_group_reaches_the_sixth_level_without_overflow() -> None:
    text = "# Guide\n\n###### Deep\n"
    assert grouped("guide.md", text).text == "# Guide\n\n###### Deep\n"


def test_a_bundle_ends_in_exactly_one_newline() -> None:
    bundled = assemble([grouped("guide.md", "# Guide\n")])
    assert bundled == "# Guide\n"


def test_a_group_is_its_parts_one_blank_line_apart() -> None:
    text = "# Guide\n\nOpening prose.\n\n## Rules\n"
    carried = grouped("guide.md", text)
    assert carried.parts == ("# Guide", "Opening prose.\n", "## Rules\n")
    assert carried.text == "# Guide\n\nOpening prose.\n\n## Rules\n"


def test_each_part_opens_one_blank_line_below_the_part_above_it() -> None:
    text = "# Guide\n\nOpening prose.\n\n- A rule.\n- Another rule.\n"
    carried = grouped("guide.md", text)
    bundled = assemble([carried])
    assert openings([carried]) == [0, 2, 4]
    assert [lines(bundled)[at] for at in openings([carried])] == [
        "# Guide\n",
        "Opening prose.\n",
        "- A rule.\n",
    ]


def test_the_parts_of_two_groups_open_in_bundle_order() -> None:
    first = grouped("guide.md", "# Guide\n\nOpening prose.\n")
    second = grouped("note.md", "# Note\n")
    bundled = assemble([first, second])
    assert openings([first, second]) == [0, 2, 4]
    assert [lines(bundled)[at] for at in openings([first, second])] == [
        "# Guide\n",
        "Opening prose.\n",
        "# Note\n",
    ]


def selecting(path: str, text: str, *named: str) -> Group:
    """One file group holding the sections the fragments name and nothing else."""
    tokens = parse(text)
    wanted = [
        token for fragment in named for token in (section(tokens, fragment) or ())
    ]
    chosen = tuple(
        token for token in regions(tokens) if any(token is one for one in wanted)
    )
    return group(path, tokens, lines(text), None, Selection(chosen), None)


OUTLINED = """## Alpha

Alpha body.

### One

One body.

### Two

Two body.

## Beta

Beta body.
"""


def test_an_unselected_ancestor_is_emitted_as_a_heading_alone() -> None:
    carried = selecting("guide.md", OUTLINED, "one")
    assert carried.text == "# Guide\n\n### Alpha\n\n#### One\n\nOne body.\n"


def test_an_ancestor_two_selections_share_is_emitted_once() -> None:
    carried = selecting("guide.md", OUTLINED, "one", "two")
    assert carried.headings == ("Guide", "Alpha", "One", "Two")


def test_an_ancestor_stands_in_the_source_order_its_author_wrote() -> None:
    text = "## Alpha\n\n### One\n\nOne body.\n\n## Beta\n\n### Two\n\nTwo body.\n"
    carried = selecting("guide.md", text, "one", "two")
    assert carried.headings == ("Guide", "Alpha", "One", "Beta", "Two")


def test_a_selected_ancestor_is_the_content_it_is_rather_than_a_heading() -> None:
    carried = selecting("guide.md", OUTLINED, "alpha")
    assert carried.text == (
        "# Guide\n\n### Alpha\n\nAlpha body.\n\n#### One\n\nOne body."
        "\n\n#### Two\n\nTwo body.\n"
    )
    assert carried.record.ancestors() == []


def test_an_ancestor_title_is_emitted_as_literal_text() -> None:
    text = "## A & [the note](note.md) <b>b</b>\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.parts[1] == "### A \\& the note b"
    assert carried.record.ancestors()[0].text == "A & the note b"


def test_an_ancestor_title_drops_the_mark_a_link_it_carries_was_deferred_by() -> None:
    text = "## A [¬ the note](note.md) heading\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.parts[1] == "### A the note heading"
    assert carried.record.ancestors()[0].text == "A the note heading"


def test_an_ancestor_record_names_its_source_heading_and_original_level() -> None:
    one = selecting("guide.md", OUTLINED, "one").record.ancestors()[0]
    assert (one.text, one.level, one.kind) == ("Alpha", 3, STRUCTURAL_ANCESTOR)
    assert one.origins == (Origin("guide.md", 1, 2, "alpha", 1),)


def test_an_ancestor_accounts_for_the_part_it_emits_and_carries_no_range() -> None:
    carried = selecting("guide.md", OUTLINED, "one")
    record = carried.record
    assert len(record.parts) == len(carried.parts) - 1 == 3
    assert record.parts[0] == record.ancestors()[0]
    assert [one.lines for one in record.ranges] == [(4, 5), (6, 7)]


def test_a_title_the_file_heading_names_is_no_ancestor() -> None:
    text = "# Guide\n\n## Run\n\n### Detail\n\nDetail body.\n"
    carried = selecting("guide.md", text, "detail")
    assert carried.text == "# Guide\n\n### Run\n\n#### Detail\n\nDetail body.\n"


def test_a_heading_a_container_carries_roots_no_ancestor_chain() -> None:
    text = "## Alpha\n\n> ### Quoted\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.headings == ("Guide", "Alpha", "One")


def test_an_ancestor_at_the_sixth_level_overflows_on_what_it_places() -> None:
    """An ancestor reaching H6 holds, and the heading beneath it is the overflow."""
    text = "##### Five\n\nFive body.\n\n###### Six\n\nSix body.\n"
    with pytest.raises(Overflow) as refused:
        selecting("guide.md", text, "six")
    assert refused.value.heading == "Six"
    assert refused.value.level == MAX_LEVEL + 1


def rewritten_lines(text: str) -> list[str]:
    """One document's lines as the bundle publishes them, `open.md` bundled."""
    tokens = parse(text)
    return rewrite(
        lines(text),
        tokens,
        list(regions(tokens)),
        {("open.md", None): "open"},
        "lifecycle.md",
        {},
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            '```mermaid\nflowchart LR\n    click Open href "open.md"\n```\n',
            '```mermaid\nflowchart LR\n    click Open href "#open"\n```\n',
        ),
        (
            "   ```mermaid\n   flowchart LR\n"
            '     click Open "open.md" _blank\n   ```\n',
            '   ```mermaid\n   flowchart LR\n     click Open "#open" _blank\n   ```\n',
        ),
        (
            "- Item\n\n  > ```mermaid\n  > flowchart LR\n"
            '  >   click Open href "open.md" "Open"\n  > ```\n',
            "- Item\n\n  > ```mermaid\n  > flowchart LR\n"
            '  >   click Open href "#open" "Open"\n  > ```\n',
        ),
        (
            '```mermaid\r\nflowchart LR\r\n  click Open "open.md";\r\n```\r\n',
            '```mermaid\r\nflowchart LR\r\n  click Open "#open";\r\n```\r\n',
        ),
    ],
    ids=["document-level", "indented-fence", "nested-containers", "crlf"],
)
def test_a_diagram_click_destination_is_rewritten_between_its_quotes(
    text: str, expected: str
) -> None:
    assert "".join(rewritten_lines(text)) == expected


def test_a_diagram_click_rewrite_keeps_one_entry_per_source_line() -> None:
    text = (
        '```mermaid\nflowchart LR\n  click Open "open.md"\n  click Shut "shut.svg"\n'
        "```\n"
    )
    published = rewritten_lines(text)
    assert len(published) == len(lines(text))
    assert published[2] == '  click Open "#open"\n'
    assert published[3] == '  click Shut "shut.svg"\n'


def test_a_diagram_click_outside_the_selection_keeps_its_source_path() -> None:
    text = (
        '# Kept\n\n```mermaid\nflowchart LR\n  click Open "open.md"\n```\n\n'
        '# Left\n\n```mermaid\nflowchart LR\n  click Open "open.md"\n```\n'
    )
    tokens = parse(text)
    published = rewrite(
        lines(text),
        tokens,
        list(section(tokens, "kept") or ()),
        {("open.md", None): "open"},
        "lifecycle.md",
        {},
    )
    assert published[4] == '  click Open "#open"\n'
    assert published[11] == '  click Open "open.md"\n'


DISPATCHING = f"# Prosiform\n\n## Dispatch\n\n{DISPATCH_PROTOCOL}\n\n"
TOGETHER = f"## Parallel dispatch\n\n{PARALLEL_PROTOCOL}\n\n"
PLAN = "Dispatch `plan.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states."
SET = (
    "Dispatch these bundles together, each to a sub-agent, as "
    "[Parallel dispatch](#parallel-dispatch) states:"
)
PROTOCOL = re.compile(r"^## (?:Parallel d|D)ispatch\n\n[^\n]*\n", re.MULTILINE)


def compiled(
    root: Path, sources: Mapping[str, str], *entries: str
) -> tuple[int, dict[str, str], str]:
    """One run over a tree of sources: its status, its bundles and its diagnostics."""
    for name, text in sources.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (root / "out").mkdir()
    errors = StringIO()
    with chdir(root):
        status = main(["-d", "json", "-o", "out", *entries], StringIO(), errors)
    folders = list((root / "out").iterdir())
    bundles = {
        one.name: one.read_text() for folder in folders for one in folder.iterdir()
    }
    return status, bundles, errors.getvalue()


def test_a_bundle_using_the_dispatch_operator_opens_with_its_protocol(
    tmp_path: Path,
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {"guide.md": "# Guide\n\nRun [\u21c9 plan](plan.md).\n", "plan.md": "# Plan\n"},
        "guide.md",
    )
    assert status == SUCCESS
    assert bundles["guide.bundle.md"] == (
        f"{DISPATCHING}# Guide\n\nRun [plan](#dispatch-plan).\n\n"
        f"## Dispatch plan\n\n{PLAN}\n"
    )
    assert bundles["plan.bundle.md"] == "# Plan\n"


def test_a_bundle_using_the_parallel_mark_states_both_protocols(
    tmp_path: Path,
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {"guide.md": "# Guide\n\nRun [\u2afd plan](plan.md).\n", "plan.md": "# Plan\n"},
        "guide.md",
    )
    assert status == SUCCESS
    assert bundles["guide.bundle.md"] == (
        f"{DISPATCHING}{TOGETHER}# Guide\n\nRun [plan](#dispatch-in-parallel).\n\n"
        f"## Dispatch in parallel\n\n{SET}\n\n- `plan.bundle.md` (plan)\n"
    )


def test_a_bundle_using_both_operators_states_each_protocol_once(
    tmp_path: Path,
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {
            "guide.md": "# Guide\n\n## One\n\nRun [\u21c9 plan](plan.md).\n\n"
            "## Two\n\nRun [\u2afd plan](plan.md).\n",
            "plan.md": "# Plan\n",
        },
        "guide.md",
    )
    assert status == SUCCESS
    bundle = bundles["guide.bundle.md"]
    assert bundle.startswith(f"{DISPATCHING}{TOGETHER}# Guide\n")
    assert bundle.count("# Prosiform") == 1
    assert bundle.count(f"## Dispatch\n\n{DISPATCH_PROTOCOL}") == 1
    assert bundle.count(f"## Parallel dispatch\n\n{PARALLEL_PROTOCOL}") == 1


def test_a_bundle_using_neither_operator_carries_no_prosiform_section(
    tmp_path: Path,
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {"guide.md": "# Guide\n\nSee [plan](plan.md).\n", "plan.md": "# Plan\n\nGo.\n"},
        "guide.md",
    )
    assert status == SUCCESS
    assert bundles["guide.bundle.md"] == (
        "# Guide\n\nSee [plan](#plan).\n\n# Plan\n\nGo.\n"
    )


def test_the_prosiform_section_precedes_a_file_heading(tmp_path: Path) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {
            "guide.md": "# Guide\n\n## Run\n\nRun [\u21c9 plan](plan.md).\n",
            "plan.md": "# Plan\n",
        },
        "guide.md#run",
    )
    assert status == SUCCESS
    assert bundles["guide__run.bundle.md"] == (
        f"{DISPATCHING}# Guide\n\n### Run\n\nRun [plan](#dispatch-plan).\n\n"
        f"#### Dispatch plan\n\n{PLAN}\n"
    )


def test_the_prosiform_section_follows_a_preamble_and_precedes_its_dispatch(
    tmp_path: Path,
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {
            "guide.md": "Intro [\u21c9 plan](plan.md).\n\n# Guide\n\nBody.\n",
            "plan.md": "# Plan\n",
        },
        "guide.md",
    )
    assert status == SUCCESS
    assert bundles["guide.bundle.md"] == (
        f"Intro [plan](#dispatch-plan).\n\n{DISPATCHING}"
        f"# Dispatch plan\n\n{PLAN}\n\n# Guide\n\nBody.\n"
    )


def test_the_prosiform_section_precedes_a_titled_entry_members_title(
    tmp_path: Path,
) -> None:
    member = "---\nprosiform: {group: notes, group-depth: 2}\n---\n"
    status, bundles, _ = compiled(
        tmp_path,
        {
            "guide.md": f"{member}Intro.\n\n# Guide\n\nAbove.\n\n"
            "## Run\n\nRun [\u21c9 plan](plan.md).\n",
            "other.md": f"{member}# Other\n\n## Run\n\nTheirs.\n",
            "plan.md": "# Plan\n",
        },
        "guide.md",
    )
    assert status == SUCCESS
    assert bundles["guide.bundle.md"].startswith(
        f"Intro.\n\n{DISPATCHING}# Guide\n\nAbove.\n\n## Run\n"
    )


@pytest.mark.parametrize(
    ("operator", "heading"),
    [
        ("\u21c9", "Dispatch"),
        ("\u2afd", "Dispatch"),
        ("\u2afd", "Parallel dispatch"),
    ],
)
def test_an_authored_heading_equal_to_a_protocol_pf_emits_is_refused(
    tmp_path: Path, operator: str, heading: str
) -> None:
    status, bundles, errors = compiled(
        tmp_path,
        {
            "guide.md": f"# Guide\n\nRun [{operator} plan](plan.md).\n\n"
            f"## {heading}\n\nMine.\n",
            "plan.md": "# Plan\n",
        },
        "guide.md",
    )
    assert status == INPUT_FAILURE
    assert bundles == {}
    [diagnostic] = [json.loads(line) for line in errors.splitlines()]
    assert diagnostic["code"] == HEADING_COLLISION


@pytest.mark.parametrize(
    ("operator", "heading"),
    [
        ("", "Dispatch"),
        ("\u21c9 ", "Parallel dispatch"),
    ],
)
def test_an_authored_protocol_heading_pf_does_not_emit_publishes(
    tmp_path: Path, operator: str, heading: str
) -> None:
    status, bundles, _ = compiled(
        tmp_path,
        {
            "guide.md": f"# Guide\n\nRun [{operator}plan](plan.md).\n\n"
            f"## {heading}\n\nMine.\n",
            "plan.md": "# Plan\n",
        },
        "guide.md",
    )
    assert status == SUCCESS
    assert f"## {heading}\n\nMine.\n" in bundles["guide.bundle.md"]


def test_each_protocol_is_the_same_bytes_in_two_corpora(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, one, _ = compiled(
        first,
        {
            "skill/guide.md": "# Guide\n\n## Act\n\n"
            "Run [\u21c9 plan](plan.md) and [\u2afd review](review.md#code).\n",
            "skill/plan.md": "# Plan\n\nRun [\u2afd review](review.md#tests).\n",
            "skill/review.md": "# Review\n\n## Code\n\nRead.\n\n## Tests\n\nRun.\n",
        },
        "skill/guide.md",
    )
    _, other, _ = compiled(
        second,
        {
            "mode.md": "Opening [\u2afd check](check.md).\n\n"
            "# Mode\n\n### Deep\n\nThen [\u21c9 check](check.md).\n",
            "check.md": "# Check\n\nDone.\n",
        },
        "mode.md",
    )
    stated = [
        PROTOCOL.findall(bundle)
        for bundle in (
            one["skill_guide.bundle.md"],
            one["skill_plan.bundle.md"],
            other["mode.bundle.md"],
        )
    ]
    expected = [
        f"## Dispatch\n\n{DISPATCH_PROTOCOL}\n",
        f"## Parallel dispatch\n\n{PARALLEL_PROTOCOL}\n",
    ]
    assert stated == [expected, expected, expected]
