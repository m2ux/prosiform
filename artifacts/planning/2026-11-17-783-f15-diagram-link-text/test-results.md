# Test Results

Results for F15 at `64c354307` on `f15-diagram-link-text`, run on 2026-11-17 in the unit checkout, with `PROSIFORM_BUILD` naming the worktree's `pf`. T1–T7 first held at `283759970`. The first agent review's fixes, through `f02eaea6b`, change no fixture result and add a circle-edge case to T6 and the glossary to T7; the coordinator's review adds the tooltip mark-tag refusal (T2, T9) and the docstring consolidation (T7) at `e70e5b864` and `32aa73de7`, and the third agent review the entry refusal (T10) at `d20610c4a` and the owner-named docstrings at `f8502500c` and `64c354307`.

## T1 Element Text Operator

`make corpus` passes each fixture whose click names a node whose text opens with an operator mark, the tooltip carrying none:

- `fixtures/dispatch/a-click-on-a-node-whose-text-opens-with-the-dispatch-mark-dispatches`: `Intake[⇉ Intake]` beside `click Intake href "intake.md"` compiles `intake.bundle.md` and points the click at it.
- `fixtures/deferral/a-click-on-a-node-whose-text-opens-with-the-deferral-mark-defers`, `fixtures/composition/a-click-on-a-node-whose-text-opens-with-the-composition-mark-composes`, `fixtures/parallel-dispatch/a-click-on-a-node-whose-text-opens-with-the-parallel-mark-joins-its-set` and `fixtures/composition/a-deferring-composing-click-carrying-no-tooltip-publishes-no-title` defer, compose, join the set and defer a composition as the same marks opening a link's text do.
- `fixtures/dispatch/a-click-on-a-node-whose-text-opens-with-a-mark-against-text-is-an-ordinary-link`: `Intake[⇉Intake]` opens no operator.

Each was a tooltip-operator fixture, reworked with the marks moved into the node text. Held.

## T2 Tooltip as Title

`make corpus` passes `fixtures/dispatch/a-dispatching-click-s-tooltip-tags-select-its-bundle-s-presets`, where `Intake[⇉ Intake]` beside the tooltip `"checks"` dispatches under `checks`, and a tooltip tag stating operator marks is refused rather than read as a preset name, as T9 shows. `fixtures/deferral/a-deferring-click-tooltip-carries-the-pick-token` and `fixtures/cli/a-click-line-entry-selects-presets-by-its-tooltip` carry `?` and `Checks` as whole tooltips. Held.

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
- `test_cli.py`: a tooltip tag of marks, alone, beside other tags or opening a tag before a blank, refused naming the line, and a tooltip tag with marks against text or after prose read as a title; a class label dispatching, a second click and a second class link refused naming both lines; the click tests rewritten to node text.
- `test_candidate.py`: a bundle changing a click's node text or tooltip fails validation.
- `test_stub_presets.py`: a deferring click carrying no tooltip, an empty tooltip and a link target gains the run's names as a tooltip.

Held.

## T7 Documented Rule

A reading of `docs/references.md` (Operators, Selection by reference, Diagram links) and the design (**Examples** and **Selection belongs to the link**, Link entries, the fixture rows) states the element text as the link text, the tooltip as the title and one link per element. `grep -rni tooltip` over `docs/`, `README.md`, `invocation.md`, the design and `src/prosiform` finds no statement that a tooltip carries an operator; `docs/references.md` and the design state the tooltip mark-tag refusal. The rule is stated in the source model's module docstring and `Click`, and the other docstrings the branch touched name it by its owner, as `source.Click`, `marks.marked` and `profile.diagram_refusals`, without restating it; `closure.py` narrates no diagram link and `tags.py` is unchanged from `main`. Held.

## T8 Full Check

`make check` exits 0: lint, format, typecheck, `make test` (2234 passed), harness (1076 passed), corpus (637 fixtures, 637 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T9 Tooltip Mark Tags

`make corpus` passes `fixtures/dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused` (`Intake[Intake]` beside the tooltip `"⇉"`) and `fixtures/dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` (the tooltip `"⇉, checks"`, `checks` a preset `intake.md` declares): each fails with `E_UNSUPPORTED_CONSTRUCT`, exit status 1, naming `click Intake` at `guide.md:11`, the message naming the tag `'⇉'` and the remedy writing the marks at the start of the element's text. pf 0.26.0 dispatched the first; the head before `e70e5b864` compiled it silently as an inline link. Held.

## T10 Entry Mark Tags

`test_cli.py::test_a_link_entry_whose_title_states_operator_marks_is_invalid_usage`: the entries `click Plan "guide.md#plan" "⇉"`, `click Plan "guide.md#plan" "¬ ?"`, `link Plan "guide.md#plan" "checks, ↳"` and `[Plan](guide.md#plan "⇉ checks")` each exit 2 with `E_INVALID_USAGE`, naming the tag as stating operator marks, and publish nothing, so no run carries a mark tag into the tooltip of a deferring diagram link it publishes. Held.
