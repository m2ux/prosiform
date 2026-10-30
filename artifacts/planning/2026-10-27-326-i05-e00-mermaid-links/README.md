# I05:E00 Mermaid Links — October 2026

> Epic planning · Created 2026-10-27

## Executive Summary

This record holds the plan for I05:E00: a `click` link in a `mermaid` fence read as a use, so the document it names is bundled and the click destination points at that document's group in the bundle. It is the first epic of I05, the standing initiative for ad hoc feature enhancements, which stays open as its epics close.

The epic is four tasks. W01 reads diagram links and counts them against the budget; W02 rewrites their destinations; W03 holds them in candidate validation and W04 renames the profile to `skill-markdown-v2` and states the rule, those two sharing one pull request. Every behaviour a source tree can produce is proven by an end-to-end corpus fixture.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The fence reader and its use in discovery and the budget |
| [W02 work item](w02.md) | Diagram destinations rewritten on emission |
| [W03 work item](w03.md) | Diagram uses held by candidate validation |
| [W04 work item](w04.md) | The `skill-markdown-v2` profile and its bundling rule |
| [W05 work item](w05.md) | The end-to-end specimen: a diagram reached through a linked document |
| [Specimen](specimen/) | The specimen source tree and the bundle `pf guide.md` published from `i05/e00/main` |
| [Joins](joins.md) | The independent row pairs that take separate pull requests, and why |

## Decisions

- **I05 is perpetual.** It holds ad hoc enhancements and does not close with its last epic.
- **#326 is the epic.** The issue is retitled and restructured in place rather than duplicated.
- **Priority 8, Ready.** The initiative and the epic carry the highest priority label on the board.
- **End-to-end first.** Each criterion a source tree can produce is shown by a corpus fixture; unit tests carry only the reader's grammar and candidate faults no sound tree produces.
- **W03 and W04 join.** Neither depends on the other and both are small, so they share one pull request.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E00 Mermaid Links](https://github.com/m2ux/prosiform/issues/326) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
