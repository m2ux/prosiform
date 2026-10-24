# A Second Operator Validation

## Revision

Task branch `i01/e09/w01-a-second-operator-and`, head `e86252664afe89fa34be3ad2f0f90687a59ca04d`, targets `i01/e09/main` at `4c612b92`. The tracked working tree is clean. The design branch `i01/e09/w01-a-second-operator-and-engineering` carries `9f693a02`.

## The Operator

AC1, AC2, AC6 and AC8 are observed by seven `dispatch` fixtures and closed over the unit suite's operator, destination and refusal tests.

A link whose text opens with `»` is withheld from this run exactly as one opening with `¬` is: the target contributes no content, adds no dependency through the link and adds no group membership, and the bundle publishes the link's text with its mark as its author wrote it. The destination is the target's URI-escaped path from the captured invocation working directory with the resolved fragment retained, which `rebased` already produces for a deferred link, so the operator adds no destination rule of its own.

The two marks are read by one function over the operators a link's text opens with. Classification and target requirements are unchanged for `¬`, and `deferred` and `dispatched` answer separately so each mark is told from the other wherever the bundle publishes it. Text opening with both is refused under `E_UNSUPPORTED_CONSTRUCT` naming the link, because one compilation cannot wait for a later run and be dispatched by this one; the refusal is raised while the run reads the source, so it is a source fault rather than a metadata one.

## The Metadata And Its Emission

AC3, AC4, AC5 and AC7 are observed by `dispatch/a-declared-dispatch-text-opens-the-bundle`, `dispatch/two-dispatch-declarations-disagree`, `dispatch/an-unknown-prosiform-key-still-fails` and `dispatch/a-metadata-field-carries-no-dispatch`.

`prosiform.dispatch` is a nonblank, printable, single-line string the compiler assigns no structure to. The entry document's text is emitted after the entry sentence in the same paragraph, so a reader meets the rule that governs the marked links and the entries as one instruction. The text is escaped as literal text, so an author's own punctuation reaches the bundle as written.

Every contributing source declaring the key states the same value. A second value fails with `E_INVALID_CONVERSION_METADATA` naming both locations and publishes nothing. The first declaration is chosen by the order the bundle arranges its groups by rather than by traversal order, so the instruction is a property of the documents rather than of the route taken to them. `metadata` remains without conversion meaning, and `dispatch` joins `root`, `group`, `group-depth` and `group-heading` as the only admitted keys.

## Composition With The Entry Line

The entry sentence is emitted where the parent's preamble places it rather than at the head, and the dispatch text joins that one paragraph. `is_entry_line` reads the sentence from where the paragraph opens with it to a closing that ends the paragraph or precedes the space the text after it is joined by, so a generated bundle is recognized as one after its declaration is read back. The unit suite asserts the composed paragraph reaches the bundle at the slot the sentence occupies.

## Full Checks

`PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01-e09-w01/src --frozen pf' make check` passes at the task head, exit status zero. See [full-check.log](full-check.log).

- Source tests: 1093 passed.
- Check-harness tests: 626 passed.
- Corpus: 260 passed, zero failures or awaited fixtures. The epic base held 253; this unit adds seven.
- Lock, lint, formatting, strict typing, layout, tables, online links, vocabulary, invocation, conformance, independence and the installed-wheel smoke all pass.

Fixture expectations were produced by running the build, not written by hand: `scripts/regenerate.py` rewrote each of the seven from the configured build's own stdout, exit status and diagnostics. Its `DECLARED` tuple carries `reference`, `resolved`, `source` and `chain` and not `message_contains`, so the three diagnostics whose wording is asserted had that assertion restored from the run's captured JSON output. The corpus holds the restored assertions.

The conformance report names 305 clauses, 55 covered by no fixture, 16 clauses with no run and three installation claims not observed by a run. Those are explicit coverage gaps rather than passing assertions; none is a clause this unit states.

## Review And Plan Changes

The corpus vocabulary admits `disagree`, which the two-declaration fixture's description states and the contract's own vocabulary does not. The design carries the operator's clauses, the glossary defines the dispatch operator and the dispatch text, and the invocation guide names the admitted key and the emission. The README's design link moves to the engineering branch's commit, which is where the contract is read.

No blocking validation finding survived in this unit. No arising issue was identified.

## Delivery

Pending task pull request publication and verified merge. The pull request for this branch targets `i01/e09/main`; the design branch raises its own against `i01/e09/engineering`. Both link #239 through the Development field.
