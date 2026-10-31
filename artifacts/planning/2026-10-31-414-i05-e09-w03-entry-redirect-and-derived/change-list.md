# Change List — W03 Entry Redirect and Derived Name

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W03 work item](../2026-10-30-414-i05-e09-mock-substitution/w03.md), its Fixtures table | The record held that the corpus runner always passes `-o`, so a redirected entry's derived name could only be a unit test. The runner names no output folder: `ad0ca74a` replaced the `-o` it used to add with a comparison of the folder a run creates against the declared bundle's name. The derived name is therefore exactly what a fixture states, and `a-redirected-entry-derives-its-name-from-the-substitute` states it rather than the record's weaker version. |
| Folded work | [W03 work item](../2026-10-30-414-i05-e09-mock-substitution/w03.md), its Proposal | The record held that "two entries naming one substitute collide", deriving one name that `derived_output` refuses as multiple distinct selections requiring an explicit `-o`. They do not: `selections` de-duplicates by `(path, fragment)`, both entries give one target, and the run publishes one bundle under the substitute's name at exit `0`. The refusal the record describes exists for two *distinct* selections deriving one name, which is a different case. The bullet now states what they do. |
| Folded work | [W03 work item](../2026-10-30-414-i05-e09-mock-substitution/w03.md), its Fixtures table, `a-redirected-referrer-carries-its-entry` | The record spelled the run `-m guide.md=stand-in.md -f stand-in.md '#run'`, which redirects nothing: `stand-in.md` is not a key, so the referrer resolves to itself and the run warns `W_MOCK_UNUSED` about `guide.md`. The fixture runs `-f guide.md`, so the referrer is the document the key names and the fragment resolves against its substitute. |
| Folded work | [W03 record](../../../README.md), reserved folder | `w03.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Folded work | [W03 work item](../2026-10-30-414-i05-e09-mock-substitution/w03.md), `w03.md` in the reserved folder | The work item states no source change. `entry` already applied the mapping to a positional reference and to `-f` when W01 landed the seam, so the row's delivery is evidence: two fixtures, four unit cases, and the record corrections above. The row's Implementation part now says so rather than implying a change to `cli.py`. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W03` now links pull request [#438](https://github.com/m2ux/prosiform/pull/438) and is ticked done, with `AC2` and `AC13` ticked. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | `src/tests/test_linked_bootstrap.py`, `make smoke` in a sandbox | Both run `uv build --wheel`, which resolves `hatchling` from the network, so both fail in this sandbox and neither fails in continuous integration. Both fail identically on the same base without this branch's change, and neither file is touched by it. Recommend no change: a check that needs the network to build a wheel is not observing a defect when the network is absent. |
| Folded work | The derived name of a run whose two *distinct* selections collide | `docs/bundles.md` states that `a/b.md` and `a_b.md` in one run fail before anything is written. They do not: the run exits `0` and publishes `a_b+a_b.bundles/a_b+a_b.bundle.md`, because the entry is one bundle join-named from both selections and `publication`'s name check runs across bundles, not across selections. The design's own "Combined selection" row states the opposite of the guide. Deferred as [#441](https://github.com/m2ux/prosiform/issues/441): it reproduces with no mapping at all, so it is neither caused by nor fixed by this row, and settling it decides which of the guide and the design is the authority. Placement is open — no epic carries it, and a new initiative is outside this session's allowance. |
| Folded work | `W_MOCK_SUBSTITUTED` with no `location` for a redirected entry | A positional entry and `-f` stand in no source, so `substituted` emits the substitution with `location` absent. Both of this row's fixtures declare the warning without a location, which is what the build does; AC7's "naming the link's location" is a statement about a redirected *link*, which has one. No change is needed, and the recording is here so a later reader does not read the absent field as a gap. |

## No change

- **The seam.** `entry` applies the mapping to a positional reference and to `-f`, and `execute` derives the run's folder and bundle name from the references it returned. Both statements are W01's, and this row adds no caller.
- **The scope of `-o`.** It names the folder the run's own folder stands in and nothing about the name, which is why the derived name follows the substitute under it.
- **The mapping's shape and the lookup.** Neither the keys, the two-step precedence nor the record changed here.
- **The fixture names.** `a-redirected-entry-derives-its-name-from-the-substitute` and `a-redirected-referrer-carries-its-entry` are the names `fixtures.md` and the epic give, and neither changed.
- **The independent row pairs.** `joins.md` states that W03 takes separate pull requests from W04, W05, W06, W07, W08 and W10, and this row is W03 alone.
- **The design clause.** Every manifest declares `Link classification and resource handling — The substitution mapping`, byte-identical at the pin `827b66fc`.
