# Validation

Evidence for each check the [work item](w11.md) names, run in the unit's worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 closure tests

`make test` passes (1410 tests). `test_closure.py`: `../outside.md` from the working directory keeps its parent segments; `skills/plan/guide.md` naming `../../../shared/conventions.md` resolves to `../shared/conventions.md`; a declaring target above is a dependency of `bundled` and a withheld target of `withholding_target` (AC21); the boundary of a single path above is `..`, and paths climbing different distances give the furthest climb.

## T2 linked bootstrap

`test_linked_bootstrap.py::test_a_declaring_link_above_the_invocation_directory_is_compiled` passes: run from `skills/`, each skill target compiles its declaring leaf above the working directory, and no `../../../` destination survives in the bundle (AC21).

## T3 corpus

`make corpus`: 386 fixtures pass, 0 fail. `inclusion/a-declaring-target-above-the-working-directory-is-compiled` compiles `../shared/conventions.md` and rewrites the link to `#conventions` (AC21).

## T4 full check

`make check` exits 0 before opening.
