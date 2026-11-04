# README Presentation — November 2026

> Documentation · Created 2026-11-04

## Executive Summary

The README introduces compilation through a detailed drawing of source documents and their bundle. The illustration uses the current `run` example and the output of the compiler at `11a872918669362260cf16b875694342f262d2c2`.

The README pairs connected panels, readable type and clear visual hierarchy with a concise introduction and two usage examples. File links are traced to their destinations in the source tree and in the bundle; the linked guides hold detailed language and invocation rules.

## Todo

- [x] Inspect the published README, earlier illustration and current example.
- [x] Render the connected layout from a real compiler run.
- [x] Inspect the image at README width and verify content and regeneration.
- [x] Publish the committed branch and its review handoff.
- [x] Identify the earlier concise prose and current source and publication rules.
- [x] Restore the concise README body with current commands and behavior.
- [x] Verify the README examples and documentation checks.
- [ ] **In progress:** Commit, push and update the review PR.
- [ ] Confirm CI at the updated head and publish the results.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Before SVG](before.svg) | The published illustration at the compiler baseline. |
| [Before preview](before.png) | The published illustration at 900 pixels wide. |
| [After preview](after.png) | The connected illustration rendered from its SVG. |
| [README-width preview](readme-width.png) | The connected illustration at 900 pixels wide. |
| [Validation](validation.md) | Tested revisions, procedures and observations. |
| [Verification script](verify.py) | Independent Markdown checks, actual compilation, SVG bounds and preview rendering. |
| [Verification results](verification.txt) | Results of the content, geometry and reproduction checks. |
| [Compiled example](compiled.md) | The complete bundle the illustrated run writes. |
| [Example generation](generation.txt) | All nine cases and their observed publication results. |
| [Renderer checks](ruff.txt) | Ruff lint and formatting results. |
| [Command-table checks](tables.txt) | Repository command and dependency table results. |
| [Link checks](links.txt) | Online resolution of all documentation references. |
| [Illustration CI result](ci.json) | Successful full repository check at the initial illustration commit. |
| [README prose](readme-prose.md) | Historical structure, text-size comparison and current validation. |
| [README before prose restoration](readme-before-prose.md) | The README at the initial illustration commit. |
| [README example checks](prose-examples.txt) | Corpus results for both retained usage examples. |
| [README command-table checks](prose-tables.txt) | Command-table results after the prose restoration. |
| [README link checks](prose-links.txt) | Online documentation reference results after the prose restoration. |

## Links

| Resource | Link |
| --- | --- |
| Published README | https://github.com/m2ux/prosiform/tree/main |
| Earlier illustration | https://github.com/m2ux/prosiform/blob/dfa94f71b/docs/images/compilation.png |
| Illustration implementation | https://github.com/m2ux/prosiform/commit/fac70a9403370a12a84da473e379367d77b0a3e8 |
| README implementation | https://github.com/m2ux/prosiform/commit/9a2b1f13e96a81d9450ce56b0f08ae38aac60d9a |
| Pull request | https://github.com/m2ux/prosiform/pull/652 |
| Full CI | https://github.com/m2ux/prosiform/actions/runs/41850363720 |
