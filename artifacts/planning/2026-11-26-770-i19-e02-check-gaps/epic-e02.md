## Overview

This epic closes the cases the repository checks still miss after the repository checks epic delivered their rules. Each row is a case its delivering session found and left outside its criterion: a construct the link check still passes over, a build word and avoided terms the vocabulary rules still admit, and a caller the reachability check counts by name alone. Within the initiative it is the remainder that makes every check exact.

## Problem

The rules the repository checks epic delivered hold for the cases their criteria named, and four neighbouring cases slip through.

- **A fenced block inside a list item is read as content.**
  [The fence reading](https://github.com/m2ux/prosiform/blob/6eb02cb5c44bf8942ad16e5c4e6104438a969438/checks/documents.py#L109-L115) recognises a fence at the left margin alone, so a link form inside an indented fence is resolved as a reference.
- **A build word the design states in a behavioural section passes.**
  "no specific slugger crate is selected yet" sits under source-heading resolution, so the independence check admits "crate", the example the vocabulary row was raised for.
- **Avoided terms survive in fixture identities.**
  The avoided-term rule reads descriptions; identities such as `the-sibling-once-closure-includes-it` and `an-html-anchor-*` still state them.
- **A variable counts as a caller.**
  [The reachability check](https://github.com/m2ux/prosiform/blob/6eb02cb5c44bf8942ad16e5c4e6104438a969438/checks/reachability.py#L51) compares names, so a definition is reached when any variable of that name is written, as `cli.Parser.error` is by `except OSError as error`.

## Proposal

- **The shared reading finds fences with the build's parser.**
  The parser that finds indented code blocks also finds fenced ones, wherever they are indented.
- **Build obligations sit in sections stating no behaviour.**
  The design's sentences on a build's packaging and parser move into a section the conformance report records as stating no behaviour, and the README pins the revised design.
- **The corpus's identities obey the avoided-term rule.**
  Fixtures whose identities state an avoided term are renamed, and the rule reads identities beside descriptions.
- **A caller is a call or a reference to the definition.**
  The reachability check counts a definition reached where the package calls it or names it through its module, class or import, not where a local variable shares its name.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e02-check-gaps/w01.md) | Fenced blocks indented inside list items | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e02-check-gaps/w02.md) | Build obligations in silent design sections | AC2 | | W03 | | |
| [W03](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e02-check-gaps/w03.md) | Avoided terms in fixture identities | AC3 | | W02 | | |
| [W04](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e02-check-gaps/w04.md) | Callers resolved beyond a shared name | AC4 | | | | |

## Acceptance Criteria

- [ ] **AC1.** A fenced block indented inside a list item is passed over by the link check while the item's own content is read, as the shared reading's own tests show.
- [ ] **AC2.** A fixture declaration naming a word that states a build's packaging or parser, "crate" among them, is reported by the independence check, as its run over a corpus declaring one shows.
- [ ] **AC3.** No fixture identity states a term `docs/glossary.md` names as deliberately not used, as the independence check over the corpus shows.
- [ ] **AC4.** A definition whose name the package writes only as a local variable, parameter or exception name fails the reachability check, as its tests show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e02-check-gaps) — each row's work item and where its case was found.
