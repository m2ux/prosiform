"""Compact diagrams retain Markdown structure and dependency links."""

import importlib.util
from pathlib import Path
from types import ModuleType
from xml.etree import ElementTree


def renderer() -> ModuleType:
    path = Path(__file__).resolve().parents[2] / "scripts" / "render-diagram.py"
    spec = importlib.util.spec_from_file_location("diagram_renderer", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compact_retains_headings_and_real_link_forms() -> None:
    body = """---
name: metadata
---
# Exact HTTP Title

Long descriptive prose.

Second descriptive paragraph.

Subsection
----------

Read [Inline](target.md) and [Reference][ref].

<https://example.com>

![Map](map.png)

[ref]: other.md#detail
"""
    compact = renderer().compact_markdown(body)
    assert compact.startswith("# Exact HTTP Title\n\n…\n\n## Subsection")
    assert "[Inline](target.md)" in compact
    assert "[Reference](other.md#detail)" in compact
    assert "[https://example.com](https://example.com)" in compact
    assert "![Map](map.png)" in compact
    assert "descriptive" not in compact
    assert "metadata" not in compact


def test_compact_does_not_promote_code_examples_to_headings_or_links() -> None:
    body = """# Real Title

```markdown
# Example Title
[Fake](missing.md)
```

    [Indented](missing.md)

`[Inline code](missing.md)`

## Next Section

- [Real](real.md)
- Other list content.
"""
    compact = renderer().compact_markdown(body)
    assert compact.startswith("# Real Title\n\n…\n\n## Next Section")
    assert "[Real](real.md)" in compact
    assert "missing.md" not in compact
    assert "Example Title" not in compact
    assert "Other list content" not in compact


def test_compact_changes_both_panels_without_changing_input() -> None:
    module = renderer()
    prose = "Long body text to omit. " * 100
    source = "# Source Title\n\n" + prose + "\n\n[Go](other.md)\n"
    output = "# Bundle Title\n\n" + prose + "\n\n[Go](#target)\n"
    inputs = {"SKILL.md": source}
    full = module.svg(inputs, "skill", output, "main", "a" * 40)
    compact = module.svg(inputs, "skill", output, "main", "a" * 40, compact=True)
    assert "Long body text" in full
    assert "Long body text" not in compact
    assert "Source Title" in compact and "Bundle Title" in compact
    assert "Go" in compact
    assert inputs == {"SKILL.md": source}
    assert int(ElementTree.fromstring(compact).attrib["height"]) < int(
        ElementTree.fromstring(full).attrib["height"]
    )


def test_compact_preserves_empty_and_rejected_states() -> None:
    module = renderer()
    assert module.compact_markdown("") == ""
    assert module.compact_markdown("# Title Only\n") == "# Title Only"
    diagram = module.svg({}, "skill", "", "main", "a" * 40, compact=True)
    assert "No bundle published." in diagram


def test_section_level_keeps_boundary_titles_and_hides_their_contents() -> None:
    body = """---
name: metadata
---
# Board
## Operations
Visible text and [Visible Link](visible.md).
### Select Project Board
[Find Theme Board](hidden.md)
#### Hidden Detail
Hidden body.
### Another Operation
<https://example.com/hidden>
## Next Area
Visible again.
##### Skipped Levels
Also hidden.
"""
    module = renderer()
    filtered = module.limit_section_content(body, 2)
    for title in (
        "Board",
        "Operations",
        "Select Project Board",
        "Another Operation",
        "Next Area",
    ):
        assert title in filtered
    for hidden in (
        "Find Theme Board",
        "Hidden Detail",
        "Hidden body",
        "example.com",
        "Skipped Levels",
        "Also hidden",
    ):
        assert hidden not in filtered
    assert "Visible again." in filtered and "Visible Link" in filtered
    assert filtered.startswith("---\nname: metadata\n---\n# Board")
    assert module.limit_section_content(body, None) == body
    assert module.limit_section_content(body, 6) == body


def test_section_level_filters_both_panels_with_optional_compaction() -> None:
    module = renderer()
    body = (
        "# Board\n## Operations\n### Select Project Board\n\n"
        "[Find Theme Board](hidden.md)\n"
    )
    inputs = {"SKILL.md": body}
    for compact in (False, True):
        diagram = module.svg(
            inputs,
            "skill",
            body,
            "main",
            "a" * 40,
            compact=compact,
            input_section_level=2,
            compiled_section_level=2,
        )
        assert diagram.count("Select Project Board") == 2
        assert "Find Theme Board" not in diagram
        ElementTree.fromstring(diagram)
    assert inputs == {"SKILL.md": body}


def test_section_level_handles_setext_titles() -> None:
    body = "Title\n=====\n\nDetails\n-------\n\nText.\n"
    assert (
        renderer().limit_section_content(body, 1)
        == "Title\n=====\n\nDetails\n-------\n"
    )


def test_panel_section_levels_are_independent() -> None:
    module = renderer()
    source = "# Input\n## Area\n### Operation\n[Input Link](input.md)\n"
    output = "# Compiled\n## Area\n### Operation\n[Compiled Link](#target)\n"
    for compact in (False, True):
        for input_level, compiled_level in ((2, None), (None, 2), (2, 3), (3, 2)):
            diagram = module.svg(
                {"SKILL.md": source},
                "skill",
                output,
                "main",
                "a" * 40,
                compact=compact,
                input_section_level=input_level,
                compiled_section_level=compiled_level,
            )
            assert ("Input Link" in diagram) == (input_level != 2)
            assert ("Compiled Link" in diagram) == (compiled_level != 2)
