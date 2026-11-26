#!/usr/bin/env python3
"""Assert every function and method the package defines is reached.

A definition is reached when the package itself names it, or when a stated
reason says what reaches it from outside the package. The suite is no such
reason: a function only a test names is one the product never runs.

The package names a definition by writing its name as a `Name`, an
`Attribute` or an import alias. Names are compared rather than calls
resolved, so a definition is reached by any use of its name, and a name the
package builds at runtime reaches nothing. The package builds no such name.
"""

import ast
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "prosiform"
PROJECT = ROOT / "src" / "pyproject.toml"

EXTERNAL_CALLERS = {
    "prosiform.metadata._MarkedScanner.scan_flow_scalar_non_spaces": (
        "ruamel.yaml's Scanner calls it while scanning a quoted scalar"
    ),
    "prosiform.profile.Watched.skipToken": (
        "markdown-it's inline parser calls it while skipping a token"
    ),
}
"""Each definition a caller outside the package reaches that no declaration
states, keyed by its qualified name, with what reaches it."""


@dataclass(frozen=True)
class Definition:
    """A module-level function or a method.

    `qualified` is its dotted path from the package, `name` the name a caller
    writes, and `own` the names its own body writes, which reach nothing but
    itself.
    """

    qualified: str
    name: str
    own: Counter[str]


def written(node: ast.AST) -> Counter[str]:
    """Count each name `node` writes as a `Name`, an `Attribute` or an alias.

    An import alias counts every dotted part of the imported name and the
    name it binds, so `import a.b as c` writes `a`, `b` and `c`.
    """
    names: Counter[str] = Counter()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names[child.id] += 1
        elif isinstance(child, ast.Attribute):
            names[child.attr] += 1
        elif isinstance(child, ast.alias):
            names.update(child.name.split("."))
            if child.asname:
                names[child.asname] += 1
    return names


def definitions(body: list[ast.stmt], scope: str) -> list[Definition]:
    """Collect the functions `body` defines and the methods of its classes.

    A class nested in a class contributes its methods too; a function nested
    in a function is part of the function that holds it.
    """
    found = []
    for node in body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            found.append(Definition(f"{scope}.{node.name}", node.name, written(node)))
        elif isinstance(node, ast.ClassDef):
            found.extend(definitions(node.body, f"{scope}.{node.name}"))
    return found


def module_name(path: Path, package: Path) -> str:
    """The dotted module name of a file under `package`."""
    parts = path.relative_to(package.parent).with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def entry_points(project: Path) -> dict[str, str]:
    """Each console script `[project.scripts]` declares, by qualified name."""
    scripts = tomllib.loads(project.read_text())["project"].get("scripts", {})
    return {
        target.replace(":", "."): f"the console script {script} declared in "
        f"{project.name}"
        for script, target in scripts.items()
    }


def is_dunder(name: str) -> bool:
    """Whether `name` is one Python and its standard library call by name."""
    return len(name) > 4 and name.startswith("__") and name.endswith("__")


@dataclass(frozen=True)
class Audit:
    """What one reading of the package found.

    `read` counts the definitions read, `reported` names each the package
    does not name with the reason that reaches it, and `failures` names each
    definition no reason reaches and each listed reason that is not needed.
    """

    read: int
    reported: list[str]
    failures: list[str]


def audit(package: Path, declared: dict[str, str], listed: dict[str, str]) -> Audit:
    """Read every module under `package` and judge each definition it holds.

    A definition is reached when the package writes its name outside its own
    body, when the language calls it by its name, or when `declared` or
    `listed` states a reason. A `listed` entry naming no definition, or one
    the package already reaches, is a failure: the list states only what no
    reading of the package can.
    """
    sources = sorted(package.rglob("*.py"))
    trees = {path: ast.parse(path.read_text(), str(path)) for path in sources}
    names: Counter[str] = Counter()
    found: list[Definition] = []
    for path, tree in trees.items():
        names.update(written(tree))
        found.extend(definitions(tree.body, module_name(path, package)))

    reported: list[str] = []
    failures: list[str] = []
    defined = {definition.qualified for definition in found}
    for definition in found:
        named = names[definition.name] > definition.own[definition.name]
        if definition.qualified in listed and named:
            failures.append(
                f"{definition.qualified} is listed as reached from outside the "
                "package, and the package names it"
            )
        elif named:
            continue
        elif is_dunder(definition.name):
            reported.append(
                f"{definition.qualified}: Python calls a method by that name"
            )
        elif definition.qualified in declared:
            reported.append(f"{definition.qualified}: {declared[definition.qualified]}")
        elif definition.qualified in listed:
            reported.append(f"{definition.qualified}: {listed[definition.qualified]}")
        else:
            failures.append(
                f"{definition.qualified} is named nowhere in the package and no "
                "reason states what reaches it"
            )
    for qualified in sorted(set(listed) - defined):
        failures.append(f"{qualified} is listed and the package defines no such name")
    return Audit(len(found), reported, failures)


def main() -> int:
    result = audit(PACKAGE, entry_points(PROJECT), EXTERNAL_CALLERS)
    for line in result.reported:
        print(f"ok   {line}")
    for failure in result.failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if result.failures:
        print(
            f"\nreachability check: {len(result.failures)} failure(s)",
            file=sys.stderr,
        )
        return 1
    print(f"\nreachability check: {result.read} definition(s), each reached")
    return 0


if __name__ == "__main__":
    sys.exit(main())
