"""Round-trip evidence that what a bundle hands off is there to be followed.

A deferral states that material is compiled in a later run, and a dispatch
that a sub-agent follows a bundle the run published beside it. The corpus
asserts only the form each takes in the bundle. This suite bundles each mode
of a copy of the work-planner example, compiles each deferred destination in
a second run, and finds each dispatched bundle in the run's own folder, so the
handoff is held by runs rather than by a reading of the published bytes.

A destination is taken from the first bundle and never restated here. The
authoring string states what the mode linked to, and compiling that string
would assert that one string compiles twice; what is compiled is the
destination the build published. Each second bundle is compared whole, so a
heading level, a preamble or a section the destination did not select fails
the comparison rather than passing as a substring.

The command is resolved by name from the environment the suite runs in, which
is the entry point the packaging declares, so no configuration and no
environment variable names the build under test.
"""

import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import pytest

REPO = Path(__file__).resolve().parents[2]
EXAMPLE = REPO / "example" / "work-planner"
COMMAND = "pf"
ENCODING = "utf-8"

DISPATCH = "\u21c9"
DEFERRAL = "\u00ac"

ERROR = "error"
PROTOCOL = "\n## Dispatch\n"

INSTRUCTION = re.compile(
    r"^Dispatch `([^`]+)` to a sub-agent, as \[Dispatch\]\(#dispatch\) states\.$",
    re.MULTILINE,
)

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1", re.MULTILINE | re.DOTALL)
SPAN = re.compile(r"`[^`\n]*`")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

ARTIFACT = (
    "---\n"
    "prosiform:\n"
    '  root: ".."\n'
    '  group: "artifacts"\n'
    "  group-depth: 2\n"
    "---\n"
    "# {title}\n"
    "\n"
    "The artifact one mode hands to a later run.\n"
    "\n"
    "## Selection\n"
    "\n"
    "SELECTION_MARKER\n"
    "\n"
    "## Held\n"
    "\n"
    "HELD_MARKER\n"
)

MODE = (
    "---\n"
    "prosiform:\n"
    '  root: ".."\n'
    '  group: "modes"\n'
    "  group-depth: 2\n"
    "---\n"
    "# Plan Mode\n"
    "\n"
    "Scopes the solution.\n"
    "\n"
    "## Procedure\n"
    "\n"
    "{rules}"
)

SELECTED = "# Artifacts\n\n## Selection\n\nSELECTION_MARKER\n"

HELD = "# Artifacts\n\n## Held\n\nHELD_MARKER\n"

SECTION = {"selection": SELECTED, "held": HELD}


def artifact(title: str) -> str:
    """An artifact document with two sections a mode can select between."""
    return ARTIFACT.format(title=title)


def mode(*rules: str) -> str:
    """A mode whose procedure states one rule per line."""
    return MODE.format(rules="".join(f"- {rule}\n" for rule in rules))


def withheld(bundle: str) -> list[tuple[str, str]]:
    """Each link the bundle published as a destination a later run compiles.

    A link this run compiled is rewritten to an anchor in the document the
    bundle is, so a destination carrying a path is what a link whose copy a
    later run performs publishes. A reference carrying a scheme names material
    outside the root and is carried as its author wrote it, which is a
    citation rather than a handoff.

    A deferral publishes its text without the mark, so the destination is the
    whole of what states it and the label states nothing. A dispatch points at
    its sub-section, an anchor in the bundle itself.

    Code is published as its author wrote it, so a link a code block or span
    shows is an example of a link rather than one the bundle published.
    """
    prose = SPAN.sub("", FENCE.sub("", bundle))
    return [
        (label, destination)
        for label, destination in LINK.findall(prose)
        if not destination.startswith("#") and SCHEME.match(destination) is None
    ]


def dispatched(bundle: str) -> list[str]:
    """Each bundle file a dispatch sub-section of the bundle names."""
    return INSTRUCTION.findall(bundle)


@dataclass(frozen=True)
class Run:
    """One invocation: its status, the bundles it wrote and its diagnostics.

    The bundle is the entry's, named for the run's own folder.
    """

    status: int
    bundle: str
    diagnostics: list[dict[str, Any]]
    bundles: dict[str, str]

    def errors(self) -> list[dict[str, Any]]:
        """The diagnostics reporting a fault rather than a warning."""
        return [
            diagnostic
            for diagnostic in self.diagnostics
            if diagnostic["severity"] == ERROR
        ]


class Tree:
    """A copy of the example tree, and the invocations that compile in it."""

    def __init__(self, root: Path) -> None:
        shutil.copytree(EXAMPLE, root)
        self.root = root

    def write(self, path: str, text: str) -> None:
        """Write one document of this scenario into the copy."""
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding=ENCODING)

    def invoke(self, *arguments: str) -> Run:
        """One run from the copy's root into a fresh folder, diagnostics as data."""
        found = shutil.which(COMMAND)
        assert found is not None, f"{COMMAND} is not on the path of this environment"
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run(
                [found, "-d", "json", "-o", folder, *arguments],
                cwd=self.root,
                capture_output=True,
                text=True,
                encoding=ENCODING,
                timeout=60,
                check=False,
            )
            written = sorted(Path(folder).iterdir())
            assert len(written) <= 1, written
            bundles = (
                {
                    one.name: one.read_bytes().decode(ENCODING)
                    for one in written[0].iterdir()
                }
                if written
                else {}
            )
            entry = written[0].name.removesuffix(".bundles") if written else ""
            bundle = bundles[f"{entry}.bundle.md"] if written else ""
        assert result.stdout == ""
        diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
        return Run(result.returncode, bundle, diagnostics, bundles)

    def run(self, entry: str) -> Run:
        """The bundles one document publishes, which carry no error."""
        run = self.invoke(entry)
        assert run.status == 0, run.diagnostics
        assert run.errors() == [], run.diagnostics
        return run

    def bundled(self, entry: str) -> str:
        """The bundle one document publishes, which carries no error."""
        return self.run(entry).bundle

    def compiled(self, destination: str) -> Run:
        """A destination the first bundle published, compiled from this root."""
        return self.invoke(destination)

    def handoffs(self, entry: str) -> list[tuple[str, str]]:
        """The links one mode handed to a later run, each resolvable from the root.

        A mode reaches its artifact by a parent-relative path and the
        destination a later run follows is the target's path from the
        invocation directory, so a destination carrying a parent segment, or
        naming no document of this copy, is one no second run resolves. The
        section each destination names is required with it, because a
        destination that dropped its fragment would select the whole document.
        """
        found = withheld(self.bundled(entry))
        for _, destination in found:
            path, _, fragment = destination.partition("#")
            assert not path.startswith(".."), destination
            assert (self.root / unquote(path)).is_file(), destination
            assert fragment, destination
        return found

    def published(self, entry: str) -> list[tuple[str, str]]:
        """The destinations one mode published that name a document of this copy.

        A link landing outside the root stays as its author wrote it, so it
        names material no run from this root compiles and is a reference rather
        than a handoff.
        """
        found = []
        for label, destination in withheld(self.bundled(entry)):
            path = unquote(destination.partition("#")[0])
            target = (self.root / path).resolve()
            inside = target.is_relative_to(self.root.resolve()) and target.is_file()
            if inside:
                found.append((label, destination))
        return found

    def modes(self) -> list[str]:
        """Every mode of this copy, as an entry named from its root."""
        return sorted(
            path.relative_to(self.root).as_posix()
            for path in (self.root / "modes").glob("*.md")
        )


@pytest.fixture
def tree(tmp_path: Path) -> Tree:
    """A fresh copy of the example tree for one scenario."""
    return Tree(tmp_path / "example")


def assert_published(run: Run, expected: str) -> None:
    """The second run published exactly the expected document and no error."""
    assert run.errors() == [], run.diagnostics
    assert run.status == 0, run.diagnostics
    assert run.bundle == expected


def handoff(tree: Tree, entry: str) -> tuple[str, str]:
    """The one link a mode handed to a later run, with its published destination."""
    found = tree.handoffs(entry)
    assert len(found) == 1, found
    return found[0]


def test_a_dispatched_bundle_is_published_beside_the_entry(tree: Tree) -> None:
    """A dispatched link names a bundle the run published, holding its section."""
    tree.write("artifacts/handoff.md", artifact("Handoff"))
    tree.write(
        "modes/handoff.md",
        mode(f"Run [{DISPATCH} Selection](../artifacts/handoff.md#selection)."),
    )
    run = tree.run("modes/handoff.md")
    assert tree.handoffs("modes/handoff.md") == []
    assert dispatched(run.bundle) == ["artifacts_handoff__selection.bundle.md"]
    assert run.bundles["artifacts_handoff__selection.bundle.md"] == SELECTED
    assert_published(tree.compiled("artifacts/handoff.md#selection"), SELECTED)


def test_a_deferred_destination_compiles(tree: Tree) -> None:
    """A deferred link's published destination yields its selected section."""
    tree.write("artifacts/handoff.md", artifact("Handoff"))
    tree.write(
        "modes/handoff.md",
        mode(f"Run [{DEFERRAL} Selection](../artifacts/handoff.md#selection)."),
    )
    label, destination = handoff(tree, "modes/handoff.md")
    assert DEFERRAL not in label, label
    assert_published(tree.compiled(destination), SELECTED)


def test_an_escaped_destination_compiles(tree: Tree) -> None:
    """A destination carrying a URI escape is resolved back by the second run."""
    tree.write("artifacts/caf\u00e9.md", artifact("Caf\u00e9"))
    tree.write(
        "modes/handoff.md",
        mode(f"Run [{DEFERRAL} Held](../artifacts/caf\u00e9.md#held)."),
    )
    _, destination = handoff(tree, "modes/handoff.md")
    assert "%" in destination, destination
    assert_published(tree.compiled(destination), HELD)


def test_both_handoffs_of_one_bundle_are_followed(tree: Tree) -> None:
    """One mode holding both operators hands off a bundle and a destination."""
    tree.write("artifacts/handoff.md", artifact("Handoff"))
    tree.write(
        "modes/handoff.md",
        mode(
            f"Run [{DISPATCH} Selection](../artifacts/handoff.md#selection).",
            f"Run [{DEFERRAL} Held](../artifacts/handoff.md#held).",
        ),
    )
    run = tree.run("modes/handoff.md")
    assert run.bundles["artifacts_handoff__selection.bundle.md"] == SELECTED
    label, destination = handoff(tree, "modes/handoff.md")
    assert DEFERRAL not in label and DISPATCH not in label, label
    path, _, fragment = destination.partition("#")
    assert (path, fragment) == ("artifacts/handoff.md", "held"), destination
    assert_published(tree.compiled(destination), SECTION[fragment])


def test_each_handoff_the_example_publishes_is_followed(tree: Tree) -> None:
    """Every handoff a mode of the example publishes can be followed.

    Each mode is bundled as its own entry. Each bundle a dispatch sub-section
    names is in that run's folder, and each distinct deferred destination the
    bundles published is compiled once in a second run. The example dispatches
    and defers, so both handoffs are among them.
    """
    published: dict[str, str] = {}
    named = 0
    for entry in tree.modes():
        run = tree.run(entry)
        for name in dispatched(run.bundle):
            assert name in run.bundles, (entry, name)
            named += 1
        for label, destination in tree.published(entry):
            published.setdefault(destination, label)
    assert named, "the example dispatches nothing"
    assert published, "the example defers nothing"
    for destination in published:
        run = tree.compiled(destination)
        assert run.errors() == [], (destination, run.diagnostics)
        assert run.status == 0, (destination, run.diagnostics)
        assert run.bundle, destination


def test_a_mode_bundle_carries_the_dispatch_protocol_once(tree: Tree) -> None:
    """A dispatching mode bundle opens with its Prosiform section's one protocol."""
    bundle = tree.bundled("modes/plan-mode.md")
    assert bundle.startswith("# Prosiform\n"), bundle
    assert bundle.count(PROTOCOL) == 1, bundle
