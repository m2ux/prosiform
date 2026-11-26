"""Assert the release tag check holds the tags naming HEAD to the build.

Each case builds a throwaway repository, tags its HEAD as a release would,
and configures a canned build reporting one version, so a tag and the
version it asserts are set apart and the check is run over each pairing.
The check's own exit status is read through `main`, pointed at that
repository, for the two faults the versioning policy forbids.
"""

import shlex
import subprocess
from pathlib import Path

import pytest
from releases import check, main
from runner import BUILD, BuildNotConfigured

GIT = [
    "git",
    "-c",
    "user.name=Release",
    "-c",
    "user.email=release@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "tag.gpgsign=false",
]


def git(repository: Path, *arguments: str) -> None:
    """Run one git command in the repository, failing the test when it fails."""
    subprocess.run(
        GIT + list(arguments), cwd=repository, check=True, capture_output=True
    )


def build(directory: Path, version: str) -> str:
    """A build reporting `version` beside a profile for `-v`, and nothing else."""
    line = directory / "version"
    line.write_text(f"tool {version} (prosiform-markdown)\n", encoding="utf-8")
    script = f'case "$1" in -v) cat {shlex.quote(str(line))} ;; *) exit 2 ;; esac'
    return shlex.join(["/bin/sh", "-c", script, "tool"])


@pytest.fixture
def repository(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A repository of one commit, with a build reporting 0.16.2 configured."""
    root = tmp_path / "repository"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "commit", "-q", "--allow-empty", "-m", "Release")
    monkeypatch.setenv(BUILD, build(tmp_path, "0.16.2"))
    return root


def tag(repository: Path, *names: str) -> None:
    """Name HEAD with each annotated tag, as a release names its merge."""
    for name in names:
        git(repository, "tag", "-a", "-m", name, name)


def test_a_commit_carrying_no_tag_passes_without_a_build(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD)
    assert check(repository) == ([], [])


def test_a_build_tag_the_build_reports_passes(repository: Path) -> None:
    tag(repository, "python/v0.16.2")
    passed, failures = check(repository)
    assert failures == []
    assert passed == ["ok   python/v0.16.2 — the build reports 0.16.2"]


def test_a_lightweight_build_tag_is_read(repository: Path) -> None:
    git(repository, "tag", "python/v0.16.3")
    assert check(repository)[1] == [
        "python/v0.16.3: the build reports 0.16.2, not 0.16.3"
    ]


def test_a_build_tag_the_build_does_not_report_fails(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag(repository, "python/v0.16.3")
    assert check(repository)[1] == [
        "python/v0.16.3: the build reports 0.16.2, not 0.16.3"
    ]
    monkeypatch.setattr("releases.ROOT", repository)
    assert main() == 1


def test_a_contract_tag_sharing_major_and_minor_passes(repository: Path) -> None:
    tag(repository, "contract/v0.16.0", "python/v0.16.2")
    passed, failures = check(repository)
    assert failures == []
    assert "ok   python/v0.16.2 — implements contract/v0.16.0" in passed


def test_a_contract_tag_differing_in_minor_fails(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tag(repository, "contract/v0.15.0", "python/v0.16.2")
    assert check(repository)[1] == [
        "python/v0.16.2: implements contract revision 0.16, "
        "and contract/v0.15.0 beside it names 0.15"
    ]
    monkeypatch.setattr("releases.ROOT", repository)
    assert main() == 1


def test_a_contract_tag_differing_in_major_fails(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(BUILD, build(repository.parent, "1.16.2"))
    tag(repository, "contract/v0.16.2", "python/v1.16.2")
    assert check(repository)[1] == [
        "python/v1.16.2: implements contract revision 1.16, "
        "and contract/v0.16.2 beside it names 0.16"
    ]


def test_a_contract_tag_alone_passes_without_a_build(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD)
    tag(repository, "contract/v0.17.0")
    assert check(repository) == (
        ["ok   contract/v0.17.0 — a contract revision tagged alone"],
        [],
    )


def test_a_tag_on_an_earlier_commit_is_not_read(repository: Path) -> None:
    tag(repository, "python/v0.15.0")
    git(repository, "commit", "-q", "--allow-empty", "-m", "Later")
    assert check(repository) == ([], [])


def test_a_tag_under_another_prefix_is_passed_over(repository: Path) -> None:
    tag(repository, "workspace/v9.9.9", "v1")
    assert check(repository) == ([], [])


def test_a_release_tag_naming_no_version_fails(repository: Path) -> None:
    tag(repository, "python/v0.16")
    assert check(repository)[1] == [
        "python/v0.16: a release tag names its version as vX.Y.Z"
    ]


def test_a_build_tag_with_no_build_configured_fails(
    repository: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD)
    tag(repository, "python/v0.16.2")
    with pytest.raises(BuildNotConfigured):
        check(repository)
    monkeypatch.setattr("releases.ROOT", repository)
    assert main() == 1
