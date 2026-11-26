"""Assert `make check-all` reports every failing check and `make check` the first.

Each case runs make over a makefile of its own that includes the
repository's `Makefile` and declares stand-in checks, then names those
stand-ins as `CHECKS` on the command line. The recipes under test are the
repository's own; only the checks they run are stand-ins, each recording
that it ran, so a case observes which checks ran and what each target
reported without running the repository's real checks.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

MAKEFILE = Path(__file__).resolve().parent.parent.parent / "Makefile"

pytestmark = pytest.mark.skipif(shutil.which("make") is None, reason="make absent")


def tree(directory: Path, *, failing: tuple[str, ...]) -> Path:
    """A makefile including the repository's, with three stand-in checks.

    Each stand-in writes a file named for itself, and those named in
    `failing` then exit nonzero.
    """
    lines = [f"include {MAKEFILE}", ""]
    for name in ("alpha", "beta", "gamma"):
        status = "false" if name in failing else "true"
        lines.extend([f"{name}:", f"\t@touch ran-{name}; {status}", ""])
    (directory / "Makefile").write_text("\n".join(lines), encoding="utf-8")
    return directory


def make(directory: Path, goal: str) -> subprocess.CompletedProcess[str]:
    """One make run over the stand-in checks, its output captured."""
    return subprocess.run(
        ["make", "--no-print-directory", goal, "CHECKS=alpha beta gamma"],
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
    )


def ran(directory: Path) -> list[str]:
    """The stand-in checks that ran, in name order."""
    return sorted(path.name.removeprefix("ran-") for path in directory.glob("ran-*"))


def test_check_all_names_every_failing_check(tmp_path: Path) -> None:
    """Two failing checks are both run and both named, and the run fails."""
    directory = tree(tmp_path, failing=("alpha", "gamma"))
    completed = make(directory, "check-all")
    assert completed.returncode != 0
    assert ran(directory) == ["alpha", "beta", "gamma"]
    assert "check-all: failed: alpha gamma" in completed.stdout


def test_check_all_passes_a_tree_where_every_check_passes(tmp_path: Path) -> None:
    directory = tree(tmp_path, failing=())
    completed = make(directory, "check-all")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert ran(directory) == ["alpha", "beta", "gamma"]
    assert "check-all: every check passed" in completed.stdout


def test_check_stops_at_the_first_failing_check(tmp_path: Path) -> None:
    directory = tree(tmp_path, failing=("alpha", "gamma"))
    completed = make(directory, "check")
    assert completed.returncode != 0
    assert ran(directory) == ["alpha"]
