#!/usr/bin/env python3
"""Assert the build installs and its entry point resolves without a checkout.

A caller in this workspace is an agent running a shell whose working
directory is wherever its own work sits. It resolves a tool by name
through `PATH`, and it carries no knowledge of where this repository is
checked out. An entry point is therefore a command that is named on an
installed environment's path, that depends on nothing about the directory
it was started in, and that reads nothing out of the repository that built
it.

Every other run of the build in these checks goes through
`uv run --project src`, which names the checkout. That run proves
the behaviour and says nothing about the packaging, so a wheel that
installed no command, or one that shipped without the glossary, would pass
the whole gate. This check is the one that observes the three properties
above, and it observes them the only way they can be observed: by building
the wheel, installing it into a throwaway environment, and invoking the
command by name from somewhere else entirely.

The invoked process inherits nothing. Its `PATH` holds the installed
environment's executable directory and no other, its working directory is
a temporary one, and the source root it bundles from is a tree written
beside that directory. An entry point the packaging never declared fails
at the lookup, because there is no command to find; one that reads the
repository fails at the bundle, because the repository is on neither the
path nor the search.

The steps depend on each other in order, so the run stops at the first one
that fails and names it. The environment is created on the Python version
`src/.python-version` names, so the version an installation is
proved against is the version the build declares rather than a second
declaration here.

The three properties are named here, under the names the repository's
installation section gives them, and the run's closing summary states them.
A report listing what no run observes reads this declaration, so the
properties an installation is held to and the properties one is said to
lack are the same words in both places.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "src"
PYTHON_VERSION = PROJECT / ".python-version"

COMMAND = "pf"
PROFILE = "skill-markdown-v3"

OBSERVED = (
    "named on the path",
    "independent of the working directory",
    "independent of this repository",
)

GLOSSARY = "prosiform/docs/glossary.md"
SITE_PACKAGES = "lib/python*/site-packages"
BIN = "bin"

ENTRY = "guide.md"
SOURCE = (
    '---\nprosiform: {root: "."}\n---\n'
    + "# Guide\n\nThe installed command bundles this document.\n"
)
BUNDLE = "# Guide\n\nThe installed command bundles this document.\n"


class Failed(Exception):
    """One step of the smoke run that did not do what installation requires."""


def uv(*arguments: str) -> subprocess.CompletedProcess[str]:
    """One `uv` invocation, its failure reported as the step that failed."""
    try:
        result = subprocess.run(
            ["uv", *arguments], capture_output=True, text=True, check=False
        )
    except FileNotFoundError as missing:
        raise Failed(
            "uv is not on the path, and the smoke run builds and installs the "
            "wheel through it"
        ) from missing
    if result.returncode != 0:
        raise Failed(
            f"uv {' '.join(arguments)} exited {result.returncode}\n"
            f"{result.stderr.strip()}"
        )
    return result


def build(workspace: Path) -> Path:
    """The wheel the project builds, written outside the repository."""
    into = workspace / "dist"
    uv("build", "--wheel", "--project", str(PROJECT), "--out-dir", str(into))
    built = sorted(into.glob("*.whl"))
    if len(built) != 1:
        raise Failed(
            f"the build wrote {len(built)} wheel(s) to {into}, and the "
            f"installation takes exactly one"
        )
    return built[0]


def install(workspace: Path, wheel: Path) -> Path:
    """An environment on the declared Python version, carrying the built wheel."""
    environment = workspace / "environment"
    uv("venv", "--python", PYTHON_VERSION.read_text().strip(), str(environment))
    uv("pip", "install", "--python", str(environment / BIN / "python"), str(wheel))
    return environment


def resolve(environment: Path) -> Path:
    """The command's path, looked up in the installed environment and nowhere else."""
    found = shutil.which(COMMAND, path=str(environment / BIN))
    if found is None:
        raise Failed(
            f"the installed environment names no {COMMAND} command, so a caller "
            f"has nothing to resolve by name"
        )
    if shutil.which("prosiform", path=str(environment / BIN)) is not None:
        raise Failed("the installed environment exposes the retired prosiform command")
    where = Path(found).resolve()
    if where.is_relative_to(ROOT):
        raise Failed(
            f"the command resolved to {where}, which is inside the repository, so "
            f"the run observes a checkout rather than an installation"
        )
    return where


def invoke(
    environment: Path, cwd: Path, *arguments: str
) -> subprocess.CompletedProcess[str]:
    """The command, by name, from a directory and an environment of its own.

    The child inherits no variable of this process: its path holds the
    installed environment's executable directory alone, so the name
    resolves there or not at all.
    """
    return subprocess.run(
        [COMMAND, *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": str(environment / BIN), "HOME": str(cwd)},
    )


def succeeded(run: subprocess.CompletedProcess[str], what: str) -> None:
    """The run's success, or the status and the reason it returned instead."""
    if run.returncode != 0:
        raise Failed(f"{what} exited {run.returncode}\n{run.stderr.strip()}")


def reported(run: subprocess.CompletedProcess[str], what: str) -> str:
    """One run's standard output, the diagnostic stream carrying nothing."""
    succeeded(run, what)
    if run.stderr:
        raise Failed(f"{what} wrote to standard error\n{run.stderr.strip()}")
    return run.stdout


def version(environment: Path, elsewhere: Path) -> str:
    """The version response, read from a directory unrelated to the repository."""
    response = reported(invoke(environment, elsewhere, "-v"), f"{COMMAND} -v")
    if PROFILE not in response:
        raise Failed(
            f"the version response {response.strip()!r} names no {PROFILE} profile"
        )
    return response.strip()


def derived(entry: str) -> str:
    """The name a run gives one entry's bundle, from its working-directory path.

    The entry's separators are written as underscores, so an entry above
    the working directory keeps its parent segments as filename text.
    """
    return str(Path(entry).with_suffix("")).replace(os.sep, "_")


def bundles(environment: Path, elsewhere: Path, sources: Path) -> None:
    """A reference bundled from a source root the repository does not hold.

    The folder `-o` names holds the bundle under its derived name and
    nothing else, and both streams carry nothing, so the installed
    command's output split is the one the contract names.
    """
    entry = os.path.relpath(sources / ENTRY, elsewhere)
    folder = elsewhere.parent / "bundles"
    folder.mkdir(exist_ok=True)
    run = invoke(environment, elsewhere, "-o", str(folder), entry)
    if reported(run, f"{COMMAND} -o {folder} {entry}"):
        raise Failed("standard output carries text, and a run writes its bundle")
    name = f"{derived(entry)}.bundle.md"
    written = sorted(path.name for path in folder.iterdir())
    if written != [name]:
        raise Failed(f"the output folder holds {written}, where the run writes {name}")
    produced = (folder / name).read_text()
    (folder / name).unlink()
    if produced != BUNDLE:
        raise Failed(
            f"the bundle differs from the one the source names\n"
            f"expected {BUNDLE!r}\nproduced {produced!r}"
        )


def publishes(environment: Path, elsewhere: Path, sources: Path) -> None:
    """Derived names, joined selections, folders and validation through the CLI.

    A run naming no folder writes into its working directory, a folder
    `-o` names holds the bundle, and a folder that does not exist refuses
    the write and keeps no temporary file.
    """
    entry = os.path.relpath(sources / ENTRY, elsewhere)
    name = derived(entry)
    for reference, published, expected in (
        (entry, f"{name}.bundle.md", BUNDLE),
        (entry + "#guide", f"{name}__guide.bundle.md", BUNDLE),
    ):
        run = invoke(environment, elsewhere, reference)
        succeeded(run, reference)
        destination = elsewhere / published
        if run.stdout or destination.read_text() != expected:
            raise Failed("derived output differs from the installed bundle")
        destination.unlink()
    run = invoke(environment, elsewhere, "-c", entry)
    succeeded(run, "check mode")
    if list(elsewhere.iterdir()) or run.stdout:
        raise Failed("check mode published a bundle")
    run = invoke(environment, elsewhere, entry, entry + "#guide")
    succeeded(run, "joined selections")
    joined = elsewhere / f"{name}+{name}__guide.bundle.md"
    if run.stdout or not joined.is_file():
        raise Failed("joined selections publish no bundle under the joined name")
    joined.unlink()
    run = invoke(environment, elsewhere, "-o", "-", entry)
    if run.returncode != 2 or run.stdout or list(elsewhere.iterdir()):
        raise Failed("standard output named as the output folder is not refused")
    folder = elsewhere / "out"
    folder.mkdir()
    run = invoke(environment, elsewhere, "-o", "out", entry)
    succeeded(run, "-o out")
    if run.stdout or [path.name for path in folder.iterdir()] != [f"{name}.bundle.md"]:
        raise Failed("the folder -o names does not hold the bundle")
    shutil.rmtree(folder)
    run = invoke(environment, elsewhere, "-o", "missing", entry)
    if run.returncode != 3 or run.stdout or list(elsewhere.iterdir()):
        raise Failed("a folder that does not exist leaves output behind")


def ships_glossary(environment: Path) -> Path:
    """The glossary the installed build carries, which travels with no checkout."""
    carried = sorted(environment.glob(f"{SITE_PACKAGES}/{GLOSSARY}"))
    if not carried:
        raise Failed(
            f"the installed environment carries no {GLOSSARY}, so the vocabulary "
            f"the diagnostics use reaches only a source tree"
        )
    return carried[0]


def smoke(workspace: Path) -> None:
    """The installation, the entry point and the run one caller makes of it."""
    if workspace.is_relative_to(ROOT):
        raise Failed(
            f"the smoke run's workspace {workspace} is inside the repository, so "
            f"the run cannot establish anything about a caller outside it"
        )

    wheel = build(workspace)
    print(f"ok   wheel        {wheel.name}")

    environment = install(workspace, wheel)
    print(f"ok   installed    {environment}")

    where = resolve(environment)
    print(f"ok   resolved     {COMMAND} — {where}, outside the repository")

    elsewhere = workspace / "elsewhere"
    elsewhere.mkdir()
    sources = workspace / "sources"
    sources.mkdir()
    (sources / ENTRY).write_text(SOURCE)

    print(f"ok   version      {version(environment, elsewhere)}")

    bundles(environment, elsewhere, sources)
    publishes(environment, elsewhere, sources)
    print(f"ok   bundled      {ENTRY} from {sources}, run from {elsewhere}")
    refused = invoke(environment, elsewhere, "-r", str(sources), ENTRY)
    if refused.returncode != 2:
        raise Failed("the installed command accepts the retired root option")
    print("ok   root option  invalid CLI usage")

    print(f"ok   glossary     {ships_glossary(environment).name}, shipped")


def main() -> int:
    workspace = Path(tempfile.mkdtemp(prefix=f"{COMMAND}-smoke-")).resolve()
    try:
        smoke(workspace)
    except Failed as failure:
        print(f"FAIL {failure}", file=sys.stderr)
        print("\nsmoke check: the installation does not stand", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    print(f"\nsmoke check: the installed command is {', '.join(OBSERVED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
