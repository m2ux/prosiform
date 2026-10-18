# Validation

The three checks this task carries, as they were run. Each was run twice: once on the tree as written, and once on a tree deliberately broken in the way its criterion forbids, so a pass is known to mean something.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e00/w01-repository-layout-readme-and` |
| Tested revision | `e913dff37608f3dec77d8ab8e3deaa78f0113272` |
| Run from | the repository root of the task worktree |
| Interpreter | system `python3`, standard library only |
| Date | 2026-10-18 |

The checks are standalone scripts under `checks/`, run directly. W03 brings them under one documented command; nothing here depends on that command existing.

## T1 Layout check

**Observes AC1.** The repository holds one tree for the fixture corpus, one for the Python build and one for documentation.

```bash
python3 checks/layout.py
```

**Pass.** Exit 0.

```text
ok   docs/ — 2 tracked file(s), the documentation this repository owns
ok   fixtures/ — 1 tracked file(s), the language-neutral fixture corpus
ok   prototype/ — 1 tracked file(s), the Python build

layout check: 3 tree(s) present
```

**Fails on a missing tree.** With `fixtures/` removed from the index by `git rm -r --cached fixtures`, the check exits 1 and names the tree. The index was restored with `git reset` afterwards.

```text
FAIL fixtures/ holds no tracked file; it is the language-neutral fixture corpus

layout check: 1 failure(s)
```

**What it establishes and what it does not.** A tree counts when git tracks a file under it, so an untracked directory a fresh checkout would not receive does not pass. The check reads the index, not the plan: it asserts the three trees the plan names exist, and says nothing about what belongs in each.

## T2 Link check

**Observes AC5.** The README's references to the design and the plan resolve.

```bash
python3 checks/links.py --online
```

**Pass.** Exit 0, with all sixteen references resolved: seven repository-relative paths, two GitHub blob and tree URLs resolved through git against `origin/engineering`, four tracker references read through `gh api`, and three badge images and one external site fetched.

```text
ok   repository https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md
ok   remote     https://github.com/users/m2ux/projects/18
ok   local      docs/glossary.md

link check: every reference resolved
```

**Fails on an unresolvable reference.** With `[a broken reference](docs/absent.md)` appended to the README, the check exits 1 and names the path. The README was restored afterwards.

```text
FAIL README.md: docs/absent.md — docs/absent.md does not exist
```

**What it establishes and what it does not.** The run above was the online one, so every reference was actually reached. Without `--online` a reference outside this repository counts as unresolved and the check fails, which is why the offline run of the same tree reports nine such references rather than passing with them unchecked. An issue, a pull request and a project board are read through `gh api` with the caller's credentials, because this repository is private and answers an unauthenticated page request with 404. The check resolves references; that the README names the tool's purpose, its installation and its invocation is a matter the pull request's review settles.

## T3 Vocabulary check

**Observes AC6.** Every contract term the design and the acceptance criteria use is defined in the glossary the documentation tree holds.

```bash
python3 checks/vocabulary.py
```

**Pass.** Exit 0. The contract's term inventory is the planning record's glossary, read from `origin/engineering`; the text that uses it is `design.md` and the Acceptance Criteria section of each `i**-e**.md` epic file in the same plan folder; the glossary under test is `docs/glossary.md` in the working tree.

```text
vocabulary check: 33 contract term(s) used across 20 source(s), every one defined in docs/glossary.md
```

**Fails on an undefined term.** With the `closure` row deleted from `docs/glossary.md`, the check exits 1 and names the term and every source that uses it. The glossary was restored afterwards.

```text
FAIL closure — used in artifacts/planning/2026-10-17-prosiform-v1/design.md,
artifacts/planning/2026-10-17-prosiform-v1/i00-e03.md (Acceptance Criteria),
artifacts/planning/2026-10-17-prosiform-v1/i00-e04.md (Acceptance Criteria),
and docs/glossary.md does not define it
```

**What it establishes and what it does not.** The inventory is independent of the file under test, so the check cannot pass by agreeing with itself. A term the inventory does not carry is invisible to it: the shipped glossary adds `resource` and `diagnostic`, which the design uses as contract terms and the planning record's glossary does not define, and those two were found by reading the design rather than by running the check. The check also says nothing about whether a definition is correct, only that one is present. It depends on the plan folder's path on the engineering branch, which is named in the script.

## Derivation of the shipped glossary

`docs/glossary.md` is the planning record's glossary checked against the design and the epic criteria, not a copy of it.

| Entry | Why |
| --- | --- |
| `resource` | The design's "Resources are text" and its link-classification rules use the term as a contract term: a reference target that is not a local Markdown document, emitted as authored and never opened. The planning record's glossary does not define it. |
| `diagnostic` | The design's exit-status and JSON-diagnostics contract fixes what a diagnostic carries, and AC6 names the tool's diagnostics as a consumer of the glossary's vocabulary. The planning record's glossary does not define it. |

The remaining entries carry the planning record's definitions unchanged. The opening paragraph names the fixture corpus and the acceptance criteria as the consumers alongside the design and the diagnostics, matching where the vocabulary is now used.
