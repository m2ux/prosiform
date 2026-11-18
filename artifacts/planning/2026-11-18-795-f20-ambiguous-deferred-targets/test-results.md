# Test Results

Results for F20 at `5c310fbaf` on `f20-ambiguous-deferred-targets`, run on 2026-11-18 in the unit checkout.

## T1 Deferred Shared Fragment

`fixtures/composition/a-deferred-directive-in-composed-content-naming-a-shared-fragment-is-refused`: the guide composes the Given section of `stage.md`, which writes `[¬↳ Later](later.md#later)`, and `later.md` holds `# Later` and `## Later`. The run fails with `E_AMBIGUOUS_SOURCE_HEADING` and exit status 1, naming the reference `later.md#later`, the resolved document `later.md`, the source `stage.md:8` and the chain `guide.md`, `stage.md#given`, `later.md#later`, and publishes nothing. The build of `origin/main` at `97a462b5c` exits 4 with `E_UNEXPECTED_INTERNAL_ERROR`. Held.

## T2 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lint, format, typecheck, `make test` (2245 passed), harness (1079 passed), corpus (640 fixtures, 640 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T3 Pick Remedy

In `test_cli.py`:

- `test_an_entry_carrying_no_pick_token_is_refused_with_a_remedy_the_run_accepts`: for the plain-path entries `work-kind.md` and `guide.md`, the remedy names the alternative in the title of each link reaching the document; `--pick epic` beside each is refused with exit status 2, and the run compiles once the link names `epic`.
- `test_a_pick_naming_no_alternative_is_refused_with_a_rerun_remedy`: a `?` entry run with `--pick bogus` or `--pick checks` keeps the rerun remedy, and `--pick epic` compiles.
- `test_a_pick_after_the_listing_compiles_the_named_alternative`: a `?` entry run with no `--pick` names the rerun remedy, and the rerun compiles.

In `test_selection.py`, `test_the_unresolved_failure_lists_each_alternative_beside_its_choice_line` holds each remedy to its case. On `origin/main` at `97a462b5c`, `pf guide.md` in `fixtures/inclusion/no-pick-of-an-alternative-fails/source` names the `--pick` rerun, and `pf --pick epic guide.md` exits 2 with `E_INVALID_USAGE`. Held.

## T4 Deferred Container-Carried Target

`fixtures/composition/a-deferred-directive-naming-a-heading-a-container-carries-is-refused`: `[¬↳ Inner](notes.md#inner)`, where `## Inner` stands in a block quote, fails with `E_NESTED_SECTION_TARGET` and exit status 1, naming the reference, the resolved document `notes.md`, the source `guide.md:8` and the chain, and publishes nothing. The build of `origin/main` at `97a462b5c` exits 4 with `E_UNEXPECTED_INTERNAL_ERROR`. Held.

## T5 Fragment Before Pick

`fixtures/composition/a-directive-naming-a-shared-fragment-and-two-alternatives-reports-the-fragment`: `[↳ Dup](stage.md#dup "alpha, beta")`, where two headings of `stage.md` take the slug `dup` and the title picks both of its alternatives, fails with `E_AMBIGUOUS_SOURCE_HEADING` and exit status 1, naming the reference, the resolved document `stage.md`, the source `guide.md:8` and the chain, and publishes nothing. The build of `origin/main` at `97a462b5c` exits 2 with `E_ALTERNATIVE_UNRESOLVED`. Held.
