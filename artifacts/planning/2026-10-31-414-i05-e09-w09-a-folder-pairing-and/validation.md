# Validation — W09 A Folder Pairing and Its Precedence

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w09-a-folder-pairing-and` on branch `i05/e09/w09-a-folder-pairing-and`, at branch head `30a669b2` unless a section names another revision. The build under test was named by `PROSIFORM_BUILD` as the worktree's own `src/.venv/bin/pf`.

The design clause the fixtures declare is `a59b62fca8ad2a155e4e32ac7857761b871cf304`, the revision `README.md` pins.

## T1 — The four fixtures pass against the build

**Ran:** `make corpus` at `30a669b2`.

**Observed:** exit `0`.

```text
mock/a-folder-key-carrying-a-section-is-refused: pass
mock/a-folder-key-redirects-each-reference-under-it: pass
mock/a-half-folder-pair-is-refused: pass
mock/an-exact-key-beats-a-folder-key: pass
corpus check: 371 fixture(s), 371 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 367 to 371, which is the four this row lands.

## T2 — Each fixture fails against the code before the change

This is the check the epic's own record warns about. W05's corpus fixture passed both ways, so a fixture is not evidence until it has been shown to fail without the change.

**Ran:** `checks/corpus.py` at `30a669b2` with the branch's `src/prosiform` replaced by the package at `3091c65b` — the base the branch was cut from — placed ahead of it on `sys.path` by a shim script. The whole corpus ran; the four fixtures below are the only ones this row adds.

**Observed:** exit `1`, four failures and no others.

```text
mock/a-folder-key-redirects-each-reference-under-it: fail
  expected.exit_status: expected 0, the run exited 2
  expected.bundles: the run wrote no guide.bundle.md
  expected.diagnostics: the run emits 1 diagnostic where 2 diagnostics are expected
    position 1: warning W_MOCK_SUBSTITUTED expected, error E_INVALID_USAGE produced
    position 2: warning W_MOCK_SUBSTITUTED expected, the run emits none
mock/an-exact-key-beats-a-folder-key: fail
  expected.exit_status: expected 0, the run exited 2
  expected.bundles: the run wrote no guide.bundle.md
  expected.diagnostics: the run emits 1 diagnostic where 3 diagnostics are expected
    position 1: warning W_MOCK_SUBSTITUTED expected, error E_INVALID_USAGE produced
    position 2: warning W_MOCK_SUBSTITUTED expected, the run emits none
    position 3: warning W_MOCK_SUBSTITUTED expected, the run emits none
mock/a-half-folder-pair-is-refused: fail
  expected.exit_status: expected 2, the run exited 0
  expected.bundles: the run wrote guide.bundle.md, which the manifest declares no bundle for
    146 bytes written, beginning b'# Guide\n\nFollow [the red'
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_INVALID_USAGE expected, warning W_MOCK_UNUSED produced
mock/a-folder-key-carrying-a-section-is-refused: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    'folder side a section' is absent
    produced "the mapping entry 'rules/#checks'='stubs/' gives a substitute naming no Markdown document, so the reference it redirects could only be published as text"
corpus check: 371 fixture(s), 367 pass, 4 fail, 0 awaited, 0 unexpected pass
```

Each difference is the row's own claim, read from the other side:

- **`a-folder-key-redirects-each-reference-under-it`.** The base refuses `-m rules/=stubs/` outright: the key `rules/` normalises to `rules`, no reference names it, and the substitute `stubs/` names no Markdown document, so `E_INVALID_USAGE` replaces both substitutions. No bundle is written.
- **`an-exact-key-beats-a-folder-key`.** The same refusal, three substitutions short.
- **`a-half-folder-pair-is-refused`.** The base accepts `-m rules/=stub.md` at exit `0`, writes a 146-byte bundle with every reference left as authored, and warns `W_MOCK_UNUSED` — the redirect that reads as one and takes effect as nothing. This is the shape the criterion refuses.
- **`a-folder-key-carrying-a-section-is-refused`.** The base refuses the value too, but for a different reason and with a message naming no section: `rules/#checks` normalises to `rules` and `#checks`, so the *substitute* `stubs/` is what fails the Markdown test. The fixture states the fault the row refuses, and the base's message does not carry it.

**And the unit cases the same way.** `src/tests/test_mock.py` with the base package ahead of it reports eighteen failures, and no other case in the file fails.

```text
FAILED test_a_folder_key_and_a_document_key_of_one_path_are_two_keys
FAILED test_a_folder_key_and_a_document_key_of_one_path_serve_together
FAILED test_a_folder_key_carrying_a_section_is_refused
FAILED test_a_folder_key_holds_only_a_path_that_continues_it_past_a_separator
FAILED test_a_folder_key_is_served_once_however_many_references_it_answered
FAILED test_a_folder_key_leaves_the_section_the_reference_named
FAILED test_a_folder_key_no_reference_named_is_unserved_with_its_separator
FAILED test_a_folder_key_redirects_a_reference_under_it_to_the_same_remainder
FAILED test_a_folder_keys_half_a_shape_is_refused_naming_the_pair
FAILED test_a_folder_pair_compiles_each_remainder_and_keeps_the_section
FAILED test_a_folder_pair_is_refused_before_any_source_is_read
FAILED test_a_folder_pair_naming_one_folder_both_ways_is_a_self_mock
FAILED test_a_folder_pairs_half_a_shape_is_refused_naming_the_pair
FAILED test_a_folder_pair_states_a_folder_on_both_sides
FAILED test_a_folder_substitute_carrying_a_section_is_refused
FAILED test_an_exact_key_answers_before_a_folder_key
FAILED test_the_longer_of_two_folder_keys_holding_one_reference_answers
FAILED test_two_spellings_of_one_folder_key_are_refused
```

Three cases were rewritten during this check because they passed on the base for the wrong reason, and the rewrites are recorded rather than the first result:

- **The marker refusal** asserted only a status of `2`, which the base reaches through a different refusal of the same value. It asserts now that the message names the folder side and the section, which only this row's refusal states.
- **The substitute-side section refusal** passed on the base because `stubs/#checks` fails the Markdown test there. It asserts now that the message names the folder side's section.
- **The "refused before any source is read" case** used a value the base accepted, so a status of `2` could not distinguish. It asserts now that the message names the half pair.

## T3 — What the feature does, from the command line

**Ran:** `pf -d json -o o -m rules/=stubs/ guide.md` over `a-folder-key-redirects-each-reference-under-it`'s tree, and the same run with `-m rules/red.md=other.md -m rules/visual/=deepest/` over `an-exact-key-beats-a-folder-key`'s.

**Observed:** exit `0` for both, and these warnings.

```text
{"code": "W_MOCK_SUBSTITUTED", "source": "rules/red.md#checks", "resolved": "stubs/red.md#checks", "location": {"file": "guide.md", "line": 6, "column": 1}}
{"code": "W_MOCK_SUBSTITUTED", "source": "rules/blue.md", "resolved": "stubs/blue.md", "location": {"file": "guide.md", "line": 6, "column": 1}}
{"code": "W_MOCK_SUBSTITUTED", "source": "rules/visual/red.md", "resolved": "deepest/red.md", "location": {"file": "guide.md", "line": 6, "column": 1}}
```

One entry served two references of one folder, each at its own remainder, and the red reference's section survived the redirect as `stubs/red.md#checks`. With the three further keys, the document key `rules/red.md` answered the red reference while `rules/` still answered the blue one and `rules/visual/` — longer than `rules/` and holding the visual reference — answered the third.

## T4 — The two refusals, through the JSON stream

**Ran:** `pf -d json -m rules/=stub.md guide.md` and `pf -d json -m rules/#checks=stubs/ guide.md` at `30a669b2`.

**Observed:** status `2` for both.

```json
{"severity": "error", "message": "argument -m/--mock: 'rules/=stub.md' names a folder on one side and a document on the other, so the entry states two different questions", "code": "E_INVALID_USAGE", "remedy": "run pf -h for usage"}
{"severity": "error", "message": "argument -m/--mock: 'rules/#checks=stubs/' gives a folder side a section, and a folder names no heading", "code": "E_INVALID_USAGE", "remedy": "run pf -h for usage"}
```

Both name the pair as the author wrote it, and both carry `E_INVALID_USAGE` with the one remedy every malformed command line carries. The refusals are raised while the grammar is read, so no source is opened and no bundle is written; the manifests declare no `bundles` for that reason, and the runner compares every file the run creates.

## T5 — The marker is read before normalisation

**Ran:** `src/tests/test_mock.py::test_a_folder_pair_states_a_folder_on_both_sides` and the two CLI cases over `paired`.

**Observed:** pass. `rules/` and `rules` reach the lookup as one path identity and remain two kinds of key, which is what `test_a_folder_key_and_a_document_key_of_one_path_are_two_keys` asserts. The mark is read from `components(text).path` before `entry` normalizes the side, so the empty segment `closure.normalized` drops has already been read. A key written `./` or `rules/./` normalises to no path and is refused as a separator that names no folder.

## T6 — A document key and a folder key of one path coexist

**Ran:** `src/tests/test_mock.py::test_a_folder_key_and_a_document_key_of_one_path_are_two_keys`, `::test_an_exact_key_answers_before_a_folder_key` and `::test_a_folder_key_and_a_document_key_of_one_path_serve_together`.

**Observed:** pass. `-m rules/=stubs/ -m rules/red.md=other.md` holds both keys, the document key answers the red reference and the folder key answers the rest. Neither refuses the other, because they are held in separate maps and the duplicate test reads both.

## T7 — The other mapping behaviour is unchanged

**Ran:** `src/tests/test_mock.py` at `30a669b2`.

**Observed:** 87 tests pass, up from the 68 the branch's base collects. The eighteen failures above account for the difference: three cases were rewritten rather than added, so the count of new cases and the count of failures on the base are one number.

The cases covering the document key, the fragment key, the four existing refusals, the entry redirect, the two warnings, the substitute as a source and the dispatch and deferral targets all pass unchanged, so the folder pairing neither shifts the answer a document pair receives nor changes the order the four refusals answer in. The corpus confirms it at the same head: 371 fixtures pass, the 19 mock fixtures that predate this row among them.

## T8 — `make conformance` maps the clause against the fixtures naming it

**Ran:** `make conformance` at `30a669b2`.

**Observed:** exit `0`.

```text
Link classification and resource handling — The substitution mapping: 23 fixture(s)
conformance report: 305 clause(s) the design states, 54 covered by no fixture, 0 declaration(s) naming no clause; 37 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes
```

The mapping's clause count rises from 19 to 23 — the four fixtures this row lands. The clause count stays at 305 and the uncovered count at 54, so the fixtures reach a clause the corpus already covered rather than a new one, which is expected: this row adds a shape of the mapping, not a clause.

## T9 — `make invocation` still agrees with the help output

**Ran:** `make invocation` at `30a669b2`.

**Observed:** exit `0`, `30 statement(s)`. The option's row and its help string are unchanged, because this row adds a shape of the value rather than an option. The documented row's folder form is `AC29`'s and lands with W11.

## T10 — `make independence` finds no implementation term in the new claims

**Ran:** `make independence` at `30a669b2`.

**Observed:** exit `0`, `every shaped term of every fixture declaration and every report entry is one the contract names`. The new descriptions and carried substrings state `rules/`, `stubs/`, `folder`, `document`, `section`, `substitute`, `one identity` and `separator alone`, each a term the contract names.

## T11 — `make check`

**Ran:** every target of `make check` on branch head `30a669b2`, in the Makefile's order. Exit `0`.

| Target | Observed |
| --- | --- |
| `lock-check` | `Resolved` from the locked set, no resolution |
| `lint` | `All checks passed` |
| `format-check` | `73 files already formatted` |
| `typecheck` | `Success: no issues found in 72 source files` |
| `test` | `1395 passed` |
| `harness` | `1027 passed` |
| `authoring` | `0 finding(s)` |
| `corpus` | `371 fixture(s), 371 pass` |
| `smoke` | wheel built, installed and run outside the repository; `ok` on all seven lines |
| `layout` | `4 tree(s) present` |
| `tables` | every command and declaration held in both directions |
| `links --online` | every reference in 212 documents resolved |
| `vocabulary` | `3332 term(s)` |
| `invocation` | `30 statement(s)` |
| `conformance` | `305 clause(s)`, `54 covered by no fixture`, `0 declaration(s) naming no clause` |
| `independence` | every shaped term is one the contract names |
| `steps` | every procedure in 59 documents |
| `mock-scenarios` | `5 scenario(s), 5 pass` |

This host reaches the package index, so `test_linked_bootstrap` and the publication tests ran and passed here rather than failing as the delivery brief expected. Both were run on the settled base worktree at `f7900aff` as well, and both pass there too, so no failing target is hidden by a environment difference.

## T12 — The declared fixtures on a branch whose inclusion is by declaration

**Ran:** `pf -m rules/=stubs/` over a tree whose every document carries `prosiform: {}`, and the same over each of the four fixtures with the declarations removed.

**Observed:** exit `0`, the same bundle either way. Every document of each fixture declares `prosiform` from the first, so no fixture changes when [I05:E11](https://github.com/m2ux/prosiform/issues/434) makes inclusion a property of the declaration. On this branch the declaration bounds inclusion no further than the writing source's root already does. The one comparison that moved was the link's line, which the three frontmatter lines shift from 3 to 6; both manifests declare the coordinate the declaring tree produces.

## T13 — Delivery

Filled in by the delivery section of `change-list.md` once the pull request, the Development link, the epic row and the merge are done.
