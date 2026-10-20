# Validation

## Overview

What the corpus comparison was measured to do on `i00/e11/w03-a-manifest-comparison-that` at `500d91f`, and the checks the delivery was held to.

Two observations run against a build other than the one this repository holds. A declaration that leaves a build its own wording cannot be measured against one build alone, so each is run against a response the comparison must accept and one it must refuse, both produced by a stub naming itself through `PROSIFORM_BUILD`. That is the whole of what the configuration is for: the runner invokes what configuration names.

## T1 The Declaration and What It Refuses

**Observes AC4, AC13.** The schema cases, in [`checks/tests/test_manifest_schema.py`](https://github.com/m2ux/prosiform/blob/i00/e11/w03-a-manifest-comparison-that/checks/tests/test_manifest_schema.py), run under `make harness`.

| Case | Asserts |
| --- | --- |
| `test_a_manifest_declaring_the_text_standard_output_carries_validates` | A manifest naming `stdout_contains` in place of `stdout` is a complete declaration. |
| `test_a_manifest_declaring_standard_output_both_ways_fails` | A manifest naming both states its output twice and is malformed. |
| `test_a_manifest_declaring_standard_output_neither_way_fails` | A manifest naming neither states nothing about the stream and is malformed. |
| `test_an_empty_text_declaration_fails` | A declaration naming no text is refused. |
| `test_a_text_entry_declared_twice_fails` | One entry declared twice is refused. |
| `test_a_text_declaration_as_a_bare_string_fails` | The declaration is a list, so a bare string is refused. |
| `test_a_diagnostic_declaring_the_text_its_message_carries_validates` | `message_contains` is a field a diagnostic may declare. |
| `test_a_diagnostic_declaring_no_message_text_validates` | Its absence leaves every fixture now in the corpus valid. |
| `test_an_empty_message_text_declaration_fails` | A declaration naming no text is refused there too. |
| `test_a_whole_message_field_fails` | No manifest declares a whole message, which would be one build's wording. |

## T2 A Response the Comparison Accepts and One It Refuses

**Observes AC4.** `fixtures/cli/informational-version-response` declares exit status 0, no diagnostics, and the two things the contract says the version response reports. The version between them is the build's own.

```bash
PROSIFORM_BUILD=…/other-version.sh  python checks/corpus.py   # prosiform 17.0.3-rc4 (skill-markdown-v1)
PROSIFORM_BUILD=…/other-profile.sh  python checks/corpus.py   # prosiform 0.1.0 (skill-markdown-v2)
```

**Pass.** The response carrying another version holds; the one naming another profile does not, and the difference names the text that was absent.

```text
cli/informational-version-response: pass

cli/informational-version-response: fail
  expected.stdout_contains: the output does not carry 1 declared text
    '(skill-markdown-v1)' is absent
    produced b'prosiform 0.1.0 (skill-markdown-v2)\n'
```

The fixture also passes against the build this repository holds, whose response is `prosiform 0.1.0 (skill-markdown-v1)` — a third version string, and the point of the declaration. Before this row no fixture stated this run at all: a file of expected bytes would have named one build's version, and the corpus had no other way to state standard output.

The runner's own cases cover the same comparison on canned output: `test_an_output_carrying_the_declared_text_passes`, `test_an_output_missing_the_declared_text_names_what_is_absent` and `test_an_output_declared_as_text_is_not_held_to_bytes`, the last running one fixture against two responses sharing nothing but the declared text.

## T3 Two Faults Under One Code

**Observes AC13.** Four fixtures declare severity `error`, code `E_INVALID_USAGE` and exit status 2. A stub build reports one of those faults — an output path naming an input source — whatever it is asked to do, and each fixture is run against it.

```bash
PROSIFORM_BUILD=…/wrong-fault.sh python checks/corpus.py
```

**Pass.** The fixture for the fault the stub reports holds; the three for other faults fail, each naming the text its message was missing and the message that arrived.

```text
cli/output-naming-an-input-source: pass

cli/fragment-only-reference-without-from: fail
  expected.diagnostics: diagnostic 1's message does not carry 2 declared texts
    '#a-section' is absent
    '--from' is absent
    produced "the output path 'source/guide.md' names an input source"

cli/diagnostics-format-unknown: fail
  expected.diagnostics: diagnostic 1's message does not carry 2 declared texts
    '--diagnostics' is absent
    'yaml' is absent
    produced "the output path 'source/guide.md' names an input source"

cli/output-naming-a-dependency-source: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    'source/note.md' is absent
    produced "the output path 'source/guide.md' names an input source"
```

Each of the four passes against the build this repository holds, which reports each fault where it belongs. The same stub run before this row's declarations passes all four, because the comparison read severity, code, reference, resolved, source and chain and nothing else — which is the defect [#52](https://github.com/m2ux/prosiform/issues/52) records.

What each fixture declares is the run's own data rather than the build's prose: the reference refused, the option whose value was outside its set, the path that named an input source. The runner's own cases hold the comparison itself — `test_a_message_carrying_the_declared_text_passes`, `test_a_message_declaration_tells_two_faults_under_one_code_apart`, `test_a_diagnostic_carrying_no_message_is_reported` and `test_a_diagnostic_declaring_no_message_text_reads_no_message`.

## The Gate

Measured in the delivery worktree at `500d91f`, with `PROSIFORM_BUILD` naming the build this repository holds.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 603 passed |
| `make harness` | 397 passed, seventeen of them this row's |
| `make corpus` | 204 fixture(s), 202 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | Installed and bundled a reference from a source root, outside the repository |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) of the documented invocation |

The corpus run is 204 fixtures where it was 203, this row's version fixture being the one added.

## Limitations

A declared text is a substring and nothing more. It states that the output carries what identifies the outcome; it states nothing about where in the output that text sits, how often it appears, or what else accompanies it. A run whose shape matters in a stronger sense than this — an ordering, a count, a field position — is not expressible, and the row that needs it is the row that decides what to add.

`message_contains` is compared against the `message` field of a diagnostic emitted as JSON. A build writing its diagnostics as prose is not reached by it, which is as the runner already stands: it asks for diagnostics as data on every run.

The three usage faults this row separates are the three the corpus holds fixtures for. `E_INVALID_USAGE` names more faults than that — a missing allowed source root and a command line naming no entry reference among them — and each remains stated by the build's own tests rather than by a fixture. Adding those fixtures is work this row did not carry, and nothing in the corpus now claims they are covered.
