# Selection

A run resolves what was asked for, and everything reachable from it, into one **selection** per region. Order and grouping are decided afterwards, from that selection.

## Closure

The run starts at the **entry references**, the arguments on the command line, and follows each dependency the selected content carries. It repeats until nothing new is reachable. The result is the **closure**.

Fragment-only references resolve against their own source document wherever that source sits, including outside its own root. A link to a sibling section of the same document is an ordinary reference; it is not a self-reference unless it names the region it sits in.

A reference back to material the closure already holds resolves to that material's destination. It expands nothing twice.

## Consolidation

Selections overlap. Asking for a section and then for its parent document would otherwise emit the section twice.

**Consolidation** unions the overlaps, so each region appears once and the larger region wins. A child selection is satisfied by its parent. Destinations are assigned from the target a reference resolved to, not from the region the reference sits in, so consolidating a child into a larger region leaves every destination as it was.

Reachability is settled before any output is arranged. A source newly included by an expansion has its own dependencies followed before the run declares the closure complete.

## Placement order

Sources are placed in the order the first reference names them: the entry references in command-line order, then each placed source's selected content in turn, in source order.

That order is the author's, not the discovery's. A preamble reading

```markdown
Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).
```

places Rules and then Conventions directly after the entry document's own sections. Writing the links in a different order writes a different bundle.

A group stands where its first source is placed.

## Structural ancestors

Selecting `Detail` from an outline of `## Alpha`, `## Beta`, `### Detail` leaves `Beta` with no content to contribute. The bundle keeps `Beta` as a heading and nothing else:

```markdown
### Alpha

Selected Alpha content.

### Beta

#### Detail

Selected Detail content.
```

That heading is a **structural ancestor**: generated structure, not a dependency. Its body is not included, its own links are not followed, and it is not a substitute for selecting its section.

Two rules keep ancestors honest:

- Each is emitted once. If discovery later selects it as content, the heading is replaced by the real one with its body rather than published twice.
- An ancestor the generated file heading already names is not emitted at all, since the file heading stands in its place.

## Boundaries

Selected regions are separated by blank lines, and the candidate is reparsed. A boundary that would absorb content into an unintended code fence, list, block quote or HTML block is refused rather than repaired. The run does not close a fence its author left open.

## What is not a dependency

Only linked material is included. A shared rule reaches a bundle because a procedure links it; it is not inferred from a filename, a heading, or a document's position in a directory tree.

Inclusion makes material available. It does not authorize executing every procedure the bundle now contains, and the run makes no claim about whether an agent obeys it.
