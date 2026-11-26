"""Assert the reachability check reads a package the way a caller names it.

Each case writes a small package the check would misread if it compared the
wrong names: a function only its own body names, a method named only as an
attribute, a function reached through an import alias, a nested function, a
method a framework calls, a reason listed for a definition that needs none
or does not exist, and a variable, parameter, exception name or keyword
argument sharing a definition's name.
"""

from pathlib import Path

import pytest
import reachability


def package(root: Path, **modules: str) -> Path:
    """A package `pkg` under `root` holding each module's source."""
    directory = root / "pkg"
    directory.mkdir()
    (directory / "__init__.py").write_text("")
    for name, source in modules.items():
        (directory / f"{name}.py").write_text(source)
    return directory


def failures(
    directory: Path,
    declared: dict[str, str] | None = None,
    listed: dict[str, str] | None = None,
) -> list[str]:
    return reachability.audit(directory, declared or {}, listed or {}).failures


def test_a_function_the_package_calls_is_reached(tmp_path: Path) -> None:
    directory = package(tmp_path, a="def used():\n    pass\n\nused()\n")
    assert failures(directory) == []


def test_a_function_named_only_by_itself_is_not_reached(tmp_path: Path) -> None:
    directory = package(tmp_path, a="def loop(n):\n    return loop(n - 1)\n")
    assert failures(directory) == [
        "pkg.a.loop is named nowhere in the package and no reason states what "
        "reaches it"
    ]


def test_a_method_named_as_an_attribute_is_reached(tmp_path: Path) -> None:
    directory = package(
        tmp_path,
        a="class Box:\n    def open(self):\n        pass\n",
        b="from pkg.a import Box\n\nBox().open()\n",
    )
    assert failures(directory) == []


def test_an_import_alias_reaches_the_function_it_imports(tmp_path: Path) -> None:
    directory = package(
        tmp_path,
        a="def run():\n    pass\n",
        b="from pkg.a import run as go\n\ngo()\n",
    )
    assert failures(directory) == []


def test_a_nested_function_is_part_of_the_function_holding_it(
    tmp_path: Path,
) -> None:
    source = "def outer():\n    def inner():\n        pass\n\nouter()\n"
    directory = package(tmp_path, a=source)
    assert reachability.audit(directory, {}, {}).read == 1


def test_a_method_the_language_calls_is_reached(tmp_path: Path) -> None:
    directory = package(
        tmp_path, a="class Box:\n    def __repr__(self):\n        pass\n"
    )
    assert failures(directory) == []


def test_a_declared_entry_point_is_reached(tmp_path: Path) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "pkg"\n\n[project.scripts]\nrun = "pkg.cli:main"\n'
    )
    directory = package(tmp_path, cli="def main():\n    pass\n")
    declared = reachability.entry_points(project)
    assert declared == {
        "pkg.cli.main": "the console script run declared in pyproject.toml"
    }
    assert failures(directory, declared) == []


def test_a_listed_framework_hook_is_reached(tmp_path: Path) -> None:
    directory = package(
        tmp_path, a="class Scanner:\n    def hook(self):\n        pass\n"
    )
    listed = {"pkg.a.Scanner.hook": "the base class calls it"}
    result = reachability.audit(directory, {}, listed)
    assert result.failures == []
    assert result.reported == ["pkg.a.Scanner.hook: the base class calls it"]


def test_a_listed_definition_the_package_names_fails(tmp_path: Path) -> None:
    directory = package(tmp_path, a="def used():\n    pass\n\nused()\n")
    assert failures(directory, listed={"pkg.a.used": "a caller"}) == [
        "pkg.a.used is listed as reached from outside the package, and the "
        "package names it"
    ]


def test_a_listed_definition_the_package_lacks_fails(tmp_path: Path) -> None:
    directory = package(tmp_path, a="")
    assert failures(directory, listed={"pkg.a.gone": "a caller"}) == [
        "pkg.a.gone is listed and the package defines no such name"
    ]


SHADOWED = "pkg.a.Box.error is named nowhere in the package and no reason " + (
    "states what reaches it"
)
BOX = "class Box:\n    def error(self):\n        pass\n"


@pytest.mark.parametrize(
    "source",
    [
        "def run():\n    error = 1\n    return error\n\nrun()\n",
        "def run(error):\n    return error\n\nrun(1)\n",
        "def run():\n    try:\n        pass\n    except OSError as error:\n"
        "        raise ValueError(error) from error\n\nrun()\n",
        "def run(items):\n    for error in items:\n        print(error)\n\nrun([])\n",
        "def run(items):\n    return [error for error in items]\n\nrun([])\n",
        "def run(items):\n    return lambda error: error\n\nrun([])\n",
        "def run(report):\n    report(error=1)\n\nrun(print)\n",
        "error = 1\nprint(error)\n",
    ],
    ids=[
        "local variable",
        "parameter",
        "exception name",
        "loop target",
        "comprehension target",
        "lambda parameter",
        "keyword argument",
        "module variable",
    ],
)
def test_a_binding_sharing_a_definitions_name_does_not_reach_it(
    tmp_path: Path, source: str
) -> None:
    directory = package(tmp_path, a=BOX + "\n" + source)
    assert failures(directory) == [SHADOWED]


def test_a_variable_of_an_enclosing_function_shadows_the_name_inside_it(
    tmp_path: Path,
) -> None:
    source = "def run():\n    error = 1\n    return lambda: error\n\nrun()\n"
    directory = package(tmp_path, a=BOX + "\n" + source)
    assert failures(directory) == [SHADOWED]


def test_a_name_a_function_loads_without_binding_reaches_the_definition(
    tmp_path: Path,
) -> None:
    source = (
        "def error():\n    pass\n\n"
        "def run(items):\n    return [error() for _ in items]\n\nrun([])\n"
    )
    directory = package(tmp_path, a=source)
    assert failures(directory) == []


def test_a_class_attribute_does_not_shadow_a_name_its_methods_load(
    tmp_path: Path,
) -> None:
    source = (
        "def error():\n    pass\n\n"
        "class Box:\n    error = None\n\n    def run(self):\n        error()\n\n"
        "Box().run()\n"
    )
    directory = package(tmp_path, a=source)
    assert failures(directory) == []


def test_a_decorator_reaches_the_function_it_names(tmp_path: Path) -> None:
    source = (
        "def wrapped(function):\n    return function\n\n"
        "@wrapped\ndef run():\n    pass\n\nrun()\n"
    )
    directory = package(tmp_path, a=source)
    assert failures(directory) == []


def test_a_name_declared_global_resolves_in_the_module(tmp_path: Path) -> None:
    source = (
        "def error():\n    pass\n\ndef run():\n    global error\n    error()\n\nrun()\n"
    )
    directory = package(tmp_path, a=source)
    assert failures(directory) == []
