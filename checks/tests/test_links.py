"""Assert the link check reads a document's references and the answers it gets.

What the check resolves is what it read, so the reading is held to a document
it would be read wrongly: a fenced example carrying references of its own, a
link form written inside a code span and inside an indented block, a link
beside each of those and one a nested bullet carries, a reference written
twice, and a heading repeated, whose second occurrence takes a fragment of
its own. The heading-slug rule the fragments rest on is held to
GitHub's own anchors in `test_slug.py`.

A silent host is told apart from a missing target.

A reference is unresolved when the host answered and said the target is
not there. A host returning a server error, and a host refusing the caller
with 403, each said nothing about the target, so they carry a verdict of
their own and leave the run passing. A host answering 401, and one
answering 405 to both methods, each answered about the target, so the
document is held to that answer. These are
measured against a server this test runs on the loopback interface, which
answers the statuses each case needs and counts the requests it received,
so the retry and the GET re-ask are observed rather than assumed.

A tracker reference takes the verdict its status takes anywhere else. The
status a tracker call produced is measured against a stand-in for `gh api`
answering the status line and the message each case names, so the one
function deciding both routes is observed on each side of the boundary.
"""

import subprocess
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import links
import pytest


def test_declared_root_and_fragment_self_reference(tmp_path: Path) -> None:
    author = tmp_path / "author"
    library = tmp_path / "library"
    author.mkdir()
    library.mkdir()
    document = author / "entry.md"
    document.write_text(
        "---\nprosiform:\n  root: ../library\n---\n"
        "# Entry\n\n[Self](#entry) and [Target](target.md#target).\n"
    )
    (library / "target.md").write_text("# Target\n")
    assert links.check(document, online=False) == ([], [])


class Answers:
    """The statuses one address returns, in order, and the requests it saw.

    A method named in `by_method` answers from its own statuses, so a host
    that refuses HEAD while serving GET is expressible, and a host that
    refuses both is told apart from it.
    """

    def __init__(self, statuses: list[int]) -> None:
        self.statuses = statuses
        self.by_method: dict[str, list[int]] = {}
        self.requests = 0

    def next_status(self, method: str) -> int:
        statuses = self.by_method.get(method, self.statuses)
        status = statuses[min(self.requests, len(statuses) - 1)]
        self.requests += 1
        return status


@pytest.fixture
def serving() -> Iterator[tuple[Answers, str]]:
    """A loopback server answering with the statuses the case names."""
    answers = Answers([200])

    class Handler(BaseHTTPRequestHandler):
        def answer(self) -> None:
            self.send_response(answers.next_status(self.command))
            self.end_headers()

        do_HEAD = answer  # noqa: N815 - the server's own spelling
        do_GET = answer  # noqa: N815 - the server's own spelling

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


def test_a_host_forbidding_both_methods_is_unreachable(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [403]
    outcome = links.retried(lambda: links.reach(address))
    assert isinstance(outcome, links.Unreachable)
    assert outcome.reason == "HTTP 403"


def test_a_host_forbidding_both_methods_is_asked_with_each_on_every_attempt(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [403]
    links.retried(lambda: links.reach(address))
    assert answers.requests == links.ATTEMPTS * 2


def test_a_host_forbidding_head_and_serving_get_resolves(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.by_method = {"HEAD": [403]}
    answers.statuses = [200]
    assert links.retried(lambda: links.reach(address)) is None
    assert answers.requests == 2


def test_a_forbidden_page_is_not_an_unresolved_reference(
    serving: tuple[Answers, str], tmp_path: Path
) -> None:
    answers, address = serving
    answers.statuses = [403]
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert failures == []
    assert len(unanswered) == 1
    assert "HTTP 403" in unanswered[0]


def test_an_unauthorised_page_is_an_unresolved_reference(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [401]
    assert links.retried(lambda: links.reach(address)) == "HTTP 401"


def test_an_unauthorised_page_is_decided_on_the_answer_to_head(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [401]
    links.retried(lambda: links.reach(address))
    assert answers.requests == 1


def test_a_document_naming_an_unauthorised_page_fails(
    serving: tuple[Answers, str], tmp_path: Path
) -> None:
    answers, address = serving
    answers.statuses = [401]
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert unanswered == []
    assert len(failures) == 1
    assert "HTTP 401" in failures[0]


def test_a_host_refusing_the_method_on_both_is_an_unresolved_reference(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [405]
    assert links.retried(lambda: links.reach(address)) == "HTTP 405"


def test_a_host_refusing_the_method_on_both_is_asked_with_each_once(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.statuses = [405]
    links.retried(lambda: links.reach(address))
    assert answers.requests == 2


def test_a_host_refusing_the_method_on_head_and_serving_get_resolves(
    serving: tuple[Answers, str],
) -> None:
    answers, address = serving
    answers.by_method = {"HEAD": [405]}
    answers.statuses = [200]
    assert links.retried(lambda: links.reach(address)) is None
    assert answers.requests == 2


def test_a_document_naming_a_host_refusing_the_method_fails(
    serving: tuple[Answers, str], tmp_path: Path
) -> None:
    answers, address = serving
    answers.statuses = [405]
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert unanswered == []
    assert len(failures) == 1
    assert "HTTP 405" in failures[0]


FENCED = """\
# Doc

A [plain reference](docs/one.md) and an <https://example.com/angle> address.

[definition]: docs/two.md

```markdown
A [fenced reference](docs/never.md) is an example rather than a reference.

[fenced definition]: docs/never-either.md
```

The [same reference](docs/one.md) written twice is one reference.

## A Heading

## A Heading
"""


def test_every_reference_a_document_carries_is_read() -> None:
    assert links.references(FENCED) == ["docs/one.md", "docs/two.md"]


def test_a_fenced_reference_is_an_example_rather_than_a_reference() -> None:
    found = links.references(FENCED)
    assert "docs/never.md" not in found
    assert "docs/never-either.md" not in found


def test_a_reference_written_twice_is_read_once() -> None:
    assert links.references(FENCED).count("docs/one.md") == 1


def test_a_repeated_heading_generates_a_numbered_fragment() -> None:
    assert links.fragments_of(FENCED) == {"doc", "a-heading", "a-heading-1"}


def test_a_fragment_a_heading_generates_resolves(tmp_path: Path) -> None:
    document = tmp_path / "doc.md"
    document.write_text(FENCED)
    assert links.resolve_local(document, "#a-heading-1") is None


def test_a_fragment_no_heading_generates_is_unresolved(tmp_path: Path) -> None:
    document = tmp_path / "doc.md"
    document.write_text(FENCED)
    assert links.resolve_local(document, "#a-heading-2") == (
        "no heading in doc.md generates #a-heading-2"
    )


def test_a_path_the_tree_does_not_hold_is_unresolved(tmp_path: Path) -> None:
    document = tmp_path / "doc.md"
    document.write_text(FENCED)
    assert links.resolve_local(document, "absent.md") == "absent.md does not exist"


def test_a_fragment_on_a_named_document_resolves_against_its_headings(
    tmp_path: Path,
) -> None:
    document = tmp_path / "doc.md"
    document.write_text("# Doc\n\nIt names [a heading](other.md#a-heading).\n")
    (tmp_path / "other.md").write_text(FENCED)
    assert links.resolve_local(document, "other.md#a-heading") is None
    assert links.resolve_local(document, "other.md#absent") == (
        "no heading in other.md generates #absent"
    )


def test_a_blob_or_tree_address_into_this_repository_is_resolved_by_git() -> None:
    prefix = links.REPOSITORY_URL_PREFIX
    assert links.is_repository_tree_url(f"{prefix}blob/engineering/README.md")
    assert links.is_repository_tree_url(f"{prefix}tree/engineering/artifacts")
    assert not links.is_repository_tree_url(f"{prefix}issues/39")
    assert not links.is_repository_tree_url("https://example.com/blob/main/README.md")


class Called:
    """One `gh api` invocation recorded, answering what the case names."""

    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.arguments: list[str] = []

    def run(self, arguments: list[str], **_: object) -> "Called":
        self.arguments = arguments
        return self


def answering(
    monkeypatch: pytest.MonkeyPatch,
    status: int | None,
    message: str,
    returncode: int = 1,
) -> Called:
    """`gh api` answering with the status line and message the case names."""
    headers = "" if status is None else f"HTTP/2.0 {status} Reported\r\nServer: t\r\n"
    called = Called(returncode, headers, message)
    monkeypatch.setattr(subprocess, "run", called.run)
    return called


def test_a_tracker_call_reports_the_status_the_response_carried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 404, "gh: Not Found (HTTP 404)")
    assert links.reported_status("HTTP/2.0 404 Not Found\r\nServer: t\r\n") == 404


def test_a_tracker_call_is_read_with_the_response_included(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = answering(monkeypatch, 200, "", returncode=0)
    links.resolve_github("https://github.com/m2ux/prosiform/issues/39")
    assert called.arguments[:4] == ["gh", "api", "--include", "--silent"]


@pytest.mark.parametrize("status", [503, 403, 404, 401, 405])
def test_a_tracker_read_and_a_direct_read_take_one_verdict(
    monkeypatch: pytest.MonkeyPatch, status: int
) -> None:
    answering(monkeypatch, status, f"gh: Reported (HTTP {status})")
    assert links.gh_api(["repos/m2ux/prosiform/issues/39"]) == links.verdict(status)


def test_a_tracker_call_reporting_a_server_status_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 503, "gh: Service Unavailable (HTTP 503)")
    outcome = links.gh_api(["repos/m2ux/prosiform/issues/39"])
    assert isinstance(outcome, links.Unreachable)
    assert outcome.reason == "HTTP 503"


def test_a_tracker_call_the_host_forbade_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 403, "gh: Forbidden (HTTP 403)")
    outcome = links.gh_api(["repos/m2ux/prosiform/issues/39"])
    assert isinstance(outcome, links.Unreachable)
    assert outcome.reason == "HTTP 403"


def test_a_tracker_call_naming_a_missing_target_is_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 404, "gh: Not Found (HTTP 404)")
    assert links.gh_api(["repos/m2ux/prosiform/issues/39"]) == "HTTP 404"


def test_a_tracker_call_carrying_no_status_is_unreachable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, None, "error connecting to api.github.com")
    outcome = links.gh_api(["repos/m2ux/prosiform/issues/39"])
    assert isinstance(outcome, links.Unreachable)
    assert outcome.reason == "error connecting to api.github.com"


def test_a_graphql_error_under_a_resolving_status_is_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 200, "gh: Could not resolve to a ProjectV2")
    assert links.gh_api(["graphql"]) == "gh: Could not resolve to a ProjectV2"


def test_a_tracker_call_the_host_answered_resolves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answering(monkeypatch, 200, "", returncode=0)
    assert links.gh_api(["repos/m2ux/prosiform/issues/39"]) is None


def test_a_document_naming_a_forbidden_tracker_reference_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, 403, "gh: Forbidden (HTTP 403)")
    address = "https://github.com/m2ux/prosiform/issues/39"
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert failures == []
    assert len(unanswered) == 1
    assert "HTTP 403" in unanswered[0]


def test_a_document_naming_a_missing_tracker_reference_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answering(monkeypatch, 404, "gh: Not Found (HTTP 404)")
    address = "https://github.com/m2ux/prosiform/issues/39"
    failures, unanswered = links.check(document(tmp_path, address), online=True)
    assert unanswered == []
    assert len(failures) == 1
    assert "HTTP 404" in failures[0]


LITERAL = """\
# Doc

A [plain reference](docs/one.md) sits beside `[a span](docs/never-span.md)`, and
`[span definition]: docs/never-span-either.md` is the spelling of a definition.

An indented block holds the same forms:

    [an indented reference](docs/never-indented.md)

    [indented definition]: docs/never-indented-either.md

- A bullet links [a listed target](docs/two.md).

    - A nested bullet links [a deeper target](docs/three.md).

[definition]: docs/four.md
"""


def test_a_reference_inside_a_code_span_is_an_example_rather_than_a_reference() -> None:
    found = links.references(LITERAL)
    assert "docs/never-span.md" not in found
    assert "docs/never-span-either.md" not in found


def test_a_reference_inside_an_indented_block_is_an_example() -> None:
    found = links.references(LITERAL)
    assert "docs/never-indented.md" not in found
    assert "docs/never-indented-either.md" not in found


def test_a_reference_beside_literal_content_is_read() -> None:
    found = links.references(LITERAL)
    assert "docs/one.md" in found
    assert "docs/four.md" in found


def test_a_reference_a_nested_bullet_carries_is_read() -> None:
    found = links.references(LITERAL)
    assert "docs/two.md" in found
    assert "docs/three.md" in found


def test_every_reference_the_literal_document_carries_is_read() -> None:
    assert links.references(LITERAL) == [
        "docs/one.md",
        "docs/two.md",
        "docs/three.md",
        "docs/four.md",
    ]


def test_a_heading_naming_a_code_span_still_generates_its_fragment() -> None:
    assert "the-link-form" in links.fragments_of("# Doc\n\n## The `link` Form\n")
