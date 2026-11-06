"""Dispatch occurrences publish the bundle for their effective preset selection."""

from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

from prosiform.cli import GUIDE
from prosiform.dispatch import PARALLEL


def test_dispatch_guide_names_the_structure_the_compiler_emits(tmp_path: Path) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Work\n\n[⫽ A](a.md)\n\n[⫽ B](b.md)\n",
    )
    written(tmp_path, "a.md", DECLARED + "# A\n")
    written(tmp_path, "b.md", DECLARED + "# B\n")
    run = invoke("--entry", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert f"sub-section headed {PARALLEL}." in " ".join(GUIDE.split())
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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    drafted = next(name for name, body in run.bundles.items() if "DRAFTED_BODY" in body)
    assert checked != drafted
    assert f'[⇉ Checks]({checked} "checks")' in run.bundle
    assert f'[⇉ Draft]({drafted} "draft")' in run.bundle
    assert len(run.bundles) == 3


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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert len(run.bundles) == 2
    name = next(name for name, body in run.bundles.items() if content in body)
    assert f'[⇉ First]({name} "{first}")' in run.bundle
    assert f'[⇉ Second]({name} "{second}")' in run.bundle
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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
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
    run = invoke("--entry", "guide.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked = next(name for name, body in run.bundles.items() if "CHECKED_BODY" in body)
    assert f'[⇉ First]({checked} "checks")' in run.bundle
    assert f'[⇉ Second]({checked} "Checks,unknown,default")' in run.bundle
    assert PARALLEL not in run.bundle
