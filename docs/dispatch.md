# Dispatch

Not every link points at material for the reader of the bundle. A guide might say "for the review pass, follow the review procedure" — and the review belongs to a different agent, run at a different time, with its own context.

Sending it anyway would pad the bundle with instructions nobody is about to follow. Leaving it out entirely would lose the procedure. A **dispatch** is the third option: the material is compiled as a bundle of its own, and the bundle that linked it says which one to hand over.

## What it looks like

One step of a procedure carries the mark. The run opens three files, and publishes two bundles: the entry's, which links the second, and the second on its own.

![The three source files on the left — modes/review.md, rules.md and protocols/publish.md — and on the right the two bundles the run wrote. modes_review.bundle.md opens with the run-pf line, then Review Mode with its procedure, the dispatch link to protocols_publish.bundle.md, and the Tests section of rules.md. protocols_publish.bundle.md opens with the run-pf line, then holds Publish alone.](images/dispatch.svg)

*Every panel is the build's own output: the left column is what the run read, the right what it wrote.*

The entry's bundle keeps the link where its author wrote it, with its mark, and points it at the file `Publish` was compiled to, as if it had been asked for on its own. A reader opens the file the link names, and an agent follows it as the [guide](../invocation.md#guide) states: give a sub-agent the linked file's path, with the inputs the dispatching step states as given, and continue with its answer. A condition the author writes stays in the prose around the link.

## What a dispatch changes

A `⇉` or `⫽` link contributes nothing to the bundle that carries it: no content, no dependency through the link, no group membership. Its target is required to exist, to declare `prosiform` and to name the heading it names, because a sub-agent will follow it and the compilation must be able to succeed.

The run compiles each distinct effective selection once, transitively: a dispatched bundle's own dispatches are further bundles in the same run folder. The selection comprises the canonical document, fragment and matching named presets. Two dispatches of one destination selecting different named presets produce distinct bundles, even if their settings happen to agree; reordered, repeated, differently cased and unknown tags add no variant. Every dispatch names its selection's bundle file, whose deterministic preset qualifier [Bundles](bundles.md#derived-names) defines.

A dispatch is compiled up front, so a deferral mark has nothing to defer: `[¬⇉ the lift](lift.md)` and `[¬⫽ the lift](lift.md)` are refused, as [References](references.md#operators) states.

Each bundle is compiled under every rule an entry's is. Budgets hold per bundle, so `depth` counts hops from that bundle's entry and the others count what that bundle alone opens, reaches and publishes.

## Where the links point

A `⇉` link publishes in place with its mark and the one blank after it, pointing at its target's bundle file. Unless it carries a [brief](#briefs), a section gains no generated structure for it, and a dispatch in a level-6 section publishes like any other.

A `⇉` link whose title carries the [pick token](references.md#the-pick-token) `?` leaves its pick to the agent that dispatches it. The run compiles its target once for each alternative the target declares, each a bundle of its own, as a link naming that alternative does, and any other name beside `?` selects the target's ordinary preset in every one of them. The section writing the link gains one dispatch-pick sub-section for it, headed `⇉ Dispatch Pick`, placed as a set's sub-section is and after it. Its body holds one dispatch line for each alternative, in declaration order, followed by an em dash and the alternative's choice line:

```markdown
### ⇉ Dispatch Pick

[⇉ Stage](stage--p-9aae….bundle.md) — One pull request's worth of work.
[⇉ Stage](stage--p-3d08….bundle.md) — Lists its tasks in a Work Breakdown table.
```

The link itself is published without its mark, its title as authored, pointing at the sub-section, and the agent hands on the one bundle whose choice line fits its work, as the guide states. A `⫽` link carrying `?` is refused, because a set hands on every member and no agent is left to pick.

The `⫽` links in a section's own content are one **set**, and a child section's links form its own. A set of two or more distinct effective selections gains one dispatch-set sub-section, headed `⫽ Dispatch Set`, one level below the section, after the section's own content and any destination sections [composition](composition.md#where-it-lands) places there, and before its child sections. The set's links are published without their marks and point at it. A set of one distinct effective selection is a single dispatch: each of its links is published as a `⇉` link to the target's bundle file, and the section gains no sub-section.

```mermaid
flowchart TD
  Section["## Plan Mode"] --> Own["its own content"]
  Section --> D2["### ⫽ Dispatch Set"]
  Section --> Child["### child sections"]
  D2 --> B2["modes_review.bundle.md"]
  D2 --> B3["modes_audit.bundle.md"]
```

*Figure 1. A Set's Sub-Section Sits Between a Section's Own Content and Its Child Sections.*

The sub-section's body holds one bare dispatch-link line for each distinct effective selection, in the order its first link is written: `[⇉ the lift](lift__do.bundle.md)`, the first link's text without its mark. It carries no bullet marker or instruction sentence; the guide states how to dispatch its members. A set states no order. A set above a group's first heading takes that heading's level.

A run carrying both kinds shows them together. Two `⫽` links form one set and publish one bundle each; a `⇉` link on its own publishes a third and stays where it was written:

![modes/review.md and three protocol files on the left. On the right, four panels: the entry's bundle with an inline dispatch link to publish and a dispatch-set sub-section listing two bundles, then code, tests and publish each as a bundle of their own.](images/parallel.svg)

*The entry's bundle links what to hand over; the three procedures are compiled as if each had been asked for on its own.*

A set, a `⇉` link carrying `?`, or one carrying a brief, whose sub-section would stand past H6, in a level-6 section or nested in a brief's or a set's sub-section, leaves no level for it, so the run fails rather than inventing one. A dispatched link with no text after its mark shows its reader nothing, and is refused too.

A dispatch in a heading the bundle emits as text alone has no link to publish, so the run publishes nothing and fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link. Such a heading is a referenced document's title its file heading absorbs, a merged group member's title its subsection absorbs, or a title standing above the selection. The entry's own title heads its bundle, so a dispatch there publishes. Its author writes the dispatch in the body beneath the heading.

## Briefs

A target can state what its dispatcher must do before handing it on: the inputs it needs written down, a check to run first. Its preset names that section as a **brief**, a fragment of its own document, as [Sources](sources.md#frontmatter) states:

```yaml
prosiform:
  default:
    brief: "#given"
```

A dispatch whose presets in force for its target name a brief carries it. In `default`, every dispatch of the target does; in a named preset, a dispatch selects it by its link title, and one selecting no preset declaring `brief` publishes as the sections above state. A named preset's brief holds over `default`'s, and two selected presets naming different briefs fail with `E_INVALID_USAGE`, naming both.

A `⇉` link carrying a brief, and a set of one, is lifted into a sub-section one level below the section writing it, headed by its mark and its link text, as `### ⇉ Investigate`. Its body is the brief's lead content, the content above its first heading, then the dispatch line naming the target's bundle file, then the brief's child sections and the sections its directives compose, each one level below the sub-section. The dispatch line therefore stands under no heading the brief emits, and its reader meets the brief's own instruction first. The link is published without its mark, its title as authored, pointing at the sub-section, and so is a diagram link naming it. The sub-section stands where a dispatch-set sub-section does, after the section's own content and composed destinations and before its child sections, after the set's own sub-section and beside the section's dispatch-pick sub-sections in the order their first links are written:

```markdown
## Plan

1. [Investigate](#⇉-investigate)

### ⇉ Investigate

Write the case number to the case file before you dispatch.

[⇉ Investigate](investigate.bundle.md)
```

*From [a-dispatch-to-a-target-declaring-a-brief-is-lifted-into-a-sub-section](../fixtures/dispatch-brief/a-dispatch-to-a-target-declaring-a-brief-is-lifted-into-a-sub-section).*

```markdown
### ⇉ Investigate

Write the case number to the case file, then [Tests](#rules).

[⇉ Investigate](investigate.bundle.md)

#### Tests

##### Rules

Run the tests.

#### Case

The case number is on the ticket.
```

*From [a-brief-s-sections-follow-its-dispatch-line](../fixtures/dispatch-brief/a-brief-s-sections-follow-its-dispatch-line).*

The brief is compiled as a `↳` composition of its section is, under the presets its dispatch selects: its links resolve through those presets' `subst` pairs layered over the target's `default`, as [Composition](composition.md#presets-and-subst) states for a contribution, and are followed into the dispatching bundle's closure, its own heading gives way to the generated one, and its child sections nest one level below it. The target's own bundle carries the section unchanged. Every dispatch of a briefed target carries its own complete copy of the brief, alike in content but for the links its own dispatch's presets route, its headings at the level its copy stands at; two dispatches sharing a sub-section share one copy. A link the brief writes to one of its own child sections points at that child in the same copy. A region a `↳` composition copies more than once is the exception for dispatches: a later copy points its dispatches at the places its first copy gave them where they name the targets the first copy's dispatches name, and a copy whose presets route them elsewhere places its own. Two copies routing one briefed dispatch apart would lift one heading naming two bundles, so the run fails with `E_HEADING_COLLISION`, as two dispatches of one text naming two selections do.

A dispatch the brief writes is a dispatch of its own: it compiles its own bundle and publishes where the brief writes it, a brief its target declares lifted by the same rules, its sub-section one level below the one holding the brief, after the brief. It is never a member of a set around the brief. A brief whose dispatches carry briefs leading back to it would be lifted inside itself without end, so the run publishes nothing and fails with `E_DISPATCH_CYCLE`, naming the chain, as `guide.md`, `a.md`, `b.md`, `a.md`, and the dispatch closing it.

A `⇉` link carrying `?` places its brief in its `⇉ Dispatch Pick` sub-section around the pick lines, as a lifted sub-section places it around its dispatch line: the lead content above them, the child sections beneath. The brief compiles with no alternative in force, so it publishes where no alternative changes it, as [Presets in force](selection.md#presets-in-force) states for a link, and the run fails with `E_ALTERNATIVE_UNRESOLVED`, listing the alternatives, where one changes it: an alternative routing a link the brief writes, or one naming a brief of its own.

In a `⫽ Dispatch Set` sub-section holding a member that carries a brief, every member is lifted into a sub-section of its own one level below the set's, headed by its mark and link text, as `#### ⇉ Investigate`, in the set's written order. A briefed member's sub-section holds the brief's lead content, the member's own dispatch line, and the brief's sections one level further down; a member carrying no brief holds its dispatch line alone. Each member's line therefore stays with its brief, and no line stands beneath another member's headings. A set none of whose members carries a brief lists its bare lines as the sections above state.

Two `⇉` links in one section with the same text and effective selection share one sub-section, and so do two naming one target with the same title tags, under the first one's text, as they share one destination. A lifted sub-section, or a heading a brief emits, past H6 fails with `E_HEADING_DEPTH_OVERFLOW`, as a set's does. A lifted heading equal to an authored heading, to `⇉ Dispatch Pick`, or to another lifted heading naming a different selection fails with `E_HEADING_COLLISION`. A `brief` naming another document, or a fragment no reference decodes, fails with `E_INVALID_CONVERSION_METADATA`, and one naming a heading its document lacks with `E_TARGET_NOT_FOUND`. A `brief` in force for a link that is no dispatch has no effect.

## The guide

The rules for following a bundle live in the guide `pf` prints with no arguments, as [Invocation](../invocation.md#guide) states, and in no bundle: what `↳`, `⇉` and `⫽` ask of an agent, what `?` on a `⇉` link asks of it, that a brief, the text above a `⇉` line in the sub-section a link points at and the sections beneath that line, is done before that bundle is handed on, and how a bundle is handed over. A bundle travels by its path: a sub-agent is given the path of the bundle file and reads it there. Its inputs are those the dispatching step states as given. How a sub-agent's question reaches the user is agent conversation rather than compiled form, so the guide states no marker and no protocol for it.

## The run-pf line

Every bundle a run writes opens with one line, whatever it holds, followed by one blank line: ``Run `pf`, then follow the guidance it prints.`` It is the bundle's first bytes, ahead of any preamble content and every heading, in wording the profile fixes. A bundle carries no protocol paragraph and no section that restates the guide, so a reader holds [the guide](#the-guide)'s rules before it meets a `↳` line, a `⇉` link or a dispatch-set sub-section.

## Depth and cycles

**Dispatch depth** is the number of dispatch hops along one chain, counted from the run's entry. A chain reaching a fourth hop warns: flattening the chain is the author's optimisation rather than a defect in the bundle, so the run publishes and says so.

A chain returning to a bundle already on it is a **cycle**, and the run fails with `E_DISPATCH_CYCLE`; a dispatch naming the run's own single selection closes the shortest one. Neither search follows a target already on its chain, so the analysis terminates on any graph of dispatches.

```mermaid
flowchart LR
  Entry["entry bundle"] --> H1["hop 1"]
  H1 --> H2["hop 2"]
  H2 --> H3["hop 3"]
  H3 --> H4["hop 4<br/>W_DISPATCH_DEPTH"]
```

*Figure 2. A Chain Reaching a Fourth Hop Publishes and Warns; the Limit Is Fixed.*


A dispatched link naming the document that writes it warns where it closes no cycle: the sub-agent is being handed material the dispatching session's own document already carries. Its author moves the procedure to a document of its own, or links it without the operator.

## Generated headings

An authored heading whose text equals the dispatch-set, dispatch-pick or a lifted [brief](#briefs) heading pf emits in the same bundle would give two sections one name, so the run refuses it with `E_HEADING_COLLISION`, naming the heading and the text it equals.

The comparison is exact, and case-sensitive: an authored heading differs from the derived one in any character publishes, and takes the ordinal the renderer gives a repeated slug.

A heading the run does not emit in that bundle is the author's there: a bundle carrying no set and no `⇉` link carrying `?` may carry any heading, `In parallel` among them.

## Target shape

A dispatch hands a procedure to a sub-agent, and a target that carries no numbered step gives the sub-agent nothing to follow. The corpus treats that as a convention rather than a defect: it compiles with no diagnostic. The same holds for a `⫽` target holding a paragraph, a numbered list, or an item linking no document.
