# Validation

The checks [W13](w13.md) to [W18](w18.md) name, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Build | `main` at [`74b00cd9`](https://github.com/m2ux/prosiform/tree/74b00cd9), the base of `i09/e05/main` |
| Design | [`4958ad38`](https://github.com/m2ux/prosiform/blob/4958ad38bc2bb6a0786f93aa6de30a7b6a2e27c9/artifacts/planning/2026-10-17-prosiform-v1/design.md), the I09 README's pin |
| Branch head | `ab8f1cae` on `i09/e05/w13-update-the-hierarchy-page`, then `080525fa` holding #583 and #584 merged from the epic base |

Probes ran `uv run --project src --frozen pf` from the worktree in scratch trees.

## T1 The Pages Against the Build

Each claim corrected, added or moved, and what showed it. A claim the read found true and left alone is not listed.

### Hierarchy (AC14)

| Claim | Change | Shown by |
| --- | --- | --- |
| Grouping-depth sections take the level below the group heading, each deeper heading keeping its distance; a member's grouping-depth heading is replaced | Corrected: the page said the level below the grouping depth becomes one level shallower | `grouping/a-section-shallower-than-the-grouping-depth`: depth-3 `### Steps` emitted `## Steps`; `grouping.py` module docstring |
| A variant's content moves one level down beneath it; a sole contributor keeps its arrangement | Added | `grouping/subheadings-name-every-member`: `### Draft` emitted `#### Draft` under each variant |
| A pair places its own document's sections; a linked document is composed under its pair before the parent merges it; a link not bundled stays its document's content | Added | `grouping/a-linked-file-is-composed-before-its-parent-merges-it`, `grouping/a-link-a-file-does-not-bundle-stays-its-content` |
| The parent (first entry document, a member) leads the merged sections, its title opens the group, other members' subsections follow the merged sections | Added | `grouping/a-section-shallower-than-the-grouping-depth`: `## Overview` after `## Steps`; `grouping.py` docstring *The parent is the first entry document* |
| A title is absorbed only where its section is emitted; the heading is literal text | Added | probe: `rules.md#one` from `guide.md` emitted `# Rules` then `### One`; `bundle.py` `escaped` |
| Group identity is exact; `E_GROUP_CONFLICT`, `E_HEADING_DEPTH_OVERFLOW`, `W_COINCIDENT_HEADING`, `E_AMBIGUOUS_SOURCE_HEADING` named | Added | design *Grouping — Group membership*, *Consistent depth*; the fixtures README catalogues |
| A composed section lands beneath the section writing it; a pair places no contribution | Added, linking [Composition](https://github.com/m2ux/prosiform/blob/i09/e05/w13-update-the-hierarchy-page/docs/composition.md#where-it-lands) | `composition/a-selected-group-pair-places-no-contribution` |
| A wordless group name fails | Moved to Sources, with its code | design *Group naming*: `E_INVALID_CONVERSION_METADATA` |

Result: pass.

### Output budget (AC15)

| Claim | Change | Shown by |
| --- | --- | --- |
| The eight named budgets and what each bounds | Added, linking the invocation table for defaults and counting rules | `limits.py` `BUDGETS`; `pf -h` |
| The refusal names 262,254, the figure counted where the bundle crossed, not 307,209 | Corrected: the page quoted 307,209 in the refusal and said the refused figure equals the published size | probe re-take at `acac858`: `E_RESOURCE_LIMIT ... reached 262254 bytes`; `composition.py` `Composing.emit` holds the budget as each part is written |
| The complete bundle is 307,209 bytes; 291,227 with `skills/guidelines.md` undeclared | Held, re-taken | probe: `--budget output-bytes=1000000` published 307,209 bytes, and 291,227 with the declaration removed |
| The re-take runs a second, raised command to read the complete size | Added | the probe above |

Result: pass.

### References (AC16)

| Claim | Change | Shown by |
| --- | --- | --- |
| A dependency's link is rewritten as Destinations states; a composition directive is a dependency placed beneath its section | Added links | design *Link classification — Composition* |
| A link to a document that declares nothing adds nothing to any source budget | Corrected: the page said any budget, though the link counts toward `links` | `inclusion/a-silent-target-is-text` (`files=1`), `inclusion/an-oversized-silent-target-is-text`; `limits.py` `LINKS` |
| A resource warns with `W_RESOURCE_PORTABILITY` | Code added | probe: `![i](p.png)` warned `W_RESOURCE_PORTABILITY` |
| A fragment naming no heading, a container-nested heading, or a shared slug fails with its code | Added | design *Section extraction — Nested target*; catalogues |
| The published link drops its marks; a withheld link is never rewritten into the bundle | Added | design *A deferred link's destination*; `deferral/a-deferral-stands-where-another-reference-carried-its-target` |
| The substitution mapping | Moved to Selection; the classification keeps the order it is asked in and links it | AC17 |

Result: pass.

### Selection (AC17)

| Claim | Change | Shown by |
| --- | --- | --- |
| Presets in force: `default` always; keyword selection; entry selection; layering and union; a preset governs its own document; each link selects for itself; `W_PRESET_UNUSED` | Moved from Sources and stated in one place | `inclusion/a-section-title-selects-its-preset`, `inclusion/a-title-matching-two-keywords-selects-both`, `inclusion/an-entry-name-reads-its-documents-presets`, `inclusion/two-presets-disagreeing-are-refused`, `inclusion/one-document-two-presets`, `inclusion/an-unused-preset-warns`, `inclusion/a-deferred-target-keeps-its-preset` |
| A document's links resolve through the `subst` pairs of every preset in force for it, by whichever reference reached it; two alternatives for one key are refused | Added (review F2, the build's behaviour) | probe: `## Plain` reaching `rules.md#one` and `## Checks` reaching `rules.md#two`; the link in `#one` compiled the `checks` substitute `y.md`, `W_SUBST_USED`; `inclusion/a-pair-a-selected-preset-overrides-records-no-substitution`; `cli.py` `governing` |
| The substitution mapping: keys, precedence, resolution, the substitute as target, entries unredirected, `W_SUBST_USED` once per pair, `W_SUBST_UNUSED` | Moved from References | `inclusion/an-entry-is-not-substituted`, `inclusion/a-pair-reached-only-outside-the-selection-is-unused`, `inclusion/a-dispatched-bundle-reads-its-own-subst`, `composition/the-writers-subst-redirects-a-directive` |
| A withheld link is not followed; a directive is | Added | design *Dispatched bundles*, *Section composition* |
| A reference reaching a placed document places nothing more | Added | design *Composition from the leaves up* |

Result: pass.

### Sources (AC18)

| Claim | Change | Shown by |
| --- | --- | --- |
| Frontmatter failures name `E_INVALID_FRONTMATTER` and `E_UNTERMINATED_FRONTMATTER` | Codes added | design *Metadata failures* |
| The page states the declaration, preset keys and their shapes and refusals, and links Selection for which presets are in force | Restructured: selection and redirection moved to Selection | AC17 |
| Capture failures name `E_SOURCE_CHANGED`, `E_SOURCE_SYMLINK`, `E_SOURCE_ACCESS`, `E_TARGET_NOT_FOUND` | Codes added | design *Metadata failures* |
| An entry's parent segments resolve from the working directory; an absolute, drive, scheme or authority entry fails `E_SOURCE_OUTSIDE_ROOT` | Added | probe: `pf -c ../x.md` exit 0; `pf -c /tmp/x.md` `E_SOURCE_OUTSIDE_ROOT` exit 1 |
| Encoding, suffix, raw HTML and unsupported constructs name their codes | Codes added | probes: `a.txt` `E_UNSUPPORTED_ENTRY_SUFFIX`, `<div>` `E_RAW_HTML` |

Result: pass.

### Validation (AC19)

| Claim | Change | Shown by |
| --- | --- | --- |
| No new content: no link or definition the sources did not write | Invariant added | `candidate.py` `NO_NEW_LINKS`, `NO_DEFINITION_LEAKAGE` |
| A boundary failure is `E_UNSAFE_BUNDLE_BOUNDARY`; any other invariant failing is a build defect, `E_UNEXPECTED_INTERNAL_ERROR`, exit 4 | Added | `cli.py` catches `Unsafe` alone around `validate`; `main` reports any other exception as status 4 |
| Every check a run refuses with, its code and exit status; every warning code | Added: *What a run refuses* | `pf -C`; `pf -h` exit statuses; probes for suffix, outside-root and raw HTML exit 1 |
| An `output-bytes` refusal names the bundle as far as the crossing part | Added | the output-budget probe |

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `ab8f1cae`, exit 0: lint, format, types; `make test` 1663 passed; `make harness` 1161 passed; the corpus 498 of 498; `make links`, `make tables` and `make vocabulary` ok. The first run failed `test_the_authoring_statements_are_stated_where_they_are_owned`, which pins the sources page's sentence on the working directory; the sentence is kept whole and the parent-segment clause follows it.

Rerun at `080525fa`, after merging `origin/i09/e05/main` (#583, #584) and resolving the docs index and invocation guide conflicts: exit 0, `make test` 1663 passed, `make harness` 1161 passed, the corpus 498 of 498, `make links` resolving `docs/selection.md#the-substitution-mapping` and `#presets-in-force` from `invocation.md` and `README.md`.

Result: pass.
