"""Round-trip evidence that the destinations a bundle publishes compile.

Both operators state that material is compiled in a later run, and the corpus
asserts only the form that material takes in the bundle. This suite bundles a
copy of the work-tracker example, reads the destinations the bundle published,
and compiles each of them in a second run, so the handoff is held by runs
rather than by a reading of the published bytes.

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
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import pytest

REPO = Path(__file__).resolve().parents[2]
EXAMPLE = REPO / "example" / "work-tracker"
COMMAND = "pf"
ENCODING = "utf-8"

DISPATCH = "\u00bb"
DEFERRAL = "\u00ac"

GENERATED_INPUT = "E_GENERATED_INPUT"
ERROR = "error"
ENTRY = "Follow ["

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
DECLARATION = re.compile(r"^  dispatch: (.+)$", re.M)

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

SELECTED = (
    "Follow [Selection](#selection). The other sections are material that "
    "procedure references.\n"
    "\n"
    "# Artifacts\n"
    "\n"
    "## Selection\n"
    "\n"
    "SELECTION_MARKER\n"
)

HELD = (
    "Follow [Held](#held). The other sections are material that "
    "procedure references.\n"
    "\n"
    "# Artifacts\n"
    "\n"
    "## Held\n"
    "\n"
    "HELD_MARKER\n"
)

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

    A dispatch publishes its mark, because the mark is what tells a reader who
    compiles the material. A deferral publishes its text without the mark, so
    the destination is the whole of what states it and the label states
    nothing.
    """
    return [
        (label, destination)
        for label, destination in LINK.findall(bundle)
        if not destination.startswith("#") and SCHEME.match(destination) is None
    ]


def declared_dispatch(skill: Path) -> str:
    """The dispatch text the entry document declares."""
    found = DECLARATION.search(skill.read_text(encoding=ENCODING))
    assert found is not None, f"{skill} declares no dispatch text"
    return found.group(1).strip().strip('"')


@dataclass(frozen=True)
class Run:
    """One invocation and what it carried on each of its streams."""

    status: int
    stdout: str
    diagnostics: list[dict[str, Any]]

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

    def read(self, path: str) -> str:
        """One document of this copy as it stands."""
        return (self.root / path).read_text(encoding=ENCODING)

    def invoke(self, *arguments: str) -> Run:
        """One invocation from the copy's root, diagnostics read as data."""
        found = shutil.which(COMMAND)
        assert found is not None, f"{COMMAND} is not on the path of this environment"
        result = subprocess.run(
            [found, "-d", "json", *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding=ENCODING,
            timeout=60,
            check=False,
        )
        diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
        return Run(result.returncode, result.stdout, diagnostics)

    def bundled(self, entry: str) -> str:
        """The bundle one document publishes, which carries no error."""
        run = self.invoke("-o", "-", entry)
        assert run.status == 0, run.diagnostics
        assert run.errors() == [], run.diagnostics
        return run.stdout

    def compiled(self, destination: str) -> Run:
        """A destination the first bundle published, compiled from this root."""
        return self.invoke("-o", "-", destination)

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


@pytest.fixture
def tree(tmp_path: Path) -> Tree:
    """A fresh copy of the example tree for one scenario."""
    return Tree(tmp_path / "example")


def assert_published(run: Run, expected: str) -> None:
    """The second run published exactly the expected document and no error."""
    assert run.errors() == [], run.diagnostics
    assert run.status == 0, run.diagnostics
    assert run.stdout == expected


def handoff(tree: Tree, entry: str) -> tuple[str, str]:
    """The one link a mode handed to a later run, with its published destination."""
    found = tree.handoffs(entry)
    assert len(found) == 1, found
    return found[0]


def test_a_dispatched_destination_compiles(tree: Tree) -> None:
    """A dispatched link's published destination yields its selected section."""
    tree.write("artifacts/handoff.md", artifact("Handoff"))
    tree.write(
        "modes/handoff.md",
        mode(f"Run [{DISPATCH} Selection](../artifacts/handoff.md#selection)."),
    )
    label, destination = handoff(tree, "modes/handoff.md")
    assert label.startswith(DISPATCH), label
    assert_published(tree.compiled(destination), SELECTED)


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
        mode(f"Run [{DISPATCH} Held](../artifacts/caf\u00e9.md#held)."),
    )
    _, destination = handoff(tree, "modes/handoff.md")
    assert "%" in destination, destination
    assert_published(tree.compiled(destination), HELD)


def test_both_destinations_of_one_bundle_compile(tree: Tree) -> None:
    """One mode holding both operators publishes two destinations that compile."""
    tree.write("artifacts/handoff.md", artifact("Handoff"))
    tree.write(
        "modes/handoff.md",
        mode(
            f"Run [{DISPATCH} Selection](../artifacts/handoff.md#selection).",
            f"Run [{DEFERRAL} Held](../artifacts/handoff.md#held).",
        ),
    )
    found = tree.handoffs("modes/handoff.md")
    assert len(found) == 2, found
    labels = [label for label, _ in found]
    assert sum(label.startswith(DISPATCH) for label in labels) == 1, labels
    assert all(DEFERRAL not in label for label in labels), labels
    compiled: dict[str, str] = {}
    for _, destination in found:
        path, _, fragment = destination.partition("#")
        assert path == "artifacts/handoff.md", destination
        assert fragment in SECTION, destination
        run = tree.compiled(destination)
        assert_published(run, SECTION[fragment])
        compiled[fragment] = run.stdout
    assert sorted(compiled) == sorted(SECTION), compiled


def test_a_declared_dispatch_text_reaches_the_entry_line(tree: Tree) -> None:
    """A mode linking the entry document's dispatch section carries its text."""
    text = declared_dispatch(tree.root / "SKILL.md")
    bundle = tree.bundled("modes/plan-mode.md")
    openings = [line for line in bundle.splitlines() if line.startswith(ENTRY)]
    assert len(openings) == 1, openings
    assert openings[0].endswith(f" {text}"), openings[0]
    assert bundle.count(text) == 1, bundle


def test_a_published_bundle_offered_as_input_is_refused(tree: Tree) -> None:
    """A bundle this run published is refused at the line its declaration occupies."""
    published = tree.bundled("modes/plan-mode.md")
    written = tree.invoke("-o", "bundle.md", "modes/plan-mode.md")
    assert written.status == 0, written.diagnostics
    assert tree.read("bundle.md") == published
    lines = tree.read("bundle.md").splitlines()
    refusal = tree.invoke("bundle.md")
    assert refusal.status == 1, refusal.diagnostics
    assert refusal.stdout == ""
    errors = refusal.errors()
    assert [error["code"] for error in errors] == [GENERATED_INPUT], errors
    reference = errors[0]["reference"]
    assert reference.startswith(ENTRY), reference
    occupied = lines.index(reference) + 1
    assert lines[0].startswith("# "), lines[0]
    assert occupied > 1, occupied
    assert errors[0]["source"] == f"bundle.md:{occupied}", errors[0]["source"]
