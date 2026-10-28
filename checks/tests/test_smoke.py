"""Assert the smoke check reads an installed command's run as the contract does.

The check installs the build and invokes the command by name, and what it
decides on is the run it gets back: the status, the two streams and the
command's own path. Each reading is held here to a run it would be read
wrongly: a success that wrote to standard error, a version response naming no
profile, a bundle differing from the source's or carried on standard output,
and a command resolving inside the repository.
"""

from pathlib import Path
from subprocess import CompletedProcess

import pytest
import smoke


def run(status: int = 0, out: str = "", err: str = "") -> CompletedProcess[str]:
    return CompletedProcess(
        args=[smoke.COMMAND], returncode=status, stdout=out, stderr=err
    )


def answering(
    monkeypatch: pytest.MonkeyPatch,
    response: CompletedProcess[str],
    bundle: str | None = None,
) -> None:
    """A command answering every run alike, writing any bundle into its run's folder."""

    def invoke(environment: Path, cwd: Path, *arguments: str) -> CompletedProcess[str]:
        if bundle is not None:
            named = smoke.derived(arguments[-1])
            folder = Path(arguments[arguments.index("-o") + 1]) / named
            folder.mkdir()
            (folder / f"{named}.bundle.md").write_text(bundle)
        return response

    monkeypatch.setattr(smoke, "invoke", invoke)


def test_a_run_that_exited_nonzero_names_the_step_and_the_reason() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.succeeded(run(status=2, err="no such option"), "pf -r")
    assert "exited 2" in str(refused.value)
    assert "no such option" in str(refused.value)


def test_a_successful_run_is_the_standard_output_it_wrote() -> None:
    assert smoke.reported(run(out="a bundle\n"), "pf") == "a bundle\n"


def test_a_run_writing_to_standard_error_is_refused() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.reported(run(out="a bundle\n", err="a warning"), "pf")
    assert "wrote to standard error" in str(refused.value)


def test_a_version_response_naming_the_profile_is_the_version(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out=f"pf 0.1.0 ({smoke.PROFILE})\n"))
    assert smoke.version(tmp_path, tmp_path) == f"pf 0.1.0 ({smoke.PROFILE})"


def test_a_version_response_naming_no_profile_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out="pf 0.1.0\n"))
    with pytest.raises(smoke.Failed) as refused:
        smoke.version(tmp_path, tmp_path)
    assert smoke.PROFILE in str(refused.value)


def test_a_bundle_differing_from_the_source_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(), "# guide\n")
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path / "elsewhere", tmp_path)
    assert "the bundle differs" in str(refused.value)


def test_a_bundle_on_standard_output_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(out=smoke.BUNDLE), smoke.BUNDLE)
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path / "elsewhere", tmp_path)
    assert "standard output carries text" in str(refused.value)


def test_a_folder_holding_no_bundle_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run())
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path / "elsewhere", tmp_path)
    assert "the output folder holds [] and []" in str(refused.value)


def test_a_bundle_writing_to_standard_error_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(err="W_RESOURCE_PORTABILITY: x\n"), smoke.BUNDLE)
    with pytest.raises(smoke.Failed) as refused:
        smoke.bundles(tmp_path, tmp_path / "elsewhere", tmp_path)
    assert "wrote to standard error" in str(refused.value)


def test_the_bundle_the_source_names_is_accepted(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, run(), smoke.BUNDLE)
    smoke.bundles(tmp_path, tmp_path / "elsewhere", tmp_path)
    assert not list((tmp_path / "bundles").iterdir())


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


def test_an_installation_with_the_retired_command_is_refused(tmp_path: Path) -> None:
    binaries = tmp_path / smoke.BIN
    binaries.mkdir()
    for command in (smoke.COMMAND, "prosiform"):
        installed = binaries / command
        installed.write_text("#!/bin/sh\n")
        installed.chmod(0o755)
    with pytest.raises(smoke.Failed, match="retired prosiform command"):
        smoke.resolve(tmp_path)


def test_a_workspace_inside_the_repository_establishes_nothing() -> None:
    with pytest.raises(smoke.Failed) as refused:
        smoke.smoke(smoke.ROOT / "workspace")
    assert "inside the repository" in str(refused.value)
