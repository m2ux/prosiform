# Group command visual validation v2

**[Review all 36 diagrams](REVIEW.md).**

This set covers 36 distinct review scenarios for the group command at main revision 08a8c0317924e69d5377464ee6961bbc948be85b. Depths 1 and 2 demonstrate different arrangements; this is a behavioral review matrix, not a Cartesian product of every depth, source tree, and option. Invalid depth 7 appears as a rejection case.

The compiler uses --group SLUG:DEPTH. Matching source sections are pooled, members retain distinct destinations, and Overview appears when member subsections accompany pooled sections. Generated names use title case and distinguish members after display transformations.

## Coverage

| Area | Cases |
| --- | ---: |
| Member structure | 8 |
| Pooled sections | 6 |
| Names and casing | 7 |
| Links and selection | 6 |
| Group combinations | 5 |
| Rejected commands/output | 4 |
| **Total** | **36** |

## Case index

| Case | Review focus |
| --- | --- |
| [01-plain-content](cases/01-plain-content.svg) | Members sit directly beneath Rules when no sections are pooled. |
| [02-preamble-and-sections](cases/02-preamble-and-sections.svg) | Overview holds preambles beside the pooled Style section. |
| [03-own-title-absorption](cases/03-own-title-absorption.svg) | A leading own H1 is represented once by its member heading. |
| [04-different-title](cases/04-different-title.svg) | An authored title different from the filename survives beneath the member. |
| [05-later-title](cases/05-later-title.svg) | The first own-name H1 is absorbed even when paragraph content precedes it; both paragraphs survive. |
| [06-headings-only](cases/06-headings-only.svg) | Heading-only sections contribute visible structure. |
| [07-title-only](cases/07-title-only.svg) | Absorbing the only title preserves a named member. |
| [08-empty-member](cases/08-empty-member.svg) | An empty document still has a member destination. |
| [09-unique-sections](cases/09-unique-sections.svg) | Unique section names need no contributor wrappers. |
| [10-shared-sections](cases/10-shared-sections.svg) | A shared heading contains a named contribution from each member. |
| [11-mixed-sections](cases/11-mixed-sections.svg) | Shared and single-contributor sections coexist. |
| [12-body-only-contributions](cases/12-body-only-contributions.svg) | Body-only contributions retain member identity at depth one. |
| [13-nested-contributions](cases/13-nested-contributions.svg) | Each contributor retains its own child section beneath the pooled heading. |
| [14-empty-contributions](cases/14-empty-contributions.svg) | A shared heading with empty contributions still names both contributors. |
| [15-simple-names](cases/15-simple-names.svg) | Generated names title-case separators and preserve HTTP. |
| [16-nested-names](cases/16-nested-names.svg) | A unique nested member needs only its filename stem. |
| [17-stem-clashes](cases/17-stem-clashes.svg) | Directory suffixes distinguish identical stems. |
| [18-deep-clashes](cases/18-deep-clashes.svg) | Qualification reaches the directory segment that distinguishes members. |
| [19-formatting-clashes](cases/19-formatting-clashes.svg) | Names remain distinct after hyphens and underscores become spaces. |
| [20-group-suffixes](cases/20-group-suffixes.svg) | Member names omit the redundant group kind when names stay distinct. |
| [21-consistent-variant-names](cases/21-consistent-variant-names.svg) | Overview and pooled variants share the group-wide member names, including a noncontributor. |
| [22-whole-member-links](cases/22-whole-member-links.svg) | Whole-document links reach distinct contributor headings. |
| [23-pooled-section-links](cases/23-pooled-section-links.svg) | References to each source Style section reach its own variant. |
| [24-absorbed-title-links](cases/24-absorbed-title-links.svg) | A link to an absorbed title reaches the member heading. |
| [25-selected-sections](cases/25-selected-sections.svg) | Selecting one section preserves its outline and excludes its sibling body. |
| [26-deferred-links](cases/26-deferred-links.svg) | Deferred targets exist but contribute no body. |
| [27-harness-selection](cases/27-harness-selection.svg) | Selecting Codex includes its common rules and leaves Claude deferred. |
| [28-ungrouped-baseline](cases/28-ungrouped-baseline.svg) | Ungrouped generated names retain paths and authored heading spelling. |
| [29-multiple-groups](cases/29-multiple-groups.svg) | Distinct slugs contribute independent groups. |
| [30-nested-precedence](cases/30-nested-precedence.svg) | The deepest named directory owns its member; both groups have content. |
| [31-repeated-directory-names](cases/31-repeated-directory-names.svg) | One slug groups matching directories in separate branches. |
| [32-unmatched-group](cases/32-unmatched-group.svg) | An existing directory with no reached members warns while the selected document compiles. |
| [33-missing-depth](cases/33-missing-depth.svg) | A folder-only group argument is invalid usage and emits no bundle. |
| [34-invalid-depth](cases/34-invalid-depth.svg) | A depth outside one through six is invalid usage. |
| [35-duplicate-slug](cases/35-duplicate-slug.svg) | A slug may be declared only once, even with different depths. |
| [36-heading-overflow](cases/36-heading-overflow.svg) | A carried heading that would exceed H6 prevents publication. |

## Sources and evidence

Each case has an isolated my-skill source tree under sources/. These small authored examples isolate the approved behaviors; they are not copies of the full example skill. The source-sha256.json manifest pins every input. Cases 26 and 27 include deferred target files for validation without including their contents in the bundle.

The SVG layout derives from the [original visual validation renderer](../2026-10-22-my-skill-visual-validation/render.py). Images display observed bundle output. Diagnostics appear beneath each image in a separate review subsection when present; complete stdout and stderr are also stored beside each image. They support review of current behavior, not independent proof that every requirement is correct.

## Reproduce

Check out the pinned revision, install its locked dependencies with uv sync --frozen --no-dev from src/, then run from this folder:

```bash
python3 render.py --compiler /path/to/prosiform/src/.venv/bin/prosiform --checkout /path/to/prosiform
```

The renderer checks the compiler revision and clean tracked files, all 36 exit statuses, publication or nonpublication, targeted content expectations and diagnostic codes, and SVG XML validity. Each successful compiler run also performs its own candidate and destination validation. Reproduction requires the compiler environment; SVG viewing needs no dependencies.
