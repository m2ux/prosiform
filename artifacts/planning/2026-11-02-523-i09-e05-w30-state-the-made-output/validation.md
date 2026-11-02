# W30-W32 Validation

The design at [ea76fd37](https://github.com/m2ux/prosiform/blob/ea76fd37b0a89663a341d802c024e8a509d88cff/artifacts/planning/2026-10-17-prosiform-v1/design.md), the commit the README's design link pins, read against the build at branch `i09/e05/w30-state-the-made-output`.

## AC34

The design states that `-o` names a folder the run makes where it is absent, refusing only one it cannot make.

| Design | Build |
| --- | --- |
| *CLI contract*, `-o DIR`: "A folder that does not exist is made, with every parent it lacks, and one the run cannot make fails as Publication states." | `pf -h`: "folder the run's own folder of bundles is written into, made if absent". The guide: "The run makes it if it is not there." `cli.py` makes `folder.parent` with its parents before any bundle is written. |
| *Validation and failure contract — Publication*: the run "makes the output folder where it does not exist, with every parent it lacks … under `-c` as without it"; one it cannot make "fails with `E_PUBLICATION_FAILED` naming the folder". | `publication/an-output-folder-that-does-not-exist-is-made` (exit 0, bundle under `made/`), `publication/a-check-run-into-a-folder-that-does-not-exist-makes-it` (`-c`, exit 0), `publication/an-output-folder-that-cannot-be-made-fails` (exit 3, `E_PUBLICATION_FAILED` naming `blocked`). |
| *Adversarial acceptance fixtures*, Publication row: "an absent `-o` folder made, under `-c` as without it, and one the run cannot make refused". | The three fixtures above. |

No clause of the design states that the output folder must exist.

## AC35

The design states that a document's links resolve through the `subst` pairs the presets of every reference reaching it select, two references mapping one key to two alternatives being refused as invalid usage.

| Design | Build |
| --- | --- |
| *Presets — One document under several selections*: the document's links "resolve through one mapping: the `subst` pairs of its `default` and of every preset a reference reaching it in the bundle selects"; "A pair one reference's selection states therefore redirects a link in content another reference bundled under `default` alone." | `cli.py` `governing` builds one table per document from every reference reaching it. `inclusion/a-pair-one-reference-selects-reaches-every-section`: `## Plain` bundles `rules.md#one` under `default`, `## Checks` selects `Checks`, and One's link to `steps.md` compiles `checked-steps.md` (`W_SUBST_USED`). `inclusion/a-pair-a-selected-preset-overrides-records-no-substitution` holds the same across two documents reaching `rules.md`. |
| The same clause: "Two references whose selected presets map one `subst` key to two alternatives are invalid usage with exit status `2`, naming the two presets". | `cli.py` `disagreeing`. `inclusion/two-references-disagreeing-about-a-subst-key-are-refused`: `## Checks` and `## Draft` select presets mapping `steps.md` two ways; exit 2, `E_INVALID_USAGE` naming `prosiform.Checks.subst and prosiform.Draft.subst`. |
| *Presets — Selected presets union*: two presets one title selects mapping one key two ways are refused. | `inclusion/two-presets-disagreeing-about-a-subst-key-are-refused`. |
| *Link classification and resource handling — The substitution mapping*: the union of the pairs "combined across every reference reaching that document as Presets states". | Links to the rule's one home. |
| *Presets — A document in several groups*: `group` stays per reference. | `inclusion/one-document-two-presets`. |

## AC36

The design's option table declares `-C`/`--codes`, `--version` and `--help`.

| Design option row | `pf -h` |
| --- | --- |
| `-C`, `--codes`: "Print every error and warning code the build can report, one per line, on standard output, and exit 0." | `-C, --codes          list this build's error and warning codes` |
| `-v`, `--version` | `-v, --version        tool version and profile identifier` |
| `-h`, `--help` | `-h, --help           usage, defaults and exit statuses` |

`-o`, `-c`, `-d` and `--budget` rows match the help as before. The fixtures `cli/informational-codes-response` and `cli/informational-long-codes-response` cite the `-C`, `--codes` row; the four `informational-*-usage` and `-version` fixtures cite the `-v`, `--version` and `-h`, `--help` rows. The conformance report counts all three rows covered.

## make check

`PROSIFORM_BUILD='uv run --project …/w30-state-the-made-output/src --frozen pf' make check` exits 0: 1663 build tests and 1165 harness tests pass, every corpus fixture passes (the four new ones among them), and `conformance` reports 356 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere and 0 reported codes the contract declares nowhere.
