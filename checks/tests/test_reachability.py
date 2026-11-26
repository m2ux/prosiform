"""Assert the reachability check reads a package the way a caller names it.

Each case writes a small package the check would misread if it compared the
wrong names: a function only its own body names, a method named only as an
attribute, a function reached through an import alias, a nested function, a
method a framework calls, and a reason listed for a definition that needs
none or does not exist.
"""

from pathlib import Path

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
