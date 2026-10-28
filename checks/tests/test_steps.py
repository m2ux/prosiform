"""Assert the step check reads a procedure's steps as the convention writes them.

A step is a heading one level below its procedure, headed `N. Action`. The
reading is held to a document that meets the convention, to each way one
breaks it, to numbered lists written as examples inside a fenced and an
indented block, and to the work-planner example itself, which the check reads.
"""

import documents
import steps

CONVERTED = """\
# Plan Mode

## Procedure

### 1. Select

Read the board.

- Take the first item.

### 2. Publish

Publish the plan.

## Operations

### *Apply* Placement

#### 1. Read the Issue

#### 2. Save the Issue

#### Run Board Reads

##### 1. Read the Board
"""


def test_a_procedure_written_as_step_sub_sections_passes() -> None:
    assert steps.failures("mode.md", CONVERTED) == []


def test_a_numbered_step_at_column_zero_fails_naming_file_and_line() -> None:
    text = "# Mode\n\n## Procedure\n\n1. Fetch the issue.\n2. Save it.\n"
    found = steps.failures("mode.md", text)
    assert [failure.split(" — ")[0] for failure in found] == [
        "mode.md:5",
        "mode.md:6",
    ]


def test_a_numbered_list_inside_a_fenced_block_passes() -> None:
    text = "## Procedure\n\n```markdown\n1. Fetch the issue.\n2. Save it.\n```\n"
    assert steps.failures("mode.md", text) == []


def test_a_numbered_list_inside_an_indented_block_passes() -> None:
    text = "## Procedure\n\nAn example:\n\n    1. Fetch the issue.\n    2. Save it.\n"
    assert steps.failures("mode.md", text) == []


def test_a_numbered_step_nested_under_a_bullet_passes() -> None:
    text = "## Procedure\n\n### 1. Select\n\n- Read the board:\n  1. Take one.\n"
    assert steps.failures("mode.md", text) == []


def test_a_step_heading_two_levels_below_its_parent_fails() -> None:
    text = "## Procedure\n\n#### 1. Select\n"
    (failure,) = steps.failures("mode.md", text)
    assert failure.startswith("mode.md:3 — step heading '1. Select' sits 2 levels")


def test_a_step_heading_reads_its_parent_past_a_deeper_sibling() -> None:
    text = "## Procedure\n\n### 1. Select\n\n#### Detail\n\n### 2. Publish\n"
    assert steps.failures("mode.md", text) == []


def test_a_repeated_step_heading_in_one_document_fails() -> None:
    text = "## Plan\n\n### 1. Select\n\n## Sync\n\n### 1. Select\n"
    (failure,) = steps.failures("mode.md", text)
    assert failure.startswith("mode.md:7 — step heading '1. Select' repeats line 3")


def test_a_step_heading_repeated_across_documents_passes() -> None:
    text = "## Procedure\n\n### 1. Select\n"
    assert steps.failures("deliver.md", text) == []
    assert steps.failures("sync.md", text) == []


def test_a_numbered_title_without_a_full_stop_is_no_step() -> None:
    text = "## Procedure\n\n#### 2026 Plan\n"
    assert steps.failures("mode.md", text) == []


def test_the_scope_is_the_work_planner_example() -> None:
    paths = steps.scope()
    assert paths
    assert all(
        path.relative_to(documents.ROOT).as_posix().startswith(steps.TREE)
        for path in paths
    )


def test_the_work_planner_example_meets_the_convention() -> None:
    for path in steps.scope():
        assert steps.failures(path.name, path.read_text()) == []
