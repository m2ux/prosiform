# References

Following a link is the whole of what a bundler does. A procedure says "adhering to the rules file", and the question is what that link means for the output: does the rules file travel inside the bundle, or is the sentence left as written?

Every link inside a source is a **reference**, and the run answers that question for each one before it compiles anything. Here one procedure carries four kinds of link, and only the first survives as a link into the bundle:

![modes/review.md and modes/rules.md on the left. On the right, the bundle: the first link rewritten to #tests, and the image, remote address and link to library/guide.md, which declares nothing, carried exactly as written.](images/references.svg)

*The first link resolved and was rewritten. The other three are text, carried byte for byte, and the run warned once that the bundle names a resource.*

## Classification

A reference is a **dependency** when it carries no scheme and no authority and names a Markdown document, or a section of one, whose leading frontmatter declares `prosiform`. A dependency is followed, its content included, and the link rewritten to the destination the bundle gives its target, as [Destinations](destinations.md) states. A composition directive is a dependency whose target lands beneath the section writing it, as [Composition](composition.md) states.

The question is asked of the target, not of the source that links it. Where either file sits decides nothing, so one document reached by two sources is one answer, and a link may name a declaring document anywhere, above the working directory included.

A `subst` pair of the writing document's presets is asked first, on the identity the reference normalized to, as [The substitution mapping](selection.md#the-substitution-mapping) states: a reference a pair redirects is a dependency on the substitute, whatever its authored path names.

Everything else is carried as text and never opened:

| Reference | What happens |
| --- | --- |
| A link to a remote address | emitted as authored; no scheme is fetched or judged |
| A link to a document that declares nothing | emitted as authored; its frontmatter is read and nothing more, so it adds no content, no group and nothing to any source budget |
| A link to a document that does not exist | emitted as authored; nothing states the bundle answers for it |
| An image, whatever it names | emitted as authored; image syntax embeds, so a document named that way is not bundleable |
| A link to a non-Markdown file | emitted as authored |

A bundle carrying an image or a link to a non-Markdown file is still a successful run, and warns once with `W_RESOURCE_PORTABILITY` that a resource it names may not be found where the bundle is read.

```mermaid
flowchart TD
  Ref["a reference in selected content"] --> Scheme{"carries a scheme<br/>or an authority?"}
  Scheme -- yes --> Text["text: carried as authored, never opened"]
  Scheme -- no --> Mapped{"a subst key of the writing<br/>document names its identity?"}
  Mapped -- yes --> Sub["substitute: resolved from<br/>the declaring document"]
  Mapped -- no --> Declares{"names a Markdown document<br/>that declares prosiform?"}
  Declares -- no --> Text
  Declares -- yes --> Dep["dependency: followed,<br/>bundled, rewritten"]
  Sub --> Dep
```

*Figure 1. A Subst Key Is Asked First, Then the Target's Declaration Decides What a Reference Becomes.*

## Selection by reference

A reference with no fragment, or an empty one, selects the whole document: its body, its preamble included, less frontmatter. A reference with a fragment selects one section — a document-level heading and its subsections, ending before the next heading of equal or higher level.

Only a heading names a section. A fragment is looked up in the original document's own heading index, exactly as spelled, so `#Run` and `#run` name different things. A fragment naming no heading in its document fails with `E_TARGET_NOT_FOUND`, one naming a heading nested inside a list or a block quote with `E_NESTED_SECTION_TARGET`, and one naming a slug two headings of the document share with `E_AMBIGUOUS_SOURCE_HEADING`.

## Operators

An operator is a mark opening a link's text, followed by a space. It states how the target is compiled, in place of the default.

| Mark | Name | States |
| --- | --- | --- |
| `¬` | **deferral** | the target is compiled by a run of its own |
| `⇉` | **dispatch** | a sub-agent follows the target |
| `⫽` | **parallel dispatch** | a sub-agent follows the target alongside the other `⫽` links of its section |
| `↳` | **composition** | the target's section is placed beneath the section writing the link |

An operator withholds what the link would otherwise add: the target contributes no content, no dependency through that link, and no group membership. Its target must still exist and must still name the heading it names, because a compilation an agent will follow is one that can succeed.

A mark on its own changes nothing but the link's own text. Placing one on the same link turns it into a dispatch, and the run publishes a second bundle rather than carrying the rules file:

![modes/review.md, rules.md and protocols/publish.md on the left. On the right, two bundles: the entry's, with a dispatch link to protocols_publish.bundle.md, and that bundle on its own holding Publish.](images/dispatch.svg)

*The link keeps its mark and points at the bundle to follow, and `publish.md` contributes no content to the bundle that linked it.*

A mark followed directly by text opens no operator. `[⇉Sync](sync.md)` is an ordinary link whose text happens to begin with an arrow, and the mark stays in the published text.

Symbols are written together, and the one blank stands between the last of them and the link's text. A deferral combines with the [composition](composition.md) mark alone, so `[¬↳ Outputs](call.md#outputs)` is a deferred composition. A dispatch is compiled up front into a bundle of its own, so `[¬⇉ Rules](rules.md)` states a dispatch no bundle publishes and is refused. A dispatch mark written against the composition mark, as in `[⇉↳ Outputs](call.md#outputs)`, is refused too: a dispatch sends the target to a sub-agent and a composition places it inline, so the two contradict. A blank between two symbols — `[¬ ⇉ Rules](rules.md)` or `[¬ ↳ Outputs](call.md#outputs)` — states no one operation and is refused, and so are two dispatch marks, `[⇉⫽ Rules](rules.md)`, which state two ways for one sub-agent to run. A link labelled with an arrow, `[→](call.md#outputs)` or `[¬→](call.md#outputs)`, is refused: composition is written with `↳`. An operator naming anything but a Markdown document or section that declares `prosiform` is refused on the same ground, and one naming a document that does not exist fails with `E_TARGET_NOT_FOUND`.

The published link carries its text without the marks and the blank after them, but a dispatch to a bundle file, which carries the dispatch mark and one blank. A deferral publishes a destination spelled from the invocation working directory, so the same command line can be run from there. A dispatch publishes a link to its target's bundle file, and a parallel set a link to its `In parallel` sub-section, which [Dispatch](dispatch.md) covers. Neither is rewritten to a destination inside the bundle, even where another reference carried the target into it: what one author withheld, another author's reference does not change.

```mermaid
flowchart TD
  Text["link text opens with marks"] --> Space{"a space follows<br/>the marks?"}
  Space -- no --> Plain["an ordinary link:<br/>the mark is text"]
  Space -- yes --> Second{"another symbol<br/>follows the space?"}
  Second -- "yes: ¬ ⇉ or ¬ ↳" --> Refused["refused: symbols<br/>are written together"]
  Second -- no --> Combined{"the marks written<br/>together"}
  Combined -- "¬⇉, ¬⫽, ⇉↳, ⫽↳ or ⇉⫽" --> Contradicts["refused: the marks<br/>cannot be carried out together"]
  Combined -- "¬, ⇉, ⫽, ↳ or ¬↳" --> Operator["an operator"]
  Operator --> Target{"names a Markdown document<br/>or section that declares?"}
  Target -- no --> RefusedToo["refused"]
  Target -- yes --> Withheld["withheld from this bundle,<br/>compiled as the mark states"]
```

*Figure 2. How a Mark at the Start of Link Text Is Read, and Where It Is Refused.*

## Diagram links

Inside a fenced block whose info string opens with `mermaid`, the destinations a diagram's link lines name are references. Each is counted against the link budget and followed like any other.

The lines are:

- `click <node> href "<destination>"` and `click <node> "<destination>"`, in any diagram
- `link <class> "<destination>"` in a class diagram
- `link <actor>: <label> @ <destination>` in a sequence diagram, whose destination is the trimmed text after the first `@`
- `links <actor>: {…}` in a sequence diagram, whose each string value is one destination

The diagram's type is the word its text opens on, once front matter, `%%{…}%%` directives and `%%` comments are set aside. A line beginning `link` in any other diagram is carried as written. Keywords match in any letter case. A line may hold several statements, each ended by a `;` outside a quoted string, as Mermaid reads them, and each `click` or class `link` statement among them is followed.

Two details follow from how Mermaid renders a link. A sequence diagram's destinations spell their anchor `#35;<slug>`, because Mermaid's sequence lexer reads a bare `#` as opening a comment. A Gantt task's `click` binds a click handler rather than drawing an anchor, so the rewritten destination is what the click opens.

A click naming a callback, a destination naming a document that declares nothing, a destination naming no document, and a C4 diagram's `$link` are carried as written and open nothing. A `links` value that is an array, or that holds a value that is no string, is refused: Mermaid renders the first as a menu whose entries are named by their positions, and the second as a link opening nothing.

A Kanban ticket's link and an HTML anchor Mermaid draws in a label are links Mermaid renders and the reader does not follow; one naming a local Markdown document is refused, so its author writes it as a `click`. Mermaid draws no anchor in a `click` tooltip or a class diagram's `link` tooltip, nor in a sequence, pie, timeline, journey, Gantt, quadrant, Git, XY, Sankey, packet, radar, treemap or C4 diagram, whose labels it draws as text, so an anchor written there is carried as written.

Every other byte of the fence is carried as written. A diagram link carries no operator, because a diagram gives it no link text to open with one.
