## Overview

`-f` and the bare-fragment positional form are removed. A section is named as `document#fragment`, which is how every other reference in the tool is already written, and `pf '#section'` becomes a usage error naming that spelling as the remedy.

## Problem

The option adds a spelling and a failure mode, and nothing needs either.

- **Every use is rewritable.** `pf -f guide.md '#stop'` and `pf 'guide.md#stop'` select the same section. Nothing is computable with `-f` that is not computable without it.
- **The obvious spelling errors.** A bare `#section` without `-f` is a usage error, so `pf '#procedure'` — the thing a caller types first — fails. An option whose absent form is an error is one that needs a prohibition to explain itself.
- **Three fixtures carry it, two of them only its absence.** `cli/fragment-only-reference-without-from` tests the refusal, `extraction/a-fragment-alone-selects-from-the-referrer` and `usage-example/a-bare-fragment-and-its-referring-document` test the capability.
- **It has no consumer.** No caller in this repository passes one document and varies its sections; the form exists because the grammar admitted it.
- **It is one more name every frontmatter rule must exclude.** The preset work refuses `-f` in frontmatter, and removing the option removes that rule with it.

## Proposal

- **`-f` is removed.** The parser declares no referrer, and `cli.entry` is reached for positional references alone.
- **`document#fragment` is the only spelling for a section.** It is what a link already is, so a caller learns one form.
- **A bare `#section` is a usage error.** It names `document#fragment` as the remedy and exits `2`, which is the code every invalid usage carries. A fragment of an implied document is a rule nothing else in the tool has, so the form is refused rather than guessed at.
- **The link form is untouched.** `[Check](#section)` inside a document resolves against the document that carries it, exactly as it does today. That is ordinary Markdown and no part of this removal reaches it.
- **The deriving of a run's name is unchanged where it can be.** A section entry still derives its name from the document it names, and the fragment-only branch that read the referrer goes with the option.
- **The design's CLI contract loses the row.** `make invocation` holds the table and the help output to each other in both directions, so the row and the option go together.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, retired option | AC7 | [I08:E02](https://github.com/m2ux/prosiform/issues/445) | | |
| W01 | The parser, the refusal and the entry | AC1, AC6 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | The derived name without a referrer | AC2 | W01 | | |
| W03 | The corpus without the three fixtures | AC3 | W01 | | |
| W04 | `invocation.md` and the guide without the row | AC4 | W01 | | |
| W05 | The substitution work it invalidated | AC5 | W03 | | |

## Acceptance Criteria

- [ ] **AC1.** `pf '#section'` is invalid usage with exit status `2`, naming `document#fragment` as the remedy, and `-f` is not an option the build accepts, as the corpus fixture `fixtures/cli/a-bare-fragment-is-invalid-usage` shows.
- [ ] **AC2.** A positional `document#fragment` derives its run's name from the document it names, exactly as it does today, as the corpus fixtures over section entries show.
- [ ] **AC3.** Every corpus fixture the three removed ones covered is either withdrawn or rewritten to the `document#fragment` spelling, and no fixture names `-f`, as `make harness` and `make corpus` show.
- [ ] **AC4.** The documented option table names no `-f` and agrees with the help output, and the guide's prose names `document#fragment` alone, as `make invocation` shows.
- [ ] **AC5.** The substitution epic's criterion for a redirected referrer is marked superseded and its fixture withdrawn, as an inspection of that epic shows.
- [ ] **AC6.** The link form is unchanged: a `[Check](#section)` link resolves against the document that carries it, as the corpus fixtures over fragment-only links show.
- [ ] **AC7.** The design states `document#fragment` as the one spelling for a section, names the removal, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.

## References

- **R0.** Epic — [I08:E03 Remove the Referrer](https://github.com/m2ux/prosiform/issues/449).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions this removal comes from.
- **R2.** [I08:E07 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) — the epic whose redirected-referrer criterion this supersedes.
