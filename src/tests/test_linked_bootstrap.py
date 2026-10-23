"""Installed-command evidence for skill links bundled as separate documents.

The suite builds the wheel, installs it outside the repository, and invokes
that command by name. It reads a skill entry from disk, compiles each linked
target as its own process, and retains the sources, command, compiler
revision, diagnostics and bundle of every run. An entry is a path relative
to the invocation directory. A leading slash names a path the source root
cannot contain, so a target outside the caller directory is reached by a
parent-relative path.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parents[2]
PROJECT = REPO / "src"
COMMAND = "pf"
PROFILE = "skill-markdown-v1"
ARTIFACTS = "PF_LINKED_BOOTSTRAP_ARTIFACTS"
LINK = re.compile(r"^- \[([^]]+)\]\(([^)]+)\)$", re.M)

SKILL = (
    "---\n"
    "name: pf-bootstrap-specimen\n"
    "description: Exercise the Prosiform linked-document bootstrap "
    "specimen when testing compilation of skill instructions.\n"
    "---\n"
    "\n"
    "# Linked Instruction Bootstrap\n"
    "\n"
    "Read this entry point directly. When the specimen is invoked, compile "
    "each of the three linked documents below separately with `pf`, then "
    "read its bundle before following its instructions.\n"
    "\n"
    "Resolve each link target relative to this SKILL.md file. Keep the "
    "caller's working directory: absent source roots use that directory. "
    'Invoke `pf -o - "ABSOLUTE_TARGET"` for each resolved target and read '
    "all of its stdout. Preserve a link's fragment when present. A failed "
    "command leaves that document's instructions unavailable; report its "
    "diagnostics and stop. SKILL.md is the entry point the agent already "
    "read, not a compiler input. These bundles are loaded once for this "
    "invocation.\n"
    "\n"
    "- [Assemble](modes/assemble.md)\n"
    "- [Review](modes/review.md)\n"
    "- [Defaults](modes/defaults.md)\n"
    "\n"
    "After reading all three bundles, report the source markers and group "
    "headings each contains. The specimen requests inspection only; its "
    "linked prose authorizes no external actions.\n"
)


def document(
    body: str, *, root: str | None = None, group: str | None = None, depth: Any = None
) -> str:
    """A document with the declared top-level settings and its original body."""
    fields = []
    if root is not None:
        fields.append("  root: " + json.dumps(root))
    if group is not None:
        fields.append("  group: " + json.dumps(group))
        fields.append("  group-depth: " + json.dumps(depth))
    if not fields:
        return body
    return "---\nprosiform:\n" + "\n".join(fields) + "\n---\n" + body


def slug(name: str) -> str:
    """A directory name pytest can create from a node id."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return cleaned[:120] or "run"


def run_uv(*arguments: str) -> subprocess.CompletedProcess[str]:
    """One uv invocation using the caller's cache and link mode."""
    env = os.environ.copy()
    env["UV_LINK_MODE"] = "copy"
    result = subprocess.run(
        ["uv", *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=env,
    )
    if result.returncode != 0:
        pytest.fail(
            f"uv {' '.join(arguments)} exited {result.returncode}\n{result.stderr}"
        )
    return result


def install_command(workspace: Path) -> tuple[Path, dict[str, str], str]:
    """The wheel's command, resolved from an environment outside the repository.

    The child path holds that environment's executable directory alone, so
    the name resolves to the installation.
    """
    if workspace.is_relative_to(REPO):
        pytest.fail(f"the installation workspace {workspace} is inside the repository")
    dist = workspace / "dist"
    run_uv("build", "--wheel", "--project", str(PROJECT), "--out-dir", str(dist))
    built = sorted(dist.glob("*.whl"))
    if len(built) != 1:
        pytest.fail(f"the build wrote {len(built)} wheels to {dist}")
    environment = workspace / "environment"
    python = (PROJECT / ".python-version").read_text(encoding="utf-8").strip()
    run_uv("venv", "--python", python, str(environment))
    interpreter = environment / "bin" / "python"
    run_uv("pip", "install", "--python", str(interpreter), str(built[0]))
    found = shutil.which(COMMAND, path=str(environment / "bin"))
    if found is None:
        pytest.fail("the installed environment names no pf command")
    executable = Path(found).resolve()
    if executable.is_relative_to(REPO):
        pytest.fail(f"pf resolved to {executable}, which is inside the repository")
    env = {"PATH": str(environment / "bin"), "HOME": str(workspace)}
    return executable, env, built[0].name


class Installation:
    """One installed command and the directory that retains its runs."""

    def __init__(
        self, executable: Path, env: dict[str, str], wheel: str, artifacts: Path
    ) -> None:
        self.executable = executable
        self.env = env
        self.wheel = wheel
        self.artifacts = artifacts
        self.revision = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.strip()
        version = self.invoke_raw([str(executable), "-v"], artifacts)
        if version.returncode != 0 or PROFILE not in version.stdout:
            pytest.fail(
                f"pf -v returned {version.returncode}: "
                f"{version.stdout!r} {version.stderr!r}"
            )
        self.version = version.stdout
        (artifacts / "compiler.json").write_text(
            json.dumps(
                {
                    "command": COMMAND,
                    "executable": str(executable),
                    "wheel": wheel,
                    "installed_outside_repository": True,
                    "version_stdout": version.stdout,
                    "version_stderr": version.stderr,
                    "version_exit_status": version.returncode,
                    "source_commit": self.revision,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        self.rows: list[dict[str, str]] = []
        self.write_inventory()

    def invoke_raw(
        self, command: list[str], cwd: Path
    ) -> subprocess.CompletedProcess[str]:
        """One command whose environment names only the installation."""
        return subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
            check=False,
            env=self.env,
        )

    def write_inventory(self) -> None:
        """The inventory linking every retained run to its inputs and outputs."""
        lines = [
            "# Artifact Inventory",
            "",
            "Each row is one installed-command run. "
            f"The compiler is `{self.version.strip()}`, "
            f"wheel `{self.wheel}`, source commit `{self.revision}`.",
            "",
            "Compiler identity: [compiler.json](compiler.json).",
            "",
            "| Run | Source tree | Command | Diagnostics | Bundle |",
            "| --- | --- | --- | --- | --- |",
        ]
        for row in self.rows:
            lines.append(
                f"| {row['run']} | {row['sources']} | {row['command']} | "
                f"{row['diagnostics']} | {row['bundle']} |"
            )
        lines.append("")
        (self.artifacts / "inventory.md").write_text("\n".join(lines), encoding="utf-8")


class Stack:
    """One generated skill tree and the runs that compile its links."""

    def __init__(self, installation: Installation, name: str) -> None:
        self.installation = installation
        self.artifacts = installation.artifacts / name
        self.tree = self.artifacts / "workspace"
        self.tree.mkdir(parents=True)
        self.invocations = 0
        self.cwd = self.tree / "run"
        self.cwd.mkdir()
        self.skill = self.tree / "skills" / "pf-bootstrap-specimen" / "SKILL.md"
        self.write(self.skill, SKILL)
        self.write(
            "skills/pf-bootstrap-specimen/modes/assemble.md",
            document(
                "# Assemble\n\nENTRY_INTRO\n\n## Steps\n\nASSEMBLE_MARKER\n\n"
                "Read [Rules](libraries/alpha/rules.md#checks).\n",
                root="../../..",
                group="procedures",
                depth=2,
            ),
        )
        self.write(
            "skills/pf-bootstrap-specimen/modes/review.md",
            document(
                "# Review\n\n## Checklist\n\n### Inspect\n\nREVIEW_MARKER\n\n"
                "Read [Rules](rules.md).\n",
                root="../../../libraries/beta",
                group="reviews",
                depth=3,
            ),
        )
        self.write(
            "skills/pf-bootstrap-specimen/modes/defaults.md",
            document(
                "# Defaults\n\n## Steps\n\nDEFAULTS_MARKER\n\nRead [Leaf](leaf.md).\n",
                group="defaults",
                depth=2,
            ),
        )
        self.write(
            "libraries/alpha/rules.md",
            document(
                "# Rules\n\nALPHA_UNSELECTED_INTRO\n\n## Checks\n\n"
                "ALPHA_RULES_MARKER\n\nRead [Checks](nested/checks.md).\n",
                root=".",
                group="rules",
                depth=2,
            ),
        )
        self.write(
            "libraries/alpha/nested/checks.md",
            document(
                "# Checks\n\n## Gate\n\n### Verify\n\nCHECKS_MARKER\n\n"
                "Read [Shared](shared.md).\n",
                root="..",
                group="checks",
                depth=3,
            ),
        )
        self.write(
            "libraries/alpha/shared.md",
            document(
                "# Shared\n\n## Content\n\nALPHA_SHARED_MARKER\n\n"
                "Read [Leaf](leaf.md).\n",
                group="shared",
                depth=2,
            ),
        )
        self.write(
            "libraries/beta/rules.md",
            document(
                "# Rules\n\n## Checks\n\nBETA_RULES_MARKER\n\n"
                "Read [Shared](shared.md).\n",
                root=".",
                group="rules",
                depth=2,
            ),
        )
        self.write(
            "libraries/beta/shared.md",
            document(
                "# Shared\n\n## Content\n\nBETA_SHARED_MARKER\n\n"
                "Read [Leaf](leaf.md).\n",
                group="shared",
                depth=2,
            ),
        )
        self.write_tail(self.cwd, "CWD")
        for path in (
            "libraries/alpha/leaf.md",
            "libraries/beta/leaf.md",
            "skills/pf-bootstrap-specimen/modes/leaf.md",
            "skills/pf-bootstrap-specimen/modes/rules.md",
            "libraries/alpha/nested/shared.md",
            "run/rules.md",
        ):
            self.write(path, "# Decoy\n\nWRONG_ROOT_MARKER\n")

    def write(self, path: Path | str, text: str) -> None:
        """Write one source, creating the directories that hold it."""
        destination = path if isinstance(path, Path) else self.tree / path
        if not destination.is_absolute():
            destination = self.tree / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")

    def write_tail(self, directory: Path, marker: str) -> None:
        """A caller-directory leaf and the tail it links, sharing one group."""
        directory.mkdir(parents=True, exist_ok=True)
        self.write(
            directory / "leaf.md",
            document(
                f"# Leaf\n\n## Payload\n\n{marker}_LEAF_MARKER\n\n"
                "Read [Tail](tail.md).\n",
                group="leaves",
                depth=2,
            ),
        )
        self.write(
            directory / "tail.md",
            document(
                f"# Tail\n\n## Payload\n\n{marker}_TAIL_MARKER\n",
                group="leaves",
                depth=2,
            ),
        )

    def targets(self) -> dict[str, Path]:
        """The skill's links, read from the entry the agent reads directly."""
        text = self.skill.read_text(encoding="utf-8")
        assert "Read this entry point directly" in text
        assert "not a compiler input" in text
        links = LINK.findall(text)
        assert [label for label, _target in links] == ["Assemble", "Review", "Defaults"]
        return {
            label: (self.skill.parent / target).resolve() for label, target in links
        }

    def entry(
        self, label: str, fragment: str | None = None, cwd: Path | None = None
    ) -> str:
        """One linked target as a path the invocation directory can name."""
        relative = os.path.relpath(self.targets()[label], cwd or self.cwd)
        assert not relative.startswith("/")
        if fragment is None:
            return relative
        return f"{relative}#{fragment}"

    def invoke(
        self,
        *arguments: str,
        cwd: Path | None = None,
        bundle: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """One installed-command run, retained with its inputs and outputs."""
        where = cwd or self.cwd
        self.invocations += 1
        record = self.artifacts / "runs" / f"{self.invocations:02}"
        record.mkdir(parents=True)
        shutil.copytree(self.tree, record / "sources")
        command = [str(self.installation.executable), "-d", "json", *arguments]
        result = self.installation.invoke_raw(command, where)
        (record / "command.json").write_text(
            json.dumps(
                {
                    "argv": command,
                    "cwd": str(where),
                    "cwd_record": where.relative_to(
                        self.installation.artifacts
                    ).as_posix(),
                    "exit_status": result.returncode,
                    "source_commit": self.installation.revision,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (record / "stdout.txt").write_text(result.stdout, encoding="utf-8")
        (record / "stderr.jsonl").write_text(result.stderr, encoding="utf-8")
        produced = record / "bundle.md"
        absent = record / "bundle-absent.txt"
        if result.returncode == 0 and result.stdout:
            produced.write_text(result.stdout, encoding="utf-8")
        elif result.returncode == 0 and bundle is not None:
            shutil.copyfile(bundle, produced)
        elif result.returncode == 0 and "-o" in arguments:
            destination = arguments[arguments.index("-o") + 1]
            if destination != "-":
                shutil.copyfile(destination, produced)
        if produced.exists():
            bundle_name = produced.relative_to(self.installation.artifacts).as_posix()
            bundle_cell = f"[bundle.md]({bundle_name})"
        else:
            absent.write_text("not produced\n", encoding="utf-8")
            bundle_cell = (
                "not produced "
                f"([bundle-absent.txt]({absent.relative_to(self.installation.artifacts).as_posix()}))"
            )
        relative = record.relative_to(self.installation.artifacts).as_posix()
        self.installation.rows.append(
            {
                "run": f"[{relative}]({relative}/)",
                "sources": f"[sources]({relative}/sources/)",
                "command": f"[command.json]({relative}/command.json)",
                "diagnostics": f"[stderr.jsonl]({relative}/stderr.jsonl)",
                "bundle": bundle_cell,
            }
        )
        self.installation.write_inventory()
        self.require_retained(record, result)
        return result

    def require_retained(
        self, record: Path, result: subprocess.CompletedProcess[str]
    ) -> None:
        """The run's sources, command, revision, diagnostics and bundle marker."""
        skill = record / "sources" / "skills" / "pf-bootstrap-specimen" / "SKILL.md"
        assert skill.read_text(encoding="utf-8") == SKILL
        command = json.loads((record / "command.json").read_text(encoding="utf-8"))
        assert command["argv"][0] == str(self.installation.executable)
        assert command["argv"][1:3] == ["-d", "json"]
        assert command["exit_status"] == result.returncode
        assert command["source_commit"] == self.installation.revision
        assert (record / "stderr.jsonl").read_text(encoding="utf-8") == result.stderr
        assert (record / "stdout.txt").read_text(encoding="utf-8") == result.stdout
        if result.returncode == 0 and ((record / "bundle.md").exists()):
            assert (record / "bundle.md").read_text(encoding="utf-8")
            assert not (record / "bundle-absent.txt").exists()
        else:
            assert (record / "bundle-absent.txt").read_text(
                encoding="utf-8"
            ) == "not produced\n"
            assert not (record / "bundle.md").exists()
        identity = json.loads(
            (self.installation.artifacts / "compiler.json").read_text(encoding="utf-8")
        )
        assert identity["source_commit"] == self.installation.revision
        assert identity["installed_outside_repository"] is True
        assert PROFILE in identity["version_stdout"]
        inventory = (self.installation.artifacts / "inventory.md").read_text(
            encoding="utf-8"
        )
        relative = record.relative_to(self.installation.artifacts).as_posix()
        assert f"]({relative}/sources/)" in inventory
        assert f"]({relative}/command.json)" in inventory
        assert f"]({relative}/stderr.jsonl)" in inventory
        assert "compiler.json" in inventory
        assert self.installation.revision in inventory

    def successful(self, result: subprocess.CompletedProcess[str]) -> str:
        """A bundle the command published, carrying no decoy and no frontmatter."""
        assert result.returncode == 0, result.stderr
        assert "WRONG_ROOT_MARKER" not in result.stdout
        assert "Linked Instruction Bootstrap" not in result.stdout
        assert "prosiform:" not in result.stdout
        assert "group-depth:" not in result.stdout
        return result.stdout

    def assert_content(
        self, output: str, markers: list[str], groups: list[str]
    ) -> None:
        """Each named marker and group heading once, with pooled payload sections."""
        for marker in markers:
            assert output.count(marker) == 1, marker
        headings = re.findall(r"^# (.+)$", output, re.M)
        for group in groups:
            assert headings.count(group) == 1, group
        assert len(re.findall(r"^## Payload$", output, re.M)) == 1


@pytest.fixture(scope="session")
def installation(tmp_path_factory: pytest.TempPathFactory) -> Installation:
    """The installed wheel and the artifact directory for this session."""
    workspace = Path(tempfile.mkdtemp(prefix="pf-bootstrap-install-"))
    executable, env, wheel = install_command(workspace)
    chosen = os.environ.get(ARTIFACTS)
    if chosen:
        artifacts = Path(chosen)
        if artifacts.exists():
            pytest.fail(f"artifact directory already exists: {artifacts}")
        artifacts.mkdir(parents=True)
    else:
        artifacts = tmp_path_factory.mktemp("linked-bootstrap-artifacts")
    return Installation(executable, env, wheel, artifacts)


@pytest.fixture
def stack(installation: Installation, request: pytest.FixtureRequest) -> Stack:
    """A fresh skill tree for one test."""
    return Stack(installation, slug(request.node.name))


def test_three_skill_links_are_independent_compilations(stack: Stack) -> None:
    """Three targets linked from the skill, each with its own root and group."""
    assemble = stack.tree / "skills/pf-bootstrap-specimen/modes/assemble.md"
    review = stack.tree / "skills/pf-bootstrap-specimen/modes/review.md"
    defaults = stack.tree / "skills/pf-bootstrap-specimen/modes/defaults.md"
    assert 'root: "../../.."' in assemble.read_text(encoding="utf-8")
    assert 'group: "procedures"' in assemble.read_text(encoding="utf-8")
    assert 'root: "../../../libraries/beta"' in review.read_text(encoding="utf-8")
    assert 'group: "reviews"' in review.read_text(encoding="utf-8")
    assert "root:" not in defaults.read_text(encoding="utf-8")
    cases = {
        "Assemble": (
            [
                "ASSEMBLE_MARKER",
                "ALPHA_RULES_MARKER",
                "CHECKS_MARKER",
                "ALPHA_SHARED_MARKER",
            ],
            ["Procedures", "Rules", "Checks", "Shared", "Leaves"],
            [
                "REVIEW_MARKER",
                "DEFAULTS_MARKER",
                "BETA_RULES_MARKER",
                "ALPHA_UNSELECTED_INTRO",
            ],
        ),
        "Review": (
            ["REVIEW_MARKER", "BETA_RULES_MARKER", "BETA_SHARED_MARKER"],
            ["Reviews", "Rules", "Shared", "Leaves"],
            ["ASSEMBLE_MARKER", "DEFAULTS_MARKER", "ALPHA_RULES_MARKER"],
        ),
        "Defaults": (
            ["DEFAULTS_MARKER"],
            ["Defaults", "Leaves"],
            [
                "ASSEMBLE_MARKER",
                "REVIEW_MARKER",
                "ALPHA_RULES_MARKER",
                "BETA_RULES_MARKER",
            ],
        ),
    }
    assert len(stack.targets()) >= 3
    for label in stack.targets():
        output = stack.successful(stack.invoke("-o", "-", stack.entry(label)))
        markers, groups, absent = cases[label]
        stack.assert_content(
            output, [*markers, "CWD_LEAF_MARKER", "CWD_TAIL_MARKER"], groups
        )
        for marker in absent:
            assert marker not in output
        if label == "Assemble":
            assert re.search(r"(?m)^## Verify$", output)
        if label == "Review":
            assert re.search(r"(?m)^## Inspect$", output)
        assert stack.skill.name not in stack.entry(label)


def test_absent_roots_follow_the_invocation_directory(stack: Stack) -> None:
    """A second caller directory supplies the leaf an absent root resolves."""
    other = stack.tree / "other-run"
    stack.write_tail(other, "OTHER")
    for label in stack.targets():
        first = stack.successful(stack.invoke("-o", "-", stack.entry(label)))
        second = stack.successful(
            stack.invoke("-o", "-", stack.entry(label, cwd=other), cwd=other)
        )
        assert "CWD_LEAF_MARKER" in first
        assert "OTHER_LEAF_MARKER" in second
        assert "OTHER_TAIL_MARKER" in second
        assert "CWD_LEAF_MARKER" not in second


def test_section_selection_keeps_the_entry_settings(stack: Stack) -> None:
    """A fragment keeps the entry file's root and drops the unselected intro."""
    output = stack.successful(stack.invoke("-o", "-", stack.entry("Assemble", "steps")))
    assert "ENTRY_INTRO" not in output
    stack.assert_content(
        output,
        ["ASSEMBLE_MARKER", "CHECKS_MARKER", "CWD_TAIL_MARKER"],
        ["Procedures", "Checks", "Leaves"],
    )


def test_explicit_output_matches_stdout_and_derived_names(stack: Stack) -> None:
    """Stdout, an explicit file and the derived filename carry one bundle."""
    target = stack.entry("Assemble")
    expected = stack.successful(stack.invoke("-o", "-", target))
    destination = stack.cwd / "assembled.md"
    result = stack.invoke("-o", str(destination), target)
    stack.successful(result)
    assert result.stdout == ""
    assert destination.read_text(encoding="utf-8") == expected
    derived = stack.cwd / "skills_pf-bootstrap-specimen_modes_assemble.bundle.md"
    published = stack.invoke(target, bundle=derived)
    assert published.returncode == 0, published.stderr
    assert published.stdout == ""
    assert derived.read_text(encoding="utf-8") == expected
    fragment = (
        stack.cwd / "skills_pf-bootstrap-specimen_modes_assemble__steps.bundle.md"
    )
    selected = stack.invoke(stack.entry("Assemble", "steps"), bundle=fragment)
    assert selected.returncode == 0, selected.stderr
    assert "ENTRY_INTRO" not in fragment.read_text(encoding="utf-8")
    assert "ASSEMBLE_MARKER" in fragment.read_text(encoding="utf-8")


def test_repeated_target_is_included_once(stack: Stack) -> None:
    """Naming one linked target twice publishes its content once."""
    target = stack.entry("Defaults")
    output = stack.successful(stack.invoke("-o", "-", target, target))
    assert output.count("DEFAULTS_MARKER") == 1
    assert output.count("CWD_LEAF_MARKER") == 1
    derived = stack.cwd / ".._skills_pf-bootstrap-specimen_modes_defaults.bundle.md"
    result = stack.invoke(target, target, bundle=derived)
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""
    assert derived.read_text(encoding="utf-8").count("DEFAULTS_MARKER") == 1


def test_shared_source_keeps_the_caller_root(stack: Stack) -> None:
    """Parents with different roots reach one absent-root source and the caller leaf."""
    stack.write(
        "libraries/alpha/via.md",
        document(
            "# Via\n\n## Body\n\nALPHA_VIA_MARKER\n\nRead [Common](common.md).\n",
            root="../../shared",
            group="alpha-via",
            depth=2,
        ),
    )
    stack.write(
        "portal/via.md",
        document(
            "# Via\n\n## Body\n\nPORTAL_VIA_MARKER\n\nRead [Common](common.md).\n",
            root="../shared",
            group="portal-via",
            depth=2,
        ),
    )
    stack.write(
        "shared/common.md",
        document(
            "# Common\n\n## Body\n\nCOMMON_MARKER\n\nRead [Leaf](leaf.md).\n",
            group="notes",
            depth=2,
        ),
    )
    stack.write("shared/leaf.md", "# Decoy\n\nWRONG_ROOT_MARKER\n")
    stack.write(
        "join.md",
        document(
            "# Join\n\n## Body\n\nJOIN_MARKER\n\n"
            "Read [Alpha](libraries/alpha/via.md).\n\n"
            "Read [Portal](portal/via.md).\n",
            root=".",
            group="join",
            depth=2,
        ),
    )
    alpha = (stack.tree / "libraries/alpha/via.md").read_text(encoding="utf-8")
    portal = (stack.tree / "portal/via.md").read_text(encoding="utf-8")
    assert 'root: "../../shared"' in alpha
    assert 'root: "../shared"' in portal
    assert "root:" not in (stack.tree / "shared/common.md").read_text(encoding="utf-8")
    output = stack.successful(stack.invoke("-o", "-", "../join.md"))
    for marker in (
        "JOIN_MARKER",
        "ALPHA_VIA_MARKER",
        "PORTAL_VIA_MARKER",
        "COMMON_MARKER",
        "CWD_LEAF_MARKER",
        "CWD_TAIL_MARKER",
    ):
        assert output.count(marker) == 1, marker
    headings = re.findall(r"^# (.+)$", output, re.M)
    for group in ("Join", "Alpha Via", "Portal Via", "Notes", "Leaves"):
        assert headings.count(group) == 1, group


def test_rewritten_destinations_are_stable(stack: Stack) -> None:
    """A second compilation rewrites the same destinations and the same file."""
    target = stack.entry("Assemble")
    first = stack.successful(stack.invoke("-o", "-", target))
    second = stack.successful(stack.invoke("-o", "-", target))
    assert first == second
    assert "[Rules](#checks-2)" in first
    assert "[Checks](#checks-1)" in first
    assert "[Shared](#shared-1)" in first
    assert "[Leaf](#leaf)" in first
    assert "[Tail](#tail)" in first
    assert "libraries/alpha/rules.md" not in first
    derived = stack.cwd / "skills_pf-bootstrap-specimen_modes_assemble.bundle.md"
    derived.write_text("STALE\n", encoding="utf-8")
    result = stack.invoke(target, bundle=derived)
    assert result.returncode == 0, result.stderr
    assert derived.read_text(encoding="utf-8") == first


def test_depth_conflict_preserves_existing_output(stack: Stack) -> None:
    """Members of one group that declare different depths publish nothing."""
    stack.write(
        "run/tail.md",
        document(
            "# Tail\n\n## Area\n\n### Payload\n\nTAIL_MARKER\n",
            group="leaves",
            depth=3,
        ),
    )
    destination = stack.cwd / "existing.md"
    destination.write_text("PRESERVE_ME\n", encoding="utf-8")
    result = stack.invoke("-o", str(destination), stack.entry("Defaults"))
    assert result.returncode == 1, result.stderr
    assert result.stdout == ""
    assert destination.read_text(encoding="utf-8") == "PRESERVE_ME\n"
    diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
    conflicts = [
        item for item in diagnostics if item["code"] == "E_GROUP_DEPTH_CONFLICT"
    ]
    assert len(conflicts) == 1, diagnostics
    locations = [conflicts[0]["location"], *conflicts[0]["related"]]
    assert {Path(loc["file"]).name for loc in locations} == {"leaf.md", "tail.md"}
    assert all(loc["line"] > 1 for loc in locations)


@pytest.mark.parametrize("depth", ["2", True, 0, 7])
def test_invalid_metadata_publishes_nothing(stack: Stack, depth: Any) -> None:
    """A depth the schema refuses leaves the existing output untouched."""
    stack.write("run/tail.md", document("# Tail\n", group="leaves", depth=depth))
    destination = stack.cwd / "invalid.md"
    destination.write_text("PRESERVE_ME\n", encoding="utf-8")
    result = stack.invoke("-o", str(destination), stack.entry("Defaults"))
    assert result.returncode == 1, result.stderr
    assert result.stdout == ""
    assert destination.read_text(encoding="utf-8") == "PRESERVE_ME\n"
    diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
    assert "E_INVALID_CONVERSION_METADATA" in [item["code"] for item in diagnostics]


def test_inventory_links_each_retained_run(stack: Stack) -> None:
    """The published inventory links the compiler revision and one run's files."""
    result = stack.invoke("-o", "-", stack.entry("Defaults"))
    stack.successful(result)
    inventory = (stack.installation.artifacts / "inventory.md").read_text(
        encoding="utf-8"
    )
    identity = json.loads(
        (stack.installation.artifacts / "compiler.json").read_text(encoding="utf-8")
    )
    assert identity["source_commit"] in inventory
    assert identity["wheel"] in inventory
    record = stack.artifacts / "runs" / "01"
    for name in ("sources", "command.json", "stderr.jsonl", "bundle.md"):
        assert (record / name).exists()
        assert name in inventory or f"{name})" in inventory
    assert (
        record / "sources" / "skills" / "pf-bootstrap-specimen" / "SKILL.md"
    ).is_file()
