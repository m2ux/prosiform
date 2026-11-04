# README Compilation Illustration — November 2026

> Documentation · Created 2026-11-04

## Executive Summary

The README introduces compilation through a detailed drawing of source documents and their bundle. The illustration uses the current `run` example and the output of the compiler at `11a872918669362260cf16b875694342f262d2c2`.

The selected direction uses the earlier illustration's connected panels, readable type and clear visual hierarchy. File links are traced to their destinations in the source tree and in the bundle.

## Todo

- [x] Inspect the published README, earlier illustration and current example.
- [x] Render the connected layout from a real compiler run.
- [x] Inspect the image at README width and verify content and regeneration.
- [ ] **In progress:** Publish the committed branch and its review handoff.

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

## Links

| Resource | Link |
| --- | --- |
| Published README | https://github.com/m2ux/prosiform/tree/main |
| Earlier illustration | https://github.com/m2ux/prosiform/blob/dfa94f71b/docs/images/compilation.png |
| Implementation | https://github.com/m2ux/prosiform/commit/fac70a9403370a12a84da473e379367d77b0a3e8 |
