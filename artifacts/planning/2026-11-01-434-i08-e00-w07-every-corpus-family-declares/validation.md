# Validation

Evidence for each check the [work item](w07.md) names, run in the unit's worktree at aa3dc350 with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Corpus

`make corpus`: 385 fixtures pass, 0 fail, the twenty renamed fixtures under their new paths. Of the expected bundles, six changed: five differ from the published ones only in the source prose this unit rewrote ("above the root", "the root holds", "allowed source root"), and the silent-target fixture's bundle is re-derived as `notes_guide.bundle.md` from its reworked tree. Every other bundle, `usage-example/` and `real-source/` among them, is byte-identical (AC12).

## T2 Silent target

`reference/a-silent-target-above-the-writing-directory-is-text` passes with exit 0: `notes/guide.md` links `../guidelines.md`, inside the working directory and above the writing document, and the link is emitted as authored. The same tree with `prosiform: {}` added to `guidelines.md` fails with `E_RAW_HTML` at `guidelines.md:6`, chain `notes/guide.md → guidelines.md`, so the declaration alone decided the passing run (AC12).

## T3 Descriptions

A `grep` for `root` over `fixtures/*/*/manifest.toml`, excluding the refused `prosiform.root`, the retired `-r` option, section roots, root-relative URLs and the `E_SOURCE_OUTSIDE_ROOT` code, finds nothing (AC12).

## T4 Conformance

`make conformance`: 305 clauses the design states, 0 declarations naming no clause. The two rewritten clause cases name the *Reference normalization and path identity* and *Compile before publishing* headings the design carries.

## T5 Full check

`make check` exits 0 at aa3dc350 before opening.
