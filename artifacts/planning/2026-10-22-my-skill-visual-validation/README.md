# My-skill visual validation

**Start here: [all 30 proposed-output images on one page](REVIEW.md).**

This review suite interprets the current [#194](https://github.com/m2ux/prosiform/issues/194) and [#195](https://github.com/m2ux/prosiform/issues/195) bodies as read on 2026-10-22: folder-only grouping, one intact section per member, own-title absorption, distinct member destinations, and consistent generated title casing.

Expected Markdown is authored from those requirements. The renderer does not derive expected output from the current compiler. These are reviewable predictions, not evidence that the issues are implemented or their acceptance criteria pass.

## Layout

```text
my-skill/
  SKILL.md
  checks/visual/final-check.md
  guides/HTTP-setup.md
  procedure.md
  quick-start.md
  rules/agents.md
  rules/claude.md
  rules/codex.md
  rules/common.md
  rules/visual/HTTP-checks.md
  rules/visual/api/common.md
  rules/visual/blue.md
  rules/visual/clash-route.md
  rules/visual/heading-h1.md
  rules/visual/heading-h2.md
  rules/visual/heading-h3.md
  rules/visual/heading-h4.md
  rules/visual/heading-h5.md
  rules/visual/heading-h6.md
  rules/visual/headings-only.md
  rules/visual/identity.md
  rules/visual/later-title.md
  rules/visual/nested/deep-note.md
  rules/visual/other-title.md
  rules/visual/plain.md
  rules/visual/preamble.md
  rules/visual/red.md
  rules/visual/route.md
  rules/visual/team-a/web/shared.md
  rules/visual/team-b/web/shared.md
  rules/visual/title-only.md
  rules/visual/web/common.md
  tips.md
```

The source snapshot matches `example/my-skill/` on main (excluding its visual-case navigation page). Existing README entry points are preserved; additional cases are selected explicitly. [SHA-256 manifest](source-sha256.json) pins every input.

## Coverage

| Case | Issue criteria | Review focus |
| --- | --- | --- |
| [01-root-documents](cases/01-root-documents.svg) | 194 AC1, 195 AC6 | Procedure and Tips are title-cased; source files stay at the root. |
| [02-default-paths](cases/02-default-paths.svg) | 194 AC1, 194 AC2, 195 AC6, 195 AC7 | Generated paths preserve slashes and HTTP; the authored heading keeps its spelling. |
| [03-preamble-only](cases/03-preamble-only.svg) | 195 AC1, 195 AC5 | One member section; no Overview wrapper. |
| [04-preamble-headings](cases/04-preamble-headings.svg) | 195 AC1, 195 AC7 | The preamble and both source sections remain inside Preamble. |
| [05-shared-section-names](cases/05-shared-section-names.svg) | 195 AC1, 195 AC4 | Blue and Red stay whole; neither Style section collects the other member. |
| [06-absorb-h1](cases/06-absorb-h1.svg) | 195 AC2 | The leading H1 becomes the member title exactly once. |
| [07-absorb-h2](cases/07-absorb-h2.svg) | 195 AC2 | The leading H2 becomes the member title exactly once. |
| [08-absorb-h3](cases/08-absorb-h3.svg) | 195 AC2 | The leading H3 becomes the member title exactly once. |
| [09-absorb-h4](cases/09-absorb-h4.svg) | 195 AC2 | The leading H4 becomes the member title exactly once. |
| [10-absorb-h5](cases/10-absorb-h5.svg) | 195 AC2 | The leading H5 becomes the member title exactly once. |
| [11-absorb-h6](cases/11-absorb-h6.svg) | 195 AC2 | The leading H6 becomes the member title exactly once. |
| [12-own-title-children](cases/12-own-title-children.svg) | 194 AC2, 195 AC2, 195 AC7 | Identity is absorbed; its child keeps its exact authored case. |
| [13-other-title](cases/13-other-title.svg) | 194 AC2, 195 AC1, 195 AC7 | The filename supplies Other Title; the different authored title remains beneath it. |
| [14-headings-only](cases/14-headings-only.svg) | 195 AC1 | The member is named even without paragraph content. |
| [15-title-only](cases/15-title-only.svg) | 195 AC1, 195 AC2 | Title absorption does not erase the member. |
| [16-later-title](cases/16-later-title.svg) | 195 AC2, 195 AC7 | Only a leading own-title heading qualifies for absorption. |
| [17-stem-clash](cases/17-stem-clash.svg) | 195 AC3 | Use the shortest distinguishing suffix after the shared prefix: Api Common and Web Common. |
| [18-deep-stem-clash](cases/18-deep-stem-clash.svg) | 195 AC3, 194 AC1 | Web Shared still clashes, so retain the distinguishing Team A or Team B segment. |
| [19-unique-nested-member](cases/19-unique-nested-member.svg) | 195 AC1, 195 AC3, 195 AC6 | A unique filename needs no directory qualifier. |
| [20-generated-versus-authored](cases/20-generated-versus-authored.svg) | 194 AC1, 194 AC2, 195 AC6, 195 AC7 | Preserve HTTP in the generated name and every character of the authored heading. |
| [21-member-destinations](cases/21-member-destinations.svg) | 195 AC1, 195 AC4 | Blue and Red whole-document links have distinct destinations; duplicate Style fragments remain distinct. |
| [22-clash-destinations](cases/22-clash-destinations.svg) | 195 AC3, 195 AC4 | The same-stem members each have a distinct named destination. |
| [23-shared-skill](cases/23-shared-skill.svg) | 195 AC1, 195 AC4, 195 AC6, 195 AC8 | Rules contains Agents and Common directly; harness files remain deferred. |
| [24-harness-codex](cases/24-harness-codex.svg) | 195 AC1, 195 AC4, 195 AC8 | Only the selected harness is present; no Overview wrapper. |
| [25-harness-claude](cases/25-harness-claude.svg) | 195 AC1, 195 AC4, 195 AC8 | Only the selected harness is present; no Overview wrapper. |
| [26-multiple-groups](cases/26-multiple-groups.svg) | 195 AC5, 195 AC6 | Each named folder contributes its own group. |
| [27-old-depth-rejected](cases/27-old-depth-rejected.svg) | 195 AC5 | The proposed CLI rejects --group rules:1 and publishes no bundle. |
| [28-duplicate-group-rejected](cases/28-duplicate-group-rejected.svg) | 195 AC5 | Repeatable means different folder slugs; the same slug twice is rejected. |
| [29-deepest-matching-folder](cases/29-deepest-matching-folder.svg) | 195 AC1, 195 AC5 | Existing deepest-folder selection is retained; the unused outer rule contributes no section. |
| [30-ungrouped-harness](cases/30-ungrouped-harness.svg) | 194 AC1, 195 AC6 | Title casing also covers the default document heading, without --group. |

The six own-title cases cover every supported source heading level (H1–H6). The CLI rows cover folder-only syntax, multiple distinct groups, rejected depth syntax, and duplicate group declarations. Nested selection is an explicitly labeled retained-behavior assumption.

## Reproduce the visuals

From this directory:

```bash
python3 render.py
```

This regenerates `REVIEW.md`, each SVG, expected body, command file, and the source manifest from [cases.json](cases.json). It validates all expected internal fragments and deferred file destinations. IBM Plex Mono is the preferred font; SVG text remains selectable.

For a raster preview:

```bash
QT_QPA_PLATFORM=offscreen ksvgtopng 2142 936 cases/05-shared-section-names.svg /tmp/shared-sections.png
```

## Current-tool evidence

The observed compiler revision is `7ba5fe9f44ade4a19b843619aeea37abf2c7f4b1`. [Run records](current-observations/runs.json) include exit codes and exact arguments. Each case has raw stdout and stderr for the proposed command and, separately, the closest legacy `--group SLUG:1` comparison. Neither observation is used to create the proposed images.

To refresh observations with an explicitly chosen compiler:

```bash
python3 render.py --compiler /absolute/path/to/prosiform
```

## Review decisions

- Member ordering follows root-relative paths, consistent with the current arrangement; issues do not request a new order.
- A source heading retains its text when nested beneath a member; a leading own-name title is absorbed at every tested level.
- Nested matching groups retain deepest-directory membership (case 29).
- Exact rejection diagnostics are unspecified. Rejection images promise no bundle, not particular wording.
- Expected files contain the complete bundle body. The generated entry preamble is omitted from the visual contract; member and section links are shown with exact destinations in the Markdown.
- Historical section-group/folder-group proposals in issue comments are outside this suite: the current #195 body specifies one folder-only `--group` option.

These images cover the finite permutations above; they are not a substitute for the implementation’s full corpus, destination, and preservation tests.
