#!/usr/bin/env python3
"""Bundle the example work-planner skill against stand-in material.

The example skill is the mapping's first real consumer. Exercising it needs
two things the shipped tree cannot give: an artifact varied without editing the
skill, and a tracker answered without a live repository. Both arrive as a
mapping, so neither touches the tree under test.

Two scenarios run here. The plan mode is bundled over `artifacts/epic.md`
stubbed, so the stub's words stand where that artifact's stood inside the merged
artifacts group and the `## Epic` heading the group emits still stands; and
`conventions.md` is redirected to a document naming a fake tracker command, so
the bundle an agent follows tells it to run the stand-in while every other
instruction stays the one that ships.

This is a check rather than a corpus fixture because the corpus cannot express
it. A `usage-example` fixture reaches the tree through a symbolic link, while a
run takes the resolved working directory, so a substitute written relative to
that link lands beside the link's target; and the build refuses a symbolic link
in any traversed component, so a fixture naming a path under `source/` cannot
read its own tree. A copied `source/` would work and would reintroduce the drift
the link prevents.

The copy is therefore made here, once per run: `example/work-planner` is copied
into a temporary directory, the scenario's stubs are written beside the copy,
and each scenario bundles the copied mode whole. One tree is maintained,
nothing is checked in twice, and the copy lasts for the run.

Every run publishes into a folder of the temporary directory, so neither the
shipped tree nor its copy is a destination. Both trees are fingerprinted either
side of the scenarios, which is what a run publishing into the skill directory
fails on.

Each scenario's expectation is the bundle the same tree produces unmocked,
reached in the same copy. Material that moves therefore moves both sides and
only a difference the substitution makes can be red. The mocked bundle is held
to four things: the run states the substitution it performed, the artifact's
heading is emitted once at the depth its own front matter decides, every byte
outside that section is the unmocked bundle's, and inside the section the
stand-in's words stand in place of the artifact's.
"""

import hashlib
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from runner import (
    BUILD,
    BuildNotConfigured,
    Difference,
    build_timeout,
    build_under_test,
    parse_diagnostics,
)

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "example" / "work-planner"
ENTRY = "modes/plan-mode.md"
BUNDLE = "modes_plan-mode.bundles/modes_plan-mode.bundle.md"

MAPPING = "mapping"
BUNDLES = "bundle"
SUBSTITUTION = "substitution"
TREE = "tree"
SUBSTITUTED = "W_MOCK_SUBSTITUTED"

ARTIFACT_STUB = """\
---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Epic

A stand-in for an epic artifact still under authoring: the sections the skill
reaches by name, each stated as the placeholder a draft carries.

## Operations

### Check Epic Prerequisites

Placeholder for the prerequisite check a drafted epic states.

### Inspect Epic Delivery

Placeholder for the delivery inspection a drafted epic states.

### Match Delivery to Tasks

Placeholder for the task matching a drafted epic states.

### Check Epic Readiness

Placeholder for the readiness check a drafted epic states.

### Check Epic Completion

Placeholder for the completion check a drafted epic states.

## Fields

### Task Matches

Placeholder for the task matches a drafted epic returns.

### Prerequisite Evidence

Placeholder for the prerequisite evidence a drafted epic returns.

### Delivery State

Placeholder for the delivery state a drafted epic records.

### Delivery Findings

Placeholder for the delivery findings a drafted epic returns.
"""

CONVENTIONS_STUB = """\
---
prosiform:
  root: "."
---
# Conventions

The prerequisites every mode's run shares: the session it starts in, where a
command runs, how a result is read, and the values its examples use. Each is
stated once here, and every step applying one links it.

## Session

Every tracker call in this run is written `./fake-gh`, the stand-in for the
tracker. Once per session, before the first `./fake-gh` call, confirm
`GH_TOKEN` and `GITHUB_TOKEN` are unset so the stand-in reads the login the
session was given.

## Repository

`./fake-gh` resolves `{owner}/{repo}` from the git remote of the directory it
runs in, so run `./fake-gh` commands inside a checkout of the repository that
holds the issues. `{other}` is a further repository the board's issues live in.

## Bodies

- Bodies, long comments and commit messages always go through a file
  (`-F body=@file`), never inline, which avoids quoting. The file holds the
  exact intended text.
- Keep these files in a working directory outside the repository.

## Helper Invocation

A helper is a script in `<workspace>`, the checkout holding this skill. It runs
from `<workspace>`, or the directory within it that its command names, under
the sandbox invoked by its absolute path, `<workspace>/scripts/sbx`. A file
kept outside `<workspace>`, such as a body file, is passed by its absolute
path.

## Command Result

Read each command's exit code and output before the next step. A failing exit
code, or a refusal the command reports, returns to the caller as an execution
error or refusal before the work continues.

## Helper Result

A helper's written body exists only on a zero exit code. An invocation failure
returns as a blocker, and only a successfully written body is published.

## Write Confirmation

Only a fresh re-read confirms a write: read the written object again and
compare it with the intended state. The write's own output confirms nothing. A
re-read that fails, or shows another state, leaves the write uncertain; that
uncertainty returns to the caller, and the write is never retried as a
different write.

- A list read can lag a write, so a written item confirms by its own read
  alone. An item still showing the preceding state has the same write repeated
  and that item read again.

## Boards

A project board sits under `users/{owner}`, or `orgs/{owner}` when
`./fake-gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.

## Example Values

Substitute the real ones:

- `936` an initiative issue, `943` and `937` its epics, `637` a task issue,
  `874` an orphan, `946` an initiative off the board, `960` a proposal;
- `950` a pull request, `I07` and `I08` initiative numbers;
- board `9` a theme board, and `419167630` its Status field id;
- `1` the Initiative Template board, `13` a board copied from it;
- `14` the Proposals Template, `15` the Proposals board;
- `m2ux` the user.
- `<checkout>` any checkout of the project, a linked worktree included.
"""


@dataclass(frozen=True)
class Stub:
    """One stand-in: the file it is written as, its bytes and what it replaces."""

    file: str
    text: str
    key: str


@dataclass(frozen=True)
class Scenario:
    """One scenario: the stand-in supplied, where it lands and what it instructs.

    `heading` is the heading the bundle carries for the stand-in's artifact, and
    `member` states whether that artifact joins a merged group: a member's title
    is an ordinary heading inside the group, so the run emits no paragraph
    beneath it and the artifact's own words stand there unchanged.
    """

    name: str
    stub: Stub
    heading: str
    member: bool
    command: str
    avoided: str

    @property
    def replaces(self) -> str:
        """The heading the stand-in would carry as a document of its own."""
        return self.heading[1:]


ARTIFACTS = Scenario(
    name="an-example-mode-bundled-against-a-stub",
    stub=Stub("epic-minimal.md", ARTIFACT_STUB, "artifacts/epic.md"),
    heading="## Epic",
    member=True,
    command="Placeholder for the prerequisite check a drafted epic states.",
    avoided="The evidence required before starting an epic's work.",
)

CONVENTIONS = Scenario(
    name="an-example-skill-told-to-use-a-fake-gh",
    stub=Stub("fake-gh-conventions.md", CONVENTIONS_STUB, "conventions.md"),
    heading="# Conventions",
    member=False,
    command="`./fake-gh`",
    avoided="uses its keyring login",
)

SCENARIOS = (ARTIFACTS, CONVENTIONS)


@dataclass(frozen=True)
class Finished:
    """One run of the build: its status, its streams and its diagnostics."""

    status: int
    stdout: bytes
    stderr: bytes

    def diagnostics(self) -> list[dict[str, object]]:
        """The JSON diagnostics the run wrote, and any line that is not one."""
        parsed, malformed = parse_diagnostics(self.stderr)
        found: list[dict[str, object]] = list(parsed)
        found.extend({"severity": "unreadable", "message": line} for line in malformed)
        return found


def depth(heading: str) -> int:
    """A heading's level, counted by the marks it opens with."""
    return len(heading) - len(heading.lstrip("#"))


def headings(text: str) -> list[str]:
    """Every heading the text carries, in the order it carries them."""
    return [line.rstrip() for line in text.splitlines() if line.startswith("#")]


def section(text: str, heading: str) -> tuple[int, int] | None:
    """One section's offsets: its heading to the next heading of its level or above."""
    level = depth(heading)
    offset = 0
    start: int | None = None
    for line in text.splitlines(keepends=True):
        if start is None:
            if line.rstrip("\n") == heading:
                start = offset
        elif line.startswith("#") and depth(line.rstrip("\n")) <= level:
            return start, offset
        offset += len(line)
    return None if start is None else (start, len(text))


def carried(text: str, heading: str) -> str:
    """What a text carries under one heading, or nothing when it carries none."""
    found = section(text, heading)
    return "" if found is None else text[found[0] : found[1]]


def titled(heading: str) -> str:
    """One heading's title, without the marks that place it."""
    return heading.lstrip("#").strip()


def placed(text: str) -> list[tuple[str, str]]:
    """Each run of prose the text carries, with the title of the heading above it.

    A document's front matter names its settings rather than its content, so it
    is skipped: the run reads it and emits none of it.
    """
    body = text
    if body.startswith("---\n"):
        end = body.find("\n---\n", len("---\n"))
        if end != -1:
            body = body[end + len("\n---\n") :]
    found: list[tuple[str, str]] = []
    heading = ""
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("#"):
            heading = titled(line)
        if not line.strip() or line.startswith("#"):
            if current:
                found.append((heading, "\n".join(current)))
                current = []
            continue
        current.append(line)
    if current:
        found.append((heading, "\n".join(current)))
    return found


def reachable(
    text: str, heading: str, baseline: str, *, member: bool
) -> list[tuple[str, str]]:
    """The blocks a run reaches, which are the ones under a heading it emits.

    A stand-in is read whole but emitted only as far as the mode's own closure
    reaches it, so a block under a heading the unmocked bundle carries is one
    the run publishes and a block under any other is material the run never
    asked for. A member of a merged group contributes no title paragraph: that
    paragraph is the group's, and the artifact's stands where the group puts it.
    """
    reached = {titled(one) for one in headings(carried(baseline, heading))}
    reached.add(titled(heading))
    return [
        one
        for one in placed(text)
        if one[0] in reached and not (member and one[0] == titled(heading))
    ]


def fingerprint(root: Path) -> dict[str, str]:
    """Every path under a tree, each file by the digest of its bytes."""
    return {
        path.relative_to(root).as_posix(): (
            hashlib.sha256(path.read_bytes()).hexdigest()
            if path.is_file()
            else "folder"
        )
        for path in sorted(root.rglob("*"))
    }


def run(working: Path, output: Path, stub: Stub | None) -> Finished:
    """One bundling run of the copied mode, publishing into the output folder.

    The output folder is one of the temporary directory's own, so neither the
    shipped tree nor its copy is a destination. A stand-in is named from the
    copied tree by a parent segment, which is where the stubs are written.
    """
    output.mkdir(parents=True, exist_ok=True)
    named = [] if stub is None else ["-m", f"{stub.key}=../stubs/{stub.file}"]
    completed = subprocess.run(
        [*build_under_test(), "-d", "json", "-o", str(output), *named, ENTRY],
        cwd=working,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=build_timeout(),
        check=False,
    )
    return Finished(completed.returncode, completed.stdout, completed.stderr)


def compare_status(name: str, finished: Finished) -> list[Difference]:
    """The run's status, against the successful bundling a scenario expects."""
    if finished.status == 0:
        return []
    detail = [
        f"wrote {line!r}"
        for line in finished.stderr.decode("utf-8", "replace").splitlines()[:4]
    ]
    return [
        Difference(MAPPING, f"{name}: the run exited {finished.status}", tuple(detail))
    ]


def compare_substitution(name: str, finished: Finished, stub: Stub) -> list[Difference]:
    """The one substitution the run states, naming the artifact and its stand-in."""
    found = [one for one in finished.diagnostics() if one.get("code") == SUBSTITUTED]
    if len(found) != 1:
        return [
            Difference(
                SUBSTITUTION,
                f"{name}: the run states {len(found)} substitution(s) where one "
                f"is expected",
                tuple(str(one.get("message")) for one in finished.diagnostics()),
            )
        ]
    message = str(found[0].get("message"))
    absent = [entry for entry in (stub.key, stub.file) if entry not in message]
    if absent:
        return [
            Difference(
                SUBSTITUTION,
                f"{name}: the substitution names neither the artifact nor its stand-in",
                (f"wrote {message!r}",),
            )
        ]
    return []


def compare_placement(
    name: str, scenario: Scenario, baseline: str, produced: str
) -> list[Difference]:
    """The artifact's heading, emitted once at the depth its front matter decides.

    A stand-in declaring the merged artifacts group is a member of it, so the
    group's level names no such document; a stand-in declaring no group is
    emitted as a title of its own. The count states that the heading appears
    once rather than once per reference that reached it.
    """
    carried_headings = headings(produced)
    differences = []
    if carried_headings.count(scenario.heading) != 1:
        differences.append(
            Difference(
                BUNDLES,
                f"{name}: the bundle carries {scenario.heading} "
                f"{carried_headings.count(scenario.heading)} times where it is "
                f"emitted once",
            )
        )
    if scenario.member and scenario.replaces in carried_headings:
        differences.append(
            Difference(
                BUNDLES,
                f"{name}: the bundle carries {scenario.replaces}, so the stand-in is "
                f"emitted as a document of its own rather than as the group member "
                f"its front matter declares",
            )
        )
    if section(baseline, scenario.heading) is None:
        differences.append(
            Difference(
                BUNDLES,
                f"{name}: the unmocked bundle carries no {scenario.heading}, so the "
                f"stand-in occupies no section of it",
            )
        )
    return differences


def compare_outside(
    name: str, scenario: Scenario, baseline: str, produced: str
) -> list[Difference]:
    """Every byte outside the section, against the unmocked bundle's."""
    held = section(baseline, scenario.heading)
    if held is None:
        return []
    start, end = held
    if baseline[:start] != produced[:start]:
        return [
            Difference(
                BUNDLES,
                f"{name}: the bundle differs ahead of {scenario.heading}, where the "
                f"run substituted nothing",
            )
        ]
    tail = len(baseline) - end
    if len(produced) < tail or baseline[end:] != produced[len(produced) - tail :]:
        return [
            Difference(
                BUNDLES,
                f"{name}: the bundle differs after {scenario.heading}, where the run "
                f"substituted nothing",
            )
        ]
    return []


def compare_section(
    name: str, scenario: Scenario, baseline: str, produced: str
) -> list[Difference]:
    """The section the stand-in occupies, against the stand-in's own words.

    The run's section carries the stand-in's prose and none of the artifact's,
    which is what "the substitute becomes the target" states: the artifact's
    paragraphs stand only where the stand-in states none, and every paragraph
    the stand-in writes is carried. The headings are held the other way, since
    a stand-in's own section headings place its text within the artifact's
    outline rather than adding headings of their own.
    """
    found = section(produced, scenario.heading)
    if found is None:
        return [
            Difference(BUNDLES, f"{name}: the bundle carries no {scenario.heading}")
        ]
    text = produced[found[0] : found[1]]
    stand_in = scenario.stub.text
    differences = [
        Difference(BUNDLES, f"{name}: the section carries no {block!r}")
        for _, block in reachable(
            stand_in, scenario.heading, baseline, member=scenario.member
        )
        if block not in text
    ]
    differences.extend(
        Difference(
            BUNDLES,
            f"{name}: the section carries {block!r}, which the stand-in does not state",
        )
        for _, block in placed(carried(baseline, scenario.heading))
        if block not in stand_in and block in text
    )
    return differences


def compare_instruction(
    name: str, scenario: Scenario, produced: str
) -> list[Difference]:
    """The instruction the bundle gives a session, against the stand-in's own.

    The redirected document names the stand-in where the shipped one names the
    tracker, so a bundle read whole is followed against the fake.
    """
    text = carried(produced, scenario.heading)
    differences = []
    if scenario.command not in text:
        differences.append(
            Difference(
                BUNDLES,
                f"{name}: the section tells the session to run no {scenario.command!r}",
            )
        )
    if scenario.avoided in text:
        differences.append(
            Difference(
                BUNDLES,
                f"{name}: the section still states {scenario.avoided!r}, so the "
                f"bundle reaches the material the stand-in exists to replace",
            )
        )
    return differences


def compare_tree(
    name: str, before: dict[str, str], after: dict[str, str]
) -> list[Difference]:
    """One tree, against the state it held before the scenarios ran."""
    if before == after:
        return []
    written = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(
        one for one in set(before) & set(after) if before[one] != after[one]
    )
    return [
        Difference(
            TREE,
            f"{name}: the runs wrote to the tree they read",
            (
                *[f"written {one}" for one in written],
                *[f"removed {one}" for one in removed],
                *[f"changed {one}" for one in changed],
            ),
        )
    ]


def report(
    scenario: Scenario, baseline: str, produced: str, finished: Finished
) -> list[Difference]:
    """Every expectation one scenario states, as the differences it did not meet."""
    return [
        *compare_status(scenario.name, finished),
        *compare_substitution(scenario.name, finished, scenario.stub),
        *compare_placement(scenario.name, scenario, baseline, produced),
        *compare_outside(scenario.name, scenario, baseline, produced),
        *compare_section(scenario.name, scenario, baseline, produced),
        *compare_instruction(scenario.name, scenario, produced),
    ]


def bundled(root: Path) -> str:
    """The bundle a run published, or nothing when it published none."""
    path = root / BUNDLE
    return path.read_text() if path.is_file() else ""


def check(working: Path) -> list[tuple[str, list[Difference]]]:
    """Both scenarios over one copy of the tree, and both trees either side.

    A run that writes no bundle is reported as the difference it is, so a red
    run names the output the run failed to publish rather than raising over the
    file it did not find.
    """
    shipped = fingerprint(SKILL)
    copy = working / "skill"
    shutil.copytree(SKILL, copy)
    copied = fingerprint(copy)
    stubs = working / "stubs"
    stubs.mkdir()
    for scenario in SCENARIOS:
        (stubs / scenario.stub.file).write_text(scenario.stub.text)

    baseline = run(copy, working / "unmocked", None)
    held = bundled(working / "unmocked")
    found: list[tuple[str, list[Difference]]] = [
        ("the copy of the tree", compare_tree("the copy", shipped, copied))
    ]
    if baseline.status != 0 or not held:
        found.append(
            ("the unmocked bundle", compare_status("the unmocked bundle", baseline))
        )
    else:
        for scenario in SCENARIOS:
            finished = run(copy, working / scenario.name, scenario.stub)
            produced = bundled(working / scenario.name)
            differences = (
                report(scenario, held, produced, finished)
                if produced
                else [
                    *compare_status(scenario.name, finished),
                    Difference(BUNDLES, f"{scenario.name}: the run wrote no {BUNDLE}"),
                ]
            )
            found.append((scenario.name, differences))
    found.append(
        (
            "the shipped example tree",
            compare_tree("the skill", shipped, fingerprint(SKILL)),
        )
    )
    found.append(
        ("the copied tree", compare_tree("the copy", copied, fingerprint(copy)))
    )
    return found


def main() -> int:
    try:
        build_under_test()
    except BuildNotConfigured as absent:
        print(f"mock scenario check: {absent}", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as scratch:
        found = check(Path(scratch))
    for name, differences in found:
        print(f"{name}: {'fail' if differences else 'pass'}")
        for difference in differences:
            print(f"  {difference.expectation}: {difference.summary}")
            for line in difference.detail:
                print(f"    {line}")
    failed = sum(1 for _, differences in found if differences)
    print(
        f"mock scenario check: {len(found)} scenario(s), {len(found) - failed} pass, "
        f"{failed} fail, held against the build {BUILD} names"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
