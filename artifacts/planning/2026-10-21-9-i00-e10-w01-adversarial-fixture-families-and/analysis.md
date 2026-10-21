# Analysis — The Families the Design Names Against the Fixtures the Corpus Holds

> Written against `i00/e10/w01-adversarial-fixture-families-and` at the epic base `68944e8`, over the 210 fixtures the corpus holds there.

## How a family is read

A manifest's `clauses` names the design clauses the fixture encodes, and thirty-five manifests already name an adversarial family among them, written `Adversarial acceptance fixtures — <Family>` or with a case after a comma. That is the declaration the family listing reads: a family is represented when a manifest names it.

The design's `## Adversarial acceptance fixtures` section lists twenty-seven families as bold-led bullets. Ten are named by a manifest at the base. The remaining seventeen are represented by fixtures that do not say so, by nothing, or by nothing a source tree can state.

## The families, and what the corpus holds for each

| Family | Held by | Verdict |
| --- | --- | --- |
| Identity | `identity/whole-document`, the six `self-reference/` fixtures | Represented, named |
| Coverage | `consolidation/`, `traversal/a-cycle-of-dependencies`, `traversal/a-second-reference-to-one-document`, `determinism/` | Represented, named |
| Destinations | `destinations/`, `identity/two-headings-sharing-a-slug`, `identity/paths-differing-only-by-suffix`, `identity/same-basename-in-two-directories`, `rewriting/two-targets-sharing-a-slug` | Represented, unnamed |
| References | `reference/`, `literal-bracket/`, `profile/raw-html-in-selected-content` | Represented, named |
| Deferral | the six `deferral/` fixtures, `citation/a-marked-reference-above-the-root` | Represented, unnamed |
| Extraction | the eleven `extraction/` fixtures | Represented, unnamed |
| Boundaries | the five `boundary/` fixtures, `extraction/an-unterminated-example-at-the-section-end` | Represented, unnamed |
| File hierarchy | `hierarchy/`, `absorbed-title/`, `depth-overflow/`, `identity/path-needing-escaping` | Represented, named |
| Grouping | the ten `grouping/` fixtures, the three `cli/group-rule-*` fixtures | Represented, unnamed |
| Partial outlines | `structural-ancestors/`, `ancestor-promotion/` | Named; the skipped-level case is held by nothing |
| Entry line | `entry-line/an-entry-destination-carrying-an-ordinal`, `delivery/an-entry-destination-is-reported` | Represented, unnamed |
| Wrapper identity | `consolidation/a-child-then-its-whole-document` | Represented, unnamed |
| Normalization | the fifteen `normalization/` fixtures, the six `confinement/` fixtures | Named; the empty-fragment case is held by nothing |
| Resources | `resource/`, `traversal/a-relative-resource-warns` | Represented, named |
| Consistency | nothing | No fixture a source tree can state |
| Validation scope | the four `validation-scope/` fixtures | Represented, unnamed |
| Generated inputs | the five `generated-input/` fixtures | Represented, unnamed |
| Delivery | the three `delivery/` fixtures, `limits/an-output-byte-budget-crossed` | Represented, unnamed |
| Parser fidelity | `reference/a-definition-spelled-across-two-lines`, `reference/a-reference-style-image-with-a-title`, `reference/a-link-inside-image-alternative-content`, `real-source/`, `diagnostics/` | Named; tabs and CRLF are held by nothing |
| Definition inventory | `reference/an-unused-definition-is-removed`, `reference/a-definition-a-container-carries`, `candidate-validation/a-definition-removed-beside-its-literal-example` | Named; case-fold-equivalent labels are held by nothing |
| Parser exhaustion | nothing | No fixture the build can meet |
| Validation modes | `candidate-validation/`, `ownership/`, `generated-input/a-bundle-offered-as-input` | Represented, unnamed |
| File-wide safety | `file-wide-safety/`, `validation-scope/an-unselected-broken-link` | Represented, named |
| Profile | the eleven `profile/` fixtures | Represented, named |
| Frontmatter | the nine `frontmatter/` fixtures | Represented, named |
| CLI | the ten `cli/` fixtures, `diagnostics/`, `usage-example/` | Represented, unnamed |
| Limits | the eleven `limits/` fixtures | Represented, unnamed |

## The gaps, and what closes each

**Five cases a source tree can state.** Each gains a fixture.

- **An outline that skips a level.** The design requires that structural ancestors keep the levels the source gave them: *Do not compress skipped levels or invent missing headings that did not exist in the source.* No fixture holds a source whose outline skips one.
- **An empty fragment.** A reference with an empty fragment selects the whole document, which step 9 of the resolution sequence states. No source in the corpus writes one.
- **Tabs carried through a rewrite.** The coordinate mapping names tabs among what maps back to original bytes. No source in the corpus carries a tab.
- **CRLF carried through a rewrite.** `frontmatter/crlf-delimiters` is the one CRLF source, and its run rewrites nothing. The parser-fidelity case is a CRLF document whose link is rewritten and whose surrounding bytes survive.
- **A label two definitions spell with different case.** The design requires the definition inventory to cover case-fold-equivalent labels while preserving first-definition resolution. `reference/an-unused-definition-is-removed` covers a repeated label spelled one way.

**Two cases no source tree can state.** Each is declared ahead of the build, naming the work that delivers it.

- **Consistency** turns on a source changing, disappearing or resolving elsewhere *during* compilation, which a static tree and one invocation cannot declare. [I00:E11:W24](https://github.com/m2ux/prosiform/issues/150) delivers it, and its AC25 states the fixture it ends with.
- **Parser exhaustion** turns on a parser resource limit suppressing a reference lookup, which `E_PARSER_REFERENCE_LIMIT` reports and no build in this initiative emits. It is raised as deferred debt and the fixture names the row that answers it.

## What is counted rather than duplicated

Three cases read as gaps and are not.

- **Wrapper identity** — *a partial file group's document destination does not satisfy a whole-document dependency without expanding its selected content* — is `consolidation/a-child-then-its-whole-document`, which is also the Destinations case about a filename heading that implies no whole-document inclusion. One fixture, two families, named by both.
- **The Markdown extension absent from the filename heading** is every fixture in the corpus: a file heading carries the root-relative path with no suffix.
- **Delivery's broken pipe and transport-oversized output** are `E_PUBLICATION_FAILED`, which no manifest declares. The family is represented by its three fixtures, so this is a case rather than a family, and it is raised as deferred debt beside parser exhaustion.
