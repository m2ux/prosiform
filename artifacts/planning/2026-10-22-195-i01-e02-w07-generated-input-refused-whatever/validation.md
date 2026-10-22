# Validation

## Revision and decision

Build revision: 4165f5c4be3491f9ef650afba897f721744279aa. Design revision: d98abb8 on engineering. The complete opening entry declaration is reserved as the output signal. Path spelling and file versus merged grouping do not participate. An authored document copying the reserved declaration is detected; code and quoted examples remain valid. Modified derivatives are outside the stated guarantee.

## Source admission and reuse

The source-admission integration cases build and reuse actual output over lower-case and mixed-case directories, with both file and merged groups. All four reuse runs fail with E_GENERATED_INPUT and empty stdout. Negative cases accept fenced examples, quoted declarations, declarations after a heading, plain prose without links and external-link prose. A selected later section still triggers detection, and frontmatter preserves the original diagnostic line (line 5).

## Corpus

The configured CLI ran all 251 fixtures: 251 pass, 0 fail, 0 awaited. Lower-case and mixed-case bundle fixtures are refused; an authored title naming a sibling bundles. The existing suffix-collision fixture and own-name title fixture pass. Code examples carry the entry declaration without refusal. Observes epic AC9 and task AC1/AC2.

Command: checks/corpus.py with PROSIFORM_BUILD naming the installed console entry point and PYTHONPATH naming this worktree's src. The interpreter and console script come from the existing w04 locked environment; source selection is explicitly this worktree.

## Unit and harness suites

pytest --config-file src/pyproject.toml --rootdir . src/tests checks/tests: 1360 passed, 1 skipped, 9.34 seconds. PATH exposes the installed console entry point and PYTHONPATH selects this revision. The skip is pre-existing. The obsolete heading probe and its helper-only tests are removed; regression coverage is at actual source admission and published-output reuse.

## Static checks

ruff check: pass. ruff format --check: 54 files already formatted. mypy: no issues in 53 source files. git diff --check: pass.

## Contract checks

checks/conformance.py and checks/independence.py both pass against the published engineering design. All 251 fixture declarations use the contract vocabulary.

## Remote checks

GitHub Checks is running for this head: https://github.com/m2ux/prosiform/actions/runs/39738407786. Its result is recorded before merge.

## Delivery limits

The user authorized CLI delivery using recorded issue/PR link evidence. The complete Development field is unavailable through the CLI and was not represented as verified. Auto-close is confirmed disabled. The target branch reports protected=false and protection.enabled=false; the administrator's protection and rules endpoints report the features unavailable on this private repository's plan.
