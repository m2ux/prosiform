# README Prose

Tested implementation: [`9a2b1f13e96a81d9450ce56b0f08ae38aac60d9a`](https://github.com/m2ux/prosiform/commit/9a2b1f13e96a81d9450ce56b0f08ae38aac60d9a).

## Structure

The README uses the concise structure found at `dfa94f71b`: definition, overview, benefits, illustrated walkthrough, installation and two usage examples. Current profile and design references remain current, and the examples use the existing fixture corpus.

The text states the source declaration requirement, the bare `pf` guide invocation and the folder containing the entry's bundle and any dispatched bundles. Source presets and link operators are documented in the existing linked guides.

Whitespace-delimited word counts over each complete Markdown file, including its alt text and commands:

| Revision | Words |
| --- | ---: |
| Earlier concise README, `dfa94f71b` | 405 |
| Initial illustration commit, `fac70a940` | 1,004 |
| Concise README | 397 |

The prose restoration changes only `README.md` in the implementation worktree. The illustration and renderer are the bytes verified at `fac70a9403370a12a84da473e379367d77b0a3e8`.

## README Examples

**Pass.** The existing corpus runner runs the two retained commands against the worktree's locked compiler. Both produce the exit status, exact bundle bytes and diagnostics their manifests declare:

- `dispatch/a-dispatched-target-is-a-bundle-of-its-own`: `pf guide.md`, two bundles.
- `extraction/section-to-the-next-sibling`: `pf 'guide.md#run'`, one section bundle.

Each runs from its fixture's `source` directory, matching the README's `cd` command. The checker receives absolute fixture paths and `PROSIFORM_BUILD` names the worktree's `src/.venv/bin/pf`.

Evidence: [example results](prose-examples.txt).

## Documentation Checks

**Pass.** The command-table check passes, all references across 203 documents resolve online, and `git diff --check` passes.

```bash
python3 checks/tables.py
python3 checks/links.py --online
git diff --check
```

Evidence: [tables](prose-tables.txt), [links](prose-links.txt).

## Full CI

The updated PR head is checked after publication.
