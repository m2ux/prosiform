# Dispatch Text: Design

The instruction a bundle opens with is repeated into every mode bundle, so its length is multiplied by the number of modes. It states the rule once, in the fewest words that carry it.

## The Repetition

- **One value, one emission per bundle.**
  `prosiform.dispatch` contributes its text to the opening line of every bundle whose sources declare it. A skill with ten modes emits the same sentence ten times across ten bundles.

- **It is read at the point of dispatch, not studied.**
  The line sits beside the entry sentence in a document an agent reads to act. A sentence that has to be parsed again on every read costs more than it states.

- **The rule is one clause.**
  A marked link is material a sub-agent compiles. Who reads it, where the target is, and why the mark survives are all stated once, in the section the metadata summarises.

## The Form

- **Verb first, actor second, object last.**
  `Compile the marked link and hand it to a sub-agent.`

- **One sentence, under seventy characters.**
  The subject is the link rather than the reader, so no clause has to explain who "you" is.

- **The detail lives in the section, not the sentence.**
  The dispatch section carries the destination rule and the reason the mark survives; the metadata carries the instruction.

## Measured

| Text | Characters |
| --- | --- |
| `A marked link is compiled by the reading agent and handed to a sub-agent, which is the run its material belongs to.` | 115 |
| `Compile the marked link and hand it to a sub-agent.` | 51 |

- **The saving is 64 characters per bundle**, 640 across ten modes, and the emitted line still reads as one instruction:

  `Follow [Prerequisites](#prerequisites). The other sections are material that procedure references. Compile the marked link and hand it to a sub-agent.`

## Decisions

- **A shorter sentence rather than a link to one.**
  The metadata is a string the compiler reads no structure in, so pointing it elsewhere would leave the opening line without the rule it is there to state.

- **The passive form goes.**
  `is compiled by the reading agent` names the reader second and costs eleven words; the imperative names the action first.
