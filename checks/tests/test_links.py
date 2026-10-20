"""Assert the link check tells a silent host apart from a missing target.

A reference is unresolved when the host answered and said the target is
not there. A host returning a server error said nothing about the target,
so it carries a verdict of its own and leaves the run passing. The two are
measured against a server this test runs on the loopback interface, which
answers the statuses each case needs and counts the requests it received,
so the retry is observed rather than assumed.
"""

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import links
import pytest


class Answers:
    """The statuses one address returns, in order, and the requests it saw."""

    def __init__(self, statuses: list[int]) -> None:
        self.statuses = statuses
        self.requests = 0

    def next_status(self) -> int:
        status = self.statuses[min(self.requests, len(self.statuses) - 1)]
        self.requests += 1
        return status


@pytest.fixture
def serving() -> Iterator[tuple[Answers, str]]:
    """A loopback server answering with the statuses the case names."""
    answers = Answers([200])

    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self) -> None:  # noqa: N802 - the server's own spelling
            self.send_response(answers.next_status())
            self.end_headers()

        do_GET = do_HEAD  # noqa: N815 - the server's own spelling

        def log_message(self, format: str, *args: object) -> None:
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        yield answers, f"http://127.0.0.1:{port}/page"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(autouse=True)
def no_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    """The retry's delay, which a test has no reason to wait out."""
    monkeypatch.setattr(links, "DELAY", 0.0)


def document(tmp_path: Path, address: str) -> Path:
    path = tmp_path / "doc.md"
    path.write_text(f"# Doc\n\nThe doc names [a page]({address}).\n")
    return path


def test_a_server_error_is_unreachable_rather_than_unresolved(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [503]
    outcome = links.retried(lambda: links.reach(address))
    assert isinstance(outcome, links.Unreachable)
    assert outcome.reason == "HTTP 503"


def test_a_missing_page_is_an_unresolved_reference(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [404]
    outcome = links.retried(lambda: links.reach(address))
    assert outcome == "HTTP 404"


def test_a_silent_host_is_attempted_the_bounded_number_of_times(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [503]
    links.retried(lambda: links.reach(address))
    assert answers.requests == links.ATTEMPTS


def test_a_host_answering_on_a_later_attempt_is_resolved(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [503, 200]
    assert links.retried(lambda: links.reach(address)) is None
    assert answers.requests == 2


def test_a_missing_page_is_decided_on_the_first_answer(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [404]
    links.retried(lambda: links.reach(address))
    assert answers.requests == 1


def test_a_document_naming_a_silent_host_resolves_and_passes(
    serving: tuple[Answers, str], tmp_path: Path
) -> None:
    answers, address = serving
    answers.statuses = [503]
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert failures == []
    assert len(unanswered) == 1
    assert "HTTP 503" in unanswered[0]


def test_a_document_naming_a_missing_page_fails(
    serving: tuple[Answers, str], tmp_path: Path
) -> None:
    answers, address = serving
    answers.statuses = [404]
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert unanswered == []
    assert len(failures) == 1
    assert "HTTP 404" in failures[0]
