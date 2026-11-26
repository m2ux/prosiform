#!/usr/bin/env python3
"""Assert every function and method the package defines is reached.

A definition is reached when the package itself names it, or when a stated
reason says what reaches it from outside the package. The suite is no such
reason: a function only a test names is one the product never runs.

The package names a definition by referring to it, as `references` reads a
reference. Names are compared rather than calls resolved, so a definition is
reached by any reference carrying its name, and a name the package builds
at runtime reaches nothing. The package builds no such name.
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
    "prosiform.cli.Parser.error": (
        "argparse's ArgumentParser calls it on an argument it cannot parse"
    ),
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
    refers to it by, and `own` the names its own body refers to, which reach
    nothing but itself.
    """

    qualified: str
    name: str
    own: Counter[str]


FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
SCOPES = (*FUNCTIONS, *COMPREHENSIONS, ast.ClassDef)

type Visible = tuple[tuple[frozenset[str], bool], ...]
"""The scopes a name is resolved in, innermost last: each scope's variables,
and whether the scope is a class body."""


def bindings(scope: ast.AST) -> frozenset[str]:
    """The names `scope` binds as variables in its own namespace.

    A parameter, a name stored or deleted, an exception name and a `match`
    capture are variables; a name `scope` declares `global` belongs to the
    module. A comprehension binds its loop targets, and an assignment
    expression inside one binds in the scope holding the comprehension. A
    `def`, a `class` and an import bind a name to what they define or
    import, so none of them is a variable.
    """
    bound: set[str] = set()
    declared: set[str] = set()
    if isinstance(scope, FUNCTIONS):
        arguments = scope.args
        parameters = [
            *arguments.posonlyargs,
            *arguments.args,
            *arguments.kwonlyargs,
            arguments.vararg,
            arguments.kwarg,
        ]
        bound.update(parameter.arg for parameter in parameters if parameter)
    if isinstance(scope, COMPREHENSIONS):
        pending: list[ast.AST] = [generator.target for generator in scope.generators]
    elif isinstance(scope, ast.Lambda):
        pending = [scope.body]
    else:
        pending = list(getattr(scope, "body", []))
    while pending:
        node = pending.pop()
        if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
            bound.add(node.id)
        elif isinstance(node, ast.ExceptHandler | ast.MatchAs | ast.MatchStar):
            if node.name:
                bound.add(node.name)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            bound.add(node.rest)
        elif isinstance(node, ast.Global):
            declared.update(node.names)
        if isinstance(node, COMPREHENSIONS):
            pending.extend(
                inner.target
                for inner in ast.walk(node)
                if isinstance(inner, ast.NamedExpr)
            )
        elif not isinstance(node, SCOPES):
            pending.extend(ast.iter_child_nodes(node))
    return frozenset(bound - declared)


def enter(visible: Visible, scope: ast.AST) -> Visible:
    """The scopes a name inside `scope`'s own namespace is resolved in.

    A class body's names are invisible to the functions and comprehensions
    it holds, as Python resolves them.
    """
    if not isinstance(scope, ast.ClassDef):
        visible = tuple(entry for entry in visible if not entry[1])
    return (*visible, (bindings(scope), isinstance(scope, ast.ClassDef)))


def parts(scope: ast.AST) -> list[tuple[ast.AST, bool]]:
    """Each child of `scope`, with whether the scope holding it evaluates it.

    A decorator, a default, an annotation and a base class are evaluated
    where the definition stands, and so is a comprehension's first iterable;
    the rest belongs to the scope itself.
    """
    if isinstance(scope, COMPREHENSIONS):
        first = scope.generators[0]
        found: list[tuple[ast.AST, bool]] = [(first.iter, True)]
        for child in ast.iter_child_nodes(scope):
            if child is first:
                found.extend(
                    (part, False)
                    for part in ast.iter_child_nodes(first)
                    if part is not first.iter
                )
            else:
                found.append((child, False))
        return found
    own: set[int] = set()
    if isinstance(scope, ast.Lambda):
        own = {id(scope.body)}
    elif isinstance(scope, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        own = {id(statement) for statement in scope.body}
    return [(child, id(child) not in own) for child in ast.iter_child_nodes(scope)]


def references(node: ast.AST, visible: Visible) -> Counter[str]:
    """Count each name `node` refers to, resolved from the scopes `visible`.

    A loaded `Name` refers to its name unless the innermost scope it
    resolves in binds that name as a variable, so a local variable, a
    parameter or an exception name sharing a definition's name refers to
    nothing; a stored or deleted `Name`, a parameter, an exception name and
    a keyword argument's name bind or label and refer to nothing either. An
    `Attribute` refers to its attribute name, a decorator to the name it
    loads, and an import alias to every dotted part of the imported name and
    the name it binds, so `import a.b as c` refers to `a`, `b` and `c`.
    """
    names: Counter[str] = Counter()
    pending: list[tuple[ast.AST, Visible]] = [(node, visible)]
    while pending:
        current, scopes = pending.pop()
        if isinstance(current, ast.Name):
            if isinstance(current.ctx, ast.Load) and not any(
                current.id in variables for variables, _ in scopes
            ):
                names[current.id] += 1
        elif isinstance(current, ast.Attribute):
            names[current.attr] += 1
        elif isinstance(current, ast.alias):
            names.update(current.name.split("."))
            if current.asname:
                names[current.asname] += 1
        if isinstance(current, SCOPES):
            inner = enter(scopes, current)
            pending.extend(
                (child, scopes if outside else inner)
                for child, outside in parts(current)
            )
        else:
            pending.extend((child, scopes) for child in ast.iter_child_nodes(current))
    return names


def definitions(body: list[ast.stmt], scope: str, visible: Visible) -> list[Definition]:
    """Collect the functions `body` defines and the methods of its classes.

    `visible` holds the scopes `body` is resolved in. A class nested in a
    class contributes its methods too; a function nested in a function is
    part of the function that holds it.
    """
    found = []
    for node in body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            found.append(
                Definition(f"{scope}.{node.name}", node.name, references(node, visible))
            )
        elif isinstance(node, ast.ClassDef):
            found.extend(
                definitions(node.body, f"{scope}.{node.name}", enter(visible, node))
            )
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

    A definition is reached when the package refers to its name outside its
    own body, when the language calls it by its name, or when `declared` or
    `listed` states a reason. A `listed` entry naming no definition, or one
    the package already reaches, is a failure: the list states only what no
    reading of the package can.
    """
    sources = sorted(package.rglob("*.py"))
    trees = {path: ast.parse(path.read_text(), str(path)) for path in sources}
    names: Counter[str] = Counter()
    found: list[Definition] = []
    for path, tree in trees.items():
        module: Visible = ((bindings(tree), False),)
        names.update(references(tree, module))
        found.extend(definitions(tree.body, module_name(path, package), module))

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
