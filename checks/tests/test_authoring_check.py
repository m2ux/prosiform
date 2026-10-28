"""The authoring check reports each departure from the example's authoring rules.

Each finding kind is one rule the work-planner guidelines state: Inputs and
Outputs lines of contract links or `None`, no Commands section, a command in
an unindented fenced block within a step, and file-relative links. A document
meeting every rule reports nothing, and the size report names a file past
either limit without making it a finding.
"""

from pathlib import Path

import authoring

PASSING = """\
---
prosiform:
  root: ".."
---
# Planning Record

A planning record is a folder.

## Operations

### Publish Planning Record

The record's folder committed and pushed.

**Inputs:** [Planning folder](#layout), [Message file](other.md#message)
**Outputs:** None

#### 1. Commit the Folder

Commit the folder from the engineering worktree.

```bash
git commit -F '<message-file>'
```

#### 2. Push the Branch

Push it, as [Layout](#layout) and [Other](other.md) state.

### Locate Planning Record

The folder for one number.

**Inputs:** None

**Outputs:** [Planning folder](#layout)

- List the matching folders.

```bash
ls '<engineering-worktree>'
```

## Fields

### Layout

```markdown
## Commands

### Template Command

```

The folder holds README.md.
"""


def write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def findings(
    tmp_path: Path, text: str, name: str = "artifacts/record.md"
) -> list[authoring.Finding]:
    path = write(tmp_path, name, text)
    write(tmp_path, "artifacts/other.md", "# Other\n\n## Message\n")
    return authoring.report(path, name, text)[0]


def line_of(text: str, needle: str, occurrence: int = 1) -> int:
    """The line holding the nth occurrence of a needle, counted from one."""
    numbers = [n for n, line in enumerate(text.splitlines(), 1) if needle in line]
    return numbers[occurrence - 1]


def kinds(found: list[authoring.Finding]) -> list[tuple[str, int]]:
    return [(finding.kind, finding.line) for finding in found]


def test_a_file_meeting_every_rule_reports_nothing(tmp_path: Path) -> None:
    assert findings(tmp_path, PASSING) == []


def test_a_command_in_a_steps_fenced_block_is_no_finding(tmp_path: Path) -> None:
    found = findings(tmp_path, PASSING)
    assert authoring.COMMAND_PLACEMENT not in {finding.kind for finding in found}


def test_prose_inputs_and_a_missing_outputs_line_are_findings(tmp_path: Path) -> None:
    text = PASSING.replace(
        "**Inputs:** [Planning folder](#layout), [Message file](other.md#message)\n"
        "**Outputs:** None\n",
        "**Inputs:** Planning-folder path and a commit message file.\n",
    )
    found = findings(tmp_path, text)
    assert kinds(found) == [
        (authoring.INPUTS, line_of(text, "### Publish")),
        (authoring.INPUTS, line_of(text, "**Inputs:** Planning")),
    ]
    assert "no **Outputs:** line" in found[0].detail
    assert "Inputs is not None" in found[1].detail


def test_a_link_without_a_contract_section_is_a_finding(tmp_path: Path) -> None:
    text = PASSING.replace("**Outputs:** None", "**Outputs:** [Folder](other.md)")
    assert kinds(findings(tmp_path, text)) == [
        (authoring.INPUTS, line_of(text, "**Outputs:** [Folder]"))
    ]


def test_inputs_running_onto_a_second_line_is_a_finding(tmp_path: Path) -> None:
    text = PASSING.replace(
        "**Inputs:** None\n", "**Inputs:** None\nand the number to look up.\n"
    )
    found = findings(tmp_path, text)
    at = line_of(text, "**Inputs:** None")
    assert kinds(found) == [(authoring.INPUTS, at)]
    assert f"runs onto line {at + 1}" in found[0].detail


def test_a_commands_section_and_each_command_in_it_are_findings(
    tmp_path: Path,
) -> None:
    text = (
        PASSING
        + "\n## Commands\n\n### Find Worktree\n\n```bash\ngit worktree list\n```\n"
    )
    found = findings(tmp_path, text)
    assert kinds(found) == [
        (authoring.COMMANDS_SECTION, line_of(text, "## Commands", 2)),
        (authoring.COMMAND_PLACEMENT, line_of(text, "```bash", 3)),
    ]
    assert "outside a step, under 'Find Worktree'" in found[1].detail


def test_a_file_with_no_commands_heading_is_no_commands_finding(
    tmp_path: Path,
) -> None:
    text = (
        "# Guidelines\n\n## Operations\n\n- **Commands in steps.**\n"
        "  No file has a Commands section, and a `## Commands` heading is retired.\n"
    )
    assert findings(tmp_path, text, "guidelines.md") == []


def test_an_indented_fenced_command_is_a_finding(tmp_path: Path) -> None:
    text = PASSING.replace(
        "```bash\ngit commit -F '<message-file>'\n```",
        "- Commit it.\n\n  ```bash\n  git commit -F '<message-file>'\n  ```",
    )
    found = findings(tmp_path, text)
    assert kinds(found) == [(authoring.COMMAND_PLACEMENT, line_of(text, "  ```bash"))]
    assert "its fence is indented" in found[0].detail


def test_a_command_in_fields_is_outside_a_step(tmp_path: Path) -> None:
    text = PASSING + "\n```bash\ngh api user\n```\n"
    found = findings(tmp_path, text)
    assert kinds(found) == [(authoring.COMMAND_PLACEMENT, line_of(text, "```bash", 3))]
    assert "under 'Layout'" in found[0].detail


def test_an_absolute_link_is_a_finding(tmp_path: Path) -> None:
    text = PASSING.replace("[Other](other.md)", "[Other](/artifacts/other.md)")
    found = findings(tmp_path, text)
    assert kinds(found) == [(authoring.FILE_RELATIVE, line_of(text, "(/artifacts"))]
    assert "absolute path" in found[0].detail


def test_a_link_written_from_the_declared_root_is_a_finding(
    tmp_path: Path,
) -> None:
    write(tmp_path, "rules.md", "# Rules\n")
    text = '---\nprosiform:\n  root: ".."\n---\n# Mode\n\nSee [Rules](rules.md).\n'
    found = findings(tmp_path, text, "modes/plan-mode.md")
    assert kinds(found) == [(authoring.FILE_RELATIVE, 7)]
    assert "declared root" in found[0].detail
    relative = text.replace("(rules.md)", "(../rules.md)")
    assert findings(tmp_path, relative, "modes/plan-mode.md") == []


def test_a_repository_url_to_a_held_file_is_a_finding(tmp_path: Path) -> None:
    url = "https://github.com/m2ux/prosiform/blob/main/README.md"
    text = f"# Mode\n\nSee [the readme]({url}).\n"
    found = findings(tmp_path, text, "modes/plan-mode.md")
    assert kinds(found) == [(authoring.FILE_RELATIVE, 3)]
    assert "repository URL" in found[0].detail


def test_a_link_in_literal_content_is_no_finding(tmp_path: Path) -> None:
    text = (
        "# Mode\n\nWrite `[Rules](/rules.md)`, never:\n\n"
        "```text\n[Rules](/rules.md)\n```\n"
    )
    assert findings(tmp_path, text, "modes/plan-mode.md") == []


def test_the_size_report_names_a_file_past_either_limit(tmp_path: Path) -> None:
    operation = (
        "### Read Item {n}\n\nOne item.\n\n**Inputs:** None\n**Outputs:** None\n\n"
    )
    many = "# Board\n\n## Operations\n\n" + "".join(
        operation.format(n=n) for n in range(9)
    )
    path = write(tmp_path, "artifacts/board.md", many)
    found, count = authoring.report(path, "artifacts/board.md", many)
    assert found == []
    assert count == 9
    assert authoring.oversized(len(many.encode()), count)
    assert not authoring.oversized(len(many.encode()), 8)
    assert authoring.oversized(authoring.SIZE_LIMIT + 1, 0)
    assert not authoring.oversized(authoring.SIZE_LIMIT, 0)


def test_each_document_falls_in_one_area() -> None:
    tree = authoring.TREE
    assert authoring.area(f"{tree}modes/plan-mode.md") == "modes"
    assert authoring.area(f"{tree}protocols/task-merge.md") == "protocols"
    assert authoring.area(f"{tree}artifacts/board.md") == "artifacts"
    assert authoring.area(f"{tree}references/notes.md") == "references"
    assert authoring.area(f"{tree}SKILL.md") == authoring.ENTRY
    assert authoring.area(f"{tree}guidelines.md") == authoring.ENTRY
