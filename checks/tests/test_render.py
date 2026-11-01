"""Assert the render check lists every diagram-link fixture and refuses a diagram
Mermaid cannot parse.

`make render` needs mermaid-cli and a headless browser, so `make check` does
not run it. What it reads is held here instead: a `rewriting/` fixture whose
bundle draws a Mermaid diagram is one the check renders, so a fixture left off
its lists is a bundle no renderer is shown to draw. A drawing that fails is a
defect the check names, never an error ending the run before the fixtures
after it are read.
"""

from pathlib import Path

import render

REWRITING = "rewriting"


def drawing_fixtures() -> set[str]:
    """Every `rewriting/` fixture whose expected bundle holds a Mermaid diagram."""
    return {
        f"{REWRITING}/{fixture.name}"
        for fixture in (render.FIXTURES / REWRITING).iterdir()
        if fixture.is_dir()
        and render.MERMAID_FENCE.search(render.expected_bundle(fixture).read_text())
    }


def test_every_drawing_rewriting_fixture_is_rendered() -> None:
    listed = set(render.RENDERED) | set(render.CLICKED)
    assert sorted(drawing_fixtures() - listed) == []


def test_every_listed_fixture_draws_a_diagram() -> None:
    """A listed fixture from any family is one whose bundle a renderer draws."""
    listed = set(render.RENDERED) | set(render.CLICKED)
    assert (
        sorted(
            name
            for name in listed
            if not render.MERMAID_FENCE.search(
                render.expected_bundle(render.FIXTURES / name).read_text()
            )
        )
        == []
    )


def test_a_diagram_mermaid_cannot_parse_is_a_defect(tmp_path: Path) -> None:
    """mermaid-cli exiting nonzero is the fixture's failure, carrying no anchors."""
    bundle = tmp_path / "bundle.md"
    bundle.write_text("```mermaid\nsequenceDiagram\n    a;b\n```\n")
    assert render.rendered(["false"], bundle) == (
        [],
        ["mermaid-cli exits 1: a diagram does not parse"],
    )
