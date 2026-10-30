# Change List — W01 Mapping, Option and Identity

> Plan changes · Created 2026-10-30

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md), [W09 work item](../2026-10-30-414-i05-e09-mock-substitution/w09.md) | The `-m, --mock` row in `invocation.md` moves from W09 to W01. `checks/invocation.py` compares the documented table with the build's help output in both directions, so an option the command offers and no table names fails `make invocation`, which `make check` runs. W09 keeps the classification detail in `docs/references.md` and the row's review. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | The `CLI contract` row for the option lands in the design on `engineering` at `9f58475d`, which `README.md` pins. `make conformance` reads each option row there as a clause, so the row is required for the declaration the three fixtures make. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | The fixture table's `a-mocked-dependency-is-compiled` row is corrected: it declared a `W_MOCK_SUBSTITUTED` diagnostic, which W04 owns and whose code the schema's warning catalogue cannot carry before that row lands. The row now declares no diagnostic, and the substitution warning is W04's. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | `w01.md`'s `entry` paragraph is corrected on the ordering, not only on the path: the mapping applies to the reference `entry` returns, after `resolve` has normalized it, which is what "after the root check" states for `inside`. The page wrote only that `entry` takes the mapping. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | The Work Breakdown's Implementation part names `bundle`, `grouping`, `candidate` and `dispatch` as well as `closure` and `cli`. A parameter held only at discovery emits the authored target and fails candidate validation against the mocked one, because emission and validation resolve each link again. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | An `## Additions from review` table records the two findings the plan could not state: that `-m` is a value-taking option in `diagnostic_format`, and that the mapping is threaded past the stages that resolve a link a second and third time. |
| Folded work | [W01 record](../../../README.md), reserved folder | `w01.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W01` now links pull request [#428](https://github.com/m2ux/prosiform/pull/428) and is ticked done, with `AC1`, `AC11` and `AC18` ticked. |
    20|
## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | [W02 work item](../2026-10-30-414-i05-e09-mock-substitution/w02.md), `AC9`, `AC10`, `AC23` | All three refusals are absent from the build at this branch head. `-m rules.md=a.md -m ./rules.md=b.md` exits `0`, and so does `-m rules.md=./rules.md`; two keys of one identity silently keep the last, and a self-mock reads as a substitution that took effect. A fragment-only key resolves to an empty path and redirects nothing, equally silently. The seam this row lands is what makes all three observable, and building the refusals here would be W02's work under another number. Recommend leaving `AC9`, `AC10` and `AC23` unticked until W02 lands. |
| Folded work | [W04 work item](../2026-10-30-414-i05-e09-mock-substitution/w04.md), `W_MOCK_SUBSTITUTED` | The substitution warning is W04's, and `fixtures/manifest.schema.json`'s warning catalogue cannot carry the code before that row adds it. `fixtures.md` requires both warning codes to have a fixture, which W04 lands. The original W01 fixture table declared `W_MOCK_SUBSTITUTED` on `a-mocked-dependency-is-compiled`; that declaration could not validate, so the fixture declares no diagnostic. Recommend W04 adds the code to the design, the schema and a fixture together. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414), `W03` | `entry` now applies the mapping, so a redirected positional entry compiles the substitute and the run derives its name from it — `AC2`'s second half, observed as `stand-in.bundles/stand-in.bundle.md`. The first half, that an explicit `-o` writes the name the caller gave, already holds, and `AC13`'s `-f` redirect holds through the same `entry` call. The fixtures are W03's to land, and this row does not claim the criteria. Recommend W03 writes its manifests against the pinned build rather than restating the seam. |
| Folded work | `docs/references.md`, the matching rule | `w09.md` names this page as the matching rule's home and says the guide keeps the one-line form. This session added the rule to `docs/references.md`, because the page is where the guide already sends a reader for classification and the option would otherwise be undocumented on it. W09 now owns the `invocation.md` row's review and the guide's one-line form. Recommend W09 re-reads its row rather than adding the rule a second time. |

## No change

- **The design's clause.** `Link classification and resource handling — The substitution mapping` is what every mock fixture declares, at `f723a85d`. This session added no clause to it; the only design change is the `CLI contract` row at `9f58475d`.
- **The mapping's shape.** An immutable value with one lookup, exact `(path, fragment)` then `(path, None)`, is what the row states and what landed. No variant was tried.
- **`-m`, `--mock`.** The name and both spellings are the user's decision recorded in the epic's record, and the option reproduces them.
- **The three fixture names.** Each is the one `fixtures.md` and the epic name. No fixture was renamed.
- **The independent row pairs.** `joins.md` states which rows take separate pull requests, and this row's neighbours are unchanged.
