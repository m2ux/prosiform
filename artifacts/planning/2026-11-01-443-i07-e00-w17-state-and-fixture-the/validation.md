# Validation

Every check the work items name, run in the worktree at `i07/e00/w17-state-and-fixture-the`, revision `2b4ee564`, with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Corpus

`make corpus` reported `377 fixture(s), 377 pass, 0 fail, 0 awaited, 0 unexpected pass`, among them:

```text
dispatch/a-dispatch-in-a-title-above-the-selection-is-refused: pass
dispatch/a-dispatch-in-an-absorbed-member-title-is-refused: pass
publication/a-file-at-the-run-folder-s-path-is-refused: pass
```

- **AC26.** The publication fixture expects exit 3 and `E_PUBLICATION_FAILED` naming `guide.bundles`. The runner compares every path the run creates, so a run that renamed the file aside and published its folder fails on exit status and on the bundle it wrote.
- **AC27.** Each dispatch fixture expects exit 1 and `E_UNSUPPORTED_CONSTRUCT` with the link's reference `publish.md` and its source line; the title-above-selection fixture also declares its chain.

## T2 Fails Without the Refusals

The three fixture trees were run against the build at `d99025c1`, the epic base before the refusals landed:

| Fixture | Result |
| --- | --- |
| `a-file-at-the-run-folder-s-path-is-refused` | exit 0; `guide.bundles` replaced by a folder of bundles, the file's bytes gone |
| `a-dispatch-in-an-absorbed-member-title-is-refused` | exit 4, `E_UNEXPECTED_INTERNAL_ERROR` (`KeyError`) |
| `a-dispatch-in-a-title-above-the-selection-is-refused` | exit 0; bundle published, dispatch target compiled by no run |

Each fails its manifest, so each fixture observes the refusal it declares.

## T3 Catalogue Rows

`fixtures/README.md` reads:

- `E_PUBLICATION_FAILED` — "… an output folder that cannot be made, a path at the run folder's own that is neither a folder nor a link, or two bundles of one run deriving one name." (AC26)
- `E_UNSUPPORTED_CONSTRUCT` — "Dispatch sub-sections — a dispatched link with no text after its mark, or a dispatch in a heading the bundle emits as text alone: a title its file heading or a member's subsection absorbs, or a title above the selection." (AC27)

## T4 Pages Against the Refusals

`grep -n -i aside docs/bundles.md docs/dispatch.md` returns one line, `docs/bundles.md:46`, which renames aside only "an earlier set". The next paragraph states that anything else at that path, a regular file among them, is refused with `E_PUBLICATION_FAILED` and left where it stands. `docs/dispatch.md` states the title-dispatch refusal under `E_UNSUPPORTED_CONSTRUCT`, the three headings it covers, and that the entry's own title publishes. (AC28)

## T5 Scalar Ceiling

`fixtures/README.md:242` reads "Resource limits — a declared budget the run crossed, named with the figure that crossed it, or a numeric scalar longer than the 65,536 characters a byte budget admits." `docs/validation.md:80` states "One scalar of either notation therefore carries at most 65,536 characters, and a longer one fails with `E_RESOURCE_LIMIT`." The figure and the code agree. (AC29)

## T6 Make Check

`make check` exited 0: lint, format, types, steps, authoring, `test` (1420 passed), `harness` (1062 passed), corpus, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios.
