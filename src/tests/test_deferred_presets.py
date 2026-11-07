"""Published deferred selections execute with the content immediate links select."""

import shlex
from pathlib import Path
from urllib.parse import quote

import pytest
from test_cli import DECLARED, invoke, written

from prosiform.profile import parse
from prosiform.source import LINK_OPEN, events, inlines, regions


@pytest.mark.parametrize("composition", [False, True], ids=["plain", "composition"])
@pytest.mark.parametrize("reference_style", [False, True], ids=["inline", "reference"])
@pytest.mark.parametrize(
    ("scope", "heading", "fragment"),
    [
        ("Scope", "Instructions", "instructions"),
        ("Release Candidate Café", "Café instructions", "café-instructions"),
    ],
    ids=["unrelated-headings", "preset-words-in-headings"],
)
@pytest.mark.parametrize(
    ("title", "selected"),
    [
        (None, False),
        ("", False),
        ("unknown,default", False),
        (" Café, Release Candidate,unknown,CAFÉ ", True),
        ("\u2003release candidate,café\u2003", True),
    ],
    ids=["absent", "empty", "unmatched", "repeated-and-unknown", "unicode-space"],
)
def test_the_published_deferred_command_matches_immediate_selected_content(
    tmp_path: Path,
    composition: bool,
    reference_style: bool,
    scope: str,
    heading: str,
    fragment: str,
    title: str | None,
    selected: bool,
) -> None:
    suffix = "" if title is None else f' "{title}"'
    mark = "¬↳" if composition else "¬"
    destination = f"../library/task%20notes.md#{fragment}"
    if reference_style:
        link = f"[{mark} Read][material]\n\n[material]: {destination}{suffix}\n"
    else:
        link = f"[{mark} Read]({destination}{suffix})\n"
    source = DECLARED + f"# Guide\n\n## {scope}\n\n" + link
    written(tmp_path, "modes/guide.md", source)
    written(
        tmp_path,
        "library/task notes.md",
        "---\nprosiform:\n"
        "  Café:\n    subst: [{live.md: cached.md}]\n"
        "  Release Candidate:\n    subst: [{draft.md: reviewed.md}]\n"
        f"---\n# Material\n\n## {heading}\n\n"
        "Read [page](live.md#details) and [notes](draft.md#details).\n",
    )
    for name in ("live", "cached", "draft", "reviewed"):
        written(
            tmp_path,
            f"library/{name}.md",
            DECLARED + f"# {name.title()}\n\n## Details\n\n{name.title()} payload.\n",
        )

    deferred = invoke("modes/guide.md", cwd=tmp_path)
    assert deferred.status == 0, deferred.stderr
    assert "payload." not in deferred.bundle
    expected_destination = f"library/task%20notes.md#{quote(fragment)}"
    tokens = parse(deferred.bundle)
    [published] = [
        token
        for inline in inlines(tokens, list(regions(tokens)))
        for _children, _at, token in events(inline.children or [])
        if token.type == LINK_OPEN and token.attrGet("href") == expected_destination
    ]
    assert published.attrGet("title") == (title or None)
    words = ["pf", str(published.attrGet("href"))]
    if (presets := published.attrGet("title")) is not None:
        words += ["--presets", str(presets)]
    command = shlex.join(words)
    activated = invoke(*shlex.split(command)[1:], cwd=tmp_path)
    assert activated.status == 0, activated.stderr

    written(
        tmp_path, "modes/guide.md", source.replace(mark, "↳" if composition else "")
    )
    immediate = invoke("modes/guide.md", cwd=tmp_path)
    assert immediate.status == 0, immediate.stderr

    def payloads(bundle: str) -> tuple[str, ...]:
        return tuple(line for line in bundle.splitlines() if line.endswith(" payload."))

    expected = (
        ("Cached payload.", "Reviewed payload.")
        if selected
        else ("Live payload.", "Draft payload.")
    )
    assert payloads(activated.bundle) == payloads(immediate.bundle) == expected
    assert ("--p-" in next(iter(activated.bundles))) is selected

    default = invoke(expected_destination, cwd=tmp_path)
    assert default.status == 0, default.stderr
    assert payloads(default.bundle) == ("Live payload.", "Draft payload.")
    assert (payloads(default.bundle) != payloads(activated.bundle)) is selected
