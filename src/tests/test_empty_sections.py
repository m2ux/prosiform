"""Empty generated wrappers yield to preserved author and target identities."""

import json
from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

from prosiform.bundle import Group
from prosiform.provenance import (
    FILENAME_WRAPPER,
    MEMBER_OVERVIEW,
    OVERVIEW_SECTION,
    PICK_SECTION,
    Generated,
    Instruction,
    Record,
)
from prosiform.pruning import prune


def test_empty_generated_preamble_subtrees_warn_and_disappear(tmp_path: Path) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n[Rules](references/contract.md#rules)\n",
    )
    source = (
        "---\nprosiform:\n  default:\n    group: {contracts: 2}\n---\n"
        "# Contract\n\n## Rules\n\nAnswer alone.\n"
    )
    written(tmp_path, "references/contract.md", source)
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "## References" not in run.bundle and "### Contract\n" not in run.bundle
    assert "## Contracts\n\n### Rules\n\nAnswer alone." in run.bundle
    warnings = [json.loads(line) for line in run.stderr.splitlines()]
    assert [d["code"] for d in warnings] == ["W_EMPTY_SECTION", "W_EMPTY_SECTION"]
    assert all(
        d["location"] == {"file": "references/contract.md", "line": 6, "column": 1}
        for d in warnings
    )
    assert (tmp_path / "references/contract.md").read_text() == source


def test_nonempty_generated_preamble_context_stays(tmp_path: Path) -> None:
    written(
        tmp_path, "guide.md", DECLARED + "# Guide\n\n[Rules](refs/contract.md#rules)\n"
    )
    written(
        tmp_path,
        "refs/contract.md",
        "---\nprosiform:\n  default:\n    group: {contracts: 2}\n---\n"
        "# Contract\n\nContext.\n\n## Rules\n\nAct.\n",
    )
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "## Refs\n\n### Contract\n\nContext." in run.bundle
    assert run.stderr == ""


@pytest.mark.parametrize(
    "link",
    [
        "[Doc](notes.md)",
        "[Doc][target]\n\n[target]: notes.md",
        '```mermaid\nflowchart TD\nN(Doc)\nclick N href "notes.md"\n```',
    ],
)
def test_document_links_keep_their_generated_member_identity(
    tmp_path: Path, link: str
) -> None:
    written(tmp_path, "guide.md", DECLARED + "# Guide\n\n" + link + "\n")
    written(
        tmp_path,
        "notes.md",
        "---\nprosiform:\n  default:\n    group: {shared: 2}\n---\n"
        "# Notes\n\n## Use\n\nContent.\n",
    )
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "### Notes\n" in run.bundle and "Content." in run.bundle
    assert "#notes" in run.bundle
    assert run.stderr == ""


@pytest.mark.parametrize(
    "source",
    [
        "# Guide\n",
        "# Guide\n\n## Empty\n\n### Also Empty\n",
        "# Guide\n\n[Empty](#empty)\n\n## Empty\n",
    ],
)
def test_authored_empty_sections_and_anchors_remain(
    tmp_path: Path, source: str
) -> None:
    written(tmp_path, "guide.md", DECLARED + source)
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert source in run.bundle
    assert run.stderr == ""


@pytest.mark.parametrize(
    "body",
    [
        "Text.",
        "- An item.",
        "```markdown\n## Empty example\n```",
        "> ## Quoted\n> Text.",
        "---",
    ],
)
def test_meaningful_sections_and_examples_keep_their_outline(
    tmp_path: Path, body: str
) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Parent\n\n### Child\n\n" + body + "\n",
    )
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "## Parent\n\n### Child" in run.bundle and body in run.bundle
    assert run.stderr == ""


def test_pruned_wrapper_positions_leave_dispatch_destinations_addressable() -> None:
    wrapper = Generated("Guide", 1, FILENAME_WRAPPER)
    overview = Generated("Overview", 2, OVERVIEW_SECTION)
    empty = Generated("Empty", 3, MEMBER_OVERVIEW)
    pick = Generated("Dispatch Pick", 2, PICK_SECTION)
    instruction = Instruction("Hand on the selected bundle.")
    group = Group(
        ("# Guide", "## Overview", "### Empty", "## Dispatch Pick", instruction.text),
        Record(
            "guide.md",
            None,
            (wrapper, overview, empty, pick),
            (overview, empty, pick, instruction),
        ),
    )
    kept, removed, positions = prune([group], {}, set())
    assert kept[0].parts == ("# Guide", "## Dispatch Pick", instruction.text)
    assert [one.heading.text for one in removed] == ["Overview", "Empty"]
    assert positions == {0: 0, 3: 1}


def test_a_protected_empty_generated_wrapper_keeps_its_ancestors() -> None:
    wrapper = Generated("Guide", 1, FILENAME_WRAPPER)
    overview = Generated("Overview", 2, OVERVIEW_SECTION)
    address = Generated("Member", 3, MEMBER_OVERVIEW)
    group = Group(
        ("# Guide", "## Overview", "### Member"),
        Record("guide.md", None, (wrapper, overview, address), (overview, address)),
    )
    kept, removed, positions = prune([group], {}, {id(address)})
    assert kept == [group] and removed == [] and positions == {0: 0, 1: 1, 2: 2}
