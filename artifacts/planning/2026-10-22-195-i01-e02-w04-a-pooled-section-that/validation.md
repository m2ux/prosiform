# Validation

Implementation revision: `bc4f53723f6de3c46a3f96afa5350cd651ee2115`, based on `b7d5599`. Contract revision: engineering `f967d3b`.

## Repository checks

Executed `make check` with `PROSIFORM_BUILD="uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01-e02-w04/src --frozen prosiform"`.

- Lock, lint, formatting and strict type checks passed.
- Implementation suite: 752 passed.
- Harness suite: 605 passed.
- Corpus: 249 fixtures passed; none failed, awaited or unexpectedly passed.
- Installation smoke, layout, command/dependency tables and authenticated documentation links passed.
- Vocabulary and invocation checks passed.
- Conformance: 245 clauses, zero uncovered clauses and zero unknown clause declarations.
- Independence passed on a targeted rerun after the contract clarified ownership of text, list items and subheadings. The initial full run reached this final target and failed because the contract rewrite removed vocabulary used by existing fixtures. No implementation changed between those runs.

Every named check target passed. The full command's initial exit status was 2 at independence; its targeted rerun exited 0.

## Contributor headings and destinations

Observed AC2 and AC3 through the actual compiler and candidate validation:

- `grouping/mixed-contributions-name-every-member`: body text and a subheading-only contribution share `Style`; generated `Agents` and `Common` headings carry their respective contents and distinct entry destinations.
- `grouping/subheadings-name-every-member`: both contributors carry `Draft`; each stays beneath its own member variant, and the two document entries reach different generated headings.
- Existing sole-contributor, title-absorption and overview fixtures pass.
- Grouping unit tests exercise body, subheading and empty contributions both with and without overview content, checking named variants and distinct destination positions.
- The existing structural-ancestor fixture passes with its selected descendant beneath its member variant; reference rewriting, outline reconstruction and source coverage are validated by the compiler.

## Consistent names

Observed AC8 through corpus runs and unit tests:

- `grouping/a-pooled-subset-keeps-group-member-names`: `g/a/notes.md`, `g/b/notes.md` and `g/c/other.md` determine names together. Only the latter two contribute `Findings`; their variants remain `B Notes` and `C Other`, matching their overview names.
- `grouping/a-variant-drops-the-group-word`: `Plan` and `Review` appear in both overview and procedure variants beneath `Modes`.
- Same-stem paths, shared prefixes and sole-contributor arrangements pass their unit and corpus checks.

## Review

Reviewed the implementation diff and all eight changed existing corpus outputs against source contributions. Pooled operations retain each member's source order beneath that member's variant. Sole-contributor sections retain their source arrangement. Whole-document and grouping-depth references follow the correct member; the actual compiler validates destinations on every successful corpus compilation.

Removed the unused body-text predicate, subset qualifier and nested-name arrangement helpers. `git diff b7d5599 --check` passes in the implementation worktree. No unit-blocking defect or separate non-trivial debt was found after these corrections.

## Remote checks

The first CI run at the implementation revision failed the same contract vocabulary check. The [rerun](https://github.com/m2ux/prosiform/actions/runs/39735191272/job/119681269711) after engineering `f967d3b` completed successfully at `bc4f53723f6de3c46a3f96afa5350cd651ee2115`. Remote CI ran the complete `make check` command successfully.
