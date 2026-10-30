# Mermaid Link Survey

Each diagram type in Mermaid 11.16.0, read from its parser and renderer in the published `mermaid` package, against the diagram links `skill-markdown-v2` reads.

## Read by v2

| Diagram | Form |
| --- | --- |
| Flowchart, swimlanes | `click <id> [href] "<url>" ["<tooltip>"] [<target>]` |
| State | `click <id> href "<url>"`, `click <id> "<url>" "<tooltip>"` |
| Gantt | `click <task> href "<url>"` |
| Class | `click <class> href "<url>"` |

## Rendered as Links, Read by This Epic

| Diagram | Form | Grammar |
| --- | --- | --- |
| Class | `link <class> "<url>" ["<tooltip>"] [<target>]` | `LINK` token, `setLink` |
| Sequence | `link <actor>: <label> @ <url>` | `addALink`, split at the first `@` |
| Sequence | `links <actor>: {"<label>": "<url>", …}` | `addLinks`, `JSON.parse` |
| Every type above | Keywords in any case | Lexer rules carry the `i` flag |

## Out of Scope

| Diagram | Form | Why |
| --- | --- | --- |
| C4 | `$link="<url>"` | Parsed and stored; the renderer draws no anchor |
| Block | Node link | The renderer can draw one; the grammar has no statement setting it |
| Kanban | `ticket` with `kanban.ticketBaseUrl` | The URL is built from configuration, not written |
| Any with HTML labels | `<a href>` in a label | A label's HTML, not diagram syntax |

## No Link Syntax

ER, requirement, mindmap, timeline, pie, quadrant, xy chart, sankey, git graph, journey, architecture, Venn, Ishikawa, Wardley, Cynefin, railroad, ABNF, EBNF, PEG, tree view and info. Sankey's and Wardley's `addLink` is an edge, not a URL.
