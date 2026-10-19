# Validation — I00:E03:W01

> The checks as they were run, and what each establishes.

## The Oracle

AC5 names a GitHub renderer, so the renderer answered for itself. Each fixture's source was pushed to the delivery branch and rendered by GitHub through its own API, and the anchor ids it generated were read off the result:

```bash
gh api "repos/m2ux/prosiform/contents/fixtures/<fixture>/source/article.md?ref=i00/e03/w01-source-heading-slugs-and" \
  -H "Accept: application/vnd.github.html"
```

| Fixture | Anchors GitHub generated, the `user-content-` prefix removed |
| --- | --- |
| `destinations/source-heading-fragments` | `article`, `whats-new-v10`, `the-code-span-and-bold-text`, `café-münster`, `notes`, `notes-1` |
| `headings/collision-with-a-natural-suffix` | `run`, `run-1`, `run-2`, `run-3`, `run-1-1` |
| `headings/an-entity-in-a-heading` | `café`, `run` |
| `headings/image-alternative-text` | `the--overview`, `run` |
| `headings/a-heading-with-no-visible-text` | `-1`, `run` |

Every fragment the build produces for those headings is the one GitHub generated, which the corpus holds byte for byte.

Three of the rows were measured before the implementation was settled and changed it.

- **An ordinal a heading already carries is passed over.** `## Run`, `## Run-1`, `## Run`, `## Run`, `## Run-1` render as `run`, `run-1`, `run-2`, `run-3`, `run-1-1`. A count that numbers from the slug alone would have given the third heading `run-1`, which the second already carries, so two headings would have shared one fragment.
- **A renderer reads no text from an image.** `## The ![A diagram](plan.png) overview` renders as `the--overview`: the alternative text contributes nothing and the space the image stood in remains, which is why the slug carries two hyphens. The design's `Source-heading resolution` clause names image alternative text among the events visible text is derived from, and the renderer does not read it.
- **A line break is discarded rather than spaced.** A Setext heading written over two lines renders as `runthe-procedure`. The line feed is a control character, which the slug's discard set already removes, so a derivation that normalized it to a space would have produced `run-the-procedure`. The design's same clause names "normalized line-break spacing".

The second and third are recorded as a finding against the design rather than as behaviour: the corpus and the build follow the renderer, which is what the criterion names.

**What it establishes and what it does not.** It establishes agreement with GitHub's own answer for the headings these fixtures carry, at one revision. No check re-runs the comparison, so a later change to the rule is caught by the corpus — which holds the measured fragments — rather than by re-asking the renderer.

## The Gate

`make check` was run whole in the delivery worktree, with `PROSIFORM_BUILD` naming the prototype by absolute path, and returned zero.

| Check | Result |
| --- | --- |
| `lock-check` | Resolved 22 packages |
| `lint` | All checks passed |
| `format-check` | 26 files already formatted |
| `typecheck` | Success: no issues found in 25 source files |
| `test` | 270 passed |
| `harness` | 180 passed |
| `corpus` | 45 fixtures, 42 pass, 0 fail, 3 awaited, 0 unexpected pass |
| `layout` | 3 trees present |
| `tables` | 12 commands and 7 declarations, each declared and named by a table |
| `links` | Every reference in 6 documents resolved |
| `vocabulary` | 34 contract terms marked, every one defined and carried |

The fixtures this row adds are among the corpus run's results:

```text
destinations/source-heading-fragments: pass
headings/a-heading-with-no-visible-text: awaited, awaiting I00:E10
headings/an-entity-in-a-heading: pass
headings/collision-with-a-natural-suffix: pass
headings/image-alternative-text: pass
```

## What the Criterion Rests On

**AC5** — a source heading's fragment equals the one a GitHub renderer generates for it, as the slug compatibility fixtures show.

Four fixtures show it, each over headings GitHub itself was asked about: punctuation and an entity discarded, a code span and strong emphasis read through, text outside ASCII lowered and kept, an image read past, a heading repeated and numbered apart, and an ordinal a heading's own text already spells passed over. Each fragment is observed as the destination a later file group takes behind the heading that produced it, so the fixture's expected bytes carry the fragment rather than a description of it.

The criterion ticks on those. The one boundary left unticked is declared rather than dropped: a heading a renderer discards entirely gets no anchor from GitHub at all, which no destination this build emits can express, and `headings/a-heading-with-no-visible-text` awaits the conformance epic with the lookup that would observe it.
