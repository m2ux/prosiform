---
prosiform:
  root: "."
---
# Bootstrap

A link whose text opens with a matching [symbol](#symbols) follows the usage instructions and is *not* read as a file.

## Compile

Compile a target file. Run from the skill's directory, which holds `SKILL.md`.

```bash
pf -o <scratch>/<name>.bundle.md <destination>
```

- `<destination>`  The link's destination as written.
- `<name>`  The destination's file name without its suffix.
- `<scratch>`  An existing working directory outside the repository.

> A non-zero exit stops the run and reports `pf`'s diagnostics.

## Symbols

| Symbol | Description | Usage |
| --- | --- | --- |
| `↳` | An inline target | [Compile](#compile) it, read the whole bundle and follow the instructions in its preamble. |
| `⇉` | A dispatched target | [Compile](#compile) it, hand the bundle to one sub-agent, with the inputs the request names, to follow the instructions in its preamble, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered to the session that dispatched it. That session puts each returned question to the user, or returns it in turn when it was itself dispatched, then dispatches again with the answers. A [run-set](#symbols) hands each dispatched item to a sub-agent of its own at once. |
| `⫽` | A run-set | Run the calls the linked section lists concurrently in this session, as parallel tool calls: top-level items together, a nested item once its parent alone has returned, an item that says "for each" once per item, together. Continue when every item, nested, per-item and dispatched, has returned. A failed item cancels nothing: the others finish, then the run-set returns every failure together as blockers. Questions dispatched items return are put to the user together once every item has returned, and only the items that asked are dispatched again, with their answers. |
