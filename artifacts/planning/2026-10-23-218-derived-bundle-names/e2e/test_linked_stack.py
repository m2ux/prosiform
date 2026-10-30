"""Black-box acceptance tests for independently bundled skill links.

Run with Python and --pf /absolute/path/to/the/installed/pf.
Each test creates real Markdown files and invokes a real executable.
"""

import argparse
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

PF = "pf"
ARTIFACTS = None
SPECIMEN = Path(__file__).parent / "bootstrap-skill" / "SKILL.md"


def document(body, *, root=None, group=None, depth=None):
    """A document with the declared top-level settings and original body."""
    fields = []
    if root is not None:
        fields.append("  root: " + json.dumps(root))
    if group is not None:
        fields.append("  group: " + json.dumps(group))
        fields.append("  group-depth: " + json.dumps(depth))
    prefix = "---\nprosiform:\n" + "\n".join(fields) + "\n---\n"
    return prefix + body if fields else body


class LinkedStackTests(unittest.TestCase):
    def setUp(self):
        self.artifacts = ARTIFACTS / self._testMethodName
        self.tree = self.artifacts / "workspace"
        self.tree.mkdir(parents=True)
        self.invocations = 0
        self.cwd = self.tree / "run"
        self.cwd.mkdir()
        self.skill = self.tree / "skills" / "pf-bootstrap-specimen" / "SKILL.md"
        self.write(self.skill, SPECIMEN.read_text(encoding="utf-8"))
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

    def write(self, path, text):
        path = self.tree / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_tail(self, directory, marker):
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

    def targets(self):
        links = re.findall(r"^- \[([^]]+)\]\(([^)]+)\)$", self.skill.read_text(), re.M)
        self.assertEqual(
            [label for label, _ in links], ["Assemble", "Review", "Defaults"]
        )
        return {label: str(self.skill.parent / target) for label, target in links}

    def invoke(self, target, *options, cwd=None):
        self.assertNotEqual(Path(target.split("#", 1)[0]), self.skill)
        self.invocations += 1
        record = self.artifacts / "runs" / f"{self.invocations:02}"
        record.mkdir(parents=True)
        shutil.copytree(self.tree, record / "sources")
        command = [PF, "-d", "json", *options, target]
        result = subprocess.run(
            command,
            cwd=cwd or self.cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        (record / "command.json").write_text(
            json.dumps(
                {
                    "argv": command,
                    "cwd": str(cwd or self.cwd),
                    "exit_status": result.returncode,
                },
                indent=2,
            )
            + "\n"
        )
        (record / "stdout.txt").write_text(result.stdout, encoding="utf-8")
        (record / "stderr.jsonl").write_text(result.stderr, encoding="utf-8")
        if result.returncode == 0 and result.stdout:
            (record / "bundle.md").write_text(result.stdout, encoding="utf-8")
        elif result.returncode == 0 and "-o" in options:
            destination = options[options.index("-o") + 1]
            if destination != "-":
                shutil.copyfile(destination, record / "bundle.md")
        return result

    def successful(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("WRONG_ROOT_MARKER", result.stdout)
        self.assertNotIn("Linked Instruction Bootstrap", result.stdout)
        self.assertNotIn("prosiform:", result.stdout)
        self.assertNotIn("group-depth:", result.stdout)
        return result.stdout

    def assert_content(self, output, markers, groups):
        for marker in markers:
            self.assertEqual(output.count(marker), 1, (marker, output))
        headings = re.findall(r"^# (.+)$", output, re.M)
        for group in groups:
            self.assertEqual(headings.count(group), 1, (group, output))
        # Two contributing files declare depth two and share this section.
        self.assertEqual(len(re.findall(r"^## Payload$", output, re.M)), 1, output)

    def test_three_skill_links_are_independent_real_compilations(self):
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
        for label, target in self.targets().items():
            with self.subTest(link=label):
                output = self.successful(self.invoke(target, "-o", "-"))
                markers, groups, absent = cases[label]
                self.assert_content(
                    output, [*markers, "CWD_LEAF_MARKER", "CWD_TAIL_MARKER"], groups
                )
                for marker in absent:
                    self.assertNotIn(marker, output)
                if label == "Assemble":
                    self.assertRegex(output, r"(?m)^## Verify$")
                if label == "Review":
                    self.assertRegex(output, r"(?m)^## Inspect$")

    def test_absent_roots_follow_the_invocation_directory_on_every_run(self):
        other = self.tree / "other-run"
        self.write_tail(other, "OTHER")
        for label, target in self.targets().items():
            with self.subTest(link=label):
                first = self.successful(self.invoke(target, "-o", "-"))
                second = self.successful(self.invoke(target, "-o", "-", cwd=other))
                self.assertIn("CWD_LEAF_MARKER", first)
                self.assertIn("OTHER_LEAF_MARKER", second)
                self.assertIn("OTHER_TAIL_MARKER", second)
                self.assertNotIn("CWD_LEAF_MARKER", second)

    def test_section_entry_keeps_its_own_root_and_dependency_settings(self):
        target = self.targets()["Assemble"] + "#steps"
        output = self.successful(self.invoke(target, "-o", "-"))
        self.assertNotIn("ENTRY_INTRO", output)
        self.assert_content(
            output,
            ["ASSEMBLE_MARKER", "CHECKS_MARKER", "CWD_TAIL_MARKER"],
            ["Procedures", "Checks", "Leaves"],
        )

    def test_explicit_file_output_matches_the_individual_stdout_bundle(self):
        target = self.targets()["Assemble"]
        expected = self.successful(self.invoke(target, "-o", "-"))
        destination = self.cwd / "assembled.md"
        result = self.invoke(target, "-o", str(destination))
        self.successful(result)
        self.assertEqual(result.stdout, "")
        self.assertEqual(destination.read_text(encoding="utf-8"), expected)

    def test_shared_group_depth_conflict_preserves_existing_output(self):
        self.write(
            "run/tail.md",
            document(
                "# Tail\n\n## Area\n\n### Payload\n\nTAIL_MARKER\n",
                group="leaves",
                depth=3,
            ),
        )
        destination = self.cwd / "existing.md"
        destination.write_text("PRESERVE_ME\n")
        result = self.invoke(self.targets()["Defaults"], "-o", str(destination))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(destination.read_text(), "PRESERVE_ME\n")
        diagnostics = [json.loads(line) for line in result.stderr.splitlines() if line]
        conflicts = [d for d in diagnostics if d["code"] == "E_GROUP_DEPTH_CONFLICT"]
        self.assertEqual(len(conflicts), 1, diagnostics)
        locations = [conflicts[0]["location"], *conflicts[0]["related"]]
        self.assertEqual(
            {Path(loc["file"]).name for loc in locations}, {"leaf.md", "tail.md"}
        )
        self.assertTrue(all(loc["line"] > 1 for loc in locations), locations)

    def test_invalid_nested_settings_fail_before_publication(self):
        for depth in ("2", True, 0, 7):
            with self.subTest(depth=depth):
                self.write(
                    "run/tail.md", document("# Tail\n", group="leaves", depth=depth)
                )
                destination = self.cwd / "invalid.md"
                destination.write_text("PRESERVE_ME\n")
                result = self.invoke(self.targets()["Defaults"], "-o", str(destination))
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(destination.read_text(), "PRESERVE_ME\n")
                diagnostics = [
                    json.loads(line) for line in result.stderr.splitlines() if line
                ]
                self.assertIn(
                    "E_INVALID_CONVERSION_METADATA", [d["code"] for d in diagnostics]
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pf", required=True, help="Installed pf executable to test")
    parser.add_argument(
        "--artifacts",
        required=True,
        type=Path,
        help="New directory retaining inputs, commands, diagnostics and bundles",
    )
    args, remaining = parser.parse_known_args()
    executable = shutil.which(args.pf)
    if executable is None:
        parser.error("pf executable is unavailable: " + args.pf)
    PF = str(Path(executable).resolve())
    ARTIFACTS = args.artifacts.resolve()
    if ARTIFACTS.exists():
        parser.error("Artifact directory already exists; select a new run directory")
    ARTIFACTS.mkdir(parents=True)
    version = subprocess.run([PF, "-v"], capture_output=True, text=True, timeout=30)
    (ARTIFACTS / "compiler.json").write_text(
        json.dumps(
            {
                "executable": PF,
                "version_stdout": version.stdout,
                "version_stderr": version.stderr,
                "version_exit_status": version.returncode,
            },
            indent=2,
        )
        + "\n"
    )
    unittest.main(argv=[__file__, *remaining])
