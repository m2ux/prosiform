"""Assert the wrapper never returns a bundle the transport did not carry whole.

These are the cases a corpus fixture cannot reach. A fixture declares a
source tree and an invocation and the runner drives that one command, so
every expectation it states is a property of the command. The wrapper is
the layer above the command: it owns the process status, the buffer and
the transport's response limit, and none of the three is observable from
inside a run of the command.

Each case therefore names a completed run — the status it returned and the
bytes it left on standard output — and asserts what the wrapper makes of
it. The end-to-end cases drive the real entry point through the wrapper,
so the status the wrapper reads is a status a process actually returned.
"""

import shutil
from pathlib import Path

import pytest

from prosiform.delivery import ENCODING, Delivery, Outcome, deliver, received

LIMIT = 4_096

BUNDLE = (
    "Follow [Guide](#guide). "
    "The rest of this bundle is material that procedure references.\n"
    "\n"
    "# Guide\n"
    "\n"
    "The command bundles this document.\n"
)
SOURCE = "# Guide\n\nThe command bundles this document.\n"
ENTRY = "guide.md"
ENTRY_POINT = "pf"


def fields(result: Delivery) -> list[str]:
    """Every string the structured result carries, for a substitution check."""
    return [value for value in vars(result).values() if isinstance(value, str)]


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A source root carrying one document the entry point can bundle."""
    (tmp_path / ENTRY).write_text(SOURCE, encoding=ENCODING)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def command(*arguments: str) -> list[str]:
    """The installed entry point, resolved by name, with its arguments.

    The wrapper wraps a process rather than a function, so the end-to-end
    cases invoke the console script the packaging declares, which is the
    command a caller reaches.
    """
    found = shutil.which(ENTRY_POINT)
    assert found is not None, f"{ENTRY_POINT} is not on the path of this environment"
    return [found, "-o", "-", *arguments]


def test_a_bundle_within_the_transport_limit_is_delivered() -> None:
    result = received(0, BUNDLE.encode(ENCODING), "", LIMIT)
    assert result.outcome is Outcome.DELIVERED
    assert result.delivered
    assert result.document == BUNDLE
    assert result.counted == len(BUNDLE.encode(ENCODING))


def test_a_bundle_exactly_at_the_transport_limit_is_delivered() -> None:
    bundle = b"x" * LIMIT
    result = received(0, bundle, "", LIMIT)
    assert result.outcome is Outcome.DELIVERED
    assert result.document == bundle.decode(ENCODING)


def test_a_bundle_over_the_transport_limit_is_a_delivery_failure() -> None:
    result = received(0, b"x" * (LIMIT + 1), "", LIMIT)
    assert result.outcome is Outcome.OVER_TRANSPORT_LIMIT
    assert not result.delivered
    assert result.counted == LIMIT + 1


def test_a_bundle_over_the_transport_limit_carries_no_part_of_the_document() -> None:
    oversized = BUNDLE + "x" * LIMIT
    result = received(0, oversized.encode(ENCODING), "", LIMIT)
    assert result.document is None
    for value in fields(result):
        assert "# Guide" not in value
        assert "x" * 16 not in value


def test_a_delivery_failure_names_the_limit_and_the_figure_that_crossed_it() -> None:
    result = received(0, b"x" * (LIMIT + 1), "", LIMIT)
    assert str(LIMIT) in result.explain()
    assert str(LIMIT + 1) in result.explain()


def test_a_transport_limit_of_nothing_is_refused() -> None:
    with pytest.raises(ValueError, match="does not mean unlimited"):
        received(0, b"", "", 0)


def test_a_nonzero_status_is_a_failure_whatever_standard_output_carried() -> None:
    result = received(1, BUNDLE.encode(ENCODING), "", LIMIT)
    assert result.outcome is Outcome.BUILD_FAILED
    assert not result.delivered
    assert result.document is None


def test_a_failure_is_read_from_the_status_and_not_from_an_empty_output() -> None:
    assert received(0, b"", "", LIMIT).outcome is Outcome.DELIVERED
    assert received(4, b"", "", LIMIT).outcome is Outcome.BUILD_FAILED


@pytest.mark.parametrize("status", [1, 2, 3, 4])
def test_every_failing_status_the_contract_names_withholds_the_document(
    status: int,
) -> None:
    result = received(status, BUNDLE.encode(ENCODING), "", LIMIT)
    assert result.outcome is Outcome.BUILD_FAILED
    assert result.status == status
    assert result.document is None


def test_the_structured_result_carries_the_diagnostic_stream() -> None:
    result = received(1, b"", '{"severity": "error"}\n', LIMIT)
    assert result.diagnostics == '{"severity": "error"}\n'


def test_a_run_of_the_entry_point_delivers_its_bundle(root: Path) -> None:
    result = deliver(command(ENTRY), LIMIT)
    assert result.outcome is Outcome.DELIVERED
    assert result.document == BUNDLE
    assert result.status == 0


def test_a_run_of_the_entry_point_over_the_transport_limit_delivers_nothing(
    root: Path,
) -> None:
    whole = deliver(command(ENTRY), LIMIT)
    assert whole.document is not None
    result = deliver(command(ENTRY), whole.counted - 1)
    assert result.outcome is Outcome.OVER_TRANSPORT_LIMIT
    assert result.status == 0
    assert result.document is None


def test_a_failing_run_of_the_entry_point_is_read_from_its_status(root: Path) -> None:
    result = deliver(command("absent.md"), LIMIT)
    assert result.outcome is Outcome.BUILD_FAILED
    assert result.status != 0
    assert result.document is None
    assert "E_TARGET_NOT_FOUND" in result.diagnostics
