"""Assert the table check reads a Makefile, a project definition and a table.

What the check compares is three readings: the targets a `Makefile` declares,
the declarations `src/pyproject.toml` carries, and the rows a document's tables
hold. Each is held here to input it would be read wrongly: a `Makefile` whose
assignments, directives and recipe lines are not targets, a project definition
whose requirements carry extras, markers and spacing, and a document whose
tables sit beside a fenced example, carry an escaped pipe, and wrap a cell
across the source lines.
"""

from pathlib import Path

import pytest
import tables
from documents import plain
from documents import tables as read_tables

MAKEFILE = """\
# The repository's checks, one target each: make check runs the set.
UV_RUN := uv run --project src --frozen
PYTHON_SOURCES = src/prosiform checks

.PHONY: check test docs

check: lint test
\tcd src && uv run pytest

test:
\t$(UV_RUN) pytest

docs/output.md: docs/input.md
\tcat $< > $@
"""

PYPROJECT = """\
[project]
requires-python = ">=3.13"
dependencies = [
    "markdown-it-py==4.2.0",
    "tomli>=2.0 ; python_version < '3.11'",
]

[dependency-groups]
dev = [
    "pytest==9.1.1",
    "ruff == 0.17.1",
    "types-jsonschema[extra]==4.26.0",
]
"""

DOCUMENT = """\
# Checks

| Check | Command |
| --- | --- |
| `layout.py` | `make layout` |
| [the tables](checks/tables.py) | [`make tables`](Makefile) |
| a cell naming a pipe | `make check` with a \\| in its text |

```markdown
| Check | Command |
| --- | --- |
| an example | `make never-declared` |
```

| Declared | Value |
| --- | --- |
| `markdown-it-py` | `==4.2.0` |
"""


@pytest.fixture
def declared(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[set[str], dict[str, str]]:
    """The two readings, taken from files written for this test."""
    makefile = tmp_path / "Makefile"
    makefile.write_text(MAKEFILE)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(PYPROJECT)
    monkeypatch.setattr(tables, "MAKEFILE", makefile)
    monkeypatch.setattr(tables, "PYPROJECT", pyproject)
    return tables.targets(), tables.declarations()


def test_every_rule_of_the_makefile_is_a_target(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    targets, _ = declared
    assert {"check", "test"} <= targets


def test_an_assignment_is_not_a_target(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    targets, _ = declared
    assert "UV_RUN" not in targets
    assert "PYTHON_SOURCES" not in targets


def test_makes_own_directive_is_not_a_target(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    targets, _ = declared
    assert not any(target.startswith(".") for target in targets)


def test_a_recipe_line_and_a_comment_are_not_targets(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    targets, _ = declared
    assert targets == {"check", "test"}


def test_the_required_python_version_is_a_declaration(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    _, items = declared
    assert items[tables.PYTHON] == ">=3.13"


def test_a_dependency_and_a_development_dependency_are_declarations(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    _, items = declared
    assert items["markdown-it-py"] == "==4.2.0"
    assert items["pytest"] == "==9.1.1"


def test_a_requirement_carrying_a_marker_declares_what_precedes_it(
    declared: tuple[set[str], dict[str, str]],
) -> None:
    _, items = declared
    assert items["tomli"] == ">=2.0 ; python_version < '3.11'"


def test_a_name_is_compared_as_the_ecosystem_compares_one() -> None:
    assert tables.key("Types_JSONSchema.Extra") == "types-jsonschema-extra"
    assert tables.key("markdown-it-py") == tables.key("Markdown_It.Py")


def test_a_command_row_names_the_target_it_writes() -> None:
    target, failure = tables.match_command(
        "README.md", {"Command": "`make layout`"}, {"layout"}
    )
    assert (target, failure) == ("layout", None)


def test_a_command_row_written_as_a_link_names_its_target() -> None:
    target, failure = tables.match_command(
        "README.md", {"Command": "[`make tables`](Makefile)"}, {"tables"}
    )
    assert (target, failure) == ("tables", None)


def test_a_command_row_naming_no_command_is_reported() -> None:
    target, failure = tables.match_command(
        "README.md", {"Command": "`make check` with a | in its text"}, {"check"}
    )
    assert target is None
    assert failure is not None and "names no command" in failure


def test_a_command_row_naming_an_undeclared_target_is_reported() -> None:
    target, failure = tables.match_command(
        "README.md", {"Command": "`make never-declared`"}, {"check"}
    )
    assert target is None
    assert failure is not None and "declares no such target" in failure


def test_a_declaration_row_names_the_item_under_the_version_it_pins() -> None:
    item, failure = tables.match_declaration(
        "README.md",
        {"Declared": "`markdown-it-py`", "Value": "`==4.2.0`"},
        {"markdown-it-py": ("markdown-it-py", "==4.2.0")},
    )
    assert (item, failure) == ("markdown-it-py", None)


def test_a_declaration_row_naming_another_version_is_reported() -> None:
    item, failure = tables.match_declaration(
        "README.md",
        {"Declared": "`markdown-it-py`", "Value": "`==4.1.0`"},
        {"markdown-it-py": ("markdown-it-py", "==4.2.0")},
    )
    assert item == "markdown-it-py"
    assert failure is not None and "==4.2.0" in failure


def test_a_declaration_row_naming_no_dependency_is_reported() -> None:
    item, failure = tables.match_declaration(
        "README.md", {"Declared": "`absent`", "Value": "`==1.0`"}, {}
    )
    assert item is None
    assert failure is not None and "declares no such dependency" in failure


def test_a_document_carries_the_tables_outside_its_fences() -> None:
    read = read_tables(DOCUMENT)
    assert [table.headers for table in read] == [
        ("Check", "Command"),
        ("Declared", "Value"),
    ]


def test_a_fenced_table_is_an_example_rather_than_a_row() -> None:
    commands = [
        plain(record["Command"])
        for table in read_tables(DOCUMENT)
        for record in table.records()
        if "Command" in table.headers
    ]
    assert "make never-declared" not in commands


def test_an_escaped_pipe_stays_inside_its_cell() -> None:
    rows = read_tables(DOCUMENT)[0].records()
    assert plain(rows[2]["Command"]) == "make check with a \\| in its text"


def test_a_cell_reduces_to_the_text_it_states() -> None:
    assert plain("[`make tables`](Makefile)") == "make tables"
    assert plain("a cell\nwrapped   across lines") == "a cell wrapped across lines"
