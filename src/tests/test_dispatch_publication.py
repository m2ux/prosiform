"""Dispatch occurrences publish the bundle for their effective preset selection."""

from io import StringIO
from pathlib import Path
from urllib.parse import quote, unquote

import pytest
from test_cli import DECLARED, invoke, written

from prosiform import cli
from prosiform.cli import GUIDE
from prosiform.closure import BundleSelection
from prosiform.dispatch import PARALLEL


def test_a_dispatch_set_publishes_its_members_as_dispatch_lines(tmp_path: Path) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Work\n\n[⫽ A](a.md)\n\n[⫽ B](b.md)\n",
    )
    written(tmp_path, "a.md", DECLARED + "# A\n")
    written(tmp_path, "b.md", DECLARED + "# B\n")
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "its section holds one set of bundles, listed as ⇉ lines." in " ".join(
        GUIDE.split()
    )
    assert f"### {PARALLEL}\n\n[⇉ A](a.bundle.md)\n[⇉ B](b.bundle.md)" in run.bundle
    assert "Give each of these" not in run.bundle
    assert "- [⇉" not in run.bundle


def task(root: Path) -> None:
    """One target with two observable destination-owned substitutions."""
    written(
        root,
        "task.md",
        "---\nprosiform:\n"
        "  checks:\n    subst: [{body.md: checked.md}]\n"
        "  draft:\n    subst: [{body.md: drafted.md}]\n"
        "  audit: {}\n"
        "---\n# Task\n\n[Body](body.md)\n",
    )
    for name, body in (
        ("body", "DEFAULT_BODY"),
        ("checked", "CHECKED_BODY"),
        ("drafted", "DRAFTED_BODY"),
    ):
        written(root, name + ".md", DECLARED + "# Body\n\n" + body + "\n")


def test_inline_dispatches_of_one_target_point_to_their_selected_contents(
    tmp_path: Path,
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n[⇉ Checks](task.md "checks")\n\n'
        '[⇉ Draft](task.md "draft")\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    drafted = next(name for name, body in run.bundles.items() if "DRAFTED_BODY" in body)
    assert checked != drafted
    assert checked == "task-checks.bundle.md"
    assert drafted == "task-draft.bundle.md"
    assert f'[⇉ Checks]({checked} "checks")' in run.bundle
    assert f'[⇉ Draft]({drafted} "draft")' in run.bundle
    assert len(run.bundles) == 3


def test_a_preset_and_source_name_collision_preserves_the_published_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n[⇉ Checks](task.md "checks")\n\n'
        '[⇉ Draft](task.md "draft")\n',
    )
    monkeypatch.chdir(tmp_path)
    assert cli.main(["-o", "out", "guide.md"], StringIO(), StringIO()) == 0
    published = {
        str(path.relative_to(tmp_path)): path.read_bytes()
        for path in (tmp_path / "out").rglob("*")
        if path.is_file()
    }
    written(tmp_path, "task-checks.md", DECLARED + "# Another Task\n")
    guide = tmp_path / "guide.md"
    guide.write_text(guide.read_text() + "\n[⇉ Other](task-checks.md)\n")
    errors = StringIO()
    assert cli.main(["-o", "out", "guide.md"], StringIO(), errors) == 3
    assert "E_PUBLICATION_FAILED" in errors.getvalue()
    assert "task-checks.md" in errors.getvalue() and "task.md" in errors.getvalue()
    assert published == {
        str(path.relative_to(tmp_path)): path.read_bytes()
        for path in (tmp_path / "out").rglob("*")
        if path.is_file()
    }


@pytest.mark.parametrize("preset", ["a+b", "a/b", "a%2Fb", "Release Candidate", "Café"])
def test_preset_names_publish_as_one_file_with_resolving_links(
    tmp_path: Path, preset: str
) -> None:
    written(tmp_path, "task.md", f'---\nprosiform:\n  "{preset}": {{}}\n---\n# Task\n')
    written(
        tmp_path, "guide.md", DECLARED + f'# Guide\n\n[⇉ Task](task.md "{preset}")\n'
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    expected = "task-" + quote(preset, safe="") + ".bundle.md"
    assert set(run.bundles) == {"guide.bundle.md", expected}
    destination = quote(expected, safe="")
    assert f"]({destination}" in run.bundle
    assert unquote(destination) == expected


def test_a_literal_plus_and_two_presets_have_distinct_names(tmp_path: Path) -> None:
    written(
        tmp_path,
        "task.md",
        '---\nprosiform:\n  a: {}\n  b: {}\n  "a+b": {}\n---\n# Task\n',
    )
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n[⇉ Both](task.md "b,a")\n\n[⇉ Literal](task.md "a+b")\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert set(run.bundles) == {
        "guide.bundle.md",
        "task-a+b.bundle.md",
        "task-a%2Bb.bundle.md",
    }
    assert (
        cli.run_folder(
            tmp_path, BundleSelection("task.md", presets=frozenset({"b", "a"}))
        ).name
        == "task-a+b.bundles"
    )


@pytest.mark.parametrize(
    ("first", "second", "content"),
    [
        ("checks", "Checks,unknown,default,checks", "CHECKED_BODY"),
        ("checks,audit", " AUDIT, checks,unknown,default, ", "CHECKED_BODY"),
        ("", "unknown,default", "DEFAULT_BODY"),
    ],
)
def test_equivalent_parallel_occurrences_publish_single_direct_dispatches(
    tmp_path: Path, first: str, second: str, content: str
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + f'# Guide\n\n[⫽ First](task.md "{first}")\n\n'
        f'[⫽ Second](task.md "{second}")\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert len(run.bundles) == 2
    name = next(name for name, body in run.bundles.items() if content in body)
    assert f'[⇉ First]({quote(name, safe="")} "{first}")' in run.bundle
    assert f'[⇉ Second]({quote(name, safe="")} "{second}")' in run.bundle
    assert PARALLEL not in run.bundle


def test_parallel_members_distinguish_variants_and_merge_equivalent_requests(
    tmp_path: Path,
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n[⫽ Checks First](task.md "checks")\n\n'
        '[⫽ Checks Again](task.md "CHECKS,unknown")\n\n'
        '[⫽ Draft First](task.md "draft")\n\n'
        '[⫽ Draft Again](task.md "draft,default")\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert len(run.bundles) == 3
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    drafted = next(name for name, body in run.bundles.items() if "DRAFTED_BODY" in body)
    assert f"[⇉ Checks First]({checked})" in run.bundle
    assert f"[⇉ Draft First]({drafted})" in run.bundle
    assert "[⇉ Checks Again]" not in run.bundle
    assert "[⇉ Draft Again]" not in run.bundle
    assert run.bundle.count("](#⫽-dispatch-set") == 4
    assert PARALLEL in run.bundle


def test_equivalent_parallel_selection_in_an_h6_needs_no_subsection(
    tmp_path: Path,
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n##### Last\n\n[⫽ First](task.md "checks")\n\n'
        '[⫽ Second](task.md "checks,unknown")\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "E_HEADING_DEPTH_OVERFLOW" not in run.stderr
    assert PARALLEL not in run.bundle


def test_a_heading_inline_set_publishes_distinct_selection_members(
    tmp_path: Path,
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n## [⫽ Checks](task.md "checks") and '
        '[⫽ Draft](task.md "draft")\n\nSection content.\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    drafted = next(name for name, body in run.bundles.items() if "DRAFTED_BODY" in body)
    assert '[Checks](#⫽-dispatch-set "checks")' in run.bundle
    assert '[Draft](#⫽-dispatch-set "draft")' in run.bundle
    assert f"[⇉ Checks]({checked})" in run.bundle
    assert f"[⇉ Draft]({drafted})" in run.bundle


def test_a_heading_inline_set_collapses_equivalent_selection_members(
    tmp_path: Path,
) -> None:
    task(tmp_path)
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Guide\n\n## [⫽ First](task.md "checks") and '
        '[⫽ Second](task.md "Checks,unknown,default")\n\nSection content.\n',
    )
    run = invoke("guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    assert f'[⇉ First]({checked} "checks")' in run.bundle
    assert f'[⇉ Second]({checked} "Checks,unknown,default")' in run.bundle
    assert PARALLEL not in run.bundle
