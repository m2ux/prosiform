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
