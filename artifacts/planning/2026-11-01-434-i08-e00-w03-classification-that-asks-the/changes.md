# Plan Changes

- **Folded work, applied** — W03 declares every corpus fixture whose targets the run compiles, the diagram-following eval workflows and the unit-test trees. Asking the target turns every undeclared link into text, so `make check` cannot pass on W03 without it; the work is blocking and [W07](https://github.com/m2ux/prosiform/issues/434)'s AC12 keeps the root-family rework, renames and the `real-source/` declaration it plans.
- **Folded work, applied** — `parser-limit/a-nesting-ceiling-the-last-valid-reference-reaches` and `parser-limit/a-reference-lookup-the-parser-declines` move from `-N 1` to `-N 2` with one more bracket: a `prosiform` mapping is YAML depth 2, so no document declares under `-N 1`.
- **Design decision, applied** — `Reference.declared`, which the epic plan's W03 item proposed, is not added: one per-bundle `Declarations` record answers by path for every stage. The epic plan's `a-w03.md` is superseded by this record's [W03](w03.md).
