# Planning Evidence

## Inspected Sources

| Source | Recorded identity | Finding |
| --- | --- | --- |
| User-linked workflow-server guidelines | Retrieved through GitHub API on 2026-10-22; Git blob `adcc76070f17dcdbab3f63ce25f60c9b8d551217` | Byte-identical to this workspace's `skills/guidelines.md` |
| Workspace | `5ae5fbeb442f642421c964b3497ef393e0d4fdca` | Skill location and shared checker inspected; existing root edits left untouched |
| Local Prosiform main checkout | `ea82c8bb03acb2f3c3ca64f6003005d4bf53ebd6`, `.worktrees/source-readme` | README, invocation guide, package metadata, profile implementation, CLI documentation and fixture inventory inspected |
| Engineering checkout | `a89c2a1a3e615719155adf24842bb595bd929029` | Existing planning layout and contract inspected |
| Contract's most recent file commit | `4cbd8a7a7e63dd145321d4d786bd57a762f1afd1` | Author-facing profile, section selection, frontmatter, link classification, path identity and validation rules inspected |
| `.project/main/AGENTS.md` | Absent | No component edit performed; `.project/main/README.md` contains only `tbd` |

The GitHub web reader could not retrieve the requested page. The authenticated API retrieval succeeded; decoding and comparing its content with the local guidelines returned equality. The source was verified live, not inferred from the local filename.

## Runtime Observation

From `.worktrees/source-readme`, the existing `src/.venv/bin/prosiform --version` reports `prosiform 0.1.0 (skill-markdown-v1)`. Its `--help` includes `--check`, `--diagnostics`, `--group SLUG:DEPTH`, `--codes`, and documented exit categories. The inspected `src/pyproject.toml` declares `0.9.0`.

These information commands establish what that executable reports, not that its installed code corresponds to the inspected source. No compatibility compilation or behavioral skill evaluation is claimed by this planning record.

## Source Discrepancies

| Concern | Evidence | Planning treatment |
| --- | --- | --- |
| Outside-root references | Design “Reference normalization and path identity” opening paragraph conflicts with “Link classification and resource handling”, the resolution table and `invocation.md` | Record the entry-versus-authored-link distinction and require fixture confirmation |
| Deferred target inspection | Design “A deferred link's target” requires document/heading confirmation while asserting no opening/parsing | Specify the observable validity and exclusion behavior; verify through existing deferral fixtures |
| Build identity | Package metadata and existing virtual-environment version disagree | Establish an isolated matching build before implementation acceptance |

## Relevant Existing Fixtures

Paths below are relative to the inspected Prosiform main checkout. They identify reusable contract evidence, not tests run during planning.

- `fixtures/profile/the-constructs-the-profile-supports/`
- `fixtures/profile/raw-html-in-selected-content/`
- `fixtures/identity/two-headings-sharing-a-slug/`
- `fixtures/identity/an-ordinal-names-no-source-heading/`
- `fixtures/reference/a-document-outside-the-root-is-text/`
- `fixtures/reference/a-definition-outside-the-selected-section/`
- `fixtures/deferral/a-marked-reference-is-not-compiled/`
- `fixtures/deferral/a-deferred-reference-naming-no-heading/`
- `fixtures/deferral/a-deferred-destination-named-from-the-root/`
- `fixtures/structural-ancestors/disjoint-selections-keep-their-outline/`
- `fixtures/depth-overflow/a-source-heading-the-shift-pushes-past-the-sixth/`
- `fixtures/frontmatter/dot-terminated/`

## Planning Validation

- Scope reflects the user's choice of general Prosiform-compatible Markdown.
- One implementation task, one mode and one PR; no compiler changes or added dependencies planned.
- Every acceptance criterion has an evidence requirement and a delivery stage.
- A sandboxed local check passed for the planning inventory, nine acceptance-criterion identifiers, all twelve fixture manifest paths and all local Markdown links outside inline code examples.
- Runtime commands were informational only; skill creation, compiler tests and independent agent evaluations are future implementation work.
- Planning files are isolated in the existing engineering worktree; unrelated `.wp/` and workspace changes are excluded from the commit.
