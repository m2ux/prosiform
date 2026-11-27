# Ledger Matrix

Each case of the [deterministic matrix](specimen-matrix.md#deterministic-matrix)'s Ledger line, with the fixture that carries it. The fixtures are corpus manifests under `fixtures/ledger/` on main; the task declaring each manifest writes its source tree and expected output. A case no source tree can state is carried by the test module named in its row. The clauses are [Build ledger](../2026-10-17-prosiform-v1/design.md#build-ledger) and the [coverage table](ledger-contract.md).

## Fixtures

| Fixture | Task | Build | Expected |
| --- | --- | --- | --- |
| `a-requested-ledger-names-each-bundle-s-sources` | E01:W02 | The ledger specimen's [run](specimens/ledger/run/) tree: `pf --ledger -o bundles '[Run](entry.md "recorded")'` | The bundles pf 0.36.0 wrote, and the specimen ledger |
| `a-ledger-leaves-the-bundles-unchanged` | E01:W02 | The [valid-two-bindings](specimens/valid-two-bindings/) control: `pf --ledger -o bundles entry.md` | The bundle hashes in [baseline.json](specimens/baseline.json), and [fixed.ledger.yaml](specimens/ledger/fixed.ledger.yaml) |
| `a-failing-run-publishes-no-ledger` | E01:W02 | The [missing-component](specimens/missing-component/) control: `pf --ledger -o bundles entry.md` | Exit 2, the control's diagnostic, and no run folder |
| `a-check-run-writes-the-ledger-to-standard-output` | E01:W02 | The run tree: `pf -c --ledger -o bundles '[Run](entry.md "recorded")'` | Standard output equal to the first fixture's ledger; an empty `bundles` folder |
| `links-from-two-sources-to-one-bundle-are-two-rows` | E01:W02 | An entry selecting a section of a grouped document by fragment, the entry and that section each dispatching one target whose `default` names a brief and a level the entry's level map names, run with `--budget depth=4` | Two `dispatches` rows naming one bundle, a `briefs` row and brief region for each, the fragment's `lines`, the region's `group`, and the overridden budget |
| `a-requested-ledger-is-published-with-its-digest` | E01:W02 | An entry declaring two alternatives, run as `pf --ledger -o bundles '[Pick](entry.md "?")' --pick beta` | A digest `sha256sum -c` passes, `picks: ["beta"]`, and `beta` in force in `content.choices` |
| `an-unchanged-set-verifies` | E01:W04 | The first fixture's published set | Verification passes |
| `a-changed-source-is-reported` | E01:W04 | That set with a source edited | The source reported |
| `a-changed-bundle-is-reported` | E01:W04 | That set with a bundle edited | The bundle reported |
| `a-set-without-a-ledger-is-refused` | E01:W04 | A run folder written without `--ledger` | Refused for its missing ledger |
| `a-missing-bundle-is-reported` | E01:W04 | That set with a bundle removed | The bundle reported |
| `a-bundle-the-ledger-does-not-name-is-reported` | E01:W04 | That set with a bundle added | The bundle reported |
| `a-ledger-this-build-cannot-read-is-refused` | E01:W04 | That set with a ledger stating `schema: 2` and its digest rewritten | Refused before any other file is opened |
| `a-changed-ledger-is-reported` | E01:W04 | That set with the ledger edited and its digest kept | The ledger reported |
| `a-ledger-without-its-digest-is-reported` | E01:W04 | That set with `ledger.yaml.sha256` removed | The missing digest reported |

## Each Case

| Matrix case | Carried by | What it holds | Clause |
| --- | --- | --- | --- |
| Selected and unselected output | `a-ledger-leaves-the-bundles-unchanged` | The same command line with and without `--ledger`: the ledger and digest appear only with it | Build ledger: Publication |
| Default and named ordering | `a-requested-ledger-names-each-bundle-s-sources` | `presets: ["default", "alpha", "small"]` and `["default", "recorded"]`; `selected` in declaration order | Build ledger: Order |
| Whole and fragment selection | `a-requested-ledger-names-each-bundle-s-sources`, `links-from-two-sources-to-one-bundle-are-two-rows` | Whole bodies and one section's `lines` | What the ledger records: `content` |
| Layout | `links-from-two-sources-to-one-bundle-are-two-rows` | `group` with `name` and `depth` on the grouped region, absent on the others | What the ledger records: `content` |
| Source hashes | `a-requested-ledger-names-each-bundle-s-sources` | Each source's hash, `content` and `metadata` uses, and no row for the redirected keys | What the ledger records: `sources` |
| Ordinary and stub substitutions | `a-requested-ledger-names-each-bundle-s-sources` | Routing pairs on the stage bundles; the stand-in on the entry bundle; the `recorded` stub | What the ledger records: `substitutions`, `stubs` |
| Briefs | `links-from-two-sources-to-one-bundle-are-two-rows` | A `briefs` row and the brief's `content` region in the dispatching bundle | What the ledger records: `briefs` |
| Dispatch, deferral and pick targets | `a-requested-ledger-names-each-bundle-s-sources`, `a-requested-ledger-is-published-with-its-digest` | A picking dispatch's `choices`; a deferral's `carries` and `published`; an entry's pick | What the ledger records: `dispatches`, `deferrals` |
| Levels and models | `a-requested-ledger-names-each-bundle-s-sources` | The level map row; `level` and `model` on the dispatch and the dispatched bundles | What the ledger records: `levels` |
| The invocation | `a-requested-ledger-names-each-bundle-s-sources`, `links-from-two-sources-to-one-bundle-are-two-rows`, `a-requested-ledger-is-published-with-its-digest` | A link entry as written, an overridden budget beside the defaults, a pick | What the ledger records: `invocation` |
| Check-mode output | `a-check-run-writes-the-ledger-to-standard-output` | The ledger on standard output, no digest and no bundle written | Build ledger: Check mode |
| Serialization and publication refusal | `a-failing-run-publishes-no-ledger`; `src/tests/test_ledger_publication.py` for a ledger the run cannot serialize, a folder it cannot write, and the ledger or digest write failing once the bundles are staged | No bundle, ledger or digest published, and an earlier set left standing; exit 3 with `E_PUBLICATION_FAILED` where publication fails | Build ledger: Publication |
| Unchanged Markdown bytes | `a-ledger-leaves-the-bundles-unchanged` | Bundle hashes equal to the frozen baseline | Build ledger: Unchanged bundles |
| Links from two sources reaching one bundle | `links-from-two-sources-to-one-bundle-are-two-rows` | Two rows, one for each source writing the link | What the ledger records: `dispatches` |
| An unchanged set | `an-unchanged-set-verifies` | Success | Stated by E01:W04 |
| A source-changed set | `a-changed-source-is-reported` | The differing source path | Stated by E01:W04 |
| A bundle-changed set | `a-changed-bundle-is-reported` | The differing bundle path | Stated by E01:W04 |
| A ledgerless set | `a-set-without-a-ledger-is-refused` | Refusal | Stated by E01:W04 |
| A missing bundle | `a-missing-bundle-is-reported` | The missing bundle | Stated by E01:W04 |
| An unlisted bundle | `a-bundle-the-ledger-does-not-name-is-reported` | The unlisted bundle | Stated by E01:W04 |
| A ledger the build cannot read | `a-ledger-this-build-cannot-read-is-refused` | Refusal naming the schema number | Stated by E01:W04 |
| A ledger differing from its digest | `a-changed-ledger-is-reported` | The ledger reported | Stated by E01:W04 |
| A ledger with no digest | `a-ledger-without-its-digest-is-reported` | The missing digest reported | Stated by E01:W04 |

## Beyond The Corpus

Cases the projection's own tests carry in `src/tests/test_ledger.py`, over real builds:

- One command line run twice over one tree writes the same ledger bytes, and the projection writes the same bytes from the same records captured in another order.
- A source whose file name holds `#`, selected by fragment, reads back by the reference grammar.
- Two composed copies routing one key to two substitutes write two rows in the contract's order.
- A preset named `off` or `no` reads back as a string.
- Two selected presets stating one substitute write one row, the further origin under `also`.
- The ledger parses under the frontmatter reader's rules and validates against the schema.
- Each warning the first fixture's build raises is absent from its ledger, and no row carries a line number.
