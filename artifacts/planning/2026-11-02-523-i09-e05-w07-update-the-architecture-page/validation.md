# Validation

Evidence for AC8–AC13 at `main` 74b00cd9 and design 4958ad38, on branch `i09/e05/w07-update-the-architecture-page`.

## AC8

- **The query.** GitNexus over the indexed revision b83f0b3d, whose `src/prosiform` tree equals 74b00cd9's (`git diff --stat b83f0b3d 74b00cd9 -- src/prosiform` is empty):

  ```cypher
  MATCH (a:File)-[r:CodeRelation {type: 'IMPORTS'}]->(b:File)
  WHERE a.filePath STARTS WITH 'src/prosiform/' AND b.filePath STARTS WITH 'src/prosiform/'
  RETURN a.filePath AS importer, b.filePath AS imported ORDER BY importer, imported
  ```

- **The result.** 57 edges over 17 files: sixteen modules and `__init__`.

  | Module | Imports |
  | --- | --- |
  | `cli` | `__init__`, access, bundle, candidate, closure, composition, diagnostics, dispatch, grouping, limits, metadata, profile, provenance, rewrite, source |
  | `candidate` | bundle, closure, profile, provenance, source |
  | `composition` | bundle, closure, dispatch, limits, provenance, rewrite, source |
  | `dispatch` | bundle, closure, diagnostics, provenance, source |
  | `grouping` | bundle, closure, heading, provenance, rewrite, source |
  | `bundle` | closure, heading, profile, provenance, rewrite, source |
  | `rewrite` | closure, profile, source |
  | `closure` | profile, source |
  | `profile` | `__init__`, limits, source |
  | `source` | limits, metadata |
  | `metadata` | diagnostics, heading, limits |
  | `access`, `diagnostics`, `heading`, `limits`, `provenance` | none within the package |

- **The page against it.** The Modules table names each of the sixteen and `__init__`; no module imports `cli`, as the page states. Each responsibility was read against the module's docstring. The flow figure follows `cli.execute`, `cli.compiled` and `cli.compose`: capture through `access`, `source` and `metadata`; `profile.parse`; classification in `closure`; `bundle`, `grouping`, `composition` and `dispatch` building groups, with `rewrite` called by `bundle` and `grouping` as each group is built and `provenance` recorded; `candidate.validate`; `cli.publication`.

## AC9

The bundles page read against `cli.publication`, `publish_folder`, `occupied`, `run_name` and the design's *Automatic output names*.

- **Added: name collisions between bundles.** `colliding` refuses two bundles of one run deriving one name with `E_PUBLICATION_FAILED`. Probe: entry `a/b.md` dispatching `a_b.md` exits 3 naming both selections. Two entries deriving one name still join (probe: `pf -o out a/b.md a_b.md` publishes `a_b+a_b.bundles/a_b+a_b.bundle.md`), as the page states.
- **Added: overlong names.** `overlong` refuses a run folder or bundle name past the filesystem's `PC_NAME_MAX`.
- **Added: an output folder that cannot be made** is refused with `E_PUBLICATION_FAILED`.
- **Added: what `-c` checks.** `publication` runs the output budget, name and occupied-path checks before the `check` branch, and makes an absent output folder under `-c` too. Probe: `pf -c -o out3/deep a_b.md` exits 0 and leaves `out3/deep` made and empty.
- **Arising.** The `-c` folder is raised as [#588](https://github.com/m2ux/prosiform/issues/588).
- **Held true.** Derived names, publication's swap, the symbolic link and regular-file cases, `-o -` and the run folder holding a source.

## AC10

The destinations page read against `source.fragments`, `bundle` link destinations and the design's *Bundle destinations*.

- **Corrected: ordinals count from one.** `fragments` gives the second heading carrying a slug the ordinal `1`; the page's code block named `-2` and Figure 1 `#run-2` and `#run-3`. Now `-1`, `#run-1` and `#run-2`, as the design's `#{heading-slug}-{n}` for the (n+1)th states.
- **Corrected: the walk covers every emitted heading.** The Prosiform section, merged-group headings, dispatch sub-sections, destination sections and contribution headings take part (dispatch sub-sections are inserted before destinations are assigned, as `dispatch`'s docstring states).
- **Added: a directive's link** points at its contribution heading, deferred or not, linking [Composition](https://github.com/m2ux/prosiform/blob/main/docs/composition.md#where-it-lands) rather than restating it.
- **Held true.** Source fragments refusing two headings of one slug (`E_AMBIGUOUS_SOURCE_HEADING`), the deferred link's rebased path, definitions removed, and what validation holds.

## AC11

The diagram-renderer page read against `scripts/render-diagram.py`, `scripts/render-example.py` and `scripts/examples.json`.

- **Fixed in the script: operator marks in amber.** `render-example.py` drew `¬`, `⇉` and `⫽` in amber and `render-diagram.py` `¬` alone, while the page says both use one drawing. `render-diagram.py` now marks all three.
- **Corrected: a case's status.** `render-example.py` fails when a case exits other than its declared `status` (`0` when absent); the page said a nonzero case merely draws.
- **Corrected: what `render-diagram.py` draws.** The entry's bundle only; a dispatched bundle is not drawn.
- **Added: an output prefix that would overwrite a source** is refused.
- **Added: where diagram links are read and checked.** A link to [Diagram links](https://github.com/m2ux/prosiform/blob/main/docs/references.md#diagram-links) and [Rendering](https://github.com/m2ux/prosiform/blob/main/checks.md#rendering), each rule's one home.

## AC12

The dispatch page read against `dispatch.py`, `cli.dispatches` and the design's dispatch clauses.

- **Added: a target must declare `prosiform`.** `refusals_of_operators` refuses an operator naming a document declaring none.
- **Added: `Run pf first` collides.** `collisions` refuses an authored heading equal to any `PROSIFORM_SECTION` heading, `Run pf first` among them; the page's list omitted it. The code `E_HEADING_COLLISION` is named.
- **Added: the cycle code** `E_DISPATCH_CYCLE`, and that a dispatch naming the run's single selection closes the shortest cycle.
- **Corrected: where sub-sections stand.** After any destination sections composition places; Figure 1's child sections sit at `###`, one level below `## Plan Mode`.
- **Removed: a repeated paragraph.** The cycle refusal was stated twice under *Depth and cycles*.
- **Linked:** the deferred directive's `↳` line to [Composition](https://github.com/m2ux/prosiform/blob/main/docs/composition.md#deferred-directives).
- **Held true.** `LIMIT = 3` (a fourth hop warns), the sub-section shapes, the Prosiform section's headings and slugs, the empty-text refusal (`cli.dispatches`), self-dispatch warning.

## AC13

The glossary read term by term against the design at 4958ad38 and the build.

- **Added: scope, destination section, contribution, run folder.** The design states each (*Section composition*, *CLI contract*), and the pages use them.
- **Corrected: preset selection by an entry.** `cli.entry_title` selects an entry's presets by the title of the section or document it names, and a dispatched target compiles as an entry.
- **Corrected: the substitution mapping combines.** `cli.governing` puts in force the pairs every reference reaching a document selects within one bundle, and refuses two mapping one key to two alternatives (review F2, W31).
- **Held true.** Every other entry; `make vocabulary` holds the term set to the design.

## Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'` at the branch head 0f1df83c exits 0: 1663 check tests, 1161 build tests, 498 of 498 fixtures, smoke, layout, tables, links (143 documents), vocabulary (49 terms), invocation (28 statements), conformance and independence.

After merging `origin/i09/e05/main` into the branch, `make check` exits 0 with the same counts at 2dd66374 (base a7eae14c) and at f6135dec (base c59894e0); CI passes at both heads.
