# Change List — W07 Substitute as a Full Source

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W07 work item](../2026-10-30-414-i05-e09-mock-substitution/w07.md), Fixtures table | The AC5 fixture's scene is stated as the record's own Fixtures table states it — `guide.md` links `notes.md` as well as `rules.md` — so both declared members are reached through a reference in the closure rather than one arriving as a positional entry. A member pulled in only by the command line could be read as a merge the invocation asked for rather than one the substitute's declaration caused. |
| Folded work | [W07 work item](../2026-10-30-414-i05-e09-mock-substitution/w07.md), Fixtures table | The AC6 fixture's outside link is written `../outside.md` from `stand-in/entry.md`, which lands on `source/outside.md` inside the fixture's tree, rather than the record's `../../outside.md` above the tree. Both are citations; the nearer one keeps the tree inside the fixture's own `source/`, so the fixture reads as one tree and the working directory the runner names is the only thing above it. |
| Folded work | [W07 work item](../2026-10-30-414-i05-e09-mock-substitution/w07.md), Test row | The row's "a substitute reached by two routes and a depth conflict naming the substitute" is stated as the four cases the pull request carries, adding a metadata failure located on the substitute and a parent-segment substitute reading its own settings. The first is what says the substitute's own bytes are validated rather than the authored target's; the second is AC20's statement, which the row's Coverage names and its Test row did not. |
| Folded work | [W07 work item](../2026-10-30-414-i05-e09-mock-substitution/w07.md), `## Additions from review` | The reserved folder's work item gains the two findings the plan could not state: that each fixture must be discriminating rather than a regression, with the counterfactual recorded outside the corpus because a manifest declares one invocation; and that AC20 is a unit case rather than a third fixture, as the epic's `fixtures.md` already records. |
| Folded work | [W07 record](../../../README.md), reserved folder | `w07.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W07` now links pull request [#439](https://github.com/m2ux/prosiform/pull/439) and is ticked done, with `AC5`, `AC6` and `AC20` ticked. |
| Folded work | `src/prosiform/metadata.py`, `src/tests/test_mock.py` | The two commits hold the component's statement and its cases apart from the fixtures, so the branch records the design statement and the corpus proof as distinct pieces of work. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | `checks/conformance.py`, clauses from paragraphs | `Conversion metadata — Source ownership` is a bold-led bullet and is addressable; the prose that states a substitution is the target outright is inside `Link classification and resource handling — The substitution mapping`, which is already a clause. Nothing new is needed here, and no paragraph was turned into a bullet for a fixture's convenience. |
| Folded work | [W08 work item](../2026-10-30-414-i05-e09-mock-substitution/w08.md), the example skill's scenarios | W08's two scenarios bundle the example tree against a stub. Neither depends on a substitute's own group or root: the stub stands where a heading stood, and the fake `gh` is a redirected reference rather than a redirected group member. No change to W08 follows from this row. Recommend W08 reads its scenarios' expectations from W04's warning fields, as W04's record already advises, and takes nothing from here. |
| Folded work | `docs/references.md`, the substitute paragraph | The page already states that the substitute's title, group and depth, root and links are the ones the run uses. This row states the same fact on the component that decides it and pins it with fixtures; the page needs no edit, and a second statement of one rule in two places is what the workspace's prose rule forbids. Recommend no change. |
| Folded work | `fixtures/mock/a-substitute-outside-the-writing-root-is-reachable`, AC20 | The epic's `fixtures.md` and the epic body both attach AC20 to that fixture, which W01 landed. This row states the capability against it and adds a unit case; it adds no third fixture and does not re-open the fixture. Recommend no change. |
| Folded work | `src/tests/test_linked_bootstrap.py` in a sandbox | It runs `uv build --wheel` and needs network the delivery sandbox denies. It fails identically on the predecessor worktree at the same base, so it is not this row's change. Recommend no change: a check that cannot run in a sandbox is not a defect in it. |

## No change

- **The component's behaviour.** `read_document` already captures the substitute's bytes and derives its settings and root from them, because the mapping normalizes the reference before the read. This row states that on `metadata.Conversion` and pins it; it adds no branch, no parameter and no second reader.
- **The mapping's shape and the lookup.** `Substitution.substitute` returns the substitute's `Reference` whole. Neither the keys, the lookup nor its precedence changed.
- **The design and its pin.** The clause this row's fixtures declare is byte-identical at `827b66fc`, and `README.md` names no other revision after this row.
- **The independent row pairs.** `joins.md` states that W06, W07 and W08 take separate pull requests, and this row touches none of their components: `metadata.py` here, `closure.py` at W06 and `checks/mock_scenarios.py` at W08.
