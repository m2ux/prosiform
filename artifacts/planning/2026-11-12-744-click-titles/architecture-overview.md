# Architecture Overview — Click Titles

> architecture-overview · [m2ux/prosiform#744](https://github.com/m2ux/prosiform/pull/744) · 2026-11-12 · revised 2026-11-13

## Summary

The pull request reads a Mermaid `click` line's or class diagram `link` line's quoted tooltip as its link's operator and title. Marks opening the tooltip, followed by a blank or its end, are the operator; the rest selects presets. So `click Intake href "intake.md" "⇉"` bundles as a dispatch and `"¬"` as a deferral. A new `marks` module holds the operator marks, the source model splits each tooltip once, and every consumer of a link's opening or title reads that split. A refusal names a click by its keyword and node, as `click Plan`; a tooltip of marks alone leaves its link no title; and a Gantt chart's click is read only as `click <task> href "<destination>"` alone, the one form Mermaid's gantt grammar parses. The corpus gains a fixture per rule, and the documentation states the rule in Diagram links. It builds epic [#739](https://github.com/m2ux/prosiform/issues/739)'s rows W01 to W03 and the fixes two independent review rounds asked for (#746, #748, #749).

## Structure

The graph places `tooltip` under a single caller, `read_diagram`, and `opened` under `tooltip` and the closure and rewrite readers. Every flow the change touches runs through `uses` or `read_diagram`; the consumers below are the callers the graph reports for those two and for `clicks`.

```mermaid
---
title: Components — Click Titles (graph-measured callers)
---
flowchart LR
    subgraph Marks [marks.py]
        Opened[opened]
        Tip[tooltip]
    end

    subgraph Source [source.py]
        Read[read_diagram]
        Linked[linked]
        Click[Click: node, opening, title, name]
        Uses[uses]
    end

    Profile[profile.diagram_refusals]

    subgraph Consumers [readers of a click]
        Closure[closure: operators, refusals]
        Cli[cli: refusals, picks, withheld]
        Dispatch[dispatch.written_in]
        Compose[Composing.directives]
        Bundle[bundle.rewrite]
        Cand[candidate: carried, intended]
    end

    Prov[provenance.click_at]

    Linked -->|node, tooltip, name, gantt form| Read
    Read -->|tooltip text| Tip
    Tip -->|marks| Opened
    Read -->|clicks| Click
    Read -->|unparsed Gantt clicks| Profile
    Click -->|use with name and tags| Uses
    Uses -->|opening, tags| Closure
    Uses -->|opening, name, tags| Cli
    Click -->|dispatched link| Dispatch
    Click -->|directive| Compose
    Click -->|destination| Bundle
    Click -->|opening, title| Cand
    Prov -->|location| Compose
    Prov -->|location| Bundle
    Prov -->|location| Cand
    Closure -->|link text| Opened

    style Opened fill:#c8e6c9,stroke:#2e7d32
    style Tip fill:#c8e6c9,stroke:#2e7d32
    style Prov fill:#c8e6c9,stroke:#2e7d32
    style Profile fill:#fff3e0,stroke:#ef6c00
    style Cli fill:#fff3e0,stroke:#ef6c00
    style Read fill:#fff3e0,stroke:#ef6c00
    style Linked fill:#fff3e0,stroke:#ef6c00
    style Click fill:#fff3e0,stroke:#ef6c00
    style Uses fill:#fff3e0,stroke:#ef6c00
    style Dispatch fill:#fff3e0,stroke:#ef6c00
    style Compose fill:#fff3e0,stroke:#ef6c00
    style Bundle fill:#fff3e0,stroke:#ef6c00
    style Cand fill:#fff3e0,stroke:#ef6c00
    style Closure fill:#f5f5f5,stroke:#9e9e9e
```

Green is new, orange changed, grey a caller reading the changed result unchanged.

### Operator marks

- **`marks.opened`.**
  Reads the run of operator marks a link's text opens with and where its text begins. It moved here from `closure.py` unchanged, so the source model can use it without importing the closure.
- **`marks.tooltip`.**
  Splits one tooltip into an *opening* (the text the operator readers read, as they read a link's text) and a *title*. An all-marks tooltip is closed with a blank, so `"⇉"` opens as `"⇉ "` with no title; a mark followed directly by text opens nothing and the whole tooltip is the title.

### Source model

- **`QUOTED`, `CLICK_LINE`, `CLASS_LINK`.**
  Capture the tooltip and the node the line is drawn on. `GANTT_CLICK` is the one Gantt line Mermaid parses, `click <task> href "<destination>"` alone.
- **`Click`.**
  Gains `node`, `opening`, `title` and `name`, the keyword as written and the node. A sequence diagram's `link` and `links` carry none.
- **`read_diagram`.**
  Sets a Gantt click written any other way aside as unparsed: a tooltip, a link target, a `;` or a missing `href`.
- **`uses`.**
  Yields a click with its opening, its name and tags read from its title, except a remote destination, which selects nothing. `Use.name` is a link's opening and a click's keyword and node.

### Consumers

- **`dispatch.written_in`.**
  Walks fences as well as inline blocks; `dispatched_link` builds a dispatched link from either. A click's link text is its node, since a tooltip may be all marks.
- **`Composing.directives`.**
  Walks fences too; `directive` resolves either form into a composition directive, located by `click_at`.
- **`bundle.rewrite`.**
  Rewrites a click's destination through `target` with its opening, tags and dispatch map, or to its contribution heading where it composes; the tooltip is left as written.
- **`candidate`.**
  `carried` gives a click use its opening as text and its title, `positions` locates it by `click_at`, and `intended` and `withdrawn` keep its tooltip and the line's destination as the bundle writes them.
- **`profile.diagram_refusals`.**
  Refuses an unparsed Gantt click naming a local Markdown document under `E_UNSUPPORTED_CONSTRUCT`; a remote one is carried as written.
- **`cli` refusals.**
  The operator, pick and directive refusals name a use by `Use.name` in their messages; the combination and pick refusals carry it as `reference`, and the target and directive refusals keep the destination there.
- **`provenance.click_at`.**
  Locates a diagram link by its line, column 0 and its destination's offset, which tells apart two links on one line.

## Behaviour

The graph reports 453 affected flows; each passes through `uses`, `read_diagram`, `linked` or `opened`, as in `Compose → Diagram` and `References → Diagram`. The order for one click is:

```mermaid
sequenceDiagram
    participant F as mermaid fence
    participant S as source.read_diagram
    participant M as marks.tooltip
    participant U as source.uses
    participant C as closure / cli
    participant B as bundle.rewrite
    F->>S: click Intake href "intake.md" "⇉"
    S->>M: tooltip "⇉"
    M-->>S: opening "⇉ ", title ""
    S-->>U: Click(destination, node, opening, title)
    U->>C: Use(opening, tags)
    C-->>C: operator refusals, pick refusals, withheld
    C->>B: dispatch map for intake.md
    B-->>F: destination replaced, tooltip as written
```

- **Read.**
  The fence line yields destination, node and tooltip; the tooltip is split once.
- **Refuse.**
  The closure and command read the opening exactly as a link's text opening, so `"¬ ⇉"`, `"¬⇉"`, `"⇉⫽"`, `"⇉↳"` and `"⫽↳"` are refused with the click's line and its name, `click Intake`, and `?` is refused on any operator but a deferral.
- **Publish.**
  Only the destination changes: to a bundle file, a dispatch-set sub-section, a deferral's working-directory path, or a contribution heading.
- **Validate.**
  Candidate validation compares the click's opening, title and destination, so a tooltip the bundle changed fails `reference preservation`.

### Gantt click

```mermaid
sequenceDiagram
    participant F as gantt fence
    participant S as source.read_diagram
    participant P as profile.diagram_refusals
    participant B as bundle.rewrite
    F->>S: click freeze href "freeze.md"
    S-->>B: Click, destination rewritten
    F->>S: click freeze href "freeze.md" _blank
    S-->>P: unparsed click
    P-->>F: E_UNSUPPORTED_CONSTRUCT naming the line
```

- **Accept.**
  The line `click <task> href "<destination>"` alone is a click like any other, its destination rewritten.
- **Refuse.**
  Any other Gantt click naming a local Markdown document is refused, since Mermaid draws no chart from it.

## What Changed

### Source model

- **The tooltip is captured and split once.**
  A click's opening and title come from one `tooltip` call, which every reader shares; marks alone leave no title.
- **A Gantt click is read in its href form alone.**
  Every other Gantt click form is set aside, and refused where it names a local document.

### Operators on clicks

- **Every operator applies to a click.**
  Dispatch, parallel sets, composition and deferral, with their refusals, read a click's opening as a link's.
- **A click's dispatch-set entry names its node.**
  The set lists a dispatched click by the node it is drawn on.
- **A refusal names the click.**
  Its message names a click by its keyword and node.

### Presets on clicks

- **The tooltip's title selects presets.**
  It carries the pick token as a link title does; a click carrying no tooltip selects none.

### Corpus

- **One fixture per rule.**
  Fixtures cover each operator on a click, the pick token, a class diagram `link`, each refused combination, the directive and target refusals and every Gantt refusal; `diagram-tooltips-supply-no-preset-selection` is removed.

### Documentation

- **Diagram links states the rule.**
  Operators, Selection by reference, the glossary's pick and Selection link it, and every design link pins `17c1f6e2f`.

## Reading Order

1. **[marks.py](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/marks.py#L42-L92)** — `opened` and `tooltip`: the one split every reader takes.
2. **[source.py: QUOTED and the line patterns](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/source.py#L161-L172)** — the captured node and tooltip, and the one Gantt form.
3. **[source.py: read_diagram and linked](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/source.py#L893-L1130)** — where a `Click` takes its opening, title and name, and a Gantt click is set aside.
4. **[source.py: uses](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/source.py#L1260-L1343)** — the click as a use, its tags read from its title.
5. **[profile.py: diagram_refusals](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/profile.py#L539-L604)** — the Gantt refusal.
6. **[cli.py: refusals_of_operators to composing_itself](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/cli.py#L1692-L2012)** — the refusals naming a click.
7. **[dispatch.py: written_in and dispatched_link](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/dispatch.py#L415-L503)** — dispatched clicks.
8. **[composition.py: directives and directive](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/composition.py#L300-L376)** — composing clicks.
9. **[bundle.py: rewrite](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/bundle.py#L643-L671)** — the destination rewritten as the operator states.
10. **[candidate.py: carried to withdrawn](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/prosiform/candidate.py#L349-L515)** — validation holding the tooltip as written.
11. **[test_cli.py](https://github.com/m2ux/prosiform/blob/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/src/tests/test_cli.py)** and **[the click fixtures](https://github.com/m2ux/prosiform/tree/0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2/fixtures/dispatch)** — the published bytes for each operator.

## Risks and Watch Points

- **An all-marks tooltip carries a closing blank in its opening.**
  The operator readers read it; no diagnostic shows it, since a refusal names the click by `Use.name`.
- **Fence walking replaced inline walking in dispatch and composition.**
  `written_in` and `directives` iterate `within` and branch on token type in place of `inlines`; inline links are found as before only while `within` yields every inline token `inlines` did. The unit, harness and corpus runs hold this.
- **Diagram link locations share the link location key.**
  `click_at` keys a click by its fence line, column 0 and destination offset; no inline block opens on a fence line, so it cannot collide with `link_at`.
- **The Gantt form is matched on the whole line.**
  `GANTT_CLICK` reads the line, so two statements on one Gantt line are both unparsed, as Mermaid's grammar has them.
- **A remote click's tooltip still opens an operator.**
  Its tags are dropped, but its opening reaches the operator refusals, which refuse an operator naming a remote address, as for a link.

## Measurements

- **Revision.** Index built with `gitnexus analyze --index-only` in the review worktree at `0ee5b6fcf657958d39a50bdb3cc55fedb7cc47c2`; 7,030 nodes, 17,702 edges, 491 flows.
- **Comparison base.** Merge base of head and `main` is `4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d`, the base itself.
- **Change surface.** `detect-changes --scope compare --base-ref 4cb6b5c4e`: 121 files, 77 changed symbols (documentation sections among them), 453 affected flows, risk critical: the flows run through the source model's diagram reader, which every compilation reaches.
- **Symbol context.** `tooltip`: one caller, `read_diagram`; calls `opened`. `opened`: callers `closure.gapped`, `operators`, `published_text`, `unmarked`, `marks.tooltip` and `rewrite.edits`; 13 flows. `read_diagram`: caller `linking`; calls `tooltip` and `linked`. `uses`: callers in `cli` (composing_itself, linked, refusals_of_directives, refusals_of_operators, refusals_of_picks, required, resourced, withheld) and `closure.boundary`.
- **Tree.** The head's tree equals #749's head `565724036`, the revision `make check` passed at.

## References

- **R1.** [Epic #739](https://github.com/m2ux/prosiform/issues/739) — acceptance criteria AC1 to AC6 and the Work Breakdown.
- **R2.** [#743](https://github.com/m2ux/prosiform/pull/743) — the build and fixtures (W01, W02).
- **R3.** [#745](https://github.com/m2ux/prosiform/pull/745) — the documentation (W03).
- **R4.** [#746](https://github.com/m2ux/prosiform/pull/746), [#748](https://github.com/m2ux/prosiform/pull/748) and [#749](https://github.com/m2ux/prosiform/pull/749) — the fixes of the two independent review rounds.
- **R5.** [Design: Link classification](https://github.com/m2ux/prosiform/blob/17c1f6e2f/artifacts/planning/2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling) — the rule the build implements.
