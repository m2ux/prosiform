"""Deferred activation retains its source title and requested preset selection."""

from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

from prosiform.candidate import TARGET_INTEGRITY, Invalid, activation
from prosiform.profile import parse
from prosiform.provenance import Instruction
from prosiform.source import LINK_OPEN, events, inlines, regions
from prosiform.tags import read as read_tags


@pytest.mark.parametrize(
    "title",
    [
        None,
        "",
        " checks, DRAFT,unknown ",
        "checks,&quot;quoted&quot;,a&#92;b",
        "café,&#10;draft",
    ],
)
@pytest.mark.parametrize("reference_style", [False, True])
def test_generated_deferred_line_preserves_the_parsed_title(
    tmp_path: Path, title: str | None, reference_style: bool
) -> None:
    suffix = "" if title is None else f' "{title}"'
    if reference_style:
        directive = f"[¬↳ Material][rules]\n\n[rules]: rules.md#steps{suffix}\n"
    else:
        directive = f"[¬↳ Material](rules.md#steps{suffix})\n"
    source = DECLARED + "# Entry\n\n" + directive
    written(tmp_path, "entry.md", source)
    written(tmp_path, "rules.md", DECLARED + "# Rules\n\n## Steps\n\nBody.\n")

    def titles(text: str) -> list[str | None]:
        tokens = parse(text)
        return [
            None if child.attrGet("title") is None else str(child.attrGet("title"))
            for inline in inlines(tokens, list(regions(tokens)))
            for _children, _at, child in events(inline.children or [])
            if child.type == LINK_OPEN
            and str(child.attrGet("href") or "") == "rules.md#steps"
        ]

    result = invoke("--entry", "entry.md", cwd=tmp_path)
    assert result.status == 0, result.stderr
    assert titles(result.bundle) == titles(source.removeprefix(DECLARED))
    assert "Body." not in result.bundle


def test_candidate_rejects_a_deferred_line_with_different_presets() -> None:
    text = '[↳ Steps](rules.md#steps "draft")\n'
    tokens = parse(text)
    [span] = list(regions(tokens))
    part = Instruction(text, activates=(("rules.md", "steps"), read_tags("checks")))
    with pytest.raises(Invalid) as refused:
        activation(part, span, tokens)
    assert refused.value.invariant == TARGET_INTEGRITY
