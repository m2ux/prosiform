"""Hold the eval page to the proof file it states.

The page names each feature workflow with the permutations its scenarios
cover, and states the cost the proof run measured, so a scenario the proof
runs without a row, or a cost the file does not record, reads as fact.
"""

import json
import re
import tomllib
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()
PROOF = json.loads((HERE / "mvp-proof.json").read_text())
ROW = re.compile(r"^\| `([a-z-]+)` \| `([a-z-]+)` \|", re.MULTILINE)


def section(heading: str) -> str:
    """The page text under one heading, up to the next of its level or above."""
    level = heading.split(" ", 1)[0]
    rest = README.split(f"\n{heading}\n", 1)[1]
    end = re.search(rf"^#{{1,{len(level)}}} ", rest, re.MULTILINE)
    return rest[: end.start()] if end else rest


def test_the_feature_table_names_each_workflow_and_scenario_the_proof_runs() -> None:
    proved = {(cell["workflow"], cell["scenario"]) for cell in PROOF["cells"]}
    named = set(ROW.findall(section("### Feature scenarios")))
    assert named == proved


def test_the_feature_table_names_each_scenario_its_workflow_declares() -> None:
    named = ROW.findall(section("### Feature scenarios"))
    declared = {
        (directory.name, scenario["name"])
        for directory in (HERE / "workflows").iterdir()
        if directory.name in {workflow for workflow, _ in named}
        for scenario in tomllib.loads((directory / "scenarios.toml").read_text())[
            "scenario"
        ]
    }
    assert set(named) == declared


def test_the_proof_section_states_the_cost_the_file_records() -> None:
    proof = section("## MVP proof")
    assert f"USD {PROOF['cost_usd']}" in proof
    assert f"{PROOF['sessions']} sessions" in proof


def test_the_page_states_one_compiled_form_carrying_the_run_pf_line() -> None:
    """AC13: one `compiled` form carrying `pf`, and no `staged` form or section."""
    forms = [row[0] for row in table_rows(section("## Forms"))]
    assert forms.count("compiled") == 1 and "staged" not in forms
    [row] = [row for row in table_rows(section("## Forms")) if row[0] == "compiled"]
    assert "run-pf line" in row[1] and "as `pf`" in row[1]
    assert "shell limited to `pf`" in row[1]
    assert "staged" not in README.lower()
    assert "Prosiform section" not in README


def table_rows(text: str) -> list[list[str]]:
    """The cells of each table row in `text`, a form's name stripped of marks."""
    return [
        [
            cell.strip().strip("`") if i == 0 else cell.strip()
            for i, cell in enumerate(line.split("|")[1:-1])
        ]
        for line in text.splitlines()
        if line.startswith("| ") and not line.startswith("| -")
    ]
