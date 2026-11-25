# Bundler Term

## Executive Summary

The product is named a bundler: the README headline, the package metadata, the supporting tools and the contract design use the noun the glossary's own verb implies, and the glossary records "compiler" as a term deliberately not used. A run's emitted bytes are untouched, so the change is a patch under the versioning rules.

The hot-fix is proposed and not yet registered. Its delivery branch is `f38-bundler-term`, cut from `main` at 684437c06 (0.34.0), with a pull request targeting `main`. The number F38 follows F37, issue #846, and holds until the issue is raised.

## Scope

Measured on `main` at 684437c06 with a case-insensitive search.

| Area | Files | What changes |
| --- | --- | --- |
| Product description | `README.md`, `src/pyproject.toml`, `src/prosiform/__init__.py` | The headline, package description and package docstring. |
| Documentation prose | `docs/glossary.md`, `docs/diagram-renderer.md`, `docs/output-budget.md`, `checks.md`, `checks/README.md` | Sentences naming the tool, and the avoided-terms row the glossary gains. |
| Eval prose and docstrings | `evals/diagram-following/README.md`, `RUNBOOK.md`, `score.py` | Sentences naming the tool. Class names are out of scope. |
| Identifiers | `scripts/render-diagram.py`, `scripts/render-example.py`, `src/tests/test_linked_bootstrap.py`, `src/tests/test_diagram_renderer.py` | Card title, option help, error messages, the `compiler_branch` and `compiler_revision` record keys, and the `compiler.json` artifact. |
| Test names and sample text | `checks/tests/test_authoring.py`, `checks/tests/test_vocabulary.py`, `evals/diagram-following/test_score.py`, `test_run.py`, `test_workflow.py` | Function names, docstrings and the sample design the vocabulary test reads. |
| Fixture description | `fixtures/headings/an-authored-heading-beside-a-generated-one/manifest.toml` | The `description` string, which no outcome reads. |
| Contract design | `artifacts/planning/2026-10-17-prosiform-v1/design.md` on `engineering` | Three statements, then the shipped links re-pinned to the revised revision. |

The noun occurs 69 times in 21 files on `main`. No occurrence is in `src/prosiform/cli.py` or any other module that emits output, and no image under `docs/images` holds the word, so no fixture outcome and no rendered example changes.

## Out of Scope

- **The verb.** "Compile" and its forms occur about 1,600 times, in the guide `pf` prints, the documentation, the fixtures and the eval. The guide is emitted output, and the eval's `compiled` form and `overcompiled`, `uncompiled` and `misordered_compile` classes are recorded in committed baselines. Replacing the verb is a contract change that needs a feature of its own.
- **Historical records.** Planning folders, run records and review artifacts on `engineering` keep the wording they were written with, the `compiler_branch` and `compiler_revision` keys of earlier run records among them.
- **Consuming skills.** Skills in other repositories that describe prosiform follow in their own repositories.

## Tasks

- [ ] Confirm scope and register F38 from [proposed-hotfix.md](proposed-hotfix.md) on board 18.
- [ ] Revise the three design statements on `engineering` and record the revision to pin.
- [ ] Cut `f38-bundler-term` from `main` in a worktree.
- [ ] Rename the product description and documentation prose, and add the avoided-terms row.
- [ ] Rename the renderer and test identifiers, with their tests.
- [ ] Rename the eval prose, docstrings and test names.
- [ ] Re-pin the shipped links to the revised design.
- [ ] Run the case-insensitive search, the previous contract tag's corpus against the build, and `make check`.
- [ ] Open the pull request to `main`, link it to F38 through Development, and verify each criterion at the merge revision.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [proposed-hotfix.md](proposed-hotfix.md) | Proposed body of F38, with its acceptance criteria. |

## Open Decisions

| Decision | Recommendation |
| --- | --- |
| Whether the verb follows in a later feature | Raise it separately after this lands; it moves the contract minor. |
| Whether the design changes in this hot-fix | Yes: the glossary and the design carry one vocabulary, so both change together. |
| Whether identifiers and record keys are renamed | Yes: a surviving `compiler.json` or `compiler_revision` reads as current fact. |
| Whether a release is cut for it | No: it ships in the next release as a build patch, 0.34.1, unless a contract change lands first. |

## Links

- [Contract design](../2026-10-17-prosiform-v1/design.md)
- [Previous hot-fix record](../2026-11-22-dispatch-section-labels/README.md)
