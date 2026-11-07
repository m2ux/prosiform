"""Each effective dispatch selection retains its publication and diagnostic facts."""

from pathlib import Path

from test_cli import DECLARED, invoke, written


def test_variant_substitutions_to_distinct_sections_report_each_pair(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entry.md",
        DECLARED
        + '# Entry\n\n[⇉ Checks](task.md "checks") [⇉ Draft](task.md "draft")\n',
    )
    written(
        tmp_path,
        "task.md",
        "---\nprosiform:\n"
        "  checks:\n    subst: [{rules.md: alternatives.md#checks}]\n"
        "  draft:\n    subst: [{rules.md: alternatives.md#draft}]\n---\n"
        "# Task\n\n[Rules](rules.md)\n",
    )
    written(
        tmp_path,
        "alternatives.md",
        DECLARED
        + "# Alternatives\n\n## Checks\n\nCHECKED_BODY\n\n## Draft\n\nDRAFT_BODY\n",
    )
    run = invoke("-d", "json", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    used = [one for one in run.diagnostics() if one["code"] == "W_SUBST_USED"]
    assert [one["resolved"] for one in used] == [
        "alternatives.md#checks",
        "alternatives.md#draft",
    ]
    assert len(run.bundles) == 3
    assert sum("CHECKED_BODY" in body for body in run.bundles.values()) == 1
    assert sum("DRAFT_BODY" in body for body in run.bundles.values()) == 1


def test_a_pair_used_by_one_variant_leaves_another_variants_pair_unused(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entry.md",
        DECLARED
        + '# Entry\n\n[⇉ Use](task.md#use "checks") [⇉ Quiet](task.md#quiet "draft")\n',
    )
    written(
        tmp_path,
        "task.md",
        "---\nprosiform:\n"
        "  checks:\n    subst: [{rules.md: checked.md}]\n"
        "  draft:\n    subst: [{rules.md: drafted.md}]\n---\n"
        "# Task\n\n## Use\n\n[Rules](rules.md)\n\n## Quiet\n\nNo dependency.\n",
    )
    written(tmp_path, "checked.md", DECLARED + "# Checked\n")
    written(tmp_path, "drafted.md", DECLARED + "# Drafted\n")
    run = invoke("-d", "json", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    unused = [one for one in run.diagnostics() if one["code"] == "W_SUBST_UNUSED"]
    assert len(unused) == 1
    assert "prosiform.draft" in unused[0]["message"]
    assert unused[0]["source"] == "rules.md"


def test_an_unselected_heading_with_parallel_links_needs_no_target_capture(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + "# Guide\n\n## Kept\n\nSelected body.\n\n"
        '## [⫽ First](task.md "checks") [⫽ Second](task.md "draft")\n\nUnselected.\n',
    )
    written(
        tmp_path, "task.md", "---\nprosiform:\n  checks: {}\n  draft: {}\n---\n# Task\n"
    )
    run = invoke("guide.md#kept", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "Selected body." in run.bundle
    assert "Unselected." not in run.bundle
    assert len(run.bundles) == 1


def test_a_parallel_link_in_an_unselected_title_is_refused_as_unplaced(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "guide.md",
        DECLARED + '# Top [⫽ First](task.md "checks") [⫽ Second](task.md "draft")\n\n'
        "## Kept\n\nSelected body.\n",
    )
    written(
        tmp_path, "task.md", "---\nprosiform:\n  checks: {}\n  draft: {}\n---\n# Task\n"
    )
    run = invoke("-d", "json", "guide.md#kept", cwd=tmp_path)
    assert run.status == 1, run.stderr
    assert run.bundles == {}
    assert run.diagnostics()[0]["code"] == "E_UNSUPPORTED_CONSTRUCT"
