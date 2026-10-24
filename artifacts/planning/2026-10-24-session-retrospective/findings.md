# Findings

> Plan · Created 2026-10-24

Six findings from the session that restored `main`. Each names what happened, what it cost, and the change that removes it. They are ordered by what they cost, not by what area of the repository they touch.

Each finding carries one disposition:

- **Script** — a reusable tool removes the guesswork.
- **Skill** — a stated rule changes what a session does.
- **Repository** — the repository's own checks or contracts change.

## F1: A red run reports one failure and hides the rest

**Repository.** The largest cost in the session, and the one with the smallest fix.

`make check` declares its targets in one dependency line and stops at the first that fails. Across six consecutive red commits, the reported target moved from `links` to `corpus` to `test`. None of the later reports was wrong; each was incomplete, and each made the previous problem invisible.

**What it cost.** Two probes to discover the tree was red on three targets, not one. A session that trusted the tip's report would have fixed one target and shipped a still-red `main`.

**The change.** Add a `check-all` target that runs every check under `make -k`, collects the failures, and prints them as one list. The reading half already exists: `make -k check` reports all four failures on a red tree and exits 0 with none on a green one, verified on this session's tree.

## F2: A crash is reported as a fixture failure

**Repository.** `checks/runner.py` decides a fixture from its manifest alone and returns one boolean. A build that reports `E_UNEXPECTED_INTERNAL_ERROR` and a build whose output drifted are both `passed == False`.

**What it cost.** A regeneration driven from the runner's verdict would have written `exit_status = 0` into the depth-overflow fixture, whose entire clause is that the run fails, and into the generated-input fixture, declaring that a published bundle compiles. Both were caught by reading, not by the tooling — and one only because the tool happened to refuse internal errors.

**The change.** A fixture's verdict needs a third state beside pass and fail: a run that failed in itself is not a result the corpus can record. The triage tool preserved in [tooling](tooling.md) already separates them; the corpus runner should return the distinction rather than a boolean.

## F3: Regenerating expectations cannot tell intent from defect

**Skill.** The corpus states what the build does. A tool that rewrites it from the build's output states what the build does *now*, which is the same thing only if the change was intended.

**What it cost.** 186 fixtures were red at once. Regenerating all of them was the obvious move and was wrong for at least four: two depth-overflow fixtures exercising a shift the parent no longer receives, one generated-input fixture whose own input was stale, and one self-reference fixture that was crashing.

**The change.** A stated rule: **a red corpus run is triaged before it is restated, and a fixture whose run failed in itself is never restated.** The category each fixture falls in decides whether a human reads it. This belongs in the workspace instructions rather than a single skill, because it governs any session touching the corpus.

## F4: `root` has three jobs and no stated scope

**Skill and contract.** `prosiform.root` decides what a document is called, which documents a link may reach, and how a link is spelled to reach one. No clause distinguishes the three, and the second and third disagree: under `root: ".."`, `[A](rules/codex.md)` resolves from the root while `[B](codex.md)` resolves from the file.

**What it cost.** Two commits misread it and were merged; five probes to separate the jobs; a broken link check whose cause took a baseline comparison to find.

**The change.** Scoped and raised as [issue #245](https://github.com/m2ux/prosiform/issues/245). The tooling change is smaller and belongs here: a session should not have to probe a declaration to learn what it does. `tooling.md` carries a probe that answers the three questions with one run each, so the answer is measured rather than inferred.

## F5: The check that was already red could not be seen

**Repository.** `checks/links.py` resolved a parent-segment link by prefixing the declared root, while the build resolved it from the file. A document the build accepted was reported as broken.

**What it cost.** The link check was red from `3d549a26` and stayed red through five commits. Because `corpus` failed first from `52851dd` onward, nobody saw it. When it finally ran, the report named seven documents — of which five were correct links the checker misresolved, and two were genuinely wrong.

**The change.** Fixed in this session's branch. The general lesson is the same as F1: a check that cannot run is a check that is not known to pass, so the set must be reported together.

## F6: Throwaway scripts were written and rewritten

**Skill.** Seven classifier scripts and five debug scripts were written under `/tmp` before the real question was formed, and `regenerate.py` was written twice, in two places, differently — once into `scripts/` and once into a planning folder.

**What it cost.** Roughly a third of the session. The two copies have since diverged by 211 diff lines, and the divergence is behavioural rather than cosmetic: the copy in `scripts/` writes as it runs and refuses nothing, while the planning copy is dry by default and refuses a run that crashed. A session reaching for the version in `scripts/` gets neither safeguard, which is the version most likely to be found first.

**The change.** Two parts. A tool that answers a recurring question belongs in `checks/` at the time it is written, beside the corpus it serves — not in `scripts/`, not in a planning folder, not in `/tmp`. And a planning record preserves a script only where the script is not reachable from the repository; where it is, the record links to it.

## What Is Not A Finding

Three things looked like problems and were not, and recording them saves the next session the same probes.

- **A fixture that reports an internal error may be declaring one.** `diagnostics/a-run-that-fails-in-itself` exists to exercise the status an unexpected failure returns, so its crash is the expectation. Triage must read the manifest before treating a crash as a fault.
- **Two spellings of one document under one root are not always a bug.** Under `root: "."` both `codex.md` and `./codex.md` resolve. The disagreement is specific to a root that steps up.
- **The corpus failing first is not the corpus being wrong.** At `15c7805`, `test` failed first and the corpus was sound. Order is not severity.
