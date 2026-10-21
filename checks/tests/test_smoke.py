"""Assert the smoke check reads an installed command's run as the contract does.

The check installs the build and invokes the command by name, and what it
decides on is the run it gets back: the status, the two streams and the
command's own path. Each reading is held here to a run it would be read
wrongly: a success that wrote to standard error, a version response naming no
profile, a bundle differing from the source's, and a command resolving inside
the repository.
"""

from pathlib import Path
from subprocess import CompletedProcess

import pytest
import smoke


def run(status: int = 0, out: str = "", err: str = "") -> CompletedProcess[str]:
    return CompletedProcess(
        args=[smoke.COMMAND], returncode=status, stdout=out, stderr=err
    )


def answering(monkeypatch: pytest.MonkeyPatch, response: CompletedProcess[str]) -> None:
    def invoke(environment: Path, cwd: Path, *arguments: str) -> CompletedProcess[str]:
        return response

    monkeypatch.setattr(smoke, "invoke", invoke)


def test_a_run_that_exited_nonzero_names_the_step_and_the_reason() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.succeeded(run(status=2, err="no such option"), "prosiform --root")
    assert "exited 2" in str(refused.value)
    assert "no such option" in str(refused.value)


def test_a_successful_run_is_the_standard_output_it_wrote() -> None:
    assert smoke.reported(run(out="a bundle\n"), "prosiform") == "a bundle\n"


def test_a_run_writing_to_standard_error_is_refused() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.reported(run(out="a bundle\n", err="a warning"), "prosiform")
    assert "wrote to standard error" in str(refused.value)


def test_a_version_response_naming_the_profile_is_the_version(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out=f"prosiform 0.1.0 ({smoke.PROFILE})\n"))
    assert smoke.version(tmp_path, tmp_path) == f"prosiform 0.1.0 ({smoke.PROFILE})"


def test_a_version_response_naming_no_profile_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out="prosiform 0.1.0\n"))
    with pytest.raises(smoke.Failed) as refused:
        smoke.version(tmp_path, tmp_path)
    assert smoke.PROFILE in str(refused.value)


def test_a_bundle_differing_from_the_source_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out="# guide\n", err=smoke.REPORT))
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path, tmp_path)
    assert "the bundle differs" in str(refused.value)


def test_a_bundle_reporting_another_destination_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(
        monkeypatch, run(out=smoke.BUNDLE, err="W_ENTRY_DESTINATION: elsewhere\n")
    )
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path, tmp_path)
    assert "another entry destination" in str(refused.value)


def test_the_bundle_and_the_report_the_source_names_are_accepted(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out=smoke.BUNDLE, err=smoke.REPORT))
    smoke.bundles(tmp_path, tmp_path, tmp_path)


def test_an_environment_naming_no_command_is_refused(tmp_path: Path) -> None:
    (tmp_path / smoke.BIN).mkdir()
    with pytest.raises(smoke.Failed) as refused:
        smoke.resolve(tmp_path)
    assert f"names no {smoke.COMMAND} command" in str(refused.value)


def test_a_command_inside_the_repository_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    binaries = tmp_path / smoke.BIN
    binaries.mkdir()
    inside = binaries / smoke.COMMAND
    inside.write_text("#!/bin/sh\n")
    inside.chmod(0o755)
    monkeypatch.setattr(smoke, "ROOT", tmp_path)
    with pytest.raises(smoke.Failed) as refused:
        smoke.resolve(tmp_path)
    assert "inside the repository" in str(refused.value)


def test_a_command_outside_the_repository_resolves(tmp_path: Path) -> None:
    binaries = tmp_path / smoke.BIN
    binaries.mkdir()
    installed = binaries / smoke.COMMAND
    installed.write_text("#!/bin/sh\n")
    installed.chmod(0o755)
    assert smoke.resolve(tmp_path) == installed.resolve()


def test_a_workspace_inside_the_repository_establishes_nothing() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.smoke(smoke.ROOT / "workspace")
    assert "inside the repository" in str(refused.value)
