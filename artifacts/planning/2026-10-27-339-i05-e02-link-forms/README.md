# I05:E02 Link Forms — October 2026

> Epic planning · Created 2026-10-27

## Executive Summary

This record holds the plan for I05:E02: every link form Mermaid 11.16.0 renders as a followable link is read as a diagram use, so the document it names is bundled and the link points at that document's group. `skill-markdown-v2` reads `click` lines alone; a class diagram's `link` line, a sequence diagram's `link` and `links` participant menus, and any-case keywords are carried as text.

The epic is three tasks sharing one pull request. W01 widens the click pattern to class `link` and any-case keywords; W02 reads sequence participant menus, several destinations to a line; W03 renames the profile to `skill-markdown-v3` and states the rule. Every behaviour a source tree can produce is proven by an end-to-end corpus fixture.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The class `link` form and any-case keywords |
| [W02 work item](w02.md) | Sequence participant menus, `link` and `links` |
| [W03 work item](w03.md) | The `skill-markdown-v3` profile and its bundling rule |
| [Survey](survey.md) | Every Mermaid 11.16.0 diagram type, the link forms it renders, and which this epic reads |

## Decisions

- **A new epic, not a fix to E00.** E00 planned the `click` forms and is released; the further forms are a further enhancement.
- **Profile v3.** v2 shipped in v0.13.0, and the same source bundles differently under the wider reader.
- **Three rows, one pull request.** The work exceeds one row's three-criterion grain; W01, W02 and W03 join so one pull request delivers the epic.
- **Any-case keywords proven end to end.** A source tree can write them, so I05's AC1 calls for a corpus fixture.
- **A `links` value holding a JSON escape is carried as written.** Its source text differs from its destination, so there is no span to rewrite.
- **Priority 8.** No edge to E01 and no shared component, so E02 runs alongside it.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E02 Link Forms](https://github.com/m2ux/prosiform/issues/339) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
