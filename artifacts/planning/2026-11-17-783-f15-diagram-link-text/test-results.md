# Test Results

Results for F15 at `283759970` on `f15-diagram-link-text`, run on 2026-11-17 in the unit checkout, with `PROSIFORM_BUILD` naming the worktree's `pf` and `origin/engineering` at `ee7c9a78f`.

## T1 Element Text Operator

`make corpus` passes each fixture whose click names a node whose text opens with an operator mark, the tooltip carrying none:

- `fixtures/dispatch/a-click-on-a-node-whose-text-opens-with-the-dispatch-mark-dispatches`: `Intake[⇉ Intake]` beside `click Intake href "intake.md"` compiles `intake.bundle.md` and points the click at it.
- `fixtures/deferral/a-click-on-a-node-whose-text-opens-with-the-deferral-mark-defers`, `fixtures/composition/a-click-on-a-node-whose-text-opens-with-the-composition-mark-composes`, `fixtures/parallel-dispatch/a-click-on-a-node-whose-text-opens-with-the-parallel-mark-joins-its-set` and `fixtures/composition/a-deferring-composing-click-carrying-no-tooltip-publishes-no-title` defer, compose, join the set and defer a composition as the same marks opening a link's text do.
- `fixtures/dispatch/a-click-on-a-node-whose-text-opens-with-a-mark-against-text-is-an-ordinary-link`: `Intake[⇉Intake]` opens no operator.

Each was a tooltip-operator fixture, reworked with the marks moved into the node text. Held.

## T2 Tooltip as Title

`make corpus` passes `fixtures/dispatch/a-dispatching-click-s-tooltip-tags-select-its-bundle-s-presets`, where `Intake[⇉ Intake]` beside the tooltip `"checks"` dispatches under `checks`, and `fixtures/dispatch/a-click-tooltip-opening-with-a-mark-states-no-operator`, where `Intake[Intake]` beside the tooltip `"⇉ checks"` is an ordinary link: the target is bundled inline, its `checks` preset unselected (`W_PRESET_UNUSED`), the tooltip carried as written. `fixtures/deferral/a-deferring-click-tooltip-carries-the-pick-token` and `fixtures/cli/a-click-line-entry-selects-presets-by-its-tooltip` carry `?` and `Checks` as whole tooltips. Held.

## T3 Refused Combinations

`make corpus` passes each refusal with `E_UNSUPPORTED_CONSTRUCT`, exit status 1, naming the click by keyword and node at the click's line:

- `fixtures/dispatch/a-click-on-a-node-whose-text-writes-a-blank-between-the-deferral-and-dispatch-marks-is-refused` (`¬ ⇉`)
- `fixtures/deferral/a-click-on-a-node-whose-text-writes-the-deferral-mark-against-the-dispatch-mark-is-refused` (`¬⇉`)
- `fixtures/dispatch/a-click-on-a-node-whose-text-writes-the-dispatch-mark-against-the-composition-mark-is-refused` (`⇉↳`)
- `fixtures/composition/a-click-on-a-node-whose-text-writes-the-parallel-mark-against-the-composition-mark-is-refused` (`⫽↳`)
- `fixtures/parallel-dispatch/a-click-on-a-node-whose-text-opens-with-two-dispatch-marks-is-refused` (`⇉⫽`)
- `fixtures/composition/a-composing-click-naming-a-whole-document-is-refused` and `fixtures/dispatch/a-dispatching-click-naming-a-document-that-declares-nothing-is-refused`, the operator's target refusals.

Held.

## T4 One Link per Element

`make corpus` passes `fixtures/reference/a-second-click-on-one-node-is-refused` and `fixtures/reference/a-second-class-diagram-link-on-one-class-is-refused`: each fails with `E_UNSUPPORTED_CONSTRUCT`, exit status 1, the diagnostic's source the second line (`guide.md:10`) and its message naming the earlier (`guide.md:9`), the second class link naming a remote address. Held.

## T5 Elements Drawn Without Text

The design's **Examples** under Link classification states that a class diagram `link`, and a `click` in a class diagram, read the class's declared label, that a class declaring none and a node no shape gives text carry no operator, and that an element of any other diagram is read for none. `make corpus` passes `fixtures/reference/a-class-diagram-link-reads-its-class-label-and-a-class-with-none-carries-no-operator`: `class Intake["⇉ Intake"]` dispatches, and `class Rules` with no label is bundled inline. Mermaid 11.17.2, rendered with mermaid-cli, draws `class Judge["⇉ Judge"]` with its label, a node with no text as its id, a node's last text, and keeps the last `click` or `link` of a node or class. Held.

## T6 Reader Unit Tests

- `test_source.py`: a node's text read from every flowchart shape, quoted and Markdown strings and `@{…}` labels among them, past edge text and quoted strings; a class's label; no text for a node with none, a class with no label, another diagram's element and a dashed id ending in the node's name; the last text winning; a tooltip read whole as the title with no operator; node marks accepted and refused as a link's text marks; a second link on one element read as repeated, and distinct elements and menu entries not.
- `test_cli.py`: a tooltip's marks stating no operator, a class label dispatching, a second click and a second class link refused naming both lines; the click tests rewritten to node text.
- `test_candidate.py`: a bundle changing a click's node text or tooltip fails validation.
- `test_stub_presets.py`: a deferring click carrying no tooltip, an empty tooltip and a link target gains the run's names as a tooltip.

Held.

## T7 Documented Rule

A reading of `docs/references.md` (Operators, Selection by reference, Diagram links) and the design (**Examples** and **Selection belongs to the link**, Link entries, the fixture rows) states the element text as the link text, the tooltip as the title and one link per element. `grep -rni tooltip` over `docs/`, `README.md`, `invocation.md`, the design and `src/prosiform` finds no statement that a tooltip carries an operator. Held.

## T8 Full Check

`make check` exits 0: lint, format, typecheck, `make test` (2221 passed), harness (1075 passed), corpus (636 fixtures, 636 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
