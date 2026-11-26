# W09 Test Evidence

Revision: prosiform `9cc103b` on `i19/e00/w09-build-tags-match-version`, run 2026-11-26 with `uv` 0.11.14.

## Check Tests

`checks/tests/test_releases.py` builds a throwaway repository per case, tags its HEAD, and configures a canned build reporting `0.16.2`.

```bash
uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . checks/tests/test_releases.py -o addopts= -v
```

| Test | Shows |
| --- | --- |
| `test_a_commit_carrying_no_tag_passes_without_a_build` | No release tag: passes, with no build configured. |
| `test_a_build_tag_the_build_reports_passes` | `python/v0.16.2` on a build reporting `0.16.2` passes. |
| `test_a_lightweight_build_tag_is_read` | A lightweight tag is read as an annotated one is. |
| `test_a_build_tag_the_build_does_not_report_fails` | `python/v0.16.3` on a build reporting `0.16.2` fails, and `main` exits 1. |
| `test_a_contract_tag_sharing_major_and_minor_passes` | `contract/v0.16.0` beside `python/v0.16.2` passes. |
| `test_a_contract_tag_differing_in_minor_fails` | `contract/v0.15.0` beside `python/v0.16.2` fails, and `main` exits 1. |
| `test_a_contract_tag_differing_in_major_fails` | `contract/v0.16.2` beside `python/v1.16.2` fails. |
| `test_a_contract_tag_alone_passes_without_a_build` | A contract tag alone passes, with no build configured. |
| `test_a_tag_on_an_earlier_commit_is_not_read` | A tag on HEAD's parent is not read. |
| `test_a_tag_under_another_prefix_is_passed_over` | `workspace/v9.9.9` and `v1` are not release tags. |
| `test_a_release_tag_naming_no_version_fails` | `python/v0.16` fails. |
| `test_a_build_tag_with_no_build_configured_fails` | A build tag with no `PROSIFORM_BUILD` raises, and `main` exits 1. |

Result: 12 passed.

## Release Commit Run

The check run over a clone of this repository checked out at `python/v0.35.0` (`b0eb7a2`), with the build that commit holds, then with faulty tags added to that clone. `run.py` imports `checks/releases.py` and points it at the clone.

```bash
PROSIFORM_BUILD="uv run --project W/release/src --frozen pf" uv run --project <worktree>/src --frozen python run.py <worktree>/checks W/release
```

The real release: exit 0.

```text
ok   python/v0.35.0 — the build reports 0.35.0
ok   python/v0.35.0 — implements contract/v0.35.0
```

With `python/v0.35.1` added: exit 1.

```text
FAIL python/v0.35.1: the build reports 0.35.0, not 0.35.1
```

With `python/v0.36.0` and `contract/v0.36.0` added: exit 1.

```text
FAIL python/v0.35.0: implements contract revision 0.35, and contract/v0.36.0 beside it names 0.36
FAIL python/v0.36.0: the build reports 0.35.0, not 0.36.0
FAIL python/v0.36.0: implements contract revision 0.36, and contract/v0.35.0 beside it names 0.35
```

## Make Check

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf" make check-all
```

Every check in `CHECKS` passed, `make releases` among them, run unsandboxed for `make links`.

```text
corpus check: 708 fixture(s), 708 pass, 0 fail, 0 awaited, 0 unexpected pass
link check: every reference in 445 document(s) resolved
releases check: no release tag names HEAD
check-all: every check passed
```
