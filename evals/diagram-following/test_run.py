"""Hold the runner to its sessions, its records, its spending cap and its classes.

Every run here starts the stub agent beside this file in place of the real
one, so no test starts a paid session. The stub writes what it found in its
workspace to a log, walks the workflow it finds there, and reports a cost
the test chooses.

The dispatch corpus is also held as a matrix: each departure the stub can
state runs every dispatch scenario in both forms, and each cell is asserted
against the class that departure predicts, so a check that fires for the
wrong reason fails where it fires.
"""

import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import workflow as source
from harness import HARNESSES, MANAGED_SETTINGS, Claude, Codex, Cursor, Opencode
from report import REPORT_JSON, REPORT_MD, RUN, SESSION, TIMEOUT, main
from run import (
    AUTHORED_SET,
    BOOTSTRAP_SET,
    BUNDLE,
    BUNDLED,
    COMPILED_SET,
    FORMS,
    LINKED_TREE,
    PROSE_BUNDLE,
    TRANSCRIPT,
    TREE,
    Ledger,
    Session,
    bundles_of,
    hook_events_seen,
    injected,
    keep,
    matrix,
    observable,
    options,
    prepare,
    run,
)
from score import (
    ACTIONS,
    SUB_AGENT_TRACE,
    SUBAGENTS,
    TRACE,
    TRACES,
    Failure,
    read_starts,
)
from score import (
    names as names_section,
)
from stub_agent import recognised
from workflow import (
    COMPILED_FORM,
    ENTRY,
    LINKED_FORM,
    Compile,
    CorpusError,
    workflows,
)

STUB = Path(__file__).resolve().parent / "stub_agent.py"
CORPUS = {workflow.name: workflow for workflow in workflows()}
CALLER_VARIABLES = (
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CONFIG_DIR",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
)
DISPATCHING = ("dispatch-beside", "dispatch-chain", "dispatch-question", "dispatch-set")
DISPATCH_FORMS = (COMPILED_SET, AUTHORED_SET)
DISPATCH_SCENARIOS = tuple(
    scenario.name for name in DISPATCHING for scenario in CORPUS[name].scenarios
)
"""The dispatch corpus's scenario names, one per dispatch workflow."""

DEPARTURES: dict[str, tuple[str, dict[str, Failure | None]]] = {
    "STUB_AGENT_NO_DISPATCH": (
        "1",
        dict.fromkeys(DISPATCH_SCENARIOS, Failure.UNDISPATCHED),
    ),
    "STUB_AGENT_SEQUENTIAL": (
        "1",
        {
            "chain": None,
            "parallel-set": Failure.SEQUENTIAL_SET,
            "set-beside-a-dispatch": Failure.SEQUENTIAL_SET,
            "returned-question": None,
        },
    ),
    "STUB_AGENT_ANSWER": (
        "1",
        {
            "chain": None,
            "parallel-set": None,
            "set-beside-a-dispatch": None,
            "returned-question": Failure.UNRELAYED_QUESTION,
        },
    ),
    "STUB_AGENT_STOP": ("1", dict.fromkeys(DISPATCH_SCENARIOS, Failure.UNFINISHED)),
}
"""Each departure script, the value it reads, and the class it predicts per cell.

A script states one departure, and a scenario states which of the checks that
departure changes. A scenario whose trace the departure leaves as the
scenario states predicts a pass, so a class that fires where its departure is
absent fails here as surely as one that does not fire where it is present.
"""


def every_session(models: list[str], forms: list[str], repetitions: int) -> int:
    """The sessions a run of the whole corpus starts on the stub's harness."""
    return len(
        matrix(list(CORPUS.values()), models, forms, repetitions, HARNESSES["claude"])
    )


def test_the_stub_recognises_the_workflow_holding_the_most_states() -> None:
    """A workflow whose states another holds is not taken for that one."""
    looping = CORPUS["looping"]
    fewer = replace(
        looping,
        name="fewer",
        diagram=replace(
            looping.diagram,
            edges=tuple(
                edge
                for edge in looping.diagram.edges
                if "Check" not in (edge.source, edge.target)
            ),
        ),
    )
    assert fewer.diagram.states < looping.diagram.states
    headings = set(looping.diagram.states)
    assert recognised(headings, [fewer, looping]) is looping
    assert recognised(headings - {"Check"}, [fewer, looping]) is fewer


def test_a_matrix_holds_no_cell_a_harness_cannot_observe() -> None:
    """A scenario whose trace outruns the path's own starts is beyond Cursor."""
    corpus = list(CORPUS.values())
    forms = [COMPILED_SET, AUTHORED_SET]
    cursor = matrix(corpus, ["m"], forms, 1, HARNESSES["cursor"])
    claude = matrix(corpus, ["m"], forms, 1, HARNESSES["claude"])
    assert len(cursor) < len(claude)
    assert all(item.workflow != "dispatch-chain" for item in cursor)
    assert any(item.workflow == "dispatch-chain" for item in claude)
    workflow = CORPUS["dispatch-set"]
    scenario = workflow.scenarios[0]
    assert observable(workflow, scenario, COMPILED_SET, HARNESSES["cursor"]) is True


def test_the_cursor_harness_completes_a_matrix_over_the_default_forms() -> None:
    """AC15: every default form reaches the matrix the Cursor harness runs.

    The runner names its forms by what a session receives, and the corpus
    names its own by what they hold, so a form the run offers in the default
    list is looked up as the corpus form it carries. One that is not resolves
    to no sections at all, and the matrix stops before a single session.
    """
    corpus = list(CORPUS.values())
    forms = list(FORMS)
    sessions = matrix(corpus, ["m"], forms, 1, HARNESSES["cursor"])
    reached = {(session.workflow, session.form) for session in sessions}
    offered = {
        (workflow.name, form)
        for workflow in corpus
        for form in forms
        if FORMS[form] in workflow.forms
    }
    assert reached <= offered
    assert {("linear", BUNDLE), ("linear", TREE)} <= reached
    assert {("branching", PROSE_BUNDLE), ("branching", LINKED_TREE)} <= reached
    assert {("dispatch-chain", COMPILED_SET)}.isdisjoint(reached)


@pytest.fixture
def log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The directory the stub agent writes what it saw to, one file a session."""
    directory = tmp_path / "log"
    directory.mkdir()
    monkeypatch.setenv("STUB_AGENT_LOG", str(directory))
    for name in CALLER_VARIABLES:
        monkeypatch.setenv(name, "caller")
    login = tmp_path / "eval" / "config" / ".credentials.json"
    login.parent.mkdir(parents=True)
    login.touch()
    return directory


def eval_run(tmp_path: Path, *extra: str) -> dict[str, Any]:
    """A run of one model through the stub agent, its records under tmp_path.

    The stub stands in for any harness, so the run names `claude`, whose
    stream carries every scenario's trace, rather than the default harness
    whose observability the corpus is sized by.
    """
    return run(
        options(
            [
                "--agent-command",
                f"{sys.executable} {STUB}",
                "--harness",
                "claude",
                "--models",
                "stub-model",
                "--workflows",
                ",".join(CORPUS),
                "--results",
                str(tmp_path / "results"),
                "--run-id",
                "test",
                "--eval-root",
                str(tmp_path / "eval"),
                "--session-budget-tokens",
                "250",
                *extra,
            ]
        )
    )


def seen(log: Path) -> list[dict[str, Any]]:
    """What each session the stub agent ran in found on starting."""
    return [json.loads(path.read_text()) for path in sorted(log.iterdir())]


def records(tmp_path: Path) -> list[dict[str, Any]]:
    """Every session record the test run wrote."""
    sessions = sorted((tmp_path / "results" / "test").rglob(SESSION))
    return [json.loads(path.read_text()) for path in sessions]


def material(session: Session) -> set[str]:
    """The files a session's workspace holds on starting.

    A bundled form's entry bundle is `workflow.md`, and every other bundle
    of its set sits beside it under the name `pf` gave it. A form read as a
    source tree gives its own files. The compiled form gives its sources, its
    bundle set in the folder `pf` writes it to, and the build. A scenario
    stating answers adds `answers.txt`.
    """
    workflow = CORPUS[session.workflow]
    scenario = next(i for i in workflow.scenarios if i.name == session.scenario)
    inputs = {f"inputs/{name}" for name in scenario.inputs}
    if scenario.answers:
        inputs.add("answers.txt")
    if session.form == COMPILED_SET:
        tree = workflow.form(COMPILED_FORM)
        folder = workflow.entry_bundle.parent
        return (
            {str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()}
            | {str(folder / name) for name in bundles_of(workflow, COMPILED_SET)}
            | inputs
        )
    if session.form in BUNDLED:
        return (
            {ENTRY}
            | inputs
            | {
                name
                for name in bundles_of(workflow, session.form)
                if name != workflow.entry_bundle.name
            }
        )
    if session.form == BOOTSTRAP_SET:
        skill = workflow.directory / source.BOOTSTRAP_DIR
        return {
            f".claude/skills/{workflow.name}/{path.relative_to(skill)}"
            for path in skill.rglob("*")
            if path.is_file()
        } | inputs
    tree = workflow.form(FORMS[session.form])
    return {
        str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()
    } | inputs


def test_the_matrix_holds_one_session_per_model_form_scenario_and_repetition() -> None:
    sessions = matrix(
        list(CORPUS.values()), ["a", "b"], list(FORMS), 5, HARNESSES["claude"]
    )
    assert (
        len(sessions) == len(set(sessions)) == every_session(["a", "b"], list(FORMS), 5)
    )
    assert len(sessions) == 2 * 5 * every_session(["a"], list(FORMS), 1)


def readme_rows(header: str) -> list[list[str]]:
    """The body rows of each README table whose first header cell is `header`.

    Each cell is its text with code-span marks removed, so a form written as
    code compares as the name the runner gives it.
    """
    lines = (source.ROOT / "README.md").read_text().splitlines()
    rows: list[list[str]] = []
    for index, line in enumerate(lines[:-1]):
        cells = [cell.strip().strip("`") for cell in line.strip().split("|")[1:-1]]
        if not cells or cells[0] != header or not lines[index + 1].startswith("| -"):
            continue
        for row in lines[index + 2 :]:
            if not row.startswith("|"):
                break
            rows.append([cell.strip().strip("`") for cell in row.split("|")[1:-1]])
    return rows


def test_the_readme_states_every_form_the_runner_offers_and_its_default() -> None:
    """AC2: the README's form table and `--forms` default read as `run.FORMS`.

    A form the runner offers that the README omits is one a reader choosing a
    run's forms cannot learn of, so the table names every form in the order
    the runner holds them, and the option's default is the list it builds.
    """
    assert [row[0] for row in readme_rows("Form")] == list(FORMS)
    forms = [row for row in readme_rows("Option") if row[0] == "--forms"]
    assert [row[1] for row in forms] == [",".join(FORMS)]
    assert options(["--budget-tokens", "1"]).forms == ",".join(FORMS)


def test_a_compiled_session_receives_its_sources_the_bundle_set_and_the_build(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC2: the compiled bundle set, its sources, and the build as `pf` on its path.

    The set sits in the folder `pf` writes it to, beside the sources a `↳`
    line names its target from, and the instruction names the entry's bundle
    there. The `pf` the session's path resolves to is the build this run was
    given through the runner's environment.
    """
    monkeypatch.setattr("run.harness_named", lambda name: Cursor())
    eval_run(
        tmp_path,
        *("--harness", "cursor", "--workflows", "dispatch-set"),
        *("--forms", COMPILED_SET, "--repetitions", "1", "--budget-tokens", "4000"),
    )
    workflow = CORPUS["dispatch-set"]
    bundles = bundles_of(workflow, COMPILED_SET)
    [entry] = seen(log)
    workspace = Path(entry["workspace"])
    folder = workflow.entry_bundle.parent
    assert {str(folder / name) for name in bundles} <= set(entry["files"])
    assert {"workflow.md", "review.md", "states/survey.md"} <= set(entry["files"])
    assert Path(entry["which_pf"]).resolve() == Path(shutil.which("pf") or "").resolve()
    assert not Path(entry["which_pf"]).is_relative_to(workspace)
    assert f"{workflow.entry_bundle.as_posix()} describes a workflow" in entry["prompt"]
    assert "run each compile from this directory" in " ".join(entry["prompt"].split())


def test_a_run_gives_each_harness_the_compiled_scenarios_its_stream_reports() -> None:
    """AC3, AC26: every compiled scenario reaches Claude; a nested one no other.

    Cursor and opencode report no sub-agent's own calls, so they are given
    the compiled scenarios whose starts and runs the session makes itself,
    `subagent-first-run`'s none, since each states a sub-agent's run, and no
    `dispatch-chain` or `dispatch-depth` scenario, whose sub-agents dispatch.
    Claude's compiled session carries a shell and its stream reports every
    sub-agent's calls, so it is given every compiled scenario, the nested
    ones among them.
    """
    corpus = list(CORPUS.values())
    for harness in (Cursor(), Opencode()):
        given = matrix(corpus, ["m"], [COMPILED_SET], 1, harness)
        assert {item.workflow for item in given} == {
            workflow.name
            for workflow in corpus
            if COMPILED_FORM in workflow.forms
            and workflow.name
            not in ("dispatch-chain", "dispatch-depth", "subagent-first-run")
        }
    claude = matrix(corpus, ["m"], [COMPILED_SET], 1, Claude())
    assert {(item.workflow, item.scenario) for item in claude} == {
        (workflow.name, scenario.name)
        for workflow in corpus
        if COMPILED_FORM in workflow.forms
        for scenario in workflow.scenarios
    }
    assert {
        ("dispatch-depth", "three-hop-chain"),
        ("dispatch-depth", "three-hop-set"),
        ("dispatch-depth", "three-hop-question"),
        ("subagent-first-run", "deep-hop-runs"),
    } <= {(item.workflow, item.scenario) for item in claude}


def test_a_harness_reporting_no_sub_agent_command_gets_no_sub_agent_run() -> None:
    """AC22, AC26: a scenario stating a sub-agent's `pf` run needs its commands.

    Claude reports them in the compiled form, whose session carries a shell,
    and in no form whose session carries none. Neither Cursor's stream nor
    opencode's carries a sub-agent's own calls. Codex exposes child starts
    while its start records carry no child commands. A harness reporting
    those commands receives the scenario; a session's own run needs a shell.
    """
    workflow = CORPUS["dispatch-set"]
    [scenario] = workflow.scenarios
    by_sub_agent = replace(scenario, compile=(Compile("review#tests"),))
    by_session = replace(scenario, compile=(Compile(None),))
    assert observable(workflow, by_sub_agent, COMPILED_SET, Claude())
    assert not observable(workflow, by_sub_agent, AUTHORED_SET, Claude())
    for harness in (Cursor(), Opencode(), Codex()):
        assert not observable(workflow, by_sub_agent, COMPILED_SET, harness)
    assert observable(
        workflow,
        by_sub_agent,
        COMPILED_SET,
        replace(Opencode(), nested_starts=True, nested_commands=True),
    )
    assert observable(workflow, by_session, COMPILED_SET, Opencode())
    assert observable(workflow, by_session, COMPILED_SET, Codex())
    alone = replace(workflow, scenarios=(by_sub_agent,))
    assert matrix([alone], ["m"], [COMPILED_SET], 1, Opencode()) == []
    assert matrix([alone], ["m"], [COMPILED_SET], 1, Codex()) == []


def test_a_harness_reporting_only_the_sessions_starts_gets_those_scenarios() -> None:
    """A deferred section's targets start from the session, so a shell harness
    reporting only the session's own starts observes them; a start a sub-agent
    makes, at any depth, it does not, nor a run a sub-agent makes.
    """
    compiled = matrix(list(CORPUS.values()), ["m"], [COMPILED_SET], 1, Cursor())
    given = {(item.workflow, item.scenario) for item in compiled}
    assert ("deferred-dispatch", "deferred-dispatch-compiled") in given
    assert ("subagent-first-run", "first-hop-run") not in given
    assert ("subagent-first-run", "deep-hop-runs") not in given
    assert not any(workflow == "dispatch-depth" for workflow, _ in given)


def test_tagged_dispatch_workflow_runs_with_selection_qualified_traces(
    tmp_path: Path, log: Path
) -> None:
    eval_run(
        tmp_path,
        "--workflows",
        "deferred-dispatch",
        "--forms",
        COMPILED_SET,
        "--repetitions",
        "1",
        "--budget-tokens",
        "4000",
    )
    found = records(tmp_path)
    assert len(found) == 2
    assert all(record["verdict"]["passed"] for record in found)
    selected = next(record for record in found if record["trace"])
    assert [entry["presets"] for entry in selected["trace"]] == [["lift"], ["strap"]]


def test_native_child_starts_admit_chains_with_no_child_command_requirement() -> None:
    """AC22: native chains are observable; per-child compiler runs need attribution."""
    corpus = [CORPUS["dispatch-depth"], CORPUS["subagent-first-run"]]
    sessions = matrix(corpus, ["m"], [COMPILED_SET], 1, Codex())
    assert {session.workflow for session in sessions} == {"dispatch-depth"}
    assert {session.scenario for session in sessions} == {
        "three-hop-chain",
        "three-hop-set",
        "three-hop-question",
    }


def test_a_compiled_claude_run_scores_each_nested_scenario_on_its_starts_runs(
    tmp_path: Path, log: Path
) -> None:
    """AC26: nested scenarios take a Claude cell, scored on each start's runs.

    The stub's compiled session carries `Bash`, so it makes each stated `pf`
    run under the start whose sub-agent makes it, and the record holds them
    there. Every cell passes, `deep-hop-runs` among them, and its review and
    ruling hold their own runs.
    """
    record = eval_run(
        tmp_path,
        *("--workflows", "dispatch-depth,subagent-first-run", "--forms", COMPILED_SET),
        *("--repetitions", "1", "--budget-tokens", "100000"),
    )
    cells = {(item["workflow"], item["scenario"]) for item in records(tmp_path)}
    assert record["started"] == len(cells) == 5
    assert {
        ("dispatch-depth", "three-hop-chain"),
        ("dispatch-depth", "three-hop-set"),
        ("dispatch-depth", "three-hop-question"),
        ("subagent-first-run", "deep-hop-runs"),
    } <= cells
    assert all(item["verdict"]["passed"] for item in records(tmp_path))
    for entry in seen(log):
        argv = entry["argv"]
        assert argv[argv.index("--tools") + 1].endswith(",Bash")
    deep = (
        tmp_path
        / "results"
        / "test"
        / "stub-model"
        / "subagent-first-run"
        / "deep-hop-runs"
        / COMPILED_SET
        / "1"
    )
    assert [(start.target, start.commands) for start in read_starts(deep)] == [
        ("Follow hop/audit#sweep. Append each state you enter to trace-sweep.log.", ()),
        (
            "Follow hop/review#scan. Append each state you enter to trace-scan.log.",
            ("pf '--entry=steps/weighing.md#weigh'",),
        ),
        (
            "Follow steps/ruling#rule. Append each state you enter to trace-rule.log.",
            ("pf '--entry=steps/recording.md#file'",),
        ),
    ]
    assert json.loads((deep / SUBAGENTS).read_text())["commands"] == ["pf"]


def test_each_session_starts_in_a_fresh_workspace_of_its_form_and_inputs(
    tmp_path: Path, log: Path
) -> None:
    record = eval_run(
        tmp_path, "--repetitions", "2", "--budget-tokens", "200000", "--parallel", "3"
    )
    sessions = matrix(
        list(CORPUS.values()), ["stub-model"], list(FORMS), 2, HARNESSES["claude"]
    )
    workspaces = (tmp_path / "eval" / "workspaces" / "test").resolve()
    expected = every_session(["stub-model"], list(FORMS), 2)
    assert record["started"] == len(sessions) == expected
    entries = seen(log)
    assert len(entries) == len(sessions)
    assert len({entry["workspace"] for entry in entries}) == len(sessions)
    found = sorted(sorted(entry["files"]) for entry in entries)
    assert found == sorted(sorted(material(session)) for session in sessions)
    for entry in entries:
        argv = entry["argv"]
        tools = "Read,Write,Edit,Glob,Grep,Agent"
        assert argv[argv.index("--tools") + 1] == tools + ",Bash"
        assert "--strict-mcp-config" in argv and "--disable-slash-commands" in argv
        assert "--mcp-config" not in argv and "--bare" not in argv
        assert argv[argv.index("--allowedTools") + 1] == "Bash(pf *)"
        assert Path(entry["pf"]).resolve() == Path(shutil.which("pf") or "").resolve()
        assert not Path(entry["pf"]).is_relative_to(entry["workspace"])
        compiled = "workflow.bundles/workflow.bundle.md"
        named = compiled if compiled in entry["files"] else ENTRY
        described = f"{named} describes a workflow" in entry["prompt"]
        assert described is (named in entry["files"])
        assert Path(entry["workspace"]).is_relative_to(workspaces)
        assert not Path(entry["workspace"]).exists()
        assert entry["config"] == str(tmp_path / "eval" / "config")
        variables = set(entry["variables"])
        assert not variables & (set(CALLER_VARIABLES) - {"CLAUDE_CONFIG_DIR"})
        assert "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS" in variables
        assert not any(
            name.startswith(("CLAUDE_CODE_", "ANTHROPIC_"))
            for name in variables - {"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"}
        )
    assert not workspaces.exists()


@pytest.mark.parametrize("held", ["results", "workspaces"])
def test_a_reused_run_id_is_refused_before_bundling_or_starting_a_session(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch, held: str
) -> None:
    """A stopped run's results or workspaces keep its id until both are removed."""
    results = tmp_path / "results" / "test"
    workspaces = tmp_path / "eval" / "workspaces" / "test"
    residue = results if held == "results" else workspaces
    residue.mkdir(parents=True)
    sentinel = residue / "kept.txt"
    sentinel.write_text("kept\n")

    def unexpected_bundle(*args: object) -> None:
        pytest.fail("a reused run id reached bundling")

    monkeypatch.setattr("run.bundles_of", unexpected_bundle)
    with pytest.raises(CorpusError, match="run id.*test.*exists"):
        eval_run(tmp_path, "--budget-tokens", "200000")
    assert sentinel.read_text() == "kept\n"
    assert not list(log.iterdir())
    assert not list(results.rglob(SESSION))


def test_a_bundled_form_is_one_file_and_the_tree_its_sources(
    tmp_path: Path, log: Path
) -> None:
    """A bundled form gives its set, a tree form its source documents."""
    eval_run(
        tmp_path,
        "--workflows",
        "looping",
        "--repetitions",
        "1",
        "--budget-tokens",
        "4000",
    )
    looping = CORPUS["looping"]
    tree_document = f"states/{looping.diagram.start.lower()}.md"
    bundle_entries = [
        entry
        for entry in seen(log)
        if sorted(name for name in entry["files"] if name.endswith(".md")) == [ENTRY]
    ]
    tree_entries = [entry for entry in seen(log) if tree_document in entry["files"]]
    assert len(bundle_entries) == 2 * len(looping.scenarios)
    assert len(tree_entries) == 2 * len(looping.scenarios)


def test_a_compiled_form_gives_its_whole_bundle_set(tmp_path: Path, log: Path) -> None:
    """A dispatching bundle set reaches the session with every bundle it names."""
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain", "--forms", COMPILED_SET),
        *("--repetitions", "1", "--budget-tokens", "4000"),
    )
    [workflow] = [CORPUS["dispatch-chain"]]
    folder = workflow.entry_bundle.parent
    expected = {str(folder / name) for name in bundles_of(workflow, COMPILED_SET)}
    for entry in seen(log):
        assert expected <= set(entry["files"])


def test_the_linked_form_walks_every_scenario_of_a_branching_workflow(
    tmp_path: Path, log: Path
) -> None:
    """Both `branching` scenarios reach the path their inputs determine.

    The session's workspace is the linked form's own source tree, so the
    rule document each decision links is present and the stub finds the
    state headings there rather than in a bundle.
    """
    eval_run(
        tmp_path,
        *("--workflows", "branching", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "4000"),
    )
    written = records(tmp_path)
    assert len(written) == len(CORPUS["branching"].scenarios)
    linked = CORPUS["branching"].form(LINKED_FORM)
    rules = {str(path.relative_to(linked)) for path in (linked / "rules").iterdir()}
    assert rules == {"rules/a.md", "rules/b.md"}
    held = {tuple(sorted(entry["files"])) for entry in seen(log)}
    for files in held:
        assert "workflow.md" in files
        assert {"states/triage.md", "states/intake.md"} <= set(files)
        assert rules <= set(files), "the linked form's rule documents are absent"
        assert "scenarios.toml" not in files
    for record in written:
        assert record["form"] == LINKED_TREE
        assert record["verdict"]["passed"] is True, record["verdict"]
        assert record["verdict"]["actual"] == record["verdict"]["expected"]


def test_the_linked_form_walks_every_scenario_of_a_looping_workflow(
    tmp_path: Path, log: Path
) -> None:
    """Both `looping` scenarios reach the path their inputs determine."""
    eval_run(
        tmp_path,
        *("--workflows", "looping", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "4000"),
    )
    written = records(tmp_path)
    assert len(written) == len(CORPUS["looping"].scenarios)
    linked = CORPUS["looping"].form(LINKED_FORM)
    rules = {str(path.relative_to(linked)) for path in (linked / "rules").iterdir()}
    assert rules == {"rules/a.md", "rules/b.md"}
    held = {tuple(sorted(entry["files"])) for entry in seen(log)}
    for files in held:
        assert "workflow.md" in files
        assert {"states/draft.md", "states/review.md"} <= set(files)
        assert rules <= set(files), "the linked form's rule documents are absent"
        assert "scenarios.toml" not in files
    for record in written:
        assert record["form"] == LINKED_TREE
        assert record["verdict"]["passed"] is True, record["verdict"]
        assert record["verdict"]["actual"] == record["verdict"]["expected"]


def test_each_session_records_its_transcript_usage_cost_and_verdict(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    eval_run(tmp_path, "--repetitions", "1", "--budget-tokens", "200000")
    written = records(tmp_path)
    assert len(written) == every_session(["stub-model"], list(FORMS), 1)
    for record in written:
        session = Session(
            record["model"],
            record["workflow"],
            record["scenario"],
            record["form"],
            record["repetition"],
        )
        directory = session.directory(tmp_path / "results" / "test")
        transcript = (directory / TRANSCRIPT).read_text().splitlines()
        assert json.loads(transcript[-1]) == record["result"]
        assert record["exit_status"] == 0
        assert record["tokens"] == 125
        trace = (directory / TRACE).read_text().split()
        assert record["usage"] == {"input_tokens": 125, "output_tokens": 0}
        verdict = record["verdict"]
        assert verdict["passed"] is True
        assert trace == verdict["actual"]
        action_files = {path.name for path in (directory / ACTIONS).iterdir()}
        workflow = CORPUS[session.workflow]
        [scenario] = (i for i in workflow.scenarios if i.name == session.scenario)
        assert action_files == {
            found[0]
            for state in trace
            if (found := workflow.walked[state].action) is not None
        } | {entry.action[0] for entry in scenario.trace if entry.action}


def test_a_failing_session_is_recorded_with_its_failure(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_STOP", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    verdict = record["verdict"]
    assert verdict["failure"] == "unfinished"
    assert verdict["actual"] == ["Entry"]


def test_a_run_ends_by_writing_its_report(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--budget-tokens", "1000"),
    )
    written = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    [cell] = written["cells"]
    assert (cell["model"], cell["form"], cell["scenario"]) == (
        "stub-model",
        BUNDLE,
        "straight-through",
    )
    assert (cell["sessions"], cell["passed"], cell["tokens"]) == (2, 2, 125)
    assert written["tokens"] == 250 and written["not_started"] == []


def test_a_budget_short_of_every_session_at_its_cap_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    with pytest.raises(
        CorpusError,
        match=r"--budget-tokens 500 does not cover the 12 sessions at "
        r"--session-budget-tokens 250, which need 3000",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear,branching", "--repetitions", "1"),
            "--budget-tokens",
            "500",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_sessions_pass_their_cap_stops_starting_sessions(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The budget covers every session's cap, and each records twice its cap.

    A session starts while the tokens recorded and its own cap fit, so the
    run starts one more session than the budget, less one cap, holds at the
    tokens each records.
    """
    monkeypatch.setenv("STUB_AGENT_TOKENS", "500")
    sessions = matrix(
        list(CORPUS.values()), ["stub-model"], list(FORMS), 1, HARNESSES["claude"]
    )
    budget = 250 * len(sessions)
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1"),
        *("--budget-tokens", str(budget), "--session-budget-tokens", "250"),
    )
    started = (budget - 250) // 500 + 1
    assert started < len(sessions)
    assert record["started"] == started
    assert record["tokens"] == 500 * started
    assert len(seen(log)) == len(records(tmp_path)) == started
    not_started = record["not_started"]
    assert not_started == [
        {
            "model": session.model,
            "workflow": session.workflow,
            "scenario": session.scenario,
            "form": session.form,
            "repetition": session.repetition,
        }
        for session in sessions[started:]
    ]
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert written["not_started"] == not_started


def test_a_session_in_flight_holds_its_cap_against_the_budget() -> None:
    ledger = Ledger(500, 250)
    assert ledger.reserve() and ledger.reserve()
    assert not ledger.fits()
    ledger.settle(100)
    assert not ledger.fits()
    ledger.settle(100)
    assert ledger.fits()


def test_the_ledger_settles_an_opencode_session_for_every_step(
    tmp_path: Path,
) -> None:
    """AC18: a session's reported spend is the sum of its steps.

    opencode reports each model step's tokens on its own `step_finish` part,
    so the ledger is settled with every step's tokens, not the last one's.
    """
    steps = [(120, 0.25), (60, 0.125), (20, 0.0625)]
    held = tmp_path / TRANSCRIPT
    held.write_text(
        "".join(
            json.dumps(
                {
                    "type": "step_finish",
                    "part": {
                        "type": "step_finish",
                        "tokens": {
                            "input": tokens - 4,
                            "output": 1,
                            "reasoning": 1,
                            "cache": {"write": 1, "read": 1},
                        },
                        "cost": cost,
                    },
                }
            )
            + "\n"
            for tokens, cost in steps
        )
    )
    harness = Opencode()
    result = harness.result(held)
    ledger = Ledger(1000, 250)
    assert ledger.reserve()
    ledger.settle(harness.tokens(result))
    assert ledger.spent == 200
    assert harness.cost(result) == 0.4375


def test_a_session_reporting_no_cost_is_charged_its_cap(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_SILENT", "1")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear,branching,looping", "--forms", PROSE_BUNDLE),
        *("--repetitions", "1", "--parallel", "1"),
        *("--budget-tokens", "1250", "--session-budget-tokens", "250"),
    )
    assert record["started"] == 5
    assert record["tokens"] == 0
    assert record["tokens_unknown"] == 5
    assert all(item["tokens"] is None for item in records(tmp_path))


def test_a_refused_agent_is_errored_not_a_trace_failure(
    tmp_path: Path, log: Path
) -> None:
    """An agent that entered no state is recorded apart from one that stopped."""
    record = eval_run(
        tmp_path,
        *("--agent-command", f"{sys.executable} -c 'import sys; sys.exit(1)'"),
        *("--workflows", "linear", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    [written] = records(tmp_path)
    assert written["verdict"]["failure"] == "errored"
    assert written["verdict"]["actual"] == []


def test_an_agent_reporting_an_error_is_errored_though_it_wrote_a_trace(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A refusal mid-run is `errored`, not a workflow the agent stopped short."""
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    assert record["exit_status"] == 0
    assert record["verdict"]["failure"] == "errored"


def test_a_run_whose_every_session_errored_is_refused_and_reported_as_such(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A spent login is a refused run, not a matrix of failing agents.

    Every session reports an error, so none entered a state. The run records
    itself refused with one session's own message as the reason, and its
    report names that instead of giving pass rates or a baseline comparison.
    """
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    monkeypatch.setenv("STUB_AGENT_REASON", "You've hit your weekly limit")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--budget-tokens", "4000"),
    )
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert record["state"] == written["state"] == "refused"
    assert written["reason"] == "You've hit your weekly limit"
    assert record["started"] == written["sessions"] == 2
    assert all(item["verdict"]["failure"] == "errored" for item in records(tmp_path))
    built = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert built["state"] == "refused"
    assert built["reason"] == "You've hit your weekly limit"
    for name in ("cells", "by_form", "by_model"):
        assert built[name] == [] and built["baseline_only"][name] == []
    assert built["baseline"] is None
    text = (tmp_path / "results" / "test" / REPORT_MD).read_text()
    assert "- **State:** `refused`" in text
    assert "You've hit your weekly limit" in text
    assert "not compared" in text and "Pass rate" not in text


def test_a_refused_run_writes_no_baseline(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    baseline = tmp_path / "baseline.json"
    with pytest.raises(
        CorpusError, match="measured no cell, so it writes no baseline: "
    ):
        main(
            [
                str(tmp_path / "results" / "test"),
                "--baseline",
                str(baseline),
                "--write-baseline",
            ]
        )
    assert not baseline.exists()


def test_a_run_with_a_genuine_mix_of_errors_and_states_is_a_result(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A real fault beside sessions that entered a state is not a refusal."""
    monkeypatch.setenv("STUB_AGENT_ERROR_ONCE", str(tmp_path / "errored"))
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--parallel", "1", "--budget-tokens", "4000"),
    )
    failures = [item["verdict"]["failure"] for item in records(tmp_path)]
    assert sorted(failures, key=str) == [None, "errored"]
    assert record["state"] == "completed" and record["reason"] is None
    written = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert written["state"] == "completed"
    assert written["cells"] and written["cells"][0]["passed"] == 1


def test_a_run_the_budget_stopped_whose_sessions_all_errored_is_refused(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sessions it never started do not turn its errored ones into a result."""
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    monkeypatch.setenv("STUB_AGENT_REASON", "You've hit your weekly limit")
    monkeypatch.setenv("STUB_AGENT_TOKENS", "500")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear,branching,looping", "--forms", PROSE_BUNDLE),
        *("--repetitions", "1", "--parallel", "1"),
        *("--budget-tokens", "1250", "--session-budget-tokens", "250"),
    )
    assert record["started"] == 3 and record["sessions"] == 5
    assert len(record["not_started"]) == 2
    assert all(item["verdict"]["failure"] == "errored" for item in records(tmp_path))
    assert record["state"] == "refused"
    assert record["reason"] == "You've hit your weekly limit"
    built = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert built["state"] == "refused" and built["cells"] == []


def test_a_run_without_a_login_starts_no_session(tmp_path: Path, log: Path) -> None:
    (tmp_path / "eval" / "config" / ".credentials.json").unlink()
    with pytest.raises(CorpusError, match="holds no login.*claude`, then `/login`"):
        eval_run(tmp_path, "--budget-tokens", "1000")
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_session_past_its_timeout_is_ended_scored_and_charged(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_HANG", str(tmp_path / "hung"))
    monkeypatch.setenv("STUB_AGENT_STOP", "2")
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    began = time.monotonic()
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--parallel", "1", "--session-timeout-seconds", "1"),
        *("--budget-tokens", "1000", "--session-budget-tokens", "250"),
    )
    assert time.monotonic() - began < 60
    assert record["started"] == 2 and record["not_started"] == []
    assert record["tokens"] == 125
    assert record["tokens_unknown"] == 1
    hung, finished = sorted(records(tmp_path), key=lambda item: item["repetition"])
    assert hung["exit_status"] == TIMEOUT and hung["tokens"] is None
    assert hung["verdict"]["failure"] == "unfinished"
    assert hung["verdict"]["actual"] == ["Entry", "Plan"]
    assert finished["exit_status"] == 0 and finished["tokens"] == 125


def test_the_context_read_finds_each_form_of_injected_context(
    tmp_path: Path,
) -> None:
    """A hook response, an appended prompt and a memory file all read as carried."""
    transcript = tmp_path / TRANSCRIPT
    cases = (
        ("a hook response", {"type": "system", "subtype": "hook_response"}),
        (
            "an appended system prompt",
            {
                "type": "system",
                "subtype": "init",
                "appendSystemPrompt": "obey another repository's rules",
            },
        ),
        (
            "a memory file",
            {
                "type": "system",
                "subtype": "init",
                "memory": "another repository's rules",
            },
        ),
    )
    for kind, message in cases:
        transcript.write_text(json.dumps(message) + "\n")
        carried = injected(transcript, False)
        assert carried is not None and carried.startswith(kind), (kind, carried)

    transcript.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                {"type": "system", "subtype": "init", "cwd": "/tmp"},
                {"type": "assistant", "message": {"content": ["Plan"]}},
                {"type": "result", "subtype": "success"},
            )
        )
    )
    assert injected(transcript, False) is None
    assert injected(tmp_path / "absent.jsonl", False) is None


def test_a_run_whose_config_installs_an_unmanaged_plugin_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """A plugin installed at a scope the organisation does not manage is refused.

    A plugin's `SessionStart` hook reaches a session before its first turn,
    and no flag the runner passes suppresses it, so a plugin the run cannot
    attribute to the organisation is a run the eval cannot measure a form in.
    """
    installed = tmp_path / "eval" / "config" / "plugins" / "installed_plugins.json"
    installed.parent.mkdir(parents=True)
    installed.write_text(
        json.dumps(
            {
                "version": 2,
                "plugins": {
                    "plugin-b@example": [{"scope": "user", "version": "0.1.0"}]
                },
            }
        )
    )
    with pytest.raises(
        CorpusError, match="installs plugin-b@example at user scope.*remove"
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            "--budget-tokens",
            "1000",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_unsigned_remote_settings_enable_a_plugin_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """Remote settings with no signature beside them are not the organisation's."""
    remote = tmp_path / "eval" / "config" / "remote-settings.json"
    remote.write_text(
        json.dumps(
            {
                "enabledPlugins": {"plugin-b@example": True},
                "env": {"EXAMPLE_SETTING": "1"},
            }
        )
    )
    with pytest.raises(
        CorpusError, match="enables a plugin.*without a signature.*remove .*remote"
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            "--budget-tokens",
            "1000",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def manage(
    config: Path,
    plugins: dict[str, str],
    environment: dict[str, str],
) -> None:
    """Install each plugin at managed scope and sign `environment`.

    Each plugin's install path holds no hooks file, so a hook the run counts
    comes from the transcripts alone, and the remote settings enable every
    plugin with a signature beside them.
    """
    installed = config / "plugins" / "installed_plugins.json"
    installed.parent.mkdir(parents=True, exist_ok=True)
    installs: dict[str, list[dict[str, str]]] = {}
    for plugin, version in plugins.items():
        place = config / "plugins" / "cache" / plugin / version
        place.mkdir(parents=True, exist_ok=True)
        installs[plugin] = [
            {"scope": "managed", "version": version, "installPath": str(place)}
        ]
    installed.write_text(json.dumps({"version": 2, "plugins": installs}))
    (config / "remote-settings.json").write_text(
        json.dumps(
            {
                "enabledPlugins": {plugin: True for plugin in plugins},
                "env": environment,
            }
        )
    )
    (config / "remote-settings.json.signature.json").write_text("{}")


def test_a_managed_configuration_is_recorded_by_count_and_fingerprint(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A managed configuration reaches every session and is counted, not named.

    A plugin installed at managed scope and enabled by signed remote settings
    starts its session; `run.json` and the report give how many managed
    plugins, environment settings and hooks there are and a fingerprint, and
    neither names a plugin, version, key or event. The plugin declares no
    hooks file, and the hook its session shows responding is counted from the
    transcript and accounted for.
    """
    config = tmp_path / "eval" / "config"
    manage(
        config,
        {"plugin-a@example": "1.0.0"},
        {"EXAMPLE_SETTING": "1", "EXAMPLE_OTHER_SETTING": "on"},
    )
    monkeypatch.setenv("STUB_AGENT_INJECT", "apply the managed rules")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    directory = tmp_path / "results" / "test"
    written = json.loads((directory / RUN).read_text())
    fingerprint = written["managed"].pop("fingerprint")
    assert written["managed"] == {"plugins": 1, "environment": 2, "hooks": 1}
    assert re.fullmatch(r"[0-9a-f]{64}", fingerprint)
    shown = (directory / RUN).read_text() + (directory / REPORT_MD).read_text()
    assert fingerprint in (directory / REPORT_MD).read_text()
    for named in (
        "plugin-a",
        "1.0.0",
        "EXAMPLE_SETTING",
        "EXAMPLE_OTHER_SETTING",
        "SessionStart",
        "apply the managed rules",
    ):
        assert named not in shown, named


def test_a_fingerprint_tells_two_managed_configurations_apart(
    tmp_path: Path, managed_settings: Path
) -> None:
    """One configuration gives one fingerprint; a changed one gives another.

    A changed version, environment key or hook event each changes the
    fingerprint, while the counts alone could not tell them apart, and a
    configuration with nothing managed has none.
    """
    claude = replace(Claude(), managed_settings=str(managed_settings))

    def fingerprint(name: str, version: str, environment: str, event: str) -> object:
        config = tmp_path / name
        manage(config, {"plugin-a@example": version}, {environment: "1"})
        return claude.managed(config, [event])["fingerprint"]

    first = fingerprint("first", "1.0.0", "EXAMPLE_SETTING", "EXAMPLE_EVENT")
    assert first == fingerprint("again", "1.0.0", "EXAMPLE_SETTING", "EXAMPLE_EVENT")
    others = {
        fingerprint("version", "1.0.1", "EXAMPLE_SETTING", "EXAMPLE_EVENT"),
        fingerprint("setting", "1.0.0", "EXAMPLE_OTHER", "EXAMPLE_EVENT"),
        fingerprint("event", "1.0.0", "EXAMPLE_SETTING", "EXAMPLE_OTHER_EVENT"),
    }
    assert first not in others and len(others) == 3
    (tmp_path / "none").mkdir()
    assert claude.managed(tmp_path / "none", []) == {
        "plugins": 0,
        "environment": 0,
        "hooks": 0,
        "fingerprint": None,
    }


def test_hook_events_are_read_from_every_transcript_once_each(
    tmp_path: Path,
) -> None:
    """Each event a hook response names counts once, whatever the sessions.

    Only the event is read, never the hook's output; a response naming no
    event counts as unnamed, and a missing transcript adds nothing.
    """
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    response = {"type": "system", "subtype": "hook_response"}
    first.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                {**response, "hook_event": "SessionStart", "output": "rules"},
                {"type": "system", "subtype": "hook_started", "hook_event": "Stop"},
                {"type": "assistant", "message": {"content": []}},
            )
        )
    )
    second.write_text(
        "not json\n"
        + json.dumps({**response, "hook_event": "SessionStart"})
        + "\n"
        + json.dumps({**response, "hook_event": "PreToolUse"})
        + "\n"
        + json.dumps(response)
    )
    seen = hook_events_seen([first, second, tmp_path / "absent.jsonl"])
    assert seen == ["PreToolUse", "SessionStart", "unnamed"]


def test_a_config_with_no_plugin_starts_every_session(
    tmp_path: Path, log: Path
) -> None:
    """A plugin listed but not enabled, and an empty enable map, are clean."""
    plugins = tmp_path / "eval" / "config" / "plugins" / "installed_plugins.json"
    plugins.parent.mkdir(parents=True)
    plugins.write_text(json.dumps({"version": 2, "plugins": {}}))
    (tmp_path / "eval" / "config" / "remote-settings.json").write_text(
        json.dumps({"enabledPlugins": {}})
    )
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1


def test_a_run_whose_settings_file_declares_a_hook_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """The directory's own settings file is refused before the first session.

    A `hooks` block in `settings.json` delivers a `SessionStart` command
    without installing a plugin, so the two files the preflight reads are
    no bound on what reaches a session. The refusal names the file and
    each event it declares, since either one arrives before the first turn.
    """
    settings = tmp_path / "eval" / "config" / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "theme": "dark",
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": "cat rules.md"}]}
                    ],
                    "PreToolUse": [
                        {"hooks": [{"type": "command", "command": "audit.sh"}]}
                    ],
                },
            }
        )
    )
    with pytest.raises(
        CorpusError,
        match=r"settings\.json declares a hook for PreToolUse, SessionStart.*"
        r"remove .*settings\.json before this run",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_settings_file_holds_only_preferences_starts_its_session(
    tmp_path: Path, log: Path
) -> None:
    """A settings file the eval may write itself is no refusal."""
    (tmp_path / "eval" / "config" / "settings.json").write_text(
        json.dumps({"theme": "dark", "model": "claude-haiku-5-5"})
    )
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1


def test_a_settings_file_that_is_not_json_is_refused(tmp_path: Path, log: Path) -> None:
    """A malformed settings file is refused as the other two files are."""
    (tmp_path / "eval" / "config" / "settings.json").write_text("{not json")
    with pytest.raises(CorpusError, match=r"settings\.json is not JSON"):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == [] and not (tmp_path / "results").exists()


HOOKED = {
    "hooks": {
        "SessionStart": [{"hooks": [{"type": "command", "command": "cat rules.md"}]}]
    }
}


def copied_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The linear workflow's diagram tree, copied where a test may plant settings."""
    corpus = tmp_path / "corpus"
    shutil.copytree(source.WORKFLOWS / "linear", corpus / "linear")
    monkeypatch.setattr(
        "run.workflows", lambda: [source.read_workflow(corpus / "linear")]
    )
    return corpus / "linear" / "diagram"


@pytest.mark.parametrize("name", ["settings.json", "settings.local.json"])
def test_a_form_tree_whose_project_settings_declare_a_hook_starts_no_session(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    """A tree's project settings reach every session copied from that tree."""
    tree = copied_tree(tmp_path, monkeypatch)
    (tree / ".claude").mkdir()
    (tree / ".claude" / name).write_text(json.dumps(HOOKED))
    with pytest.raises(
        CorpusError,
        match=rf"\.claude/{re.escape(name)} declares a hook for SessionStart.*"
        rf"remove .*{re.escape(name)} before this run",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", TREE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == [] and not (tmp_path / "results").exists()


@pytest.mark.parametrize("name", ["settings.json", "settings.local.json"])
def test_a_claude_directory_above_the_workspaces_declaring_a_hook_starts_no_session(
    tmp_path: Path, log: Path, name: str
) -> None:
    """An ancestor's project settings reach every session under the eval root."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / name).write_text(json.dumps(HOOKED))
    with pytest.raises(
        CorpusError,
        match=rf"\.claude/{re.escape(name)} declares a hook for SessionStart.*"
        r"--eval-root",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == [] and not (tmp_path / "results").exists()


def test_a_claude_directory_above_the_workspaces_without_a_hook_starts_its_session(
    tmp_path: Path, log: Path
) -> None:
    """An ancestor's settings that declare no hook are no refusal."""
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps({"theme": "dark"}))
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1


@pytest.fixture(autouse=True)
def managed_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The managed settings path a run reads, planted under tmp_path.

    The host's own file is never read: the Claude harness holds this path in
    its `managed_settings` field, absent until a test writes the file.
    """
    path = tmp_path / "managed" / "managed-settings.json"
    held = replace(Claude(), managed_settings=str(path))
    monkeypatch.setattr("run.harness_named", lambda name: held)
    return path


def test_a_managed_settings_hook_is_counted_and_its_sessions_start(
    tmp_path: Path, log: Path, managed_settings: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The host's managed hook reaches every session, so the run counts it.

    The administrator owns the file and Claude Code reads it wherever the
    configuration directory points, so the run starts its sessions and
    counts each hook event the transcripts show a hook responding to, not
    each the file declares, naming neither the file nor an event. The hook's
    response is the managed hook's, so it is no context the run failed to
    account for.
    """
    managed_settings.parent.mkdir()
    managed_settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": "cat rules.md"}]}
                    ],
                    "Stop": [],
                    "PreToolUse": [
                        {"hooks": [{"type": "command", "command": "audit.sh"}]}
                    ],
                }
            }
        )
    )
    monkeypatch.setenv("STUB_AGENT_INJECT", "apply the host's rules")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1
    shown = (tmp_path / "results" / "test" / RUN).read_text()
    written = json.loads(shown)
    fingerprint = written["managed"].pop("fingerprint")
    assert written["managed"] == {"plugins": 0, "environment": 0, "hooks": 1}
    assert re.fullmatch(r"[0-9a-f]{64}", fingerprint)
    for named in ("managed-settings.json", "PreToolUse", "SessionStart"):
        assert named not in shown, named


def test_an_absent_managed_settings_file_counts_no_hook(
    tmp_path: Path, log: Path, managed_settings: Path
) -> None:
    """A host with no managed settings file records nothing and starts its sessions."""
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert written["managed"] == {
        "plugins": 0,
        "environment": 0,
        "hooks": 0,
        "fingerprint": None,
    }


def test_a_managed_settings_file_declaring_no_hook_counts_none(
    tmp_path: Path, log: Path, managed_settings: Path
) -> None:
    """Managed preferences are no hook, so nothing is recorded."""
    managed_settings.parent.mkdir()
    managed_settings.write_text(json.dumps({"permissions": {"deny": ["WebFetch"]}}))
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert written["managed"] == {
        "plugins": 0,
        "environment": 0,
        "hooks": 0,
        "fingerprint": None,
    }


def test_a_managed_settings_file_that_is_not_json_is_refused(
    tmp_path: Path, log: Path, managed_settings: Path
) -> None:
    """An unreadable managed file is refused rather than read as declaring nothing."""
    managed_settings.parent.mkdir()
    managed_settings.write_text("{not json")
    with pytest.raises(CorpusError, match=r"managed-settings\.json is not JSON"):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == [] and not (tmp_path / "results").exists()


def test_the_claude_harness_defaults_its_managed_settings_to_the_hosts_path() -> None:
    """The unplanted harness reads the platform's system path."""
    assert Claude().managed_settings in MANAGED_SETTINGS.values()


def test_a_session_carrying_injected_context_fails_the_run(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A hook response the run did not supply is context it cannot measure through."""
    injected = "For work in elsewhere repositories, apply its rules skill"
    monkeypatch.setenv("STUB_AGENT_INJECT", injected)
    with pytest.raises(
        CorpusError,
        match=r"1 session\(s\) carried context this run did not supply.*carried a "
        r"hook response carrying .*apply its rules skill",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    [entry] = seen(log)
    assert entry["config"] == str(tmp_path / "eval" / "config")


def test_a_run_naming_every_carrying_session_starts_its_sessions(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The refusal names each session that carried context, not only the first."""
    monkeypatch.setenv("STUB_AGENT_INJECT", "another repository's rules")
    with pytest.raises(CorpusError) as raised:
        eval_run(
            tmp_path,
            *("--workflows", "linear,branching", "--forms", BUNDLE),
            *("--repetitions", "1", "--budget-tokens", "4000"),
        )
    message = str(raised.value)
    assert "3 session(s)" in message
    assert message.count("stub-model/linear/straight-through/bundle/1") == 1
    assert not (tmp_path / "results" / "test" / RUN).exists()


@pytest.mark.parametrize(
    ("workflow", "form"),
    [
        (workflow, form)
        for workflow in DISPATCHING
        for form in (COMPILED_SET, AUTHORED_SET)
    ],
    ids=lambda item: str(item),
)
def test_a_dispatch_scenario_takes_a_session_in_each_of_its_forms(
    tmp_path: Path, log: Path, workflow: str, form: str
) -> None:
    """AC1: each dispatch scenario runs in its compiled and authored forms."""
    eval_run(
        tmp_path,
        *("--workflows", workflow, "--forms", form),
        *("--repetitions", "1", "--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert (record["workflow"], record["form"]) == (workflow, form)
    assert record["verdict"]["passed"] is True, record["verdict"]
    assert record["verdict"]["actual"] == record["verdict"]["expected"]
    [scenario] = CORPUS[workflow].scenarios
    assert record["trace"] == [
        {
            "section": entry.section,
            "presets": sorted(entry.presets),
            "together": entry.together,
            "action": None if entry.action is None else list(entry.action),
        }
        for entry in scenario.trace
    ]


def test_the_report_gives_each_dispatch_scenarios_pass_rate_per_model_and_form(
    tmp_path: Path, log: Path
) -> None:
    """AC2: the report holds one cell per dispatch scenario, model and form.

    The run takes two models over the four dispatch scenarios in both
    forms, two repetitions each, the stub agent passing every session, so
    each cell reads two sessions and a pass rate of one. A second run over
    the compiled form stops its agent after one state, so its cells read a
    run that did not complete, and the report's per-scenario cells separate
    the rates the two forms give.
    """
    record = eval_run(
        tmp_path,
        *("--models", "stub-a,stub-b"),
        *("--workflows", ",".join(DISPATCHING)),
        *("--repetitions", "2", "--budget-tokens", "20000"),
    )
    built = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert record["started"] == built["sessions"] == 2 * 4 * 2 * 2
    assert built["state"] == "completed"
    cells = {
        (cell["model"], cell["form"], cell["workflow"], cell["scenario"]): cell
        for cell in built["cells"]
    }
    assert len(cells) == 2 * 2 * 4
    for workflow in DISPATCHING:
        [scenario] = CORPUS[workflow].scenarios
        for model in ("stub-a", "stub-b"):
            for form in (COMPILED_SET, AUTHORED_SET):
                cell = cells[(model, form, workflow, scenario.name)]
                assert (cell["sessions"], cell["passed"]) == (2, 2)
                assert cell["pass_rate"] == 1.0
    text = (tmp_path / "results" / "test" / REPORT_MD).read_text()
    assert text.count("| 100% |") >= 2 * 2 * 4


def session_of(record: dict[str, Any]) -> Session:
    """The session a record was written for."""
    return Session(
        record["model"],
        record["workflow"],
        record["scenario"],
        record["form"],
        record["repetition"],
    )


def test_a_dispatch_session_records_its_sub_agents_beside_its_trace(
    tmp_path: Path, log: Path
) -> None:
    """AC3: the record sits beside the trace and the cost the session recorded.

    A session's sub-agent starts are read from its transcript as it settles
    and written to `subagents.json`, so the scorer reads the record rather
    than opening the transcript again. Each entry names the section the
    sub-agent followed, what it returned and whether it started beside the
    entry above it. The scenario's sub-agent returns a question, the session
    starts it again with the answers in `answers.txt`, and the session passes
    on its path, its record and the sub-agent's action.
    """
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-question"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert {SUBAGENTS, TRACE, SESSION, TRANSCRIPT} <= {
        path.name for path in directory.iterdir()
    }
    [scenario] = CORPUS["dispatch-question"].scenarios
    [entry] = scenario.trace
    starts = read_starts(directory)
    assert [(start.returned, start.together) for start in starts] == [
        ("question", False),
        ("done", False),
    ]
    assert all(names_section(start.target, entry.section) for start in starts)
    assert record["verdict"]["passed"] is True


def test_a_sub_agents_trace_is_kept_beside_the_dispatching_sessions(
    tmp_path: Path, log: Path
) -> None:
    """AC16: a dispatched section's own path survives the workspace.

    A sub-agent following a section that holds a chart of its own records its
    states to `trace-<section>.log`, the name the instruction states. The
    session's path is kept beside it, so the two are read as one dispatch
    rather than as a nested chart's states mistaken for the outer path.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / TRACE).write_text("Scope\nGather\n")
    stated = "trace-review.log"
    (workspace / stated).write_text("read\nrank\n")
    records = tmp_path / "records"
    records.mkdir()
    keep(workspace, records)
    assert sorted(path.name for path in records.glob(TRACES)) == [stated, TRACE]
    assert (records / TRACE).read_text() == "Scope\nGather\n"
    assert (records / stated).read_text() == "read\nrank\n"


def handed_prompts(directory: Path) -> list[str]:
    """The prompt each `Agent` call in a session's transcript gave its sub-agent."""
    return [
        block["input"]["prompt"]
        for line in (directory / TRANSCRIPT).read_text().splitlines()
        if (said := json.loads(line)).get("type") == "assistant"
        for block in said["message"]["content"]
        if isinstance(block, dict) and block.get("name") == "Agent"
    ]


@pytest.mark.parametrize("form", DISPATCH_FORMS)
def test_a_scored_dispatch_keeps_the_sub_agents_trace_it_was_given(
    tmp_path: Path, log: Path, form: str
) -> None:
    """AC16, AC25: each sub-agent is told its trace's name, and the run keeps it.

    The session's instruction tells it to hand each sub-agent the name
    `keep()` reads, and the stub's sub-agent writes only the trace its prompt
    names. So the kept traces are those the instruction caused, in the
    compiled and the authored form alike, beside the session's own path.
    """
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", form, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    directory = session_of(record).directory(tmp_path / "results" / "test")
    [scenario] = CORPUS["dispatch-chain"].scenarios
    stated = [
        SUB_AGENT_TRACE.format(section=entry.section.partition("#")[2])
        for entry in scenario.trace
    ]
    assert record["verdict"]["passed"] is True
    prompts = handed_prompts(directory)
    assert len(prompts) == len(stated)
    assert all(name in prompt for name, prompt in zip(stated, prompts, strict=True))
    assert sorted(path.name for path in directory.glob(TRACES)) == sorted(
        [TRACE, *stated]
    )
    assert (directory / TRACE).read_text().split() == list(scenario.path)


def test_a_sub_agent_untold_its_trace_name_keeps_none(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC25: the sub-agent trace exists only because the instruction names it.

    An instruction without the sentence naming the sub-agent trace leaves the
    session nothing to hand on, so the stub's sub-agents are told no name and
    the run keeps the session's path alone.
    """
    text = source.INSTRUCTION.read_text()
    untold = tmp_path / "instruction.md"
    untold.write_text(
        re.sub(
            r"- When a state dispatches a sub-agent.*?\n(?=- )",
            "",
            text,
            flags=re.DOTALL,
        )
    )
    stated = SUB_AGENT_TRACE.format(section="<section>")
    assert stated in text
    assert stated not in untold.read_text()
    monkeypatch.setattr(source, "INSTRUCTION", untold)
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", AUTHORED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert all("trace-" not in prompt for prompt in handed_prompts(directory))
    assert [path.name for path in directory.glob(TRACES)] == [TRACE]


def test_a_run_starting_no_sub_agent_is_undispatched(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: a bundle set read and not dispatched is `undispatched`."""
    monkeypatch.setenv("STUB_AGENT_NO_DISPATCH", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "undispatched"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert read_starts(directory) == ()


def test_a_run_that_ran_a_set_in_sequence_is_sequential_set(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: a set's bundles started, but one after another."""
    monkeypatch.setenv("STUB_AGENT_SEQUENTIAL", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-set"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "sequential_set"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert [start.together for start in read_starts(directory)] == [False, False]


def test_a_question_the_session_answered_is_unrelayed_question(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A sub-agent's question not started again is answered in its place."""
    monkeypatch.setenv("STUB_AGENT_ANSWER", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-question"),
        *("--forms", AUTHORED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "unrelayed_question"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert [start.returned for start in read_starts(directory)] == ["question"]


def test_a_dispatch_run_that_stopped_short_is_unfinished(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: the completion check is read before any dispatch check."""
    monkeypatch.setenv("STUB_AGENT_STOP", "1")
    monkeypatch.setenv("STUB_AGENT_NO_DISPATCH", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "unfinished"
    assert record["verdict"]["actual"] == ["Entry"]


def test_a_scenario_dispatching_nothing_records_no_start(
    tmp_path: Path, log: Path
) -> None:
    """A workflow dispatching nothing passes the dispatch checks with no record."""
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["passed"] is True
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert (directory / SUBAGENTS).is_file()
    assert read_starts(directory) == ()


def dispatch_run(tmp_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """A run over every dispatch scenario in both forms, by scenario and form."""
    eval_run(
        tmp_path,
        *("--workflows", ",".join(DISPATCHING)),
        *("--forms", ",".join(DISPATCH_FORMS)),
        *("--repetitions", "1", "--budget-tokens", "8000"),
    )
    written = records(tmp_path)
    cells = {(record["scenario"], record["form"]): record for record in written}
    assert len(written) == len(cells) == len(DISPATCHING) * len(DISPATCH_FORMS)
    return cells


def test_the_departure_table_names_every_dispatch_scenario() -> None:
    """Each script's predicted class is stated for the corpus the run walks."""
    for departure, (_, predicted) in DEPARTURES.items():
        assert set(predicted) == set(DISPATCH_SCENARIOS), departure


@pytest.mark.parametrize("departure", DEPARTURES, ids=str)
def test_a_departure_is_classified_across_every_dispatch_scenario(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch, departure: str
) -> None:
    """AC4: each scenario in each form takes the class its script predicts."""
    value, predicted = DEPARTURES[departure]
    monkeypatch.setenv(departure, value)
    cells = dispatch_run(tmp_path)
    assert set(cells) == {
        (scenario, form) for scenario in DISPATCH_SCENARIOS for form in DISPATCH_FORMS
    }
    for (scenario, form), record in cells.items():
        verdict = record["verdict"]
        due = predicted[scenario]
        assert verdict["failure"] == (None if due is None else str(due)), (
            f"{departure} over {scenario}/{form}: {verdict}"
        )
        assert verdict["passed"] is (due is None), verdict


def test_a_clean_run_passes_every_dispatch_cell(tmp_path: Path, log: Path) -> None:
    """AC4: with no departure scripted, every scenario in both forms passes."""
    cells = dispatch_run(tmp_path)
    for (scenario, form), record in cells.items():
        verdict = record["verdict"]
        assert verdict["passed"] is True, f"{scenario}/{form}: {verdict}"
        assert verdict["failure"] is None
        assert verdict["actual"] == verdict["expected"]


def test_a_compiled_session_runs_pf_bare_and_compiles_a_composition_line(
    tmp_path: Path,
) -> None:
    """AC12: the build under test is `pf` on a compiled session's path.

    The shell the session gets runs bare `pf` for the guide and compiles a
    `↳` line, which a bundle set alone cannot do.
    """
    workflow = CORPUS["dispatch-chain"]
    scenario = workflow.scenarios[0]
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    sets = {(workflow.name, COMPILED_SET): bundles_of(workflow, COMPILED_SET)}
    prepare(workspace, workflow, scenario, COMPILED_SET, sets)
    assert not (workspace / "bin" / "pf").exists()
    pf = "pf"
    guide = subprocess.run([pf], capture_output=True, text=True, check=False)
    assert guide.stdout.startswith("pf compiles"), guide.stdout
    (workspace / "guide.md").write_text(
        "---\nprosiform: {}\n---\n# Guide\n\n## Run\n\nDo [↳ Steps](plan.md#steps).\n"
    )
    (workspace / "plan.md").write_text(
        "---\nprosiform: {}\n---\n# Plan\n\n## Steps\n\nCount the files.\n"
    )
    compiled = subprocess.run(
        [pf, "--entry", "guide.md", "-o", str(tmp_path / "out")],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    assert compiled.returncode == 0, compiled.stderr
    [written] = (tmp_path / "out").glob("*.bundles/guide.bundle.md")
    assert "Count the files." in written.read_text()


def test_every_form_is_given_pf_on_its_path_and_a_shell_limited_to_it(
    tmp_path: Path, log: Path
) -> None:
    """Every form can run the build; workspace material contains no pf copy."""
    eval_run(
        tmp_path,
        *("--repetitions", "1", "--budget-tokens", "100000"),
    )
    entries = seen(log)
    assert entries
    for entry in entries:
        argv = entry["argv"]
        assert "bin/pf" not in entry["files"]
        assert Path(entry["pf"]).is_file()
        assert argv[argv.index("--allowedTools") + 1] == "Bash(pf *)"
        assert argv[argv.index("--tools") + 1].endswith(",Bash")
    transcripts = [
        path.read_text() for path in (tmp_path / "results" / "test").rglob(TRANSCRIPT)
    ]
    assert all('"command": "pf"' in text for text in transcripts)


def test_a_run_naming_the_staged_form_is_refused_as_an_unknown_form(
    tmp_path: Path, log: Path
) -> None:
    """AC18: one `compiled` form, and `staged` names none."""
    assert "staged" not in FORMS
    with pytest.raises(CorpusError, match="unknown form staged"):
        eval_run(tmp_path, "--forms", "staged", "--budget-tokens", "4000")
    assert not list(log.iterdir())
