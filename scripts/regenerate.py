"""Rewrite a fixture's expectations from the run the configured build produces.

Each named fixture is run exactly as the corpus runner runs it. Its
`expected/stdout.md` is replaced with the bytes the run produced, and the
`[expected]` block of `manifest.toml` is replaced with the exit status and
diagnostics the run returned. Everything outside that block is left as the
fixture wrote it, so the description, clauses and invocation of a fixture
are never rewritten by a run.
"""

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "fixtures"
BUILD = os.environ["PROSIFORM_BUILD"]
MANIFEST = "manifest.toml"
DECLARED = ("reference", "resolved", "source", "chain")


def quote(value: str) -> str:
    """One TOML basic string, keeping the characters the manifest wrote.

    A control character has no place in a basic string, so it is written as
    the escape the TOML grammar names it by. A newline in a heading's text
    is one the candidate reads across two lines, and the manifest still
    states the exact text that heading carries.
    """
    escaped = []
    for character in value:
        if character == "\\":
            escaped.append("\\\\")
        elif character == '"':
            escaped.append('\\"')
        elif character == "\n":
            escaped.append("\\n")
        elif character == "\r":
            escaped.append("\\r")
        elif character == "\t":
            escaped.append("\\t")
        elif ord(character) < 0x20 or ord(character) == 0x7F:
            escaped.append(f"\\u{ord(character):04X}")
        else:
            escaped.append(character)
    return '"' + "".join(escaped) + '"'


def render(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(render(one) for one in value) + "]"
    return quote(value)


def run(fixture: Path, manifest: dict) -> tuple[int, bytes, bytes]:
    invocation = manifest["invocation"]
    declared = manifest.get("fault")
    requested = ["-x", declared] if declared is not None else []
    cwd = fixture / invocation.get("cwd", ".")
    argv = [
        *shlex.split(BUILD),
        "-o",
        "-",
        "-d",
        "json",
        *requested,
        *invocation["arguments"],
    ]
    completed = subprocess.run(
        argv, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, check=False
    )
    return completed.returncode, completed.stdout, completed.stderr


def diagnostics(stderr: bytes) -> list[dict]:
    found = []
    for line in stderr.decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        one = json.loads(line)
        kept = {key: one[key] for key in DECLARED if key in one}
        found.append({"severity": one["severity"], "code": one["code"], **kept})
    return found


def block(manifest: dict, status: int, found: list[dict]) -> str:
    """The `[expected]` block, as the manifest spells one."""
    expected = manifest["expected"]
    lines = ["[expected]", f"exit_status = {status}"]
    for key in ("stdout", "stdout_contains"):
        if key in expected:
            lines.append(f"{key} = {render(expected[key])}")
    if expected.get("absent"):
        lines.append(f"absent = {render(expected['absent'])}")
    for one in found:
        lines.append("")
        lines.append("[[expected.diagnostics]]")
        for key in ("severity", "code", *DECLARED):
            if key in one:
                lines.append(f"{key} = {render(one[key])}")
    return "\n".join(lines) + "\n"


def rewrite(text: str, manifest: dict, status: int, found: list[dict]) -> str:
    """The manifest with its `[expected]` block replaced and nothing else."""
    at = text.index("[expected]")
    return text[:at] + block(manifest, status, found)


for name in sys.argv[1:]:
    fixture = CORPUS / name
    text = (fixture / MANIFEST).read_text()
    manifest = tomllib.loads(text)
    status, stdout, stderr = run(fixture, manifest)
    if "E_UNEXPECTED_INTERNAL_ERROR" in stderr.decode("utf-8", "replace"):
        print(f"internal error, left alone: {name}")
        continue
    if "stdout" in manifest["expected"]:
        (fixture / manifest["expected"]["stdout"]).write_bytes(stdout)
    found = diagnostics(stderr)
    (fixture / MANIFEST).write_text(rewrite(text, manifest, status, found))
    print(f"rewrote {name}: exit {status}, {len(found)} diagnostic(s)")
