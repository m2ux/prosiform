# Tooling

> Plan · Created 2026-10-24

Three tools, each removing one of the guesses the session made. The first two are preserved and raised as [issue #243](https://github.com/m2ux/prosiform/issues/243); the third is new here. Each is stated as what it must do, so the implementation is free to differ.

## T1: A check run that reports every failure

**Removes** [F1](findings.md#f1-a-red-run-reports-one-failure-and-hides-the-rest).

`make check` stops at the first failing target. `make -k check` continues and reports each, which was verified on this session's tree: four failures where `make check` names one, and exit 0 with none when the tree is green.

**What it must do:**

- Run every target `check` declares, whether or not an earlier one failed.
- Print each failing target and the count of its failures, so the set is one screen.
- Exit nonzero when any target failed.
- Name each failure by target rather than by line number, since `Makefile:56` does not say `corpus`.

**Where it belongs:** a `check-all` target in `Makefile`, beside the `check` target it complements. The two answer different questions — `check` asks whether the tree is good, `check-all` asks what is wrong with it — so both should exist.

**What it costs:** the target itself is one line. The summary is a small shell or Python step. No new dependency.

## T2: A triage that separates a crash from drift

**Removes** [F2](findings.md#f2-a-crash-is-reported-as-a-fixture-failure) and [F3](findings.md#f3-regenerating-expectations-cannot-tell-intent-from-defect).

Preserved at [corpus drift tools](../../2026-10-24-corpus-drift-tools/triage.py), raised as [issue #243](https://github.com/m2ux/prosiform/issues/243). Restated here as the properties it must not lose.

**What it must do:**

- Report a run's exit status and internal errors *before* comparing any bytes, because a run that failed in itself has more wrong with it than its output.
- Read the manifest first: a fixture declaring `E_UNEXPECTED_INTERNAL_ERROR` is exercising that outcome, not reporting a fault.
- Classify the byte difference so a reader knows the shape of it — lines inserted, removed, both, reordered, or rewritten in place.
- Export the category as data, so a restatement can select on it.

**What it must not do:** decide whether a difference is intended. That judgement is the reader's, and the tool's job is to make it about the changed fixtures rather than about all of them.

## T3: A restatement that cannot record a fault

**Removes** [F3](findings.md#f3-regenerating-expectations-cannot-tell-intent-from-defect) and [F6](findings.md#f6-throwaway-scripts-were-written-and-rewritten).

Preserved at [corpus drift tools](../../2026-10-24-corpus-drift-tools/regenerate.py), raised as [issue #243](https://github.com/m2ux/prosiform/issues/243).

**What it must do:**

- Write nothing without an explicit flag, so the set a change would rewrite is read before any of it is written.
- Replace exactly two things: the declared output file, and the `[expected]` block of the manifest. Copy the manifest around that block through byte for byte, because re-rendering escapes every non-ASCII character in the file and hides the line a reviewer needed.
- Refuse a fixture whose run reports an internal error, name it, and exit nonzero.
- Restrict a rewrite to one category, so a change accepts the drift it intended and leaves the rest for a reader.

**What it must not do:** rewrite a fixture's input. The source tree, the description, the clauses and the invocation are what the expectation is *about*, so a run that edits them records the build's behaviour as the fixture's premise.

**Where it belongs:** `checks/`, beside `runner.py` and `manifests.py`, importing both rather than copying them. The copy in `scripts/` should be removed when this lands.

## T4: A probe that answers what a declaration does

**Removes** [F4](findings.md#f4-root-has-three-jobs-and-no-stated-scope).

New here. A declaration's behaviour took five ad-hoc probes to separate, and each probe was a temporary directory, a source pair, and a build run. The same shape recurs for any frontmatter key, so the probe is worth keeping.

**What it must do:**

- Take a source template and a set of declaration variants, build each, and print the derived filename and the heading of each result side by side.
- Print, for a link under each variant, whether it resolved and to what identity.
- Run from a temporary directory and leave nothing behind, which is the part every hand-written probe got wrong.

**Why it is a probe rather than a test:** its output is a table a human reads to decide what the rule *is*, before any fixture states what it must be. Once the rule is settled, the table becomes a fixture and the probe is no longer needed for that key.

**A worked result**, from the runs that settled `root`:

| Declared root | Derived filename | Heading | `[x](codex.md)` | `[x](rules/codex.md)` |
| --- | --- | --- | --- | --- |
| `"."` | `a.bundle.md` | `# A` | resolves | resolves |
| `".."` | `rules_a.bundle.md` | `# Rules` | fails | resolves |

One run each. The table is what the session assembled from five separate probes.

## T5: A checkout that removes itself

**Removes** the leftover worktrees named in [F6](findings.md#f6-throwaway-scripts-were-written-and-rewritten).

Already written: [revision-check](../../2026-10-24-237-work-planner-link-capture/revision-check.py), raised as [issue #237](https://github.com/m2ux/prosiform/issues/237). The session created three baseline worktrees by hand and left two behind, which is the exact failure that script exists to prevent.

**What it must do:** resolve a branch or tag to a commit, create a detached checkout at it, run a supplied command there, and remove the checkout whatever the command returns. Two of the three were still present when this record was written and were removed by hand.

## What Each Tool Would Have Saved

| Tool | Probes it removes | Rough cost avoided |
| --- | --- | --- |
| `check-all` | The reported failure being one of three | Two probes, and the risk of shipping a still-red tree |
| Triage | Writing seven classifier scripts | Half the session's tooling time |
| Restatement | Rebuilding manifests, and two near-inversions | One manifest churn across 177 files, and two wrong fixtures |
| Root probe | Five ad-hoc probe directories | Several rebuilds per question |
| Running a revision locally | Three worktrees, two left behind | Manual cleanup, and the risk that a bisect comparison is contaminated |
