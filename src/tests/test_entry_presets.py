"""Explicit entry grammar and occurrence selection through the command path."""

from collections.abc import Callable
from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

from prosiform import cli, source
from prosiform.closure import BundleSelection
from prosiform.tags import read


@pytest.mark.parametrize(
    "arguments",
    [
        ("guide.md",),
        ("--entry", "guide.md", "--entry", "guide.md"),
        ("--entry", "guide.md", "--presets", "", "--presets", "checks"),
        ("--presets", "checks"),
        ("--entry", '[Guide](guide.md "checks")'),
        ("--entry", "guide.md", "--tags", "checks"),
        ("--ent", "guide.md"),
        ("--entry", "guide.md", "--pre", "checks"),
    ],
)
def test_the_single_entry_grammar_refuses_other_forms(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    written(tmp_path, "guide.md", DECLARED + "# Guide\n")
    run = invoke(*arguments, cwd=tmp_path)
    assert run.status == 2
    assert "E_INVALID_USAGE" in run.stderr
    assert run.bundles == {}


def test_an_entry_destination_may_contain_brackets_and_parentheses(
    tmp_path: Path,
) -> None:
    written(tmp_path, "[note](draft).md", DECLARED + "# Note\n\nBody.\n")
    run = invoke("--entry", "[note](draft).md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "Body." in run.bundle


PRESETS = (
    "---\nprosiform:\n"
    "  default:\n    subst: [{body.md: default.md}]\n"
    "  checks:\n    subst: [{body.md: checked.md}]\n"
    "  draft: {}\n---\n"
)


def tree(root: Path) -> None:
    written(
        root,
        "guide.md",
        PRESETS + "# Checks and Draft\n\n## Report\n\n[Body](body.md)\n",
    )
    for name in ("default", "checked"):
        written(root, name + ".md", DECLARED + "# Body\n\n" + name.upper() + "\n")


@pytest.mark.parametrize("fragment", ["", "#report"])
@pytest.mark.parametrize(
    "tags", ["checks,draft", " DRAFT,\u2003Checks,checks,unknown,default,, "]
)
def test_entry_and_authored_link_select_the_same_destination_presets(
    tmp_path: Path, fragment: str, tags: str
) -> None:
    tree(tmp_path)
    written(
        tmp_path,
        "entry.md",
        DECLARED + "[Label](guide.md" + fragment + ' "' + tags + '")\n',
    )
    direct = invoke("--entry", "guide.md" + fragment, "--presets", tags, cwd=tmp_path)
    linked = invoke("--entry", "entry.md", cwd=tmp_path)
    assert direct.status == linked.status == 0, (direct.stderr, linked.stderr)
    for run in (direct, linked):
        assert "CHECKED" in run.bundle
        assert "DEFAULT" not in run.bundle
        assert "unknown" not in run.stderr
    qualifier = "--p-13c9f40cda0225cb29b9fa2332a291e8950291238a73b75fed0cd1521986f6e8"
    expected = "guide" + ("__report" if fragment else "") + qualifier + ".bundle.md"
    assert list(direct.bundles) == [expected]


@pytest.mark.parametrize("tags", [None, "", "unknown,default"])
def test_headings_and_labels_select_no_presets(
    tmp_path: Path, tags: str | None
) -> None:
    tree(tmp_path)
    arguments = [] if tags is None else ["--presets", tags]
    run = invoke("--entry", "guide.md", *arguments, cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "DEFAULT" in run.bundle and "CHECKED" not in run.bundle
    assert list(run.bundles) == ["guide.bundle.md"]
    for heading, label in (("Checks", "Draft"), ("Unrelated", "Another label")):
        written(
            tmp_path,
            "entry.md",
            DECLARED + f'# {heading}\n\n[{label}](guide.md "checks")\n',
        )
        linked = invoke("--entry", "entry.md", cwd=tmp_path)
        assert linked.status == 0, linked.stderr
        assert "CHECKED" in linked.bundle and "DEFAULT" not in linked.bundle


def test_both_consumers_call_the_shared_reader(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tree(tmp_path)
    written(tmp_path, "entry.md", DECLARED + '[Link](guide.md "checks,draft")\n')
    calls: list[tuple[str, str | None]] = []

    def observe(consumer: str) -> Callable[[str | None], frozenset[str]]:
        def reading(text: str | None) -> frozenset[str]:
            calls.append((consumer, text))
            return read(text)

        return reading

    monkeypatch.setattr(cli, "read_tags", observe("cli"))
    monkeypatch.setattr(source, "read_tags", observe("source"))
    run = invoke("--entry", "entry.md", "--presets", "other", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert ("cli", "other") in calls
    assert ("source", "checks,draft") in calls


def test_a_selected_dispatch_names_and_compiles_its_qualified_bundle(
    tmp_path: Path,
) -> None:
    tree(tmp_path)
    written(
        tmp_path, "entry.md", DECLARED + '[⇉ Review](guide.md#report "checks,draft")\n'
    )
    run = invoke("--entry", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    name = cli.bundle_file(
        BundleSelection("guide.md", "report", frozenset({"checks", "draft"}))
    )
    assert f"]({name}" in run.bundle
    assert "CHECKED" in run.bundles[name]
    assert "DEFAULT" not in run.bundles[name]


def test_a_dispatch_only_input_inside_the_entry_run_folder_is_refused(
    tmp_path: Path,
) -> None:
    written(tmp_path, "guide.md", DECLARED + "# Guide\n\n[⇉ Task](task.md)\n")
    written(
        tmp_path, "task.md", DECLARED + "# Task\n\n[Rules](guide.bundles/rules.md)\n"
    )
    written(tmp_path, "guide.bundles/rules.md", DECLARED + "# Rules\n\nKeep.\n")
    run = invoke("--entry", "guide.md", "-o", str(tmp_path), cwd=tmp_path)
    assert run.status == 2
    assert "holds the input source" in run.stderr
    assert (tmp_path / "guide.bundles/rules.md").read_text().endswith("Keep.\n")


def test_the_guide_specifies_resolution_and_shell_quoting() -> None:
    run = invoke()  # invoke supplies -o; a bare invocation is observed in test_cli.
    assert run.status == 2
    guide = " ".join(cli.GUIDE.split())
    for rule in (
        "Resolve its destination from the document carrying the link",
        "Qualify a same-document fragment with that document's path",
        "its title as one --presets argument, shell-quoted where needed",
        "pf --entry modes/review.md#review --presets 'checks, final draft'",
        "Preserve the same tags when compiling a deferred link in a later run",
    ):
        assert rule in guide


def test_leading_dash_values_attach_to_their_options(tmp_path: Path) -> None:
    written(
        tmp_path,
        "-guide.md",
        "---\nprosiform:\n  '-checks':\n    group: {reviews: 1}\n---\n"
        "# Guide\n\nBody.\n",
    )
    run = invoke("--entry=-guide.md", "--presets=-checks", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "# Reviews\n\n## Guide\n\nBody." in run.bundle
    assert list(run.bundles)[0].startswith("-guide--p-")
    assert "pf --entry=-guide.md --presets=-checks" in cli.GUIDE


@pytest.mark.parametrize("tagged_first", [False, True])
def test_occurrences_union_explicit_group_pairs(
    tmp_path: Path, tagged_first: bool
) -> None:
    links = ["[Plain](rules.md)", '[Checks](rules.md "checks")']
    if tagged_first:
        links.reverse()
    written(tmp_path, "entry.md", DECLARED + "# Entry\n\n" + "\n\n".join(links))
    written(
        tmp_path,
        "rules.md",
        "---\nprosiform:\n  checks:\n    group: {reviews: 1}\n---\n"
        "# Rules\n\nRules body.\n",
    )
    run = invoke("--entry", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "\n# Rules\n" not in run.bundle
    assert "## Reviews\n\n### Rules\n\nRules body." in run.bundle
    assert run.bundle.count("Rules body.") == 1


@pytest.mark.parametrize("depth", [None, 1])
def test_a_later_occurrence_activates_substitution_at_the_reference_depth(
    tmp_path: Path, depth: int | None
) -> None:
    written(
        tmp_path,
        "entry.md",
        "---\nprosiform:\n  checks:\n    subst: [{old.md: new.md}]\n---\n"
        "# Guide\n\n[Body](old.md)\n",
    )
    written(tmp_path, "old.md", DECLARED + '# Old\n\n[Back](entry.md "checks")\n')
    written(tmp_path, "new.md", DECLARED + "# New\n\nSelected stand-in.\n")
    arguments = [] if depth is None else ["--budget", f"depth={depth}"]
    run = invoke("--entry", "entry.md", *arguments, cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "[Body](#new)" in run.bundle
    assert "Selected stand-in." in run.bundle
    assert "W_SUBST_USED" in run.stderr
