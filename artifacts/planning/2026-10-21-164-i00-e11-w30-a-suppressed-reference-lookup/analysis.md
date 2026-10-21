# Analysis

Two questions decide what this row delivers: whether the parser's own expansion budget is reachable with every public limit at its default, and how the Parser exhaustion family's clause is spelled in the inventory a manifest names clauses from. Both are settled below against the build on `i00/e11/main` at `232a528`.

## A budget below every public limit

Yes, and it is reached on a command line that declares no budget at all.

The profile configures the parser with a nesting ceiling of its own, set to the declared nesting budget plus a fixed headroom of 20 levels. The declared budget counts *container* nesting — a block quote or a list item, which is what CommonMark calls a container — while the ceiling counts inline nesting into the same figure. No budget is declared over inline nesting, so the two counts cross on different sources: a document whose containers nest nowhere still opens 85 inline brackets and reaches the ceiling.

Measured against the default `--max-nesting` of 64, so a ceiling of 84:

| Open brackets before the reference | Outcome |
| --- | --- |
| 84 | The lookup resolves and the parse returns the reference the source names |
| 85 | The lookup is declined and the parse raises |

The declining source is 135 bytes, nests no container, names one reference and sits one hop from the entry. Against the budgets it is held to:

| Budget | Default | What the declining source counts |
| --- | --- | --- |
| `--max-files` | 256 | 1 |
| `--max-file-bytes` | 1048576 | 135 |
| `--max-input-bytes` | 16777216 | 135 |
| `--max-output-bytes` | 262144 | 0, since nothing is published |
| `--max-targets` | 4096 | 1 |
| `--max-links` | 32768 | 1 |
| `--max-nesting` | 64 | 0 |
| `--max-expansion-depth` | 8 | 1 |

So the condition the family names — reference-expansion suppression below the tool's public input and output limits — is producible, and producible on an invocation naming only the entry reference. The two fixtures already on this base reach the same code by declaring `--max-nesting 1`, which lowers the ceiling to 21 and makes the invocation itself the reason the ceiling was near. They state the viability gate rather than the family.

The row therefore carries behaviour as well as fixtures. The failing run's diagnostic names the source it could not index, because the lookup never ran and nothing the run holds names the reference. The abandoned scan does name it: the scan stops inside a label the parser had opened, and the text from that point to the end of the inline content carries the label and the destination its construct spells. Reading that span is what lets the failure name the reference whose lookup was suppressed, which the task issue's AC1 requires.

## The family's clause

`"Adversarial acceptance fixtures — Parser exhaustion"`.

A clause names the design heading it sits under, an em dash, and the rule under that heading. The family list sits under the `Adversarial acceptance fixtures` heading and each family is a bold lead within it, so the corpus already carries clauses of exactly this shape, among them `"Adversarial acceptance fixtures — Identity"` and `"Adversarial acceptance fixtures — Definition inventory"`.

A fixture covering one part of a family's sentence names that part after a comma, as `"Adversarial acceptance fixtures — Partial outlines, ancestor promotion after dependency expansion"` does. The family's sentence names a second case in its own words, so the run that spends the budget on its last valid reference declares `"Adversarial acceptance fixtures — Parser exhaustion, a case that consumes the budget on its last valid reference"`.

Neither existing fixture names the family, and neither takes the clause: both declare the viability gate they were written for, and an invocation that lowers the ceiling is not the condition the family states. The two fixtures this row adds declare the family clause, and the failing one declares the gate beside it, since it is the same detection observed under the condition the family names.

## What the row delivers

- The declined lookup named in the failure, so `E_PARSER_REFERENCE_LIMIT` carries the reference rather than only the source that could not be indexed.
- Two corpus fixtures reaching the ceiling with every budget at its default, declaring the family clause, one failing and one succeeding on the budget's last valid reference.
- The existing failing fixture's expected reference brought to the reference the run now names.
