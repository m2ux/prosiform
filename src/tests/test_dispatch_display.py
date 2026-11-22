"""Dispatch marks distinguish hand-offs from navigation to local sections."""

from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

BRIEF = (
    '---\nprosiform:\n  default:\n    brief: "#contract"\n---\n'
    "# Read\n\n## Contract\n\nRead one input.\n"
)


@pytest.mark.parametrize(
    ("shape", "published"),
    [
        ("Read(⇉ Inspect)", "Read(Inspect)"),
        ('Read["⇉ Inspect"]', 'Read["Inspect"]'),
        ('Read["`⇉ Inspect`"]', 'Read["`Inspect`"]'),
        (
            'Read@{shape: rect, label: "⇉ Inspect"}',
            'Read@{shape: rect, label: "Inspect"}',
        ),
        (
            'Read@{label: "\\u21c9 Inspect", shape: rect}',
            'Read@{label: "Inspect", shape: rect}',
        ),
        (
            'Read@{other: &text "⇉ Inspect", label: *text}',
            'Read@{other: &text "⇉ Inspect", label: "Inspect"}',
        ),
        (
            'Read@{key: &key label, *key : "⇉ Inspect"}',
            'Read@{key: &key label, *key : "Inspect"}',
        ),
    ],
)
def test_a_diagram_local_dispatch_names_its_plain_section(
    tmp_path: Path, shape: str, published: str
) -> None:
    written(tmp_path, "read.md", BRIEF)
    written(tmp_path, "direct.md", DECLARED + "# Direct\n")
    source = (
        DECLARED + "# Guide\n\n## Work\n\n[⇉ Inspect](read.md)\n\n"
        "[⇉ Direct](direct.md)\n\n```mermaid\nflowchart TD\n"
        + shape
        + "\nDirect(⇉ Direct)\nUnlinked(⇉ Inspect)\n"
        'click Read href "read.md"\nclick Direct href "direct.md"\n```\n'
    )
    written(tmp_path, "guide.md", source)
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "### Inspect\n" in run.bundle
    assert "### ⇉ Inspect" not in run.bundle
    assert "[Inspect](#inspect)" in run.bundle
    assert "[⇉ Inspect](read.bundle.md)" in run.bundle
    assert published in run.bundle
    assert 'click Read href "#inspect"' in run.bundle
    assert "Direct(⇉ Direct)" in run.bundle
    assert 'click Direct href "direct.bundle.md"' in run.bundle
    assert "Unlinked(⇉ Inspect)" in run.bundle
    assert (tmp_path / "guide.md").read_text() == source


@pytest.mark.parametrize("before", [True, False])
def test_label_edits_preserve_click_offsets_on_shared_lines(
    tmp_path: Path, before: bool
) -> None:
    written(tmp_path, "read.md", BRIEF)
    written(tmp_path, "direct.md", DECLARED + "# Direct\n")
    pair = ['Read["⇉ Inspect"]', 'click Read href "read.md"']
    if not before:
        pair.reverse()
    line = "; ".join([*pair, "Direct(⇉ Direct)", 'click Direct href "direct.md"'])
    written(
        tmp_path,
        "guide.md",
        DECLARED
        + "# Guide\n\n## Work\n\n```mermaid\nflowchart TD\n"
        + line
        + "\n```\n",
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert 'Read["Inspect"]' in run.bundle
    assert 'click Read href "#inspect"' in run.bundle
    assert "Direct(⇉ Direct)" in run.bundle
    assert 'click Direct href "direct.bundle.md"' in run.bundle


def test_class_label_marks_follow_the_compiled_destination(tmp_path: Path) -> None:
    written(tmp_path, "read.md", BRIEF)
    written(tmp_path, "direct.md", DECLARED + "# Direct\n")
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Work\n\n```mermaid\nclassDiagram\n"
        'class Read["⇉ Inspect"]\nclass Direct["⇉ Direct"]\n'
        'link Read "read.md"\nlink Direct "direct.md"\n```\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert 'class Read["Inspect"]' in run.bundle
    assert 'class Direct["⇉ Direct"]' in run.bundle
    assert 'link Read "#inspect"' in run.bundle


def test_a_picking_dispatch_has_a_plain_heading_and_local_graph_label(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "read.md",
        "---\nprosiform:\n  fast:\n    choice: fast read\n"
        "  deep:\n    choice: deep read\n---\n# Read\n",
    )
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Work\n\n```mermaid\nflowchart TD\n"
        'Read(⇉ Inspect)\nclick Read href "read.md" "?"\n```\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "### Dispatch Pick\n" in run.bundle
    assert "### ⇉ Dispatch Pick" not in run.bundle
    assert "Read(Inspect)" in run.bundle
    assert 'click Read href "#dispatch-pick" "?"' in run.bundle
    assert run.bundle.count("[⇉ Inspect](") == 2


def test_a_plain_lifted_heading_colliding_with_authored_text_is_refused(
    tmp_path: Path,
) -> None:
    written(tmp_path, "read.md", BRIEF)
    written(
        tmp_path,
        "guide.md",
        DECLARED
        + "# Guide\n\n## Work\n\n[⇉ Inspect](read.md)\n\n### Inspect\n\nAuthored.\n",
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 1
    assert "E_HEADING_COLLISION" in run.stderr


def test_plain_dispatch_pick_is_reserved_for_generated_picks(tmp_path: Path) -> None:
    written(tmp_path, "read.md", BRIEF)
    written(tmp_path, "guide.md", DECLARED + "# Guide\n\n[⇉ Dispatch Pick](read.md)\n")
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 1
    assert "E_HEADING_COLLISION" in run.stderr
