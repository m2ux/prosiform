# Change list

Every change this delivery session made to the plan, and every change it held for the user. The session's allowance covered task creation, epic creation, migration, re-prioritisation and folded work; a new initiative is outside it.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Task creation | [#185](https://github.com/m2ux/prosiform/issues/185) `[I00:E11:W38] A Build Word the Design States in Lower Case` | Raised as a task issue and hoisted into epic [#39](https://github.com/m2ux/prosiform/issues/39) as row W38, depending on W34, with AC43 added to the epic's criteria. |
| Task creation | [#186](https://github.com/m2ux/prosiform/issues/186) `[I00:E11:W39] An Avoided Term in a Corpus Declaration` | Raised as a task issue and hoisted into epic [#39](https://github.com/m2ux/prosiform/issues/39) as row W39, depending on W34, with AC44 added to the epic's criteria. |
| Folded work | Epic [#39](https://github.com/m2ux/prosiform/issues/39), criteria AC43 and AC44 | Added to the epic the two deferred rows cover, so each row's Coverage names a criterion the epic states. |
| Re-prioritisation | Board [Bundling](https://github.com/users/m2ux/projects/18), items for #185 and #186 | Added at Backlog, which is where a row with no started delivery sits. |
| Re-prioritisation | Board [Bundling](https://github.com/users/m2ux/projects/18), item for [#172](https://github.com/m2ux/prosiform/issues/172) | Set to Done on the task merge; the epic stays In Progress while W36 and W37 are open. |

## Held

Nothing. No change this session met fell outside the allowance, and no work it found needs an initiative of its own.

## What the deferred items are

- **W38 — a build word the design states in lower case.** The design's status and parser sections name the builds that implement the contract, so `crate` is a word the design states and the corpus's vocabulary admits it. It is the one term of the retired inventory's sixty that the positive rule does not report. The fix reads the vocabulary from the design's contract text rather than from the sections the conformance report already records as stating no behaviour, which is non-trivial and changes a second check's reading.
- **W39 — an avoided term in a corpus declaration.** The glossary names six terms as deliberately not used, and nothing holds a fixture declaration to that table; the design's ordinary prose admits `include` and `branches`. The fix reports an avoided term with the reason the glossary gives and rewords the declaration that states one, which is work of its own rather than a correction to this rule.
