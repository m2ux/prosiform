# W08 Validation

## Tested Revision

Task head: `1cc499063effd0f3995bc1dd757f078ddaae8c34`, based on `d0444a092cd1c7ddfc27d0994578811748bd35ac` (`i10/e07/main`). The worktree is clean. The change consists of the existing 40-case source test and four exact-output corpus fixtures; no production implementation changed.

## Published Command Parity

Pass: 40 cases, independently repeated in a detached checkout at the corrected final head through `revision-check.py` and `uv run --project src --frozen pytest src/tests/test_deferred_presets.py`.

The compiler publishes the deferred link first. The test parses that actual output, obtains its rebased destination and decoded title, builds shell-safe command words from those values, and executes that later command. Its payload is compared against immediate compilation of the same authored occurrence. Inline/reference-style links and plain/composition deferral cover unrelated/preset-word headings, Unicode fragments and filenames with spaces, absent/empty/unknown tags, multiword preset names, repetition, case and Unicode whitespace. Meaningful selections produce cached and reviewed payloads and a qualified bundle identity; the same command without tags produces live and draft payloads. This observes AC17 and AC18 rather than only comparing title strings.

## Publication Corpus

Pass: 537 fixtures, 537 pass, 0 fail, 0 awaited, 0 unexpected pass, using the configured external build at the corrected final head, independently repeated in a detached checkout through `revision-check.py`. Four dedicated fixtures cover rebased reference-style deferral, generated deferred activation, immediate selected composition and the prescribed later command. The immediate and activated expected bundles carry the same cached and reviewed payloads. Each manifest declares the design clauses it observes.

## Repository Checks

The sandboxed `make check` initially stopped on 13 wheel-installation setup errors: the sandbox deliberately has no network and Hatchling resolution needed PyPI. Its other 1,888 source tests passed. No test assertion failed in that run.

The network-enabled configured `make check` at the previous head passed all 1,901 source tests, all 1,634 deterministic harness tests, lint, formatting, type checking and lock verification. That run also passed the corpus, installed-wheel smoke, layout, tables, online links, vocabulary and invocation, but conformance rejected one new manifest declaration, `CLI contract — Automatic output names`, which is not a design clause. The final commit removes that incorrect declaration and retains the fixture's three applicable clauses. Focused conformance and independence checks pass with zero declarations naming no clause. The complete final-head `make check` passed (exit 0): 1,901 source tests, 1,634 deterministic harness tests, 537/537 corpus fixtures, installed-wheel smoke, lock, lint, formatting, type checking, layout, tables, online links, vocabulary, invocation, conformance and independence. The build configuration is `PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w08-deferred-links-retain-their/src --frozen pf'`. No paid evaluation session is started by this target.

## Review

The generated deferred line retains the original decoded title and uses the invocation-relative destination. The activated command fixture uses that destination/title list. The immediate/activated output wrappers differ because their entry documents differ; the selected content agrees. The source tests assert this content and also the default-selection negative control. Existing compiler behavior satisfies both criteria without a production repair.

## Delivery

[Task pull request](https://github.com/m2ux/prosiform/pull/671) targets `i10/e07/main`. The user explicitly confirmed the repository's auto-close setting is disabled for this session. No setting was changed. Merge and criterion recording await complete validation.

## Plan Changes

None applied or held. No arising issue or deferred debt identified.
