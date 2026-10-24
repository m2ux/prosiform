# Corpus Drift Triage — October 2026

> Plan · Created 2026-10-24

## Executive Summary

A behaviour change moves what the build produces, and the corpus states what it produced before. Restoring a green run then means restating two hundred fixtures, and the shortest way to do that is to write the build's current output into every fixture a red run names. That turns the build's behaviour into the corpus's truth: a fault the change introduced becomes the fixture that declares it, and the corpus goes green having lost the ability to report the fault.

This record preserves the two tools written while bringing `main` back from that position, in general purpose form. One reports why a fixture differs, separating a run that crashed or returned another exit status from output that drifted, so drift a change intended is read apart from a defect it carried. The other restates a fixture from a run, dry by default, editing only the declared output and the `[expected]` block, and refusing any run that reports an internal error.

The standalone issue raised from this record is [corpus drift triage and expectation restatement](https://github.com/m2ux/prosiform/issues/243).

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Triage](triage.py) | Classifies each fixture's difference, so drift is read before it is accepted |
| [Restatement](regenerate.py) | Rewrites the declared output and `[expected]` block from a run; dry unless `--write` |

## The Problem Each Tool Answers

**Drift is not one thing.** The tools exist because two kinds of red run look alike and must not be treated alike. A build that reports an internal error, or returns an exit status the fixture does not declare, has a fault that no expectation should record. A build whose output moved has drift that an expectation should record. Only the second is a rewrite. Triage reports the first before it compares a single byte, and restatement refuses it outright.

**Rewriting by hand is unreviewable at scale.** The restatement edits two things and copies everything else through. A manifest is not re-rendered, so a non-ASCII clause keeps its em dash, a declaration keeps its order, and the diff a reviewer reads is the expectation and nothing else. Re-rendering the manifest from parsed TOML escaped every em dash in 177 manifests while this record was written.

**Accepting drift blindly removes the corpus's value.** `--only` restricts a rewrite to one category, so a change accepts the drift it intended and leaves every other category for a reader. The dry run is what makes that practical: the set is read before any of it is written.

## Evidence

Both tools ran against the corpus at the revision this record was written, with `PROSIFORM_BUILD` naming the locked build.

| Tool | Result |
| --- | --- |
| `triage.py` | 253 fixtures read, all identical; the one fixture that declares an internal error is read as identical rather than as a fault |
| `regenerate.py` (dry) | 253 fixtures considered, 0 written, 0 refused — a green tree has nothing to restate |
| `regenerate.py`, one stale fixture | Dry run named the fixture and left it stale; `--write` restored it; `git checkout` returned the tree |
| `regenerate.py`, a manifest without `[expected]` | Refused rather than guessed at |

The green-tree dry run is the load-bearing result: the tool that rewrites expectations reports nothing to rewrite when the expectations hold, so it cannot drift the corpus on a run that had nothing to correct.

## What It Reached

Bringing `main` back needed a third reading the tools cannot supply, and it is recorded here because it is the judgement the tools leave to a reader.

| Fixture | What a blind rewrite would have recorded |
| --- | --- |
| `depth-overflow/a-source-heading-the-shift-pushes-past-the-sixth` | The parent is no longer shifted, so the overflow stopped being reachable through it; restating would have declared success for a fixture whose clause is that the run fails |
| `generated-input/a-bundle-offered-as-input` | The fixture's own input still carried the superseded entry paragraph, so the run accepted a bundle; restating would have declared that a published bundle compiles |
| `self-reference/a-section-link-to-its-whole-document` | An internal error that restatement refuses, which is what surfaced the fault rather than the drift |
| `boundary/a-nested-list-and-the-list-below-it` | An internal error from an index the entry paragraph's new position left unguarded |

Each was corrected at its input or at the build before any expectation was restated. The triage categories named three of the four; the crash refusal named the rest.

## Links

| Resource | Link |
| --- | --- |
| Issue | [Corpus Drift Tools](https://github.com/m2ux/prosiform/issues/243) |
| Corpus | [`fixtures/`](https://github.com/m2ux/prosiform/tree/main/fixtures) |
| Runner | [`checks/runner.py`](https://github.com/m2ux/prosiform/tree/main/checks/runner.py) |
