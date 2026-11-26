# Command-Line Tests Read Against the Corpus

> Overlap table for W05. Source measured: prosiform `main` at [`b0eb7a2`](https://github.com/m2ux/prosiform/tree/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be).

Each test pytest collects from `src/tests/test_cli.py` has one row: what it asserts, the corpus fixtures that assert the same outcome, and whether they hold all of it. The Verdict column is the user's: approve or refuse removal of a held test.

## Summary

| Held? | Tests |
| --- | --- |
| held | 238 |
| partly held | 224 |
| not held | 80 |
| cannot decide | 0 |
| **Total** | **542** |

No test is undecided.

- **held** — the named fixtures together assert every outcome the test asserts.
- **partly held** — the fixtures assert part of it; *What is missing* names the rest.
- **not held** — no fixture asserts it; *Holding fixtures* reads `none`.

### Why a test is partly or not held

A fixture runs `pf -d json` as a subprocess and compares exit status, diagnostics (severity, code and the declared `message_contains`, `reference`, `resolved`, `source`, `chain`, `location`), bundle bytes and standard output. A test outside that reach stays partly or not held:

- **In-process calls.** Tests of `probe`, `recheck`, `names`, `publication`, budget parsing and `read_document` assert a function's return or raised error. A fixture reaches the same outcome only through a whole run.
- **Fields no manifest declares.** `remedy`, `related`, a full message beyond `message_contains`, the absence of a field, and a source left unchanged after a fault.
- **The human diagnostic format.** The runner always appends `-d json`, so a test of text-format stderr, or of `-djson`, `-d=json` and `-cdjson` spellings, is out of reach.
- **Input variants.** The fixture states the outcome for a sibling input: a Markdown link where the test uses a Mermaid click, a deferral where it uses a dispatch, one blank where it uses two, a chain where it uses branching.
- **Faults the contract does not name.** A refused rename during the swap (restore and no-restore) has no fault mode, so no fixture reaches it.

### Calls for the user's judgement

- **Held across two fixtures.** `test_one_entry_source_selects_several_inputs` is held only by `self-reference/a-section-link-to-its-whole-document` and `cli/several-entries-joined-into-one-name` together.
- **Held on a near input.** `test_an_entry_naming_a_member_of_one_heading_opens_on_its_title` (the fixture's group has a second member); `test_a_diagnostic_below_a_stripped_block_names_the_line_of_the_file` (the fixture strips a 3-line block, the test a 4-line one); `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a deferred dispatch]` (the fixture declares `message_contains` "deferral mark" and "dispatch", the test checks "dispatch mark").
- **Held by a specific code.** `test_a_source_that_is_not_valid_utf8_reaches_no_generic_handler` is held because `E_INVALID_ENCODING` excludes the internal-fault path.
- **Message wording held by `message_contains`.** In diagram and node-text tests, a fixture whose `message_contains` names the clicked element and the key phrase is counted as holding the message.

## Method

1. **Per-test coverage.** `test_cli.py` ran under coverage with one dynamic context per pytest node id (542 passed); 8 tests cover no line of `src/prosiform` (they read the guide constant), so 534 tests carry lines.
2. **Per-fixture coverage.** The corpus ran with `PROSIFORM_BUILD` naming a wrapper that runs `pf` under coverage, its context the fixture identity found from the working directory, its data files parallel and then combined (708 fixtures, 708 pass).
3. **Shortlist.** [`shortlist.py`](shortlist.py) lists, per test, the fixtures covering every line the test covers in each module it exercises, closest first; with none, the fixtures covering most of its lines. 272 tests had a containing fixture and 262 had none.
4. **Reading.** Each test was read against its candidates' manifests and expected bundles, and against manifests found by grepping the code or phrase it asserts. Line containment shortlisted; reading decided.

The commands are in the [README](README.md#reproduction).

## The table

Grouped by test area, in the order the file first reaches each area.

| Area | Tests | held | partly held | not held |
| --- | --- | --- | --- | --- |
| Responses and guide | 16 | 3 | 10 | 3 |
| Usage | 60 | 21 | 23 | 16 |
| Limits | 39 | 13 | 23 | 3 |
| Diagnostics | 17 | 2 | 9 | 6 |
| Headings and grouping | 20 | 8 | 11 | 1 |
| Publication | 27 | 13 | 9 | 5 |
| Source access | 40 | 21 | 12 | 7 |
| Presets and subst | 61 | 17 | 29 | 15 |
| Profile | 13 | 8 | 3 | 2 |
| Frontmatter | 15 | 9 | 3 | 3 |
| Alternatives and picks | 21 | 4 | 16 | 1 |
| Entry forms | 11 | 7 | 2 | 2 |
| Deferral | 41 | 18 | 17 | 6 |
| Dispatch | 62 | 35 | 20 | 7 |
| Faults | 11 | 2 | 7 | 2 |
| Resources | 5 | 5 | 0 | 0 |
| References | 7 | 7 | 0 | 0 |
| Composition | 11 | 6 | 4 | 1 |
| Self-reference | 7 | 7 | 0 | 0 |
| Validation scope | 7 | 3 | 4 | 0 |
| Source consistency | 6 | 1 | 5 | 0 |
| Boundaries | 2 | 1 | 1 | 0 |
| Diagrams | 43 | 27 | 16 | 0 |

### Responses and guide

16 tests: 3 held, 10 partly held, 3 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_the_version_response_names_the_version_and_the_profile` | -v prints pf, the exact version and profile; succeeds; stderr empty | `cli/informational-version-response` | partly held | the exact version string between pf and the profile |  |
| `test_the_help_response_shows_usage_defaults_and_exit_statuses` | -h starts with the usage line, shows default text, exit statuses heading and each status 0-4 | `cli/informational-usage-response` | partly held | usage: prefix at the start, default text, the exit statuses heading and status-number layout |  |
| `test_a_bare_command_prints_the_guide` | no arguments prints the exact guide, succeeds, stderr empty, writes nothing | `cli/informational-guide-response` | partly held | the whole guide byte for byte (fixture checks fragments) |  |
| `test_the_guide_states_each_rule_an_agent_follows_a_bundle_by` | guide text carries each usage, symbol and dispatch rule | `cli/informational-guide-response` | partly held | pick rule on a ⇉ link, leaves to you, named from the working directory, applies to several |  |
| `test_the_guide_hands_a_bundle_over_by_the_path_of_its_file` | guide says hand over the bundle file path, no framing, take answer, model choice | `cli/informational-guide-response` | held |  | approved |
| `test_the_guide_opens_on_following_a_bundle` | guide opens on Following a bundle, follow as written, symbol grammar before usage | `cli/informational-guide-response` | partly held | opening line, the words as written and it meets, symbol grammar preceding usage |  |
| `test_the_guide_leaves_a_briefs_stated_work_to_the_sub_agent` | guide says a brief's asks are done first and its stated work is the sub-agent's | `cli/informational-guide-response` | held |  | approved |
| `test_the_guide_states_a_sub_agents_inputs_are_the_dispatching_steps` | guide names the dispatching step's inputs exactly twice and never the step that led there | `cli/informational-guide-response` | partly held | the count of exactly two and the absence of the step that led there |  |
| `test_the_guide_is_plain_text` | guide has no headings, backticks, asterisks, underscores or links in prose | none | not held |  |  |
| `test_the_help_response_names_the_bare_command` | -h says running with no arguments prints the guide | none | not held |  |  |
| `test_the_codes_response_names_every_code_the_build_can_emit` | -C prints every code sorted one per line, succeeds, stderr empty | `cli/informational-codes-response` | partly held | the full sorted code list (fixture checks three codes) |  |
| `test_the_codes_reported_are_the_codes_the_build_declares` | CODES constant equals the sorted union of declared code sets | none | not held |  |  |
| `test_an_informational_response_needs_no_source_root` | -v, -h and -C each succeed | `cli/informational-version-response`, `cli/informational-usage-response`, `cli/informational-codes-response` | held |  | approved |
| `test_an_informational_long_option_responds_as_its_short_form[-C---codes]` | --codes run equals -C run in status and streams | `cli/informational-long-codes-response`, `cli/informational-codes-response` | partly held | full equality of the two responses (fixtures check the same fragments) |  |
| `test_an_informational_long_option_responds_as_its_short_form[-v---version]` | --version run equals -v run in status and streams | `cli/informational-long-version-response`, `cli/informational-version-response` | partly held | full equality of the two responses (fixtures check the same fragments) |  |
| `test_an_informational_long_option_responds_as_its_short_form[-h---help]` | --help run equals -h run in status and streams | `cli/informational-long-usage-response`, `cli/informational-usage-response` | partly held | full equality of the two responses (fixtures check the same fragments) |  |

### Usage

60 tests: 21 held, 23 partly held, 16 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_argument_naming_no_entry_reference_is_no_bare_command[arguments0]` | -c alone is invalid usage naming entry reference, stdout empty | `cli/a-command-line-naming-no-entry-reference` | held |  | approved |
| `test_an_argument_naming_no_entry_reference_is_no_bare_command[arguments1]` | -d json alone is invalid usage naming entry reference, stdout empty | `cli/a-command-line-naming-no-entry-reference` | partly held | -d json with no other argument (fixture adds -c) |  |
| `test_an_argument_naming_no_entry_reference_is_no_bare_command[arguments2]` | -o . alone is invalid usage naming entry reference, stdout empty | `cli/a-command-line-naming-no-entry-reference` | partly held | -o . with no entry not exercised (fixture uses -c) |  |
| `test_long_options_are_invalid_usage[--output]` | --output alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--check]` | --check alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--diagnostics]` | --diagnostics alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-files]` | --max-files alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-file-bytes]` | --max-file-bytes alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-input-bytes]` | --max-input-bytes alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-output-bytes]` | --max-output-bytes alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-targets]` | --max-targets alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-links]` | --max-links alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-nesting]` | --max-nesting alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--max-expansion-depth]` | --max-expansion-depth alone is invalid usage, no bundle | `cli/an-option-the-contract-does-not-declare`, `cli/abbreviated-options-are-invalid-usage` | partly held | this long spelling not exercised; fixtures cover other undeclared options |  |
| `test_long_options_are_invalid_usage[--cod]` | --cod abbreviation alone is invalid usage, no bundle | `cli/abbreviated-options-are-invalid-usage` | partly held | abbreviation of an informational option with no entry not exercised |  |
| `test_long_options_are_invalid_usage[--vers]` | --vers abbreviation alone is invalid usage, no bundle | `cli/abbreviated-options-are-invalid-usage` | partly held | abbreviation of an informational option with no entry not exercised |  |
| `test_long_options_are_invalid_usage[--he]` | --he abbreviation alone is invalid usage, no bundle | `cli/abbreviated-options-are-invalid-usage` | partly held | abbreviation of an informational option with no entry not exercised |  |
| `test_every_option_the_contract_declares_is_accepted` | -o, -c and -d json together with an entry succeed | `cli/validation-only-run-with-an-output-folder` | held |  | approved |
| `test_an_option_the_contract_does_not_declare_is_refused[--manifest]` | undeclared --manifest with an entry is invalid usage | `cli/an-option-the-contract-does-not-declare` | held |  | approved |
| `test_an_option_the_contract_does_not_declare_is_refused[--watch]` | undeclared --watch with an entry is invalid usage | `cli/an-option-the-contract-does-not-declare` | held |  | approved |
| `test_an_option_the_contract_does_not_declare_is_refused[--cache]` | undeclared --cache with an entry is invalid usage | `cli/an-option-the-contract-does-not-declare` | held |  | approved |
| `test_a_missing_entry_is_invalid_usage` | a run with only -o and no entry is invalid usage naming entry reference, no bundle | `cli/a-command-line-naming-no-entry-reference` | held |  | approved |
| `test_a_run_naming_no_entry_reference_is_invalid_usage` | a run naming no entry in a source root is invalid usage, no bundle | `cli/a-command-line-naming-no-entry-reference` | held |  | approved |
| `test_a_bare_fragment_is_invalid_usage_naming_the_section_spelling` | #a-section alone is invalid usage, reference is the fragment, message names document#fragment | `cli/a-bare-fragment-is-invalid-usage` | partly held | the reference field equal to the fragment |  |
| `test_a_usage_failure_is_reported_before_an_input_failure` | unknown option with a missing entry file is a usage failure, not input | none | not held |  |  |
| `test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage[yaml]` | -d yaml is invalid usage, no bundle | `cli/diagnostics-format-unknown` | held |  | approved |
| `test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage[]` | -d with an empty value is invalid usage, no bundle | `cli/diagnostics-format-unknown` | partly held | the empty value not exercised; fixture covers yaml |  |
| `test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage[TEXT]` | -d TEXT is invalid usage, no bundle | `cli/diagnostics-format-unknown` | partly held | the upper-case TEXT value not exercised; fixture covers yaml |  |
| `test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage[jsonl]` | -d jsonl is invalid usage, no bundle | `cli/diagnostics-format-unknown` | partly held | the jsonl value not exercised; fixture covers yaml |  |
| `test_a_usage_failure_reaching_no_document_carries_no_chain` | An undeclared option exits 2 and its diagnostic carries no chain field | `cli/an-option-the-contract-does-not-declare` | partly held | absence of the chain field; the runner compares declared fields only |  |
| `test_a_fault_in_the_command_line_carries_the_invalid_usage_code[arguments0]` | An option-only command line naming no entry exits 2 with E_INVALID_USAGE | `cli/a-command-line-naming-no-entry-reference` | held |  | approved |
| `test_a_fault_in_the_command_line_carries_the_invalid_usage_code[arguments1]` | A bare fragment entry exits 2 with E_INVALID_USAGE | `cli/a-bare-fragment-is-invalid-usage` | held |  | approved |
| `test_a_fault_in_the_command_line_carries_the_invalid_usage_code[arguments2]` | An unknown diagnostic format exits 2 with E_INVALID_USAGE | `cli/diagnostics-format-unknown` | held |  | approved |
| `test_a_fault_in_the_command_line_carries_the_invalid_usage_code[arguments3]` | An undeclared option exits 2 with E_INVALID_USAGE | `cli/an-option-the-contract-does-not-declare` | held |  | approved |
| `test_a_missing_entry_carries_the_invalid_usage_code` | A command line naming no entry exits 2 with E_INVALID_USAGE | `cli/a-command-line-naming-no-entry-reference` | held |  | approved |
| `test_a_run_folder_holding_an_input_source_carries_the_invalid_usage_code` | A run folder holding a dependency source exits 2 with E_INVALID_USAGE | `cli/run-folder-holding-a-dependency-source` | held |  | approved |
| `test_a_link_entry_whose_title_states_operator_marks_is_invalid_usage[click Plan "guide.md#plan" "\u21c9"]` | click entry tooltip of marks: exit 2, stderr says states operator marks, no bundles | none | not held |  |  |
| `test_a_link_entry_whose_title_states_operator_marks_is_invalid_usage[click Plan "guide.md#plan" "\xac ?"]` | click entry tooltip of marks: exit 2, stderr says states operator marks, no bundles | none | not held |  |  |
| `test_a_link_entry_whose_title_states_operator_marks_is_invalid_usage[link Plan "guide.md#plan" "checks, \u21b3"]` | link-line entry tooltip tag of marks: exit 2, states operator marks, no bundles | none | not held |  |  |
| `test_a_link_entry_whose_title_states_operator_marks_is_invalid_usage[[Plan](guide.md#plan "\u21c9 checks")]` | Markdown entry title with marks: exit 2, states operator marks, no bundles | none | not held |  |  |
| `test_a_stray_or_repeated_pick_is_invalid_usage[arguments0]` | --pick beside a plain path: exit 2, only E_INVALID_USAGE, no bundles | `cli/a-pick-beside-a-plain-path-is-invalid-usage` | held |  | approved |
| `test_a_stray_or_repeated_pick_is_invalid_usage[arguments1]` | --pick beside a link titled without ?: exit 2, only E_INVALID_USAGE | `cli/a-pick-beside-a-link-carrying-no-pick-token-is-invalid-usage` | held |  | approved |
| `test_a_stray_or_repeated_pick_is_invalid_usage[arguments2]` | --pick beside a click entry titled without ?: exit 2, only E_INVALID_USAGE | `cli/a-pick-beside-a-link-carrying-no-pick-token-is-invalid-usage` | partly held | click line entry form |  |
| `test_a_stray_or_repeated_pick_is_invalid_usage[arguments3]` | two --pick naming different alternatives: exit 2, only E_INVALID_USAGE | `cli/a-repeated-pick-is-invalid-usage` | held |  | approved |
| `test_a_stray_or_repeated_pick_is_invalid_usage[arguments4]` | --pick with no entry: exit 2, only E_INVALID_USAGE | `cli/a-pick-without-an-entry-is-invalid-usage` | held |  | approved |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[[Plan](guide.md#plan) and [Other](guide.md#other)]` | entry text holding two links: exit 2, only E_INVALID_USAGE | `cli/a-text-holding-two-links-is-invalid-usage` | held |  | approved |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[[Plan](guide.md#plan).]` | link followed by a period: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[[Plan](guide.md#plan) trailing]` | link followed by trailing text: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[Defer [the plan](guide.md#plan "checks").]` | sentence containing one link: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[click Plan "guide.md#plan"; click Other "guide.md#other"]` | two click lines in one entry: exit 2, only E_INVALID_USAGE | `cli/a-text-holding-two-links-is-invalid-usage` | partly held | two click lines (fixture holds two Markdown links) |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[# [Plan](guide.md#plan)]` | link inside an ATX heading: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[###### [Plan](guide.md#plan "checks")]` | link inside a level-six heading: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[[Plan](guide.md#plan)\n---]` | link followed by a setext underline: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_text_written_as_a_link_but_not_one_link_is_invalid_usage[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[Plan]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]](guide.md#plan)]` | deeply nested bracket text: exit 2, only E_INVALID_USAGE | none | not held |  |  |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[0]` | A zero budget override is refused as usage failure | `limits/a-zero-override-is-refused` | held |  | approved |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[-1]` | A negative budget override is refused as usage failure | `limits/a-negative-override-is-refused` | held |  | approved |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[1.5]` | A fractional budget override is refused as usage failure | none | not held |  |  |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[0x10]` | A hexadecimal budget override is refused as usage failure | none | not held |  |  |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[ 1]` | A budget override with a leading space is refused as usage failure | none | not held |  |  |
| `test_a_budget_override_that_is_no_positive_decimal_integer_is_refused[]` | An empty budget override value is refused as usage failure | none | not held |  |  |

### Limits

39 tests: 13 held, 23 partly held, 3 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_budget_entry_sets_the_budget_it_names[files]` | --budget files=123 parses to 123, other budgets keep defaults | `limits/a-file-count-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[file-bytes]` | --budget file-bytes=123 parses to 123, other budgets keep defaults | `limits/a-source-byte-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[input-bytes]` | --budget input-bytes=123 parses to 123, other budgets keep defaults | `limits/an-input-byte-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[output-bytes]` | --budget output-bytes=123 parses to 123, other budgets keep defaults | `limits/an-output-byte-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[targets]` | --budget targets=123 parses to 123, other budgets keep defaults | `limits/a-target-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[links]` | --budget links=123 parses to 123, other budgets keep defaults | `limits/a-link-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[nesting]` | --budget nesting=123 parses to 123, other budgets keep defaults | `limits/a-nesting-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_a_budget_entry_sets_the_budget_it_names[depth]` | --budget depth=123 parses to 123, other budgets keep defaults | `limits/an-expansion-depth-budget-crossed` | partly held | the parsed value and other budgets' defaults (in-process return); fixture shows the budget enforced |  |
| `test_budget_entries_naming_several_budgets_set_each` | three budget entries in both spellings each parse to their values | none | not held |  |  |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries0-'key']` | --budget key=1 is one invalid-usage diagnostic naming 'key', no bundle | `cli/an-unknown-budget-name-is-invalid-usage` | held |  | approved |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries1-carries no '=']` | --budget files is one invalid-usage diagnostic saying carries no '=', no bundle | `cli/a-malformed-budget-entry-is-invalid-usage` | held |  | approved |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries2-names no budget]` | --budget =1 is one invalid-usage diagnostic saying names no budget, no bundle | `cli/a-budget-entry-naming-no-budget-is-invalid-usage` | held |  | approved |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries3-no positive decimal integer]` | --budget files= is one invalid-usage diagnostic saying no positive decimal integer, no bundle | `limits/a-zero-override-is-refused`, `limits/a-negative-override-is-refused` | partly held | an empty value not exercised; message no positive decimal integer not asserted |  |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries4-no positive decimal integer]` | --budget files=0 is one invalid-usage diagnostic saying no positive decimal integer, no bundle | `limits/a-zero-override-is-refused` | partly held | message no positive decimal integer not asserted |  |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries5-files budget is named twice]` | files budget given twice is one invalid-usage diagnostic saying named twice, no bundle | `cli/a-budget-named-twice-is-refused` | held |  | approved |
| `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage[entries6-below 2]` | nesting=1 is one invalid-usage diagnostic saying below 2, no bundle | `cli/a-nesting-budget-below-two-is-refused` | held |  | approved |
| `test_an_unknown_budget_name_is_reported_with_every_name_admitted` | unknown budget name message lists every admitted budget name | `cli/an-unknown-budget-name-is-invalid-usage` | held |  | approved |
| `test_a_reference_selecting_again_counts_no_target` | re-selecting a reached document counts no target; targets=2 run succeeds | none | not held |  |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[files-2]` | files budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/a-file-count-budget-crossed`, `limits/a-named-budget-bounds-the-run` | partly held | remedy naming --budget files |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[file-bytes-16]` | file-bytes budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/a-source-byte-budget-crossed` | partly held | budget name in message; remedy naming --budget file-bytes |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[input-bytes-60]` | input-bytes budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/an-input-byte-budget-crossed` | partly held | budget name in message; remedy naming --budget input-bytes |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[output-bytes-64]` | output-bytes budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/an-output-byte-budget-crossed` | partly held | budget name in message; remedy naming --budget output-bytes |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[targets-2]` | targets budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/a-target-budget-crossed` | partly held | budget name in message; remedy naming --budget targets |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[links-1]` | links budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/a-link-budget-crossed` | partly held | budget name in message; remedy naming --budget links |  |
| `test_a_crossed_budget_fails_the_run_and_names_the_budget[depth-1]` | depth budget crossed fails E_RESOURCE_LIMIT, message and remedy name the budget, no bundle | `limits/an-expansion-depth-budget-crossed` | partly held | budget name in message; remedy naming --budget depth |  |
| `test_a_crossed_nesting_budget_fails_rather_than_reinterpreting_the_source` | Nesting deeper than the nesting budget fails E_RESOURCE_LIMIT | `limits/a-nesting-budget-crossed` | held |  | approved |
| `test_a_parsing_safety_budget_an_unselected_construct_crosses_names_the_source` | Unselected over-nested construct fails E_RESOURCE_LIMIT naming source, reference, chain, indexing message | `file-wide-safety/an-unselected-construct-crosses-a-safety-limit` | partly held | message wording (cannot be safely indexed) |  |
| `test_a_source_byte_budget_is_an_indexing_failure_too` | file-bytes budget on a section entry fails naming the source as an indexing failure | `limits/a-source-byte-budget-crossed` | partly held | source field on a section entry; message wording (cannot be safely indexed) |  |
| `test_a_run_wide_budget_names_no_single_source` | A run-wide files budget failure carries no source field and no indexing message | `limits/a-file-count-budget-crossed` | partly held | absence of the source field; message wording |  |
| `test_a_target_at_the_expansion_depth_is_bundled` | A target exactly at the depth budget is bundled | `limits/a-target-at-the-expansion-depth` | held |  | approved |
| `test_a_crossed_budget_publishes_no_output_file` | An output-bytes budget crossed fails and publishes no bundle | `limits/an-output-byte-budget-crossed` | held |  | approved |
| `test_a_budget_stands_at_the_number_the_profile_declares` | The files budget default is 256 and a plain run succeeds | `cli/a-bundle-written-into-the-working-directory` | partly held | the FILES.default constant equal to 256 |  |
| `test_a_lookup_the_parser_declines_fails_the_run` | A declined parser lookup fails E_PARSER_REFERENCE_LIMIT with source and chain, no bundle | `parser-limit/a-reference-lookup-the-parser-declines` | held |  | approved |
| `test_a_ceiling_reached_by_the_last_valid_reference_bundles_it` | Nesting reaching the ceiling on the last valid reference bundles it with no diagnostic | `parser-limit/a-nesting-ceiling-the-last-valid-reference-reaches` | held |  | approved |
| `test_a_declined_lookup_names_the_reference_under_the_default_budgets` | A declined lookup under default budgets fails E_PARSER_REFERENCE_LIMIT naming reference and source | `parser-limit/a-lookup-suppressed-below-every-declared-budget` | held |  | approved |
| `test_a_budget_spent_on_the_last_valid_reference_bundles_it` | Default nesting spent on the last valid reference bundles it without a parser-limit error | `parser-limit/a-budget-spent-on-the-last-valid-reference` | held |  | approved |
| `test_each_bundle_holds_the_file_budget_for_its_own_closure` | File budget counted per bundle closure: files=4 succeeds, files=3 fails with E_RESOURCE_LIMIT, nothing published | `dispatch/a-dispatched-target-crossing-the-file-budget` | partly held | the within-budget success at files=4 |  |
| `test_each_bundle_counts_expansion_depth_from_its_own_entry` | Expansion depth counted from each bundle's own entry: depth=1 succeeds publishing both bundles | none | not held |  |  |
| `test_a_multiplying_composition_fails_before_it_is_whole` | Multiplying composition crosses output budget mid-composition; reported count below the whole bundle size | `composition/a-multiplying-composition-crossing-the-output-budget` | partly held | the reported byte count lying between the budget and the whole bundle size |  |

### Diagnostics

17 tests: 2 held, 9 partly held, 6 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_short_diagnostic_forms_report_usage_as_json[arguments0]` | -djson then an unknown option gives usage failure as one JSON diagnostic | `cli/an-option-the-contract-does-not-declare` | partly held | the attached -djson spelling; the runner always passes -d json |  |
| `test_short_diagnostic_forms_report_usage_as_json[arguments1]` | -d=json then an unknown option gives usage failure as one JSON diagnostic | `cli/an-option-the-contract-does-not-declare` | partly held | the -d=json spelling; the runner always passes -d json |  |
| `test_short_diagnostic_forms_report_usage_as_json[arguments2]` | -cdjson then an unknown option gives usage failure as one JSON diagnostic | `cli/an-option-the-contract-does-not-declare` | partly held | the clustered -cdjson spelling; the runner always passes -d json |  |
| `test_short_diagnostic_forms_report_usage_as_json[arguments3]` | -d json then an unknown option gives usage failure as one JSON diagnostic | `cli/an-option-the-contract-does-not-declare` | held |  | approved |
| `test_diagnostic_selection_respects_values_terminators_and_last_option[arguments0]` | -djson after -- is an entry; suffix failure reported in text format | none | not held |  |  |
| `test_diagnostic_selection_respects_values_terminators_and_last_option[arguments1]` | -o-djson takes -djson as the folder; usage failure reported in text format | none | not held |  |  |
| `test_diagnostic_selection_respects_values_terminators_and_last_option[arguments2]` | last -d wins: -d=json then -dtext reports usage failure in text format | none | not held |  |  |
| `test_a_declared_root_is_an_input_failure` | entry declaring prosiform root fails with one E_INVALID_CONVERSION_METADATA at line 2 column 13 | `inclusion/a-declared-root-is-refused` | partly held | root declared on the entry itself; fixture declares it on a dependency |  |
| `test_no_code_reports_a_missing_root` | no E_ROOT_NOT_FOUND code exists | none | not held |  |  |
| `test_a_failing_run_writes_its_diagnostics_as_data` | a usage failure in JSON is one diagnostic carrying only the declared fields | `cli/an-option-the-contract-does-not-declare` | partly held | the bound on the diagnostic's field set |  |
| `test_a_failing_run_writes_its_diagnostics_as_text` | a usage failure in text format starts with the code and a colon | none | not held |  |  |
| `test_an_entry_reference_stands_at_the_head_of_its_own_chain` | entry fragment naming no heading fails with a chain of the entry alone | `file-wide-safety/an-unselected-construct-crosses-a-safety-limit`, `depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth` | partly held | an entry fragment naming no heading; fixtures show the entry heading its chain for other failures |  |
| `test_a_failure_names_every_reference_that_reached_it` | two-hop target failure carries chain, reference, resolved and source | `diagnostics/a-failure-two-hops-from-the-entry-reference` | held |  | approved |
| `test_a_document_a_dependency_reached_reports_the_route_to_it` | raw HTML in a dependency fails with one E_RAW_HTML whose chain is entry then dependency | `profile/raw-html-in-selected-content`, `diagnostics/a-failure-two-hops-from-the-entry-reference` | partly held | raw HTML in a dependency reported with its route chain |  |
| `test_a_refusal_names_the_construct_and_where_it_sits` | A wiki link refusal carries reference, guide.md:6 source and a message naming a wiki link | `profile/unsupported-construct` | partly held | message wording naming a wiki link |  |
| `test_a_coincidence_reads_as_text` | coincident file headings warning rendered in the human stderr format | `identity/two-documents-sharing-a-title` | partly held | human (non-JSON) diagnostic format; fixture holds only success and the code |  |
| `test_a_dispatch_warning_reads_as_text` | Human-format dispatch depth warning text with chain and related lines | none | not held |  |  |

### Headings and grouping

20 tests: 8 held, 11 partly held, 1 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_entry_naming_a_member_of_one_heading_opens_on_its_title` | entry naming a one-heading group member bundles opening on its title | `grouping/an-entry-naming-a-member-carrying-one-heading` | held |  | refused |
| `test_an_entry_naming_the_absorbed_title_of_a_member_opens_on_that_title` | entry fragment naming a member's absorbed title opens on that title | none | not held |  |  |
| `test_a_reference_into_a_member_of_one_heading_reaches_its_subsection` | link to a one-heading member is rewritten to its subsection anchor | `grouping/a-reference-to-a-member-carrying-one-heading` | held |  | approved |
| `test_two_untitled_sources_sharing_a_basename_stay_distinguishable` | Two untitled same-basename sources take path headings with their directories | `identity/same-basename-in-two-directories` | partly held | the untitled entry's own path heading |  |
| `test_two_sources_sharing_a_title_take_distinct_destinations` | Two same-title documents take note and note-1 destinations in link order | `identity/two-documents-sharing-a-title` | held |  | approved |
| `test_documents_are_ordered_as_the_entry_links_name_them` | Documents follow the order the entry's links name them, not path order | `determinism/groups-in-first-link-order`, `determinism/entry-references-in-source-order` | held |  | approved |
| `test_groups_are_ordered_by_first_link` | Groups follow first-link order: entry links before their dependencies' links | `determinism/groups-in-first-link-order`, `traversal/a-cycle-of-dependencies` | partly held | sibling links ordered before their own dependencies (branching order) |  |
| `test_members_are_ordered_by_first_link` | Group members follow the parent's link order, not path order | `grouping/a-document-no-group-matches` | partly held | a member link order that differs from path order |  |
| `test_one_document_named_twice_is_one_group` | A document reached by two spellings is bundled once | `normalization/two-spellings-of-one-document` | held |  | approved |
| `test_two_paths_differing_only_by_suffix_are_two_groups` | Paths differing only by suffix are two groups with exact bundle and W_COINCIDENT_HEADING | `identity/paths-differing-only-by-suffix` | held |  | approved |
| `test_coinciding_file_headings_warn_once_naming_every_source` | Three case-variant file headings warn once with exact message, remedy, location and related | `identity/two-documents-sharing-a-title` | partly held | one warning over three case-variant headings; message wording, remedy, location and related |  |
| `test_a_path_heading_is_located_at_its_document` | Coinciding path headings warn located at the first document, related naming the second | `identity/paths-differing-only-by-suffix` | partly held | path headings differing by case; location and related |  |
| `test_the_parent_title_coincides_with_a_file_heading` | The entry title coinciding with a linked file heading warns, located at guide.md | `identity/two-documents-sharing-a-title` | partly held | the entry's own heading in the coinciding set; location and related |  |
| `test_each_coinciding_set_warns_in_bundle_order` | Two coinciding heading sets each warn, in bundle order | `identity/two-documents-sharing-a-title` | partly held | two coinciding sets and the order of their warnings |  |
| `test_headings_an_author_repeats_warn_of_nothing` | Authored repeated headings across and within documents raise no warning | `destinations/source-heading-fragments` | partly held | repeats across documents and a subheading matching another file heading |  |
| `test_members_whose_names_coincide_publish_and_warn` | two group members named Note publish with distinct destinations and one coincident-heading warning | `grouping/two-members-sharing-a-name-beneath-an-entry` | partly held | exact message wording, remedy, location and related entry |  |
| `test_a_heading_beyond_the_sixth_level_fails_and_publishes_nothing` | heading shifted past level six fails E_HEADING_DEPTH_OVERFLOW, no bundle | `depth-overflow/a-source-heading-the-shift-pushes-past-the-sixth` | held |  | approved |
| `test_a_structural_ancestor_beyond_the_sixth_level_fails_by_its_own_name` | structural ancestor pushed past level six fails, message naming 'Levels' at level 7 | `depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth` | partly held | message naming the ancestor and level 7 |  |
| `test_a_heading_overflowing_in_a_later_member_names_that_member_s_chain` | overflow in a later group member names that member as source and chain | `grouping/a-nested-group-pushing-a-heading-past-the-sixth-fails` | partly held | overflow in the second member of a multi-member group (fixture group has one member) |  |
| `test_a_set_in_a_level_six_section_is_refused` | Set in a level-six section fails E_HEADING_DEPTH_OVERFLOW, nothing published | `parallel-dispatch/a-set-in-a-level-six-section-is-refused` | held |  | approved |

### Publication

27 tests: 13 held, 9 partly held, 5 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_run_folder_holding_a_dependency_source_is_invalid_usage` | run folder holding a dependency source is invalid usage, message input source, folder untouched | `cli/run-folder-holding-a-dependency-source` | partly held | message wording input source |  |
| `test_an_author_folder_named_like_the_entry_is_left_as_it_was` | author folder named like the entry is left as it was; bundle goes to guide.bundles | `cli/an-author-folder-named-like-the-entry-is-left-untouched` | held |  | approved |
| `test_a_bundle_is_written_into_the_folder_o_names` | -o build writes guide.bundles/guide.bundle.md with the expected bytes, stdout empty | `cli/a-bundle-written-into-the-folder-o-names` | held |  | approved |
| `test_a_bundle_is_written_into_the_working_directory_without_o` | without -o the bundle lands in the working directory, both streams empty | `cli/a-bundle-written-into-the-working-directory` | held |  | approved |
| `test_one_entry_source_selects_several_inputs` | a section entry linking other inputs names the run folder guide__run and carries the section once | `self-reference/a-section-link-to-its-whole-document`, `cli/several-entries-joined-into-one-name` | held |  | refused |
| `test_standard_output_named_as_the_folder_is_invalid_usage` | -o - is one invalid-usage diagnostic naming standard output, nothing written | `cli/standard-output-named-as-the-output-folder` | held |  | approved |
| `test_a_validation_only_run_publishes_nothing` | -c run leaves stdout empty and writes no bundle | `cli/validation-only-run` | held |  | approved |
| `test_a_validation_only_run_with_an_output_folder_writes_nothing` | -c with -o succeeds and leaves the folder empty | `cli/validation-only-run-with-an-output-folder` | held |  | approved |
| `test_a_refused_write_is_a_publication_failure` | refusing stdout on -v gives publication failure naming standard output | none | not held |  |  |
| `test_a_successful_run_publishes_the_bundle_and_nothing_else` | A successful run exits 0, no diagnostics, bundle bytes are the opening plus source | `cli/a-bundle-written-into-the-working-directory` | held |  | approved |
| `test_a_run_that_cannot_publish_reports_the_publication_failure_alone` | An output folder that cannot be made exits 3 with E_PUBLICATION_FAILED alone | `publication/an-output-folder-that-cannot-be-made-fails` | held |  | approved |
| `test_a_run_folder_is_published_through_one_rename` | run folder published by a single rename into the output folder | `cli/a-bundle-written-into-the-folder-o-names` | partly held | single rename (in-process os.rename observation) |  |
| `test_a_run_folder_replaces_the_earlier_one_whole` | earlier run folder replaced whole, stale dispatched bundle removed | none | not held |  |  |
| `test_a_failed_run_leaves_the_earlier_folder_alone` | failing run leaves an earlier run folder's bundle intact | `profile/raw-html-in-selected-content` | partly held | earlier run folder left intact; fixture holds only the failure |  |
| `test_an_output_path_the_run_cannot_make_is_a_publication_failure` | output folder under a file fails with publication status E_PUBLICATION_FAILED | `publication/an-output-folder-that-cannot-be-made-fails` | held |  | approved |
| `test_a_set_whose_member_fails_validation_writes_no_bundle` | set whose later member exceeds output budget fails E_RESOURCE_LIMIT, writes nothing, no warnings | `limits/an-output-byte-budget-crossed` | partly held | later member of a multi-bundle set failing; withheld member warnings; unit function's Failure |  |
| `test_a_set_whose_member_cannot_be_written_writes_no_bundle` | unwritable member fails E_PUBLICATION_FAILED naming it, earlier folder kept | none | not held |  |  |
| `test_two_bundles_deriving_one_name_publish_nothing[False]` | two bundles deriving one file name fail E_PUBLICATION_FAILED naming both sources, nothing written | none | not held |  |  |
| `test_two_bundles_deriving_one_name_publish_nothing[True]` | check run: two bundles deriving one name fail E_PUBLICATION_FAILED, nothing written | none | not held |  |  |
| `test_an_output_folder_that_does_not_exist_is_made_by_the_run[False]` | missing output folder is made along with the run folder | `publication/an-output-folder-that-does-not-exist-is-made` | held |  | approved |
| `test_an_output_folder_that_does_not_exist_is_made_by_the_run[True]` | check run makes the missing output folder but no run folder | `publication/a-check-run-into-a-folder-that-does-not-exist-makes-it` | held |  | approved |
| `test_a_set_is_published_whole_once_every_member_validates` | three-member set published together, member warnings reported after | `dispatch/each-section-keeps-its-own-dispatch-link-inline` | partly held | per-member warning reporting (unit function's Reporter output) |  |
| `test_a_validation_only_set_validates_every_member_and_writes_none` | check run writes nothing and still fails a member over the output budget | `cli/validation-only-run`, `limits/an-output-byte-budget-crossed` | partly held | output budget failure of a set member inside a check run |  |
| `test_a_set_leaves_every_file_it_does_not_produce_as_it_was` | publishing a set leaves unrelated files, folders and hidden files untouched | `cli/an-author-folder-named-like-the-entry-is-left-untouched` | partly held | another run's bundle folder and a hidden .run.new file beside the run folder |  |
| `test_a_run_leaves_every_file_in_its_folder_it_does_not_produce` | run into an -o folder leaves foreign files there as they were | `cli/a-bundle-written-into-the-folder-o-names` | partly held | pre-existing foreign bundle and note in the output folder |  |
| `test_a_validation_only_run_bundles_and_publishes_nothing` | -c run succeeds and writes no bundle | `cli/validation-only-run` | held |  | approved |
| `test_a_validation_only_run_still_reports_a_bundle_it_cannot_build` | -c run still fails E_HEADING_DEPTH_OVERFLOW | `depth-overflow/a-source-heading-the-shift-pushes-past-the-sixth`, `composition/a-composition-failing-in-a-check-run-publishes-nothing` | partly held | depth overflow under -c; fixtures hold each half separately |  |

### Source access

40 tests: 21 held, 12 partly held, 7 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_source_reached_through_a_link_is_refused_before_any_output_check` | symlinked entry fails with one E_SOURCE_SYMLINK and writes no folder | `cli/output-naming-what-a-link-points-at` | held |  | approved |
| `test_an_entry_reference_resolves_to_the_path_the_caller_wrote` | entry() resolves a dotted path as resolve() does (unit) | none | not held |  |  |
| `test_an_entry_suffix_outside_the_profile_is_an_input_failure` | A .txt entry fails exit 1 with E_UNSUPPORTED_ENTRY_SUFFIX naming the reference | `profile/entry-suffix-outside-the-profile` | held |  | approved |
| `test_an_entry_suffix_is_classified_case_insensitively` | An upper-case Markdown suffix entry bundles successfully | `profile/markdown-suffixes-in-mixed-case` | held |  | approved |
| `test_an_entry_naming_no_document_is_an_input_failure` | An entry naming a file that does not exist fails exit 1 with E_TARGET_NOT_FOUND | none | not held |  |  |
| `test_an_entry_the_root_cannot_contain_is_an_input_failure[/guide.md]` | A root-relative entry fails exit 1 with E_SOURCE_OUTSIDE_ROOT | `normalization/root-relative-entry-reference` | held |  | approved |
| `test_an_entry_the_root_cannot_contain_is_an_input_failure[C:/guide.md]` | A drive-path entry fails exit 1 with E_SOURCE_OUTSIDE_ROOT | `normalization/a-drive-path` | held |  | approved |
| `test_an_entry_the_root_cannot_contain_is_an_input_failure[//host/guide.md]` | A protocol-relative entry fails exit 1 with E_SOURCE_OUTSIDE_ROOT | `normalization/a-protocol-relative-url` | held |  | approved |
| `test_a_source_that_is_not_valid_utf8_is_an_input_failure` | A non-UTF-8 byte fails exit 1 with E_INVALID_ENCODING at guide.md, message naming UTF-8, no bundle | `profile/source-not-utf8`, `profile/invalid-byte-mid-document` | partly held | message wording naming UTF-8 |  |
| `test_a_source_that_is_not_valid_utf8_reaches_no_generic_handler` | A UTF-16 byte-order-marked source fails exit 1 with a specific error, not the internal fault | `profile/utf16-byte-order-mark` | held |  | refused |
| `test_a_probe_answers_a_silent_target_whatever_its_size` | probe answers SILENT for oversized undeclaring targets, with or without a block | `inclusion/an-oversized-silent-target-is-text` | partly held | the unit return; a silent target headed by a title-only block |  |
| `test_a_probe_answers_a_declaring_target` | probe answers DECLARING for a byte-order-marked CRLF dot-closed declaration | `inclusion/an-oversized-declaring-target-fails` | partly held | the unit return; byte-order mark, CRLF and dot-closer spellings on a probed target |  |
| `test_a_probe_crossing_the_byte_budget_before_its_closer_fails` | probe raises E_RESOURCE_LIMIT when the block closer lies past the byte budget | `inclusion/an-oversized-declaring-target-fails` | partly held | the unit raise; a closer lying past the budget |  |
| `test_a_probe_refuses_an_invalid_declaration` | probe raises invalid metadata for a bad key and unterminated frontmatter for an open block | `inclusion/a-preset-key-holding-a-scalar-is-refused` | partly held | the unit raise; an unterminated block on a probed target |  |
| `test_a_probe_refuses_a_link` | probe raises E_SOURCE_SYMLINK for a symbolic link | `inclusion/a-probe-follows-no-link` | partly held | the unit raise; the CLI outcome is held |  |
| `test_a_fragment_selects_the_section_its_heading_roots` | entry fragment bundles the section its heading roots | `extraction/section-to-the-next-sibling`, `extraction/a-subsection-inside-the-section` | held |  | approved |
| `test_a_fragment_naming_a_container_nested_heading_is_refused` | entry fragment naming a blockquote-nested heading fails E_NESTED_SECTION_TARGET | `extraction/nested-section-target` | held |  | approved |
| `test_a_fragment_naming_no_heading_is_a_missing_target` | entry fragment naming no heading fails E_TARGET_NOT_FOUND | `extraction/a-heading-only-in-a-code-example`, `identity/an-ordinal-names-no-source-heading` | held |  | approved |
| `test_an_empty_fragment_is_a_whole_document_reference` | entry reference guide.md# bundles the whole document as guide.md does | `normalization/an-empty-fragment` | partly held | empty fragment on an entry reference; fixture covers a link |  |
| `test_a_title_the_allowed_source_root_cannot_contain_names_no_document` | A heading spelling a path above the root resolves nothing and the run succeeds silently | none | not held |  |  |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the spec](https://e.test/s.md)-\xac]` | Deferral link to a remote address refused E_UNSUPPORTED_CONSTRUCT at guide.md:6, nothing published | `deferral/a-deferred-link-naming-a-remote-address` | held |  | approved |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the spec](https://e.test/s.md)-\u21c9]` | Dispatch link to a remote address refused E_UNSUPPORTED_CONSTRUCT at guide.md:6, nothing published | `dispatch/a-dispatched-link-naming-a-remote-address` | held |  | approved |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the diagram](plan.png)-\xac]` | Deferral link to a non-Markdown resource refused E_UNSUPPORTED_CONSTRUCT at guide.md:6 | `deferral/a-deferred-link-naming-a-resource` | held |  | refused |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the diagram](plan.png)-\u21c9]` | Dispatch link to a non-Markdown resource refused E_UNSUPPORTED_CONSTRUCT at guide.md:6 | `dispatch/a-dispatched-link-naming-a-resource` | held |  | refused |
| `test_an_operator_naming_no_document_under_the_root_is_refused[![{mark} the architecture](plan.png)-\xac]` | Deferral image refused E_UNSUPPORTED_CONSTRUCT at guide.md:6, nothing published | `deferral/a-deferred-image` | held |  | approved |
| `test_an_operator_naming_no_document_under_the_root_is_refused[![{mark} the architecture](plan.png)-\u21c9]` | Dispatch image refused E_UNSUPPORTED_CONSTRUCT at guide.md:6, nothing published | `dispatch/a-dispatched-image` | held |  | approved |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the rules](../outside.md)-\xac]` | Deferral link to a document above the root refused E_UNSUPPORTED_CONSTRUCT at guide.md:6 | `deferral/a-deferred-link-naming-a-document-above-the-working-directory` | held |  | approved |
| `test_an_operator_naming_no_document_under_the_root_is_refused[[{mark} the rules](../outside.md)-\u21c9]` | Dispatch link to a document above the root refused E_UNSUPPORTED_CONSTRUCT at guide.md:6 | `dispatch/a-dispatched-link-naming-a-document-above-the-working-directory` | held |  | approved |
| `test_a_parallel_link_naming_no_markdown_under_the_root_is_refused[https://example.test/plan.md]` | Parallel link to a remote address refused E_UNSUPPORTED_CONSTRUCT naming the reference | `parallel-dispatch/a-parallel-link-naming-a-remote-address` | held |  | approved |
| `test_a_parallel_link_naming_no_markdown_under_the_root_is_refused[image.png]` | Parallel link to a non-Markdown resource refused E_UNSUPPORTED_CONSTRUCT naming the reference | none | not held |  |  |
| `test_each_diagram_fence_is_read_once_per_parse_of_a_run` | Each diagram fence parsed once per run; sequence links line rewritten | `rewriting/a-sequence-diagram-link-and-links-line-anchors` | partly held | the read-once count of diagram fences (in-process) |  |
| `test_an_operator_naming_no_document_is_a_missing_target[\xac]` | Deferral link to missing document: E_TARGET_NOT_FOUND with reference, source, chain, names-no-document message | `deferral/a-deferred-reference-naming-no-document`, `publication/a-failing-run-publishes-no-bundle` | partly held | message wording names no document |  |
| `test_an_operator_naming_no_document_is_a_missing_target[\u21c9]` | Dispatch link to missing document: E_TARGET_NOT_FOUND with reference, source, chain, names-no-document message | `inclusion/operators-keep-the-absent-target-refusal` | partly held | message wording names no document |  |
| `test_an_operator_naming_no_document_is_a_missing_target[\u2afd]` | Parallel link to missing document: E_TARGET_NOT_FOUND with reference, source, chain, names-no-document message | none | not held |  |  |
| `test_an_operator_naming_a_silent_document_is_refused[\xac]` | Deferral link to a silent document refused E_UNSUPPORTED_CONSTRUCT, declares-no-prosiform message | `deferral/a-deferred-link-naming-a-document-above-the-working-directory` | partly held | silent document inside the root and declares no prosiform wording |  |
| `test_an_operator_naming_a_silent_document_is_refused[\u21c9]` | Dispatch link to a silent document refused E_UNSUPPORTED_CONSTRUCT, declares-no-prosiform message | `dispatch/a-dispatching-click-naming-a-document-that-declares-nothing-is-refused`, `dispatch/a-dispatched-link-naming-a-document-above-the-working-directory` | partly held | a Markdown link form naming a silent document inside the root |  |
| `test_an_operator_naming_a_silent_document_is_refused[\u2afd]` | Parallel link to a silent document refused E_UNSUPPORTED_CONSTRUCT, declares-no-prosiform message | none | not held |  |  |
| `test_a_fragment_only_link_naming_no_heading_is_a_missing_target` | Fragment-only link naming no heading: E_TARGET_NOT_FOUND, reference, resolved, source | `inclusion/a-fragment-naming-no-heading` | held |  | approved |
| `test_an_entry_naming_a_silent_document_fails_before_any_source_is_read` | Entry naming a silent document fails E_TARGET_NOT_FOUND before reading other sources | `inclusion/an-entry-naming-a-silent-document` | held |  | approved |
| `test_an_entry_naming_no_document_is_a_missing_target` | Entry naming no document fails E_TARGET_NOT_FOUND with names-no-document message | none | not held |  |  |

### Presets and subst

61 tests: 17 held, 29 partly held, 15 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_entry_is_bundled_as_named_whatever_its_presets_state` | entry's own subst pair does not redirect it; bundle is the entry; W_SUBST_UNUSED | `inclusion/an-entry-is-not-substituted` | held |  | approved |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries0-prosiform.default.subst[1] key './rules.md' names the identity the key of prosiform.default.subst[0] names]` | Two subst keys naming one document exit 2 E_INVALID_USAGE at guide.md, no bundle | `inclusion/a-duplicate-subst-entry-is-refused` | held |  | approved |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries1-prosiform.default.subst[1] key 'rules.md#Checks' names the identity]` | Two identical section subst keys exit 2 E_INVALID_USAGE at guide.md | `inclusion/a-duplicate-subst-entry-is-refused` | partly held | duplicate keys carrying a section fragment |  |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries2-prosiform.default.subst[1] key 'notes/../rules.md' names the identity]` | A parent-segment subst key duplicating another exits 2 E_INVALID_USAGE at guide.md | `inclusion/a-duplicate-subst-entry-is-refused` | partly held | a duplicate key spelled with a parent segment |  |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries3-prosiform.default.subst[0] maps 'rules.md' to './rules.md', which name one identity]` | A subst key mapped to itself exits 2 E_INVALID_USAGE at guide.md | `inclusion/a-subst-key-naming-its-value-is-refused` | held |  | approved |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries4-prosiform.default.subst[0] maps 'guide.md#Checks' to '#Checks', which name one identity]` | A section key mapped to its own fragment-only spelling exits 2 E_INVALID_USAGE | `inclusion/a-subst-key-naming-its-value-is-refused` | partly held | a section key against a fragment-only value of the same document |  |
| `test_a_subst_rule_stated_twice_or_against_itself_is_refused[entries5-prosiform.default.subst[0] key '#Checks' names a section alone]` | A fragment-only subst key exits 2 E_INVALID_USAGE at guide.md | `inclusion/a-section-only-subst-key-is-refused` | held |  | approved |
| `test_subst_keys_naming_distinct_identities_are_admitted[entries0]` | A document key and a section key of it are both admitted | `mock/a-document-key-and-a-section-key-together` | held |  | approved |
| `test_subst_keys_naming_distinct_identities_are_admitted[entries1]` | Same-basename keys in different folders are both admitted | none | not held |  |  |
| `test_subst_keys_naming_distinct_identities_are_admitted[entries2]` | A section key mapped to a fragment-only value is admitted | none | not held |  |  |
| `test_two_selected_presets_stating_different_group_pairs_are_refused[drafted0-{reviews: 2}]` | Co-selected presets with different group depths exit 2 with exact message, location, related | `inclusion/two-presets-disagreeing-are-refused` | partly held | exact message with the selecting tags; related entry |  |
| `test_two_selected_presets_stating_different_group_pairs_are_refused[drafted1-{drafts: 1}]` | Co-selected presets with different groups exit 2 with exact message, location, related | `inclusion/two-presets-stating-two-groups-are-refused` | partly held | exact message with the selecting tags; related entry |  |
| `test_two_selected_presets_mapping_one_key_two_ways_are_refused` | Co-selected presets mapping one key two ways exit 2 with exact message and related | `inclusion/two-presets-disagreeing-about-a-subst-key-are-refused` | partly held | keys differing only in spelling; exact message and related entry |  |
| `test_selected_presets_agreeing_about_a_setting_union` | Co-selected presets agreeing on group and subst union; document placed once under Reviews | `inclusion/a-link-title-selecting-two-complete-preset-names` | partly held | agreeing subst pairs spelled differently |  |
| `test_a_selected_preset_disagreeing_with_default_holds_over_it` | A selected preset's group and subst hold over default's without refusal | `inclusion/a-pair-a-selected-preset-overrides-records-no-substitution` | partly held | a selected group pair holding over default's group pair |  |
| `test_presets_one_tag_selection_leaves_unselected_disagree_with_nothing` | An unselected preset disagreeing with the selected one causes no refusal | `inclusion/one-document-two-presets` | held |  | approved |
| `test_a_linking_documents_presets_never_reach_the_document_it_links` | A link entry's selected preset places the guide; the linked document keeps its own default | `inclusion/a-dependencys-preset-comes-from-itself` | partly held | the linking document's default overridden and the linked document's default applying |  |
| `test_a_preset_no_tag_selects_warns_and_the_run_publishes` | Two unselected presets warn in order with exact message, no location and remedy; run publishes | `inclusion/a-section-matching-no-preset-selects-default` | partly held | two warnings in order; full message, absent location, remedy wording |  |
| `test_selected_presets_and_default_warn_nothing` | A selected preset beside default publishes with empty stderr | `inclusion/a-pair-a-selected-preset-overrides-records-no-substitution` | held |  | approved |
| `test_a_preset_one_reference_selects_is_used_though_another_leaves_it` | A preset one link selects raises no unused warning though another link leaves it | `inclusion/one-document-two-presets` | partly held | an untagged reference beside the selecting one |  |
| `test_a_preset_a_dispatched_bundle_selects_is_used` | A preset selected inside a dispatched bundle raises no unused warning; two bundles | `inclusion/a-stage-routing-on-two-axes-raises-no-warning` | partly held | a preset selected by a link inside a dispatched bundle |  |
| `test_a_preset_on_a_deferred_only_document_warns_nothing` | A deferred-only document's preset warns nothing; deferral published as authored | `inclusion/a-deferred-target-keeps-its-preset` | held |  | approved |
| `test_a_document_both_deferred_and_bundled_is_weighed` | A document both deferred and bundled has its unselected preset warned | `inclusion/a-section-matching-no-preset-selects-default` | partly held | a document both deferred and bundled |  |
| `test_an_entry_carrying_no_title_selects_no_named_preset[guide.md#plan]` | plain path entry selects no named preset; no Reviews group | `inclusion/a-whole-document-entry-selects-default`, `inclusion/an-unused-preset-warns` | held |  | approved |
| `test_an_entry_carrying_no_title_selects_no_named_preset[[Plan](guide.md#plan)]` | untitled Markdown link entry selects no named preset; no Reviews group | `inclusion/a-whole-document-entry-selects-default` | partly held | untitled Markdown link entry form |  |
| `test_an_entry_carrying_no_title_selects_no_named_preset[click Plan "guide.md#plan"]` | click entry without tooltip selects no named preset; no Reviews group | `inclusion/a-whole-document-entry-selects-default` | partly held | click line entry carrying no tooltip |  |
| `test_two_sections_reaching_one_document_each_select_its_presets` | two sections select Checks and Draft of one document; it appears under Reviews and Drafts | `inclusion/one-document-two-presets`, `grouping/a-group-placed-by-a-document-in-two-groups` | held |  | approved |
| `test_a_document_a_later_round_reaches_again_takes_that_selection` | a later-discovered document's link selects Draft on an already reached document | `inclusion/two-documents-placing-one-document-in-two-groups`, `inclusion/a-later-title-selection-activates-a-direct-substitution` | partly held | a later-round link adding a group placement to a document the entry already selected |  |
| `test_two_sections_selecting_two_depths_for_one_group_conflict` | two presets of one document give one group two depths: exit 1, E_GROUP_CONFLICT | `grouping/conflicting-member-depths` | partly held | conflict arising from two presets of one document selected by two references |  |
| `test_a_selected_preset_pair_holds_over_default` | pair(): selected preset's group pair over default; default otherwise; None without either | `inclusion/two-documents-placing-one-document-in-two-groups`, `inclusion/default-applies-in-every-section`, `inclusion/a-section-matching-no-preset-selects-default` | partly held | the unit function's return, including None when no preset states a pair |  |
| `test_a_whole_document_link_entry_selects_by_its_title` | whole-document link entry titled checks bundles under Reviews (exact bundle) | `inclusion/a-dependencys-preset-comes-from-itself` | held |  | approved |
| `test_an_untitled_whole_document_entry_selects_no_preset` | plain path entry selects no preset; bundle not under Reviews | `inclusion/a-whole-document-entry-selects-default`, `inclusion/an-unused-preset-warns` | held |  | approved |
| `test_a_reference_in_a_preamble_selects_no_preset` | untitled preamble link selects no preset of its target | `inclusion/a-link-title-selects-its-preset` | partly held | the link written in a preamble |  |
| `test_a_tagged_reference_selects_independently_of_heading_nesting[### Detail\n\n-True]` | tagged link under a nested subheading still selects Checks | `inclusion/a-presets-pairs-reach-the-reference-it-governs` | partly held | a deeper subheading between the section and the link |  |
| `test_a_tagged_reference_selects_independently_of_heading_nesting[> ### Quoted\n\n-True]` | tagged link after a blockquoted heading still selects Checks | `inclusion/a-presets-pairs-reach-the-reference-it-governs` | partly held | a heading inside a blockquote before the link |  |
| `test_a_depth_disagreement_names_the_selected_preset` | group depth conflict: E_GROUP_CONFLICT message and related entry name selected Checks preset | `grouping/conflicting-member-depths` | partly held | message naming the selected preset; related location and message |  |
| `test_an_unknown_prosiform_key_fails[dispatch]` | prosiform key dispatch holding a scalar fails E_INVALID_CONVERSION_METADATA | `inclusion/a-preset-key-holding-a-scalar-is-refused` | partly held | key named dispatch |  |
| `test_an_unknown_prosiform_key_fails[dispatched]` | prosiform key dispatched holding a scalar fails E_INVALID_CONVERSION_METADATA | `inclusion/a-preset-key-holding-a-scalar-is-refused` | partly held | key named dispatched |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{"rules.md?x": stub.md}-rules.md?x-carries the query 'x']` | subst side carrying a query fails E_INVALID_CONVERSION_METADATA at the entry | `inclusion/a-subst-side-is-read-by-the-reference-grammar` | held |  | approved |
| `test_a_subst_side_is_read_by_the_reference_grammar[{rules.md: "stub%zz.md"}-stub%zz.md-carries the escape '%zz']` | subst side carrying a bad escape fails, naming it | none | not held |  |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{rules.md: "stub%2Fx.md"}-stub%2Fx.md-decodes to a path separator]` | subst side decoding to a path separator fails, naming it | none | not held |  |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{"/rules.md": stub.md}-/rules.md-names the root-relative path]` | root-relative subst side fails, naming it | none | not held |  |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{"C:/rules.md": stub.md}-C:/rules.md-names the drive path]` | drive-path subst side fails, naming it | none | not held |  |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{"rules\\\\x.md": stub.md}-rules\\x.md-with a backslash]` | subst side with a backslash fails, naming it | none | not held |  |  |
| `test_a_subst_side_is_read_by_the_reference_grammar[{rules.md: "https://example.com/stub.md"}-https://example.com/stub.md-carries a scheme or an authority, so it names no local document]` | subst side carrying a scheme fails as naming no local document | none | not held |  |  |
| `test_a_subst_pair_the_reference_grammar_reads_is_admitted` | sides above the root, encoded, or quoted for a colon are admitted and each warns unused | `inclusion/a-subst-side-is-read-by-the-reference-grammar`, `mock/an-unused-key-warns-and-publishes` | partly held | ../ side and %20 key admitted; each pair warning W_SUBST_UNUSED on a successful run |  |
| `test_a_used_routing_pair_raises_no_warning` | An alternative's used routing pair redirects the link and raises no diagnostic | `inclusion/a-used-routing-pair-raises-no-warning` | held |  | approved |
| `test_a_routing_pair_whose_link_sits_outside_the_selection_stays_quiet` | A routing pair whose key only an unselected section links raises nothing and bundles no substitute | `inclusion/a-routing-pair-outside-the-selection-stays-quiet` | held |  | approved |
| `test_a_routing_pair_naming_a_section_is_named_by_a_link_to_it` | A section-keyed routing pair named by an unselected link to that section raises nothing | `inclusion/a-routing-pair-outside-the-selection-stays-quiet` | partly held | a section-keyed pair (checklist.md#steps) rather than a whole-document key |  |
| `test_a_routing_pair_no_link_of_its_document_names_warns_unused` | Pairs no link of the document names warn W_SUBST_UNUSED in order, message naming the document | `inclusion/a-stale-routing-pair-warns-unused` | partly held | the second warning for a section-keyed pair (checklist.md#other); message wording beyond the document name |  |
| `test_a_stand_in_beside_a_routing_pair_still_warns` | A stub pair beside an alternative's routing pair warns W_SUBST_USED with fragment source and resolved | `inclusion/a-shim-s-stub-warns-beside-a-stage-s-routes` | partly held | the route is an alternative's pair, not an ordinary preset; fragment-keyed source checklist.md#steps resolved stub.md#steps |  |
| `test_a_pair_an_ordinary_preset_shares_routes_in_either_order[order0]` | A pair stated by both an alternative and an ordinary preset routes silently, alternative first | `inclusion/a-shared-pair-routes-with-the-alternative-first` | held |  | approved |
| `test_a_pair_an_ordinary_preset_shares_routes_in_either_order[order1]` | A pair stated by both an ordinary preset and an alternative routes silently, ordinary preset first | `inclusion/a-shared-pair-routes-with-the-ordinary-preset-first` | held |  | approved |
| `test_a_stand_in_no_selected_link_uses_still_warns_unused` | A stub key linked only in an unselected section warns W_SUBST_UNUSED | `inclusion/an-entry-stub-no-link-uses-warns` | partly held | the stub's key is linked by an unselected section of the document, not by no document |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key0-identities0-True]` | Unit names(): whole-document key named by a whole-document link | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key1-identities1-True]` | Unit names(): whole-document key named by a section link | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key2-identities2-True]` | Unit names(): section key named by a link to that section | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key3-identities3-False]` | Unit names(): section key not named by a whole-document link | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key4-identities4-False]` | Unit names(): section key not named by a link to another section | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key5-identities5-False]` | Unit names(): key not named by a link to another path | none | not held |  |  |
| `test_a_link_names_a_key_for_its_section_or_its_whole_document[key6-identities6-False]` | Unit names(): key not named by an empty link set | none | not held |  |  |

### Profile

13 tests: 8 held, 3 partly held, 2 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n<div>raw</div>\n-E_RAW_HTML]` | Block raw HTML fails exit 1, one E_RAW_HTML error at a guide.md line, no bundle | `profile/raw-html-in-selected-content` | held |  | approved |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nA paragraph carrying <span>raw</span> markup.\n-E_RAW_HTML]` | Inline raw HTML fails exit 1, one E_RAW_HTML error at a guide.md line, no bundle | `reference/an-html-link-naming-a-local-document` | held |  | approved |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nSee [[page]] for the procedure.\n-E_UNSUPPORTED_CONSTRUCT]` | A wiki link fails exit 1 with one E_UNSUPPORTED_CONSTRUCT at a guide.md line | `profile/unsupported-construct` | held |  | approved |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n![[page]]\n-E_UNSUPPORTED_CONSTRUCT]` | A wiki embed fails exit 1 with one E_UNSUPPORTED_CONSTRUCT at a guide.md line | `profile/unsupported-construct` | partly held | the embed spelling with a leading exclamation mark is not exercised; only a plain wiki link |  |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nA claim[^1] needing support.\n-E_UNSUPPORTED_CONSTRUCT]` | A footnote reference fails exit 1 with one E_UNSUPPORTED_CONSTRUCT at a guide.md line | none | not held |  |  |
| `test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n## Run {#custom-id}\n-E_UNSUPPORTED_CONSTRUCT]` | A heading attribute fails exit 1 with one E_UNSUPPORTED_CONSTRUCT at a guide.md line | none | not held |  |  |
| `` test_a_source_the_profile_accepts_bundles[# Guide\n\nA code span naming `[[page]]` is prose about a wiki link.\n] `` | A wiki link inside a code span bundles successfully | `profile/extension-lookalikes` | held |  | approved |
| `test_a_source_the_profile_accepts_bundles[# Guide\n\nAn escaped \\[\\[page\\]\\] is literal text.\n]` | An escaped wiki link spelling bundles successfully | `profile/extension-lookalikes` | held |  | approved |
| `test_a_source_the_profile_accepts_bundles[# Guide\n\nA paragraph mentioning {#custom-id} names no section.\n]` | An attribute spelling in paragraph prose bundles successfully | `profile/extension-lookalikes` | held |  | approved |
| `` test_a_source_the_profile_accepts_bundles[# Guide\n\n```html\n<div>raw</div>\n```\n] `` | HTML inside a fenced code block bundles successfully | `profile/html-in-a-code-example` | held |  | approved |
| `test_a_source_the_profile_accepts_bundles[# Guide\n\n- [ ] open\n- [x] done\n\n[x]: page.md\n]` | Task markers beside a definition labelled x bundle successfully | `profile/task-markers-protected-from-definitions` | held |  | approved |
| `test_a_section_entry_is_read_under_the_profile` | A section entry carrying raw HTML fails exit 1; human stderr opens with E_RAW_HTML naming guide.md | `composition/a-deferred-body-that-fails-fails-when-activated` | partly held | the human (non-JSON) diagnostic format |  |
| `test_a_fragment_reference_reads_the_whole_document_it_names` | A fragment entry whose section carries raw HTML fails exit 1; human stderr opens with E_RAW_HTML | `composition/a-deferred-body-that-fails-fails-when-activated` | partly held | the human (non-JSON) diagnostic format |  |

### Frontmatter

15 tests: 9 held, 3 partly held, 3 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_unterminated_frontmatter_opener_is_an_input_failure` | An unclosed opener fails exit 1 with E_UNTERMINATED_FRONTMATTER at guide.md:1, no bundle | `frontmatter/unterminated-block` | held |  | approved |
| `test_transport_metadata_reaches_no_parse` | A byte-order mark and metadata block are stripped; raw HTML below fails with a raw HTML message | `profile/raw-html-in-selected-content`, `frontmatter/optional-mark` | partly held | message wording; no fixture refuses content below a byte-order-marked block |  |
| `test_a_diagnostic_below_a_stripped_block_names_the_line_of_the_file` | A diagnostic below a stripped metadata block names the file line | `profile/unsupported-construct` | held |  | refused |
| `test_a_diagnostic_below_a_mark_and_its_block_names_the_line_of_the_file` | A diagnostic below a byte-order mark and block names the file line | `profile/unsupported-construct`, `frontmatter/optional-mark` | partly held | line numbering below a byte-order mark |  |
| `test_a_first_line_that_is_no_opener_declares_nothing[ ---\nprosiform: {}\n---\n\nSee [[page]] now.\n]` | An indented first delimiter declares nothing: E_TARGET_NOT_FOUND, declares no prosiform | `frontmatter/indented-delimiter` | held |  | approved |
| `test_a_first_line_that_is_no_opener_declares_nothing[--- \nprosiform: {}\n---\n\nSee [[page]] now.\n]` | A delimiter with trailing space declares nothing: E_TARGET_NOT_FOUND, declares no prosiform | `frontmatter/delimiter-with-trailing-spaces` | held |  | approved |
| `test_a_first_line_that_is_no_opener_declares_nothing[+++\nprosiform = {}\n+++\n\nSee [[page]] now.\n]` | A TOML fence declares nothing: E_TARGET_NOT_FOUND, declares no prosiform | `frontmatter/toml-fence` | held |  | approved |
| `test_a_first_line_that_is_no_opener_declares_nothing[{\n  "prosiform": {}\n}\n\nSee [[page]] now.\n]` | A JSON object head declares nothing: E_TARGET_NOT_FOUND, declares no prosiform | none | not held |  |  |
| `test_a_first_line_that_is_no_opener_declares_nothing[***\nprosiform: {}\n---\n\nSee [[page]] now.\n]` | A thematic-break first line declares nothing: E_TARGET_NOT_FOUND, declares no prosiform | none | not held |  |  |
| `test_a_first_line_that_is_no_opener_declares_nothing[\n---\nprosiform: {}\n---\n\nSee [[page]] now.\n]` | A blank first line leaves no opener: E_TARGET_NOT_FOUND, declares no prosiform | `frontmatter/leading-blank-line` | held |  | approved |
| `test_a_crlf_delimited_block_is_stripped_by_the_command` | A CRLF-delimited block is stripped and a diagnostic below names file line 5 | `frontmatter/crlf-delimiters`, `profile/unsupported-construct` | partly held | diagnostic line numbering below a CRLF block |  |
| `test_a_section_entry_is_stripped_too` | A section entry below a stripped block fails naming the file line | `composition/a-deferred-body-that-fails-fails-when-activated` | held |  | approved |
| `test_a_stripped_source_the_profile_accepts_bundles` | A byte-order mark plus a dot-closed block bundles successfully | `frontmatter/optional-mark`, `frontmatter/dot-terminated` | held |  | approved |
| `test_a_crlf_source_is_read_without_newline_translation` | read_document keeps CRLF body text and reports first line 4 | none | not held |  |  |
| `test_metadata_carries_no_conversion_meaning` | A dispatch key under metadata has no effect and its text is not bundled | `frontmatter/a-metadata-field-carries-no-conversion-meaning` | held |  | approved |

### Alternatives and picks

21 tests: 4 held, 16 partly held, 1 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_document_with_no_alternative_in_force_is_refused[]` | An untitled link to an alternatives document exits 2 E_ALTERNATIVE_UNRESOLVED listing them | `inclusion/no-pick-of-an-alternative-fails` | held |  | approved |
| `test_a_document_with_no_alternative_in_force_is_refused[ "saga"]` | An unknown title name exits 2 E_ALTERNATIVE_UNRESOLVED listing the alternatives | `inclusion/an-unknown-alternative-name-fails` | held |  | approved |
| `test_a_document_with_no_alternative_in_force_is_refused[ "checks"]` | A title selecting only an ordinary preset exits 2 E_ALTERNATIVE_UNRESOLVED | `inclusion/no-pick-of-an-alternative-fails` | partly held | a title selecting only an ordinary preset |  |
| `test_an_entry_carrying_no_pick_token_is_refused_with_a_remedy_the_run_accepts[work-kind.md-[Body](work-kind.md "epic")]` | The routed document as entry is refused with a remedy; --pick is invalid; a picking link entry bundles | `inclusion/no-pick-of-an-alternative-fails`, `cli/a-pick-beside-a-plain-path-is-invalid-usage`, `inclusion/a-link-picks-an-alternative-beside-an-ordinary-preset` | partly held | the routed document as the entry itself; remedy wording |  |
| `test_an_entry_carrying_no_pick_token_is_refused_with_a_remedy_the_run_accepts[guide.md-guide.md]` | An unpicked link is refused with a remedy; --pick is invalid; a picking link bundles | `inclusion/no-pick-of-an-alternative-fails`, `cli/a-pick-beside-a-plain-path-is-invalid-usage`, `inclusion/a-link-picks-an-alternative-beside-an-ordinary-preset` | partly held | remedy wording |  |
| `test_a_copy_an_alternative_routes_is_remedied_at_the_link_placing_it[links0-stage.md#given-write the brief 'stage.md#given' so it bundles with no alternative in force, since the picking dispatch carrying it leaves the pick to its agent]` | A picking dispatch whose brief is routed exits 2 naming stage.md#given with the brief remedy | `dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` | partly held | remedy wording |  |
| `test_a_copy_an_alternative_routes_is_remedied_at_the_link_placing_it[links1-stage.md#given-name the alternative that fits your task in the title of the directive or dispatch placing this copy]` | A non-picking dispatch whose brief is routed exits 2 naming stage.md#given with the copy remedy | `dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` | partly held | a dispatch carrying no pick token; remedy wording |  |
| `test_a_copy_an_alternative_routes_is_remedied_at_the_link_placing_it[links2-stage.md#given-write the brief 'stage.md#given' so it bundles with no alternative in force, since the picking dispatch carrying it leaves the pick to its agent]` | composition copy then picking dispatch: E_ALTERNATIVE_UNRESOLVED, reference stage.md#given, brief remedy | `dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` | partly held | remedy text; a composed copy written before the picking dispatch |  |
| `test_a_copy_an_alternative_routes_is_remedied_at_the_link_placing_it[links3-stage.md#notes-name the alternative that fits your task in the title of the directive or dispatch placing this copy]` | two unpicked composed copies: E_ALTERNATIVE_UNRESOLVED names routed copy stage.md#notes, copy remedy | `composition/a-copy-picking-no-alternative-beside-one-picking-one-is-refused` | partly held | remedy text; reference choosing the routed copy among two unpicked copies |  |
| `test_a_picking_dispatch_s_brief_fails_at_the_picking_dispatch` | plain then picking dispatch: failure at picking dispatch line, reference stage.md#given, brief remedy | `dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` | partly held | remedy text; a plain dispatch of the same target written first |  |
| `test_a_default_pair_an_alternative_agrees_with_routes_in_a_copy` | composed copy picking alpha whose pair agrees with default publishes with no diagnostics | `inclusion/a-default-pair-an-alternative-agrees-with-routes`, `composition/an-ordinary-preset-agreeing-with-a-copys-alternative-routes` | partly held | default pair agreeing inside a composed copy (fixtures cover an inclusion link, or an ordinary preset in a copy) |  |
| `test_an_entry_picking_one_alternative_bundles_its_route` | link entry titled task bundles task body; Checks warns W_PRESET_UNUSED with exact message | `inclusion/an-unpicked-alternative-raises-no-warning` | partly held | pick made in a link entry title; exact warning message |  |
| `test_a_first_run_pick_bundles_the_named_alternative[[\xac Body](work-kind.md "?")-Task-Body]` | marked ? link entry with --pick Task bundles task body | `deferral/the-task-pick-bundles-the-kind-router`, `cli/a-link-entry-opening-with-the-deferral-mark-ignores-it` | held |  | approved |
| `test_a_first_run_pick_bundles_the_named_alternative[click Body "work-kind.md" "?"-Task-Body]` | click entry with ? and --pick Task bundles task body | `deferral/the-task-pick-bundles-the-kind-router` | partly held | click line entry carrying the pick token |  |
| `test_a_first_run_pick_bundles_the_named_alternative[link Body "work-kind.md" "? , checks"-Task-Body]` | link-line entry with ? beside checks and --pick Task bundles task body | `deferral/the-task-pick-bundles-the-kind-router` | partly held | class-diagram link line entry; pick token beside a preset tag |  |
| `test_a_pick_naming_no_alternative_is_refused_with_a_rerun_remedy[bogus]` | --pick bogus: E_ALTERNATIVE_UNRESOLVED listing, rerun remedy; then --pick epic succeeds | `deferral/the-pick-token-command-lists-the-kind-routers-alternatives`, `deferral/the-epic-pick-bundles-the-kind-router` | partly held | a --pick naming no alternative; remedy text; exact message |  |
| `test_a_pick_naming_no_alternative_is_refused_with_a_rerun_remedy[checks]` | --pick of an ordinary preset: E_ALTERNATIVE_UNRESOLVED, rerun remedy; then --pick epic succeeds | `deferral/the-pick-token-command-lists-the-kind-routers-alternatives`, `deferral/the-epic-pick-bundles-the-kind-router` | partly held | a --pick naming an ordinary preset; remedy text; exact message |  |
| `test_a_pick_after_the_listing_bundles_the_named_alternative` | ? entry without pick lists alternatives with rerun remedy; rerun --pick epic bundles epic body | `deferral/the-pick-token-command-lists-the-kind-routers-alternatives`, `deferral/the-epic-pick-bundles-the-kind-router` | partly held | remedy text; exact message |  |
| `test_two_alternatives_in_force_are_refused_before_their_pairs_compare` | two sections picking epic and task: E_ALTERNATIVE_UNRESOLVED listing, source work-kind.md, nothing published | `inclusion/two-links-picking-different-alternatives-fail` | held |  | approved |
| `test_a_pick_without_a_title_beside_it_is_one_in_force` | untitled link beside an epic-picking link adds no pick; epic body bundled | none | not held |  |  |
| `test_a_dispatched_bundle_counts_the_references_within_it` | inclusion picking epic and dispatch picking task each count alone; two bundles; Checks warns unused | `dispatch-brief/two-briefs-picking-different-alternatives-publish` | partly held | an inclusion beside a dispatch picking another alternative; the W_PRESET_UNUSED for Checks |  |

### Entry forms

11 tests: 7 held, 2 partly held, 2 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\xac Plan](guide.md#plan "checks")]` | deferral mark on link entry ignored; section bundled under Reviews as plain entry | `cli/a-link-entry-opening-with-the-deferral-mark-ignores-it`, `inclusion/an-entry-name-reads-its-documents-presets` | held |  | approved |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\u21b3 Plan](guide.md#plan "checks")]` | composition mark on link entry ignored; section bundled under Reviews as plain entry | `cli/a-link-entry-opening-with-the-composition-mark-ignores-it`, `inclusion/an-entry-name-reads-its-documents-presets` | held |  | approved |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\u21c9 Plan](guide.md#plan "checks")]` | dispatch mark on link entry ignored; section bundled under Reviews as plain entry | `cli/a-link-entry-opening-with-the-dispatch-mark-ignores-it`, `inclusion/an-entry-name-reads-its-documents-presets` | held |  | approved |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\u2afd Plan](guide.md#plan "checks")]` | parallel dispatch mark on link entry ignored; section bundled under Reviews as plain entry | `cli/a-link-entry-opening-with-the-parallel-dispatch-mark-ignores-it`, `inclusion/an-entry-name-reads-its-documents-presets` | held |  | approved |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\xac\u21b3\u21c9\u2afd Plan](guide.md#plan "checks")]` | combined marks on link entry ignored; bundle equals plain entry | `cli/a-link-entry-opening-with-a-malformed-mark-combination-ignores-it`, `inclusion/an-entry-name-reads-its-documents-presets` | held |  | approved |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[[\u21c9\xac Plan](guide.md#plan "Checks, unknown")]` | reversed marks ignored; title Checks beside unknown tag selects Checks; bundle equals plain entry | `cli/a-link-entry-opening-with-a-malformed-mark-combination-ignores-it`, `composition/activated-title-selection-under-unrelated-headings`, `cli/unknown-preset-names-select-default` | partly held | this mark order on an entry together with an unknown tag beside a known preset |  |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[click Plan "guide.md#plan" "checks"]` | click line entry selects Checks by tooltip; bundle equals Markdown entry | `cli/a-click-line-entry-selects-presets-by-its-tooltip` | held |  | refused |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[click Plan href "guide.md#plan" "checks" _blank]` | click href form with target entry selects Checks; bundle equals Markdown entry | `cli/a-click-line-entry-selects-presets-by-its-tooltip` | partly held | click entry written with href and a link target |  |
| `test_a_link_entry_bundles_its_destination_whatever_marks_open_it[link Plan "guide.md#plan" "checks"]` | class-diagram link line entry selects Checks; bundle equals Markdown entry | `cli/a-class-diagram-link-line-entry-selects-presets-by-its-tooltip` | held |  | approved |
| `test_an_indented_link_entry_bundles_as_its_link[    ]` | space-indented link entry bundles as the unindented link | none | not held |  |  |
| `test_an_indented_link_entry_bundles_as_its_link[\t]` | tab-indented link entry bundles as the unindented link | none | not held |  |  |

### Deferral

41 tests: 18 held, 17 partly held, 6 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[\u21c9 fast-True]` | deferral title tag opening with marks refused: exit 1, E_UNSUPPORTED_CONSTRUCT, source, reference | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused` | partly held | Markdown deferral link title; a tag of marks followed by text |  |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[checks, \xac-True]` | deferral title tag of marks beside checks refused: exit 1, E_UNSUPPORTED_CONSTRUCT | `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | Markdown deferral link title (fixture is a click tooltip); deferral mark as the tag |  |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[checks,\n\u21c9 fast-True]` | deferral title with newline then marks tag refused: E_UNSUPPORTED_CONSTRUCT | `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | Markdown deferral link title; tag after a newline; marks followed by text |  |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[\xa0\u21c9 fast-True]` | deferral title tag led by no-break space then marks refused | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused` | partly held | Markdown deferral link title; no-break space before marks; marks followed by text |  |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[with \u21b3 Given-False]` | deferral title with a mark mid-tag publishes successfully | none | not held |  |  |
| `test_a_local_link_title_tag_stating_operator_marks_is_refused[\u21c9Fast-False]` | deferral title with mark against text publishes successfully | none | not held |  |  |
| `test_a_deferral_publishes_its_pick_token_as_authored[\xac the body-work-kind.md-?]` | deferral to work-kind.md titled ? publishes the link with title as authored | `deferral/a-deferral-carries-the-pick-token` | held |  | approved |
| `test_a_deferral_publishes_its_pick_token_as_authored[\xac the body-work-kind.md-checks, ?]` | deferral titled checks, ? publishes title as authored | `deferral/a-deferral-carries-the-pick-token`, `deferral/a-deferred-directive-carries-the-pick-token-beside-a-fixed-tag` | partly held | pick token beside a fixed tag on a plain deferral (fixture has it on a deferred directive) |  |
| `test_a_deferral_publishes_its_pick_token_as_authored[\xac\u21b3 the body-work-kind.md#populate-?]` | deferred directive titled ? publishes title as authored | `deferral/a-deferred-directive-carries-the-pick-token-beside-a-fixed-tag`, `deferral/a-mode-publishes-its-kind-router-link-with-the-pick-token` | partly held | deferred directive carrying ? alone |  |
| `test_a_deferral_publishes_its_pick_token_as_authored[\xac\u21b3 the body-work-kind.md#populate-checks, ?]` | deferred directive titled checks, ? publishes title as authored | `deferral/a-deferred-directive-carries-the-pick-token-beside-a-fixed-tag` | held |  | approved |
| `test_a_bundled_link_carrying_the_pick_token_is_refused[the body]` | ordinary link with ? refused: exit 1, E_UNSUPPORTED_CONSTRUCT, reference link text, pick token message | `deferral/an-ordinary-link-carrying-the-pick-token-is-refused` | held |  | approved |
| `test_a_bundled_link_carrying_the_pick_token_is_refused[\u21b3 the body]` | composition directive with ? refused: exit 1, E_UNSUPPORTED_CONSTRUCT, reference link text | `deferral/a-directive-carrying-the-pick-token-is-refused` | held |  | approved |
| `test_a_bundled_link_carrying_the_pick_token_is_refused[\u2afd the body]` | parallel dispatch with ? refused: exit 1, E_UNSUPPORTED_CONSTRUCT, reference link text | `dispatch/a-parallel-dispatch-carrying-the-pick-token-is-refused` | held |  | approved |
| `test_a_link_to_a_silent_document_keeps_the_pick_token_as_text` | link titled ? to a document declaring nothing publishes with title kept | none | not held |  |  |
| `test_a_deferral_stating_no_one_pick_is_refused[-names no alternative]` | untitled deferral to work-kind.md refused: exact message names no alternative, reference, resolved | `deferral/a-deferral-naming-no-alternative-to-a-section-writing-a-routed-link-is-refused` | partly held | untitled deferral to a whole document; exact message wording |  |
| `test_a_deferral_stating_no_one_pick_is_refused[ "checks"-names no alternative]` | deferral titled checks refused: exact message names no alternative, reference, resolved | `deferral/a-deferral-naming-no-alternative-to-a-section-writing-a-routed-link-is-refused` | partly held | whole-document target; exact message wording |  |
| `test_a_deferral_stating_no_one_pick_is_refused[ "epic, task"-names 'Epic', 'Task']` | deferral naming two alternatives refused: exact message, reference, resolved | `deferral/a-deferral-naming-two-alternatives-is-refused` | partly held | exact message wording |  |
| `test_a_deferral_stating_no_one_pick_is_refused[ "epic, ?"-names 'Epic' beside the pick token '?']` | deferral naming epic beside ? refused: exact message, reference, resolved | `deferral/a-deferral-naming-an-alternative-beside-the-pick-token-is-refused` | partly held | exact message wording |  |
| `test_a_deferral_naming_no_alternative_to_unrouted_content_publishes[\xac the fields-]` | untitled deferral to section with no routed link publishes as authored | `deferral/a-deferral-naming-no-alternative-to-a-section-no-alternative-routes-publishes` | held |  | approved |
| `test_a_deferral_naming_no_alternative_to_unrouted_content_publishes[\xac the fields- "checks"]` | deferral titled checks to unrouted section publishes as authored | `deferral/a-deferral-naming-no-alternative-to-a-section-no-alternative-routes-publishes` | partly held | an ordinary preset title on the deferral |  |
| `test_a_deferral_naming_no_alternative_to_unrouted_content_publishes[\xac\u21b3 the fields-]` | untitled deferred directive to unrouted section publishes as authored | `deferral/a-deferred-directive-naming-no-alternative-to-a-section-no-alternative-routes-publishes` | held |  | approved |
| `test_a_deferral_naming_no_alternative_to_unrouted_content_publishes[\xac\u21b3 the fields- "checks"]` | deferred directive titled checks to unrouted section publishes as authored | `deferral/a-deferred-directive-naming-no-alternative-to-a-section-no-alternative-routes-publishes` | partly held | an ordinary preset title on the deferred directive |  |
| `test_an_entry_title_naming_the_targets_alternative_is_no_deferrals_pick` | entry titled epic does not pick for an untitled deferral; refused names no alternative | none | not held |  |  |
| `test_a_deferral_whose_later_run_fails_otherwise_needs_no_pick` | untitled deferral to a section that fails anyway publishes as authored | none | not held |  |  |
| `test_a_deferral_whose_later_run_fails_for_want_of_a_pick_is_refused` | untitled deferral whose unrouted body fails is refused: names no alternative | `deferral/a-deferral-naming-no-alternative-to-a-section-writing-a-routed-link-is-refused` | partly held | untitled whole-document deferral whose unrouted target fails |  |
| `test_a_pick_token_on_a_deferral_to_no_alternatives_is_refused` | deferral with ? to document without alternatives refused: exit 1, exact message | `deferral/a-pick-token-deferral-to-a-document-without-alternatives-is-refused` | partly held | exact message wording |  |
| `test_a_deferral_naming_one_pick_or_needing_none_publishes[work-kind.md- "Task, checks"]` | deferral naming one alternative beside checks publishes as authored | `deferral/a-deferral-naming-one-alternative-publishes` | held |  | approved |
| `test_a_deferral_naming_one_pick_or_needing_none_publishes[body.md-]` | untitled deferral to document without alternatives publishes as authored | `deferral/a-marked-reference-is-not-bundled` | held |  | approved |
| `test_a_deferral_naming_one_pick_or_needing_none_publishes[body.md- "checks"]` | titled deferral to document without alternatives publishes title as authored | `deferral/a-reference-title-survives-rebased-publication`, `deferral/a-marked-reference-is-not-bundled` | held |  | approved |
| `test_a_marked_reference_under_the_root_is_not_bundled` | deferred link's target is not bundled | `deferral/a-marked-reference-is-not-bundled` | held |  | approved |
| `test_a_deferred_link_publishes_its_text_without_the_mark` | deferred link published without its mark, pointing from the bundle folder | `deferral/a-marked-reference-is-not-bundled` | held |  | approved |
| `test_the_blanks_after_the_mark_go_with_it[[\xac  the rules](rules.md)]` | two blanks after the deferral mark are removed with it | `deferral/a-marked-reference-is-not-bundled` | partly held | more than one blank after the mark; fixture writes one space |  |
| `test_the_blanks_after_the_mark_go_with_it[[\xac \tthe rules](rules.md)]` | a space and tab after the deferral mark are removed with it | `deferral/a-marked-reference-is-not-bundled` | partly held | a tab among the blanks after the mark; fixture writes one space |  |
| `test_a_mark_with_no_space_after_it_opens_an_ordinary_link[\xac]` | deferral mark with no space is an ordinary bundled link, no diagnostic | `deferral/a-deferral-mark-with-no-space-after-it-opens-an-ordinary-link` | held |  | approved |
| `test_a_deferral_stands_where_another_reference_carried_its_target` | deferral keeps its path though another link bundles the target | `deferral/a-deferral-stands-where-another-reference-carried-its-target` | held |  | approved |
| `test_a_deferred_fragment_of_its_own_document_is_not_bundled` | A deferred fragment-only link publishes the path from the bundle folder; the section is not bundled | `deferral/a-deferred-fragment-of-its-own-document` | held |  | approved |
| `test_a_deferred_reference_naming_no_document_fails` | A deferral naming no document fails E_TARGET_NOT_FOUND with names no document message, no bundle | `deferral/a-deferred-reference-naming-no-document` | partly held | message wording (names no document) |  |
| `test_a_deferred_reference_naming_no_heading_fails` | A deferral naming no heading fails E_TARGET_NOT_FOUND with reference, resolved and chain, no bundle | `deferral/a-deferred-reference-naming-no-heading` | held |  | approved |
| `test_a_deferred_destination_is_the_target_path_from_the_bundle_folder` | A deferred link's destination is the target path from the bundle folder | `deferral/a-deferred-destination-named-from-the-bundle-folder` | held |  | approved |
| `test_a_document_only_a_deferral_names_contributes_nothing` | A document only a deferral names contributes no heading and no content | `deferral/a-marked-reference-is-not-bundled`, `deferral/a-deferred-destination-named-from-the-bundle-folder` | held |  | approved |
| `test_a_heading_a_container_carries_confirms_a_deferral` | A deferral to a container-nested heading succeeds, publishing the rebased path | none | not held |  |  |

### Dispatch

62 tests: 35 held, 20 partly held, 7 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_dispatch_carrying_the_pick_token_lists_a_bundle_for_each_alternative[?]` | dispatch titled ? writes one bundle per alternative and a pick listing | `dispatch/a-dispatch-carrying-the-pick-token-lists-a-bundle-for-each-alternative` | held |  | approved |
| `test_a_dispatch_carrying_the_pick_token_lists_a_bundle_for_each_alternative[checks, ?]` | dispatch titled checks, ? writes per-alternative bundles selecting Checks | `dispatch/a-dispatch-carrying-the-pick-token-beside-a-preset-selects-it-in-each-bundle` | held |  | approved |
| `test_a_dispatch_carrying_the_pick_token_lists_a_bundle_for_each_alternative[Checks,?]` | dispatch titled Checks,? writes per-alternative bundles selecting Checks | `dispatch/a-dispatch-carrying-the-pick-token-beside-a-preset-selects-it-in-each-bundle` | partly held | capitalised, unspaced title spelling |  |
| `test_a_dispatch_naming_an_alternative_beside_the_pick_token_is_refused` | dispatch naming epic beside ? refused: exit 1, E_UNSUPPORTED_CONSTRUCT, exact message | `deferral/a-deferral-naming-an-alternative-beside-the-pick-token-is-refused` | partly held | dispatch link (fixture is a deferral); exact message wording |  |
| `test_a_dispatch_carrying_the_pick_token_to_no_alternatives_is_refused` | dispatch with ? to document without alternatives refused: exact message | `deferral/a-pick-token-deferral-to-a-document-without-alternatives-is-refused` | partly held | dispatch link (fixture is a deferral); exact message wording |  |
| `test_a_mark_with_no_space_after_it_opens_an_ordinary_link[\u21c9]` | dispatch mark with no space is an ordinary bundled link, no diagnostic | `dispatch/a-dispatch-mark-with-no-space-after-it-opens-an-ordinary-link` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a deferred dispatch]` | deferral then dispatch mark refused E_UNSUPPORTED_CONSTRUCT, nothing published | `dispatch/a-deferred-dispatch-is-refused` | held |  | refused |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a deferred parallel dispatch]` | deferral then parallel mark refused, nothing published | `parallel-dispatch/a-deferred-parallel-dispatch-is-refused` | held |  | approved |
| `test_a_dispatched_reference_under_the_root_is_not_bundled` | dispatched target contributes nothing to the entry bundle | `dispatch/a-dispatched-target-is-a-bundle-of-its-own` | held |  | approved |
| `test_a_dispatched_link_stays_inline_pointing_at_its_bundle_file` | dispatch link stays inline with its mark pointing at the target's bundle file | `dispatch/a-dispatched-target-is-a-bundle-of-its-own` | held |  | approved |
| `test_a_run_publishes_a_bundle_for_each_target_its_dispatches_reach` | nested dispatches each publish a bundle, section target named plan__steps | `dispatch/a-chain-of-two-dispatches`, `dispatch/a-dispatched-bundle-named-from-the-working-directory`, `dispatch/a-dispatched-section-of-the-entry-is-a-hop` | held |  | approved |
| `test_one_target_dispatched_from_two_sections_is_one_bundle` | one target dispatched from two sections is one bundle all links name | `dispatch/each-section-keeps-its-own-dispatch-link-inline` | held |  | approved |
| `test_an_in_parallel_sub_section_precedes_the_child_sections_of_its_section` | dispatch-set sub-section sits after section content, before child sections | `parallel-dispatch/sets-in-sibling-and-nested-sections`, `parallel-dispatch/a-section-carrying-both-operators` | held |  | approved |
| `test_a_set_above_the_first_heading_takes_its_level` | set in the preamble above the first heading takes a level-2 sub-section | `parallel-dispatch/sets-in-sibling-and-nested-sections` | partly held | set written above the first heading |  |
| `test_a_dispatch_in_a_linked_document_sits_under_its_shifted_section` | dispatch in an untitled linked document publishes inline under its file heading | none | not held |  |  |
| `test_a_dispatch_in_a_level_six_section_publishes_inline` | dispatch in a level-6 section publishes inline, no diagnostic | `dispatch/a-dispatch-in-a-level-six-section-publishes` | held |  | approved |
| `test_a_picking_dispatch_of_its_own_document_warns_once` | picking dispatch of its own section warns W_DISPATCH_SELF exactly once | `dispatch/a-dispatch-of-a-section-of-its-own-document-by-fragment-warns` | partly held | picking dispatch (pick token) warning once across alternative bundles |  |
| `test_a_picking_dispatch_in_a_level_six_section_is_refused` | picking dispatch in a level-6 section fails E_HEADING_DEPTH_OVERFLOW | none | not held |  |  |
| `test_an_authored_heading_equal_to_the_dispatch_pick_is_refused` | authored heading equal to the dispatch-pick sub-section fails E_HEADING_COLLISION | none | not held |  |  |
| `test_an_authored_heading_equal_to_the_dispatch_set_is_refused` | authored Dispatch Set heading fails E_HEADING_COLLISION naming it, with location | `parallel-dispatch/a-dispatch-set-heading-is-refused-beside-a-set` | partly held | diagnostic location line 8 column 1 |  |
| `test_a_heading_pf_does_not_emit_in_the_bundle_publishes[-Prosiform]` | authored Prosiform heading publishes with nothing dispatched, no diagnostic | `dispatch/a-prosiform-heading-publishes-where-nothing-is-dispatched` | held |  | approved |
| `test_a_heading_pf_does_not_emit_in_the_bundle_publishes[-In parallel]` | authored In parallel heading publishes with nothing dispatched | `parallel-dispatch/an-in-parallel-heading-publishes-beside-a-set` | partly held | In parallel heading in a bundle dispatching nothing |  |
| `test_a_heading_pf_does_not_emit_in_the_bundle_publishes[Run [\u21c9 plan](plan.md).-In parallel]` | In parallel heading publishes beside a dispatch | `dispatch/a-parallel-heading-publishes-beside-a-dispatch-only` | held |  | approved |
| `test_a_heading_pf_does_not_emit_in_the_bundle_publishes[Run [\u21c9 plan](plan.md).-Prosiform]` | Prosiform heading publishes in a dispatching bundle | `dispatch/a-prosiform-heading-publishes-in-a-dispatching-bundle` | held |  | approved |
| `test_a_heading_pf_does_not_emit_in_the_bundle_publishes[Run [\u21c9 plan](plan.md).-Dispatch plan]` | Dispatch plan heading publishes beside a dispatch | `dispatch/a-dispatch-heading-publishes-beside-a-dispatch` | held |  | approved |
| `test_an_empty_dispatch_reached_through_a_link_names_the_route` | empty dispatch in a linked document refused, naming reference, source and route | `dispatch/a-dispatch-link-with-no-text-is-refused` | partly held | reached through a linked document (chain via steps.md) |  |
| `test_a_link_opening_with_two_dispatch_marks_is_refused` | link opening with both dispatch marks refused, naming the link | `dispatch/a-link-carrying-two-dispatch-marks` | held |  | approved |
| `test_a_dispatch_in_an_absorbed_title_is_refused[\u21c9]` | dispatch in a linked document's absorbed title refused with route and remedy | `dispatch/a-dispatch-in-an-absorbed-member-title-is-refused`, `composition/a-directive-in-an-absorbed-title-has-no-scope` | partly held | dispatch in a whole linked document's absorbed title; remedy present |  |
| `test_a_dispatch_in_an_absorbed_title_is_refused[\u2afd]` | parallel link in a linked document's absorbed title refused with route and remedy | `dispatch/a-dispatch-in-an-absorbed-member-title-is-refused`, `composition/a-directive-in-an-absorbed-title-has-no-scope` | partly held | parallel mark in a whole linked document's absorbed title; remedy present |  |
| `test_a_dispatch_in_an_absorbed_member_title_is_refused` | dispatch in a merged member's absorbed title refused at the member line | `dispatch/a-dispatch-in-an-absorbed-member-title-is-refused` | held |  | approved |
| `test_a_dispatch_in_a_title_above_the_selection_is_refused` | dispatch in a title above the selected section refused with source and chain | `dispatch/a-dispatch-in-a-title-above-the-selection-is-refused` | held |  | approved |
| `test_a_dispatch_in_the_entry_s_own_title_still_publishes` | dispatch in the entry's title publishes in the heading and its bundle | `parallel-dispatch/a-parallel-link-in-a-heading-of-a-set-of-one-publishes-as-a-dispatch` | partly held | dispatch in the entry's own title and the opening line naming it |  |
| `test_a_link_opening_with_two_dispatch_marks_is_refused_where_it_names_nothing` | two dispatch marks refused even on a link naming a non-document file | `dispatch/a-link-carrying-two-dispatch-marks` | partly held | link naming a non-Markdown resource |  |
| `test_a_chain_of_three_dispatches_raises_no_warning` | A chain of three dispatches succeeds with no diagnostic | `dispatch/a-chain-of-three-dispatches` | held |  | approved |
| `test_a_fourth_dispatch_warns_naming_the_chain` | A fourth dispatch warns W_DISPATCH_DEPTH naming chain, location and related hops; five bundles | `dispatch/a-fourth-dispatch-warns` | partly held | location and related fields |  |
| `test_a_dispatched_section_of_the_entry_is_a_hop` | Dispatching an entry section warns W_DISPATCH_SELF then W_DISPATCH_DEPTH with the chain through it | `dispatch/a-dispatched-section-of-the-entry-is-a-hop` | held |  | approved |
| `test_a_deferred_link_in_a_dispatched_closure_is_no_hop` | A deferral at the end of a three-dispatch chain counts as no hop and raises nothing | none | not held |  |  |
| `test_a_dispatch_a_bundled_dependency_carries_is_a_hop` | A dispatch carried by a bundled dependency counts as a hop and warns W_DISPATCH_DEPTH | none | not held |  |  |
| `test_two_links_dispatching_one_deep_target_warn_once` | Two links dispatching one deep target warn W_DISPATCH_DEPTH once | `dispatch/a-fourth-dispatch-warns` | partly held | two links dispatching the same target producing one warning |  |
| `test_a_cycle_of_dispatches_is_refused_naming_the_chain` | A dispatch cycle fails E_DISPATCH_CYCLE naming the chain, no bundles | `dispatch/a-cycle-of-dispatches-is-refused` | held |  | approved |
| `test_a_dispatch_of_the_entry_is_a_cycle` | A dispatch back to the entry fails E_DISPATCH_CYCLE with chain ending at the entry | `dispatch/a-cycle-of-dispatches-is-refused` | partly held | a cycle returning to the entry document itself |  |
| `test_a_section_dispatching_its_own_document_is_a_cycle` | A selected section dispatching its whole document fails E_DISPATCH_CYCLE with its chain | `dispatch/a-dispatch-of-its-own-whole-document-is-a-cycle` | held |  | approved |
| `test_a_section_dispatched_from_its_own_document_warns_once` | Dispatching an own section by path warns W_DISPATCH_SELF once with location; section bundle bytes | `dispatch/a-dispatch-of-a-section-of-its-own-document-by-path-warns` | partly held | location field |  |
| `test_a_fragment_only_dispatch_names_its_own_document` | A fragment-only dispatch warns W_DISPATCH_SELF only | `dispatch/a-dispatch-of-a-section-of-its-own-document-by-fragment-warns` | held |  | approved |
| `test_a_dispatched_bundle_carrying_a_deferral_opens_with_the_run_pf_line` | A dispatched bundle carrying a deferral opens with the run-pf line, as the entry does | `dispatch/a-plain-deferral-in-a-dispatched-bundle-opens-with-the-run-pf-line` | held |  | approved |
| `test_a_dispatched_target_whose_bundling_fails_publishes_nothing` | Missing target inside a dispatched target fails with E_TARGET_NOT_FOUND and publishes nothing | `dispatch/a-deferred-dispatch-in-a-dispatched-bundle-is-refused`, `dispatch/a-dispatched-target-crossing-the-file-budget` | partly held | E_TARGET_NOT_FOUND raised inside a dispatched target's closure |  |
| `test_a_link_opening_with_a_guillemet_is_bundled` | A link whose text opens with a guillemet is an ordinary link and bundled | none | not held |  |  |
| `test_a_dispatched_section_carrying_steps_raises_nothing` | Dispatched section carrying steps publishes with no diagnostic | `dispatch/a-dispatched-section-carrying-steps` | held |  | approved |
| `test_a_dispatched_section_of_fields_raises_nothing` | Dispatched section of fields publishes with no diagnostic, link rewritten to its bundle file | `dispatch/a-dispatched-section-of-fields` | held |  | approved |
| `test_a_sections_parallel_links_point_at_one_sub_section_listing_each_bundle` | Section's parallel links point at one dispatch-set sub-section listing each bundle; exact bundle bytes | `parallel-dispatch/a-set-in-one-section`, `parallel-dispatch/sets-in-sibling-and-nested-sections` | held |  | approved |
| `test_a_target_named_twice_in_one_set_is_listed_once` | Target named twice in one set listed once in the dispatch-set sub-section | `parallel-dispatch/a-target-named-twice-in-one-set-is-listed-once` | held |  | approved |
| `test_a_child_sections_parallel_links_form_its_own_set` | Child section's parallel links form their own set with an ordinal-suffixed sub-section | `parallel-dispatch/sets-in-sibling-and-nested-sections` | held |  | approved |
| `test_a_section_carrying_both_operators_keeps_its_dispatches_inline` | Section with both operators keeps dispatch inline, set in sub-section; one target both dispatched and in set | `parallel-dispatch/a-section-carrying-both-operators` | partly held | one target named by both an inline dispatch and a parallel link in the same section |  |
| `test_a_parallel_target_of_any_shape_publishes_with_no_diagnostic[Some prose.\n]` | Parallel target of any shape publishes with no diagnostic as an inline dispatch bundle (prose target) | `parallel-dispatch/a-target-holding-a-paragraph-publishes` | held |  | approved |
| `test_a_parallel_target_of_any_shape_publishes_with_no_diagnostic[1. First.\n2. Second.\n]` | Parallel target of any shape publishes with no diagnostic as an inline dispatch bundle (numbered list target) | `parallel-dispatch/a-target-holding-a-numbered-list-publishes` | held |  | approved |
| `test_a_parallel_target_of_any_shape_publishes_with_no_diagnostic[- An item linking no document.\n]` | Parallel target of any shape publishes with no diagnostic as an inline dispatch bundle (bullet linking no document) | `parallel-dispatch/a-target-holding-an-item-linking-no-document-publishes` | held |  | approved |
| `test_a_parallel_target_of_any_shape_publishes_with_no_diagnostic[- [A](a.md)\n  - [B](https://example.test/b.md)\n]` | Parallel target of any shape publishes with no diagnostic as an inline dispatch bundle (nested list linking a remote address) | `parallel-dispatch/a-target-holding-a-paragraph-publishes`, `parallel-dispatch/a-target-holding-an-item-linking-no-document-publishes` | partly held | a target holding a nested list whose item links a remote address |  |
| `test_a_parallel_mark_with_the_dispatch_mark_is_refused[\u2afd\u21c9 the reviews]` | Link opening with parallel then dispatch mark refused, reference and two-ways message | `parallel-dispatch/a-link-carrying-the-parallel-mark-and-the-dispatch-operator` | held |  | approved |
| `test_a_parallel_mark_with_the_dispatch_mark_is_refused[\u21c9\u2afd the reviews]` | Link opening with dispatch then parallel mark refused, reference and two-ways message | `dispatch/a-link-carrying-two-dispatch-marks` | held |  | approved |
| `test_a_parallel_mark_with_no_space_after_it_opens_an_ordinary_link` | Parallel mark with no space after it opens an ordinary link, bundled, no diagnostic | `parallel-dispatch/a-parallel-mark-with-no-space-after-it-opens-an-ordinary-link` | held |  | approved |
| `test_a_parallel_dispatch_is_a_hop_of_a_chain` | Parallel dispatch counts as a chain hop: W_DISPATCH_DEPTH with chain and location | none | not held |  |  |
| `test_a_parallel_dispatch_closing_a_cycle_is_refused` | Parallel dispatches closing a cycle refused E_DISPATCH_CYCLE, nothing published | `dispatch-brief/a-cycle-of-briefs-in-a-deep-set-is-refused-as-a-cycle` | partly held | a cycle closed by plain parallel links (fixture's cycle runs through briefs) |  |

### Faults

11 tests: 2 held, 7 partly held, 2 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_refused_swap_restores_the_earlier_folder` | refused rename of the new set restores the earlier folder, E_PUBLICATION_FAILED | none | not held |  |  |
| `test_a_refused_swap_that_cannot_restore_names_where_the_earlier_set_is` | refused restore names the .pf.old aside path in message and remedy | none | not held |  |  |
| `test_an_earlier_set_that_cannot_be_removed_warns_on_a_published_run` | unremovable earlier set warns W_EARLIER_SET_RETAINED naming the aside path; new set published | `publication/an-earlier-set-the-run-cannot-remove-warns` | partly held | warning naming the aside path; aside contents kept |  |
| `test_a_candidate_disagreeing_with_its_provenance_publishes_nothing` | A candidate dropping content fails as internal error naming no accidental omissions, no bundle | `diagnostics/a-run-that-fails-in-itself` | partly held | the provenance mismatch trigger and message wording |  |
| `test_an_error_the_contract_does_not_name_is_an_internal_error_as_data` | An unnamed exception yields internal-error status and one error E_UNEXPECTED_INTERNAL_ERROR, no bundle | `diagnostics/a-run-that-fails-in-itself` | held |  | approved |
| `test_an_error_the_contract_does_not_name_is_an_internal_error_as_text` | An unnamed exception in text format writes one exact human diagnostic line | `diagnostics/a-run-that-fails-in-itself` | partly held | the human text diagnostic line |  |
| `test_the_source_changed_fault_fails_the_run_and_publishes_nothing` | The source-changed fault fails E_SOURCE_CHANGED, publishes nothing and rewrites the source | `source-consistency/a-source-that-changes-during-bundling` | partly held | the source bytes rewritten in the tree |  |
| `test_the_internal_fault_names_the_run_and_publishes_nothing` | The internal fault fails with internal-error status and E_UNEXPECTED_INTERNAL_ERROR, no bundle | `diagnostics/a-run-that-fails-in-itself` | held |  | approved |
| `test_a_run_asking_for_no_fault_meets_none` | A run asking for no fault succeeds silently and leaves the source unchanged | `cli/a-bundle-written-into-the-working-directory` | partly held | the source bytes left unchanged |  |
| `test_a_fault_the_contract_does_not_declare_is_a_usage_failure[other]` | An unknown fault value is invalid usage naming the value and three faults, source unchanged | `cli/an-unknown-fault-is-invalid-usage` | partly held | the source bytes left unchanged |  |
| `test_a_fault_the_contract_does_not_declare_is_a_usage_failure[]` | An empty fault value is invalid usage naming the value and three faults, source unchanged | `cli/an-unknown-fault-is-invalid-usage` | partly held | an empty fault value; the source bytes left unchanged |  |

### Resources

5 tests: 5 held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_image_naming_a_markdown_document_carries_no_document` | image naming a Markdown document emitted as authored, document not bundled | `resource/an-image-naming-a-local-document` | held |  | approved |
| `test_an_image_naming_a_markdown_document_warns_once_on_portability` | image naming a Markdown document warns W_RESOURCE_PORTABILITY once | `resource/an-image-naming-a-local-document` | held |  | approved |
| `test_a_bundle_naming_no_resource_does_not_warn_on_portability` | scheme link raises no portability warning | `resource/a-bundle-naming-no-resource-does-not-warn` | held |  | approved |
| `test_an_unmarked_image_is_emitted_as_authored` | relative image emitted as authored | `traversal/a-relative-resource-warns` | held |  | approved |
| `test_an_unmarked_resource_is_emitted_as_authored` | scheme link emitted as authored | `normalization/a-scheme-and-an-authority-in-selected-content`, `traversal/resources-are-not-dependencies` | held |  | approved |

### References

7 tests: 7 held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_reference_under_the_root_is_bundled_and_rewritten` | declaring target bundled and link rewritten to its heading | `inclusion/a-declaring-target-is-bundled` | held |  | approved |
| `test_a_reference_to_a_section_under_the_root_carries_that_section` | section link carries that section only and is rewritten | `traversal/a-declaring-reference-is-bundled` | held |  | approved |
| `test_a_reference_outside_the_root_is_emitted_as_authored` | link above the working directory emitted as authored, target not read | `normalization/a-reference-above-the-working-directory-is-text`, `citation/a-reference-above-the-working-directory` | held |  | approved |
| `test_a_root_relative_reference_inside_a_source_is_emitted_as_authored` | root-relative link inside a source emitted as authored, not bundled | `confinement/a-root-relative-reference-inside-a-source` | held |  | approved |
| `test_a_drive_path_inside_a_source_is_emitted_as_authored` | drive-path link inside a source emitted as authored, not bundled | `confinement/a-drive-path-inside-a-source` | held |  | approved |
| `test_a_link_naming_no_document_is_text` | links to a missing and an undeclaring document are text, no diagnostic | `inclusion/a-link-naming-no-document-is-text`, `traversal/a-declaring-reference-is-bundled` | held |  | approved |
| `test_a_reference_under_the_root_naming_no_heading_publishes_nothing` | link naming a missing heading fails E_TARGET_NOT_FOUND with resolved document | `reference/a-reference-naming-no-heading-of-a-declaring-document` | held |  | approved |

### Composition

11 tests: 6 held, 4 partly held, 1 not held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_deferred_composition_is_written_with_its_marks_together` | deferred directive keeps its generated line, target not composed, no diagnostic | `composition/a-deferral-whose-step-and-target-select-no-preset-is-kept` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a dispatch written against the composition mark]` | dispatch mark against composition mark refused, nothing published | `composition/a-dispatch-mark-written-against-the-composition-mark-is-refused` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a parallel dispatch written against the composition mark]` | parallel mark against composition mark refused, nothing published | `composition/a-parallel-mark-written-against-the-composition-mark-is-refused` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[an arrow label]` | arrow label refused E_UNSUPPORTED_CONSTRUCT mentioning arrow | `composition/an-arrow-label-is-refused` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a deferred arrow label]` | deferred arrow label refused mentioning arrow | `composition/a-deferred-arrow-label-is-refused` | held |  | approved |
| `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing[a blank between the deferral and composition marks]` | blank between deferral and composition marks refused as not written together | `composition/a-blank-between-the-deferral-mark-and-the-composition-mark-is-refused` | held |  | approved |
| `test_an_arrow_label_names_the_link_and_points_at_the_composition_mark` | arrow-label refusal names reference and source, remedy points at the composition mark | `composition/an-arrow-label-is-refused` | partly held | remedy naming the composition mark |  |
| `test_a_directive_composing_a_section_of_its_own_document_warns` | A directive composing an own section by fragment warns W_COMPOSE_SELF with reference, resolved, location | `composition/a-directive-composing-a-section-of-its-own-document-by-fragment-warns` | partly held | location field |  |
| `test_a_deferred_directive_composing_its_own_document_raises_no_warning` | A deferred directive naming an own section raises no warning | none | not held |  |  |
| `test_a_composing_click_in_the_preamble_is_refused_naming_it` | Composing click in the preamble refused naming the click as a preamble directive | `composition/a-directive-in-a-preamble-has-no-scope` | partly held | the click form and preamble-directive message wording |  |
| `test_a_cycle_of_directives_names_each_earlier_directive_as_related` | Directive cycle refused at the closing directive's location, earlier directives listed as related | `composition/a-cycle-of-directives-is-refused` | partly held | the related entries naming each earlier directive |  |

### Self-reference

7 tests: 7 held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_link_to_the_section_carrying_it_resolves_to_that_section` | A link to its own section resolves to that section, emitted once | `self-reference/a-link-to-the-same-section` | held |  | approved |
| `test_identity_is_compared_after_the_path_and_the_fragment_resolve` | A self-link spelled with ./ and a percent escape resolves to the section | `self-reference/a-link-spelled-another-way-to-the-same-section` | held |  | approved |
| `test_a_preamble_link_to_its_own_document_resolves_to_that_document` | A preamble link to its own document resolves to the document heading | `self-reference/a-preamble-link-to-its-own-document` | held |  | approved |
| `test_a_section_link_to_its_whole_document_is_an_ancestor_inclusion` | A section linking its whole document succeeds as an ancestor inclusion | `self-reference/a-section-link-to-its-whole-document` | held |  | approved |
| `test_a_link_to_another_section_of_one_file_is_no_self_reference` | A link to another section of the same file succeeds | `self-reference/a-link-to-another-section-of-the-same-file` | held |  | approved |
| `test_classification_is_the_same_before_and_after_consolidation` | Child-selected and ancestor-selected runs produce the same bundle body | `ownership/an-ancestor-reference-with-the-child-selected`, `ownership/an-ancestor-reference-after-consolidation` | held |  | approved |
| `test_a_self_reference_resolves_the_same_after_consolidation` | A nested section's self-link resolves to its own heading when the whole document is selected | `ownership/a-self-reference-after-consolidation` | held |  | approved |

### Validation scope

7 tests: 3 held, 4 partly held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_unselected_broken_link_does_not_fail_the_run` | A deferral naming no document in an unselected section leaves the run successful | `inclusion/every-stage-reads-one-selection`, `validation-scope/an-unselected-broken-link` | held |  | approved |
| `test_an_unselected_self_link_does_not_fail_the_run` | A deferred self-link in an unselected section leaves the run successful | `inclusion/every-stage-reads-one-selection`, `deferral/a-deferred-fragment-of-its-own-document` | partly held | a deferred link to its own unselected section |  |
| `test_the_same_sibling_fails_once_the_closure_includes_it` | A sibling reached by closure fails on its deferral naming no document | `validation-scope/the-sibling-once-closure-includes-it`, `deferral/a-deferred-reference-naming-no-document` | partly held | a deferral naming no document as the reached sibling's defect |  |
| `test_a_profile_refusal_a_named_document_did_not_select_does_not_fail` | Raw HTML in an unselected section of the named document leaves the run successful | `validation-scope/an-unselected-refusal-in-a-named-document`, `inclusion/every-stage-reads-one-selection` | held |  | approved |
| `test_a_profile_refusal_a_reached_document_did_not_select_does_not_fail` | Raw HTML in an unselected section of a reached document leaves the run successful | `validation-scope/an-unselected-refusal-in-a-reached-document` | held |  | approved |
| `test_a_profile_refusal_the_run_selected_still_fails` | Raw HTML in the selected section fails E_RAW_HTML with chain of the section entry | `profile/raw-html-in-selected-content` | partly held | a section entry and its chain |  |
| `test_a_refusal_in_a_reached_document_the_closure_selected_fails` | Raw HTML in a reached document fails E_RAW_HTML naming its source line and chain | `profile/raw-html-in-selected-content` | partly held | raw HTML in a reached document, with source other.md:6 and chain |  |

### Source consistency

6 tests: 1 held, 5 partly held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_source_nothing_wrote_passes_the_recheck` | Unit recheck passes for an unchanged captured source | `cli/a-bundle-written-into-the-working-directory` | partly held | the recheck function called directly |  |
| `test_a_source_written_after_the_read_fails_the_recheck` | Unit recheck raises E_SOURCE_CHANGED input failure for rewritten bytes | `source-consistency/a-source-that-changes-during-bundling` | partly held | the recheck function's raised Failure and status checked directly |  |
| `test_a_source_removed_after_the_read_fails_the_recheck` | Unit recheck raises E_SOURCE_CHANGED for a removed source | `source-consistency/a-source-that-changes-during-bundling` | partly held | a removed source; the recheck function called directly |  |
| `test_a_source_resolving_elsewhere_fails_the_recheck` | Unit recheck raises E_SOURCE_CHANGED with identity changed for a swapped directory | `source-consistency/a-source-that-changes-during-bundling` | partly held | a source resolving elsewhere; message wording (identity changed) |  |
| `test_a_source_written_during_the_run_publishes_nothing` | A source rewritten mid-run fails E_SOURCE_CHANGED and publishes nothing | `source-consistency/a-source-that-changes-during-bundling` | held |  | approved |
| `test_a_source_removed_during_the_run_publishes_nothing` | A source removed mid-run fails E_SOURCE_CHANGED and publishes nothing | `source-consistency/a-source-that-changes-during-bundling` | partly held | a source removed rather than rewritten |  |

### Boundaries

2 tests: 1 held, 1 partly held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_an_unsafe_boundary_is_an_input_failure` | Two lists a definition separates fail E_UNSAFE_BUNDLE_BOUNDARY with reference, source, message, remedy | `boundary/two-lists-a-definition-separates` | partly held | source field; message wording; remedy |  |
| `test_an_unsafe_boundary_publishes_no_file` | An unsafe boundary fails E_UNSAFE_BUNDLE_BOUNDARY and publishes no bundle | `boundary/two-lists-a-definition-separates` | held |  | approved |

### Diagrams

43 tests: 27 held, 16 partly held.

| Test | What it asserts | Holding fixtures | Held? | What is missing | Verdict |
| --- | --- | --- | --- | --- | --- |
| `test_a_links_array_is_refused_naming_its_line` | Sequence links array refused E_UNSUPPORTED_CONSTRUCT naming its line, with a remedy | `reference/a-links-value-that-is-an-array` | partly held | presence of a remedy |  |
| `test_an_anchor_mermaid_draws_as_no_anchor_is_carried[tooltip]` | HTML anchor in a click tooltip is carried as text, run succeeds | `reference/an-html-anchor-mermaid-draws-as-no-anchor-is-text` | held |  | refused |
| `test_an_anchor_mermaid_draws_as_no_anchor_is_carried[pie-label]` | HTML anchor in a pie label is carried as text, run succeeds | `reference/an-html-anchor-mermaid-draws-as-no-anchor-is-text` | held |  | refused |
| `test_an_anchor_mermaid_draws_as_no_anchor_is_carried[sequence-note]` | HTML anchor in a sequence note is carried as text, run succeeds | `reference/an-html-anchor-mermaid-draws-as-no-anchor-is-text` | held |  | refused |
| `test_an_anchor_in_a_label_beside_a_click_is_still_refused` | Anchor in a node label sharing a line with a click is still refused naming the label's reference | `reference/an-html-anchor-in-a-node-label-naming-a-local-document` | partly held | node statement and click on one line; reference field |  |
| `test_every_click_on_one_line_is_followed` | Every click statement on one line is followed and rewritten | `rewriting/every-click-on-one-diagram-line` | held |  | refused |
| `test_a_dispatching_click_points_at_its_target_s_bundle_file[click Intake href]` | Dispatching click (href form) rewritten to target's bundle file; target bundle bytes | `dispatch/a-click-on-a-node-whose-text-opens-with-the-dispatch-mark-dispatches` | held |  | refused |
| `test_a_dispatching_click_points_at_its_target_s_bundle_file[click Intake]` | Dispatching click (short form) rewritten to target's bundle file; target bundle bytes | `dispatch/a-diagram-dispatch-names-its-model-in-a-comment`, `dispatch/a-dispatching-click-s-tooltip-tags-select-its-bundle-s-presets` | held |  | refused |
| `test_a_dispatching_click_s_tooltip_tags_select_its_bundle_s_presets` | Dispatching click's tooltip tags select its bundle's presets | `dispatch/a-dispatching-click-s-tooltip-tags-select-its-bundle-s-presets` | held |  | refused |
| `test_a_deferring_click_points_at_its_target_s_path` | Deferring click rewritten to target's path from the bundle folder, target not bundled | `deferral/a-click-on-a-node-whose-text-opens-with-the-deferral-mark-defers` | held |  | refused |
| `test_a_deferring_click_carries_the_pick_token` | Deferring click carries the pick token tooltip as written | `deferral/a-deferring-click-tooltip-carries-the-pick-token` | held |  | refused |
| `test_a_dispatching_click_carrying_the_pick_token_points_at_its_pick` | Dispatching click with pick token points at a local pick section listing each alternative bundle | `dispatch-brief/a-diagram-mark-identifies-a-bundle-handoff-rather-than-a-local-section` | held |  | refused |
| `test_a_parallel_click_carrying_the_pick_token_is_refused` | Parallel click carrying the pick token refused E_UNSUPPORTED_CONSTRUCT, pick-token message | `dispatch/a-parallel-dispatch-carrying-the-pick-token-is-refused` | partly held | the click form (fixture uses a parallel link) |  |
| `test_parallel_clicks_join_their_section_s_set` | Parallel clicks join their section's set; clicks point at dispatch-set sub-section | `parallel-dispatch/a-click-on-a-node-whose-text-opens-with-the-parallel-mark-joins-its-set` | held |  | refused |
| `test_a_composing_click_points_at_its_contribution` | Composing click rewritten to its contribution, section composed under the diagram's section | `composition/a-click-on-a-node-whose-text-opens-with-the-composition-mark-composes` | held |  | refused |
| `test_a_click_tooltip_selects_presets_as_a_link_title` | Ordinary click tooltip tags select presets as a link title does | `reference/a-click-tooltip-selects-presets-as-a-link-title` | held |  | refused |
| `test_a_node_mark_followed_by_text_opens_an_ordinary_click` | Node mark written against text opens an ordinary click, bundled, no diagnostic | `dispatch/a-click-on-a-node-whose-text-opens-with-a-mark-against-text-is-an-ordinary-link` | held |  | refused |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\u21c9-\u21c9]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (tooltip dispatch mark) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\xac\u21b3-\xac\u21b3]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (tag deferral and composition marks) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | this tag variant and remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\u21c9, checks-\u21c9]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (dispatch mark beside a preset tag) | `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[checks, \xac \u21c9-\xac \u21c9]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (preset tag then deferral and dispatch marks) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | this tag variant and remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\xac ?-\xac ?]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (deferral mark with pick token) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | this tag variant and remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\u21b3 Given-\u21b3 given]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (composition mark before text, tag lowercased) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | this tag variant, its lowercased report and remedy text |  |
| `test_a_tooltip_tag_stating_operator_marks_is_refused[\xa0\u21c9-\u21c9]` | Click tooltip tag made of operator marks refused naming the click, the tag, and remedy text (dispatch mark after a no-break space) | `dispatch/a-click-tooltip-of-the-dispatch-mark-is-refused`, `dispatch/a-click-tooltip-tag-of-operator-marks-beside-other-tags-is-refused` | partly held | the leading no-break space variant and remedy text |  |
| `test_a_tooltip_tag_opening_with_no_operator_marks_is_a_title[with \u21b3 Given]` | Tooltip with marks not at its start is a title carried as written, target bundled | `rewriting/a-flowchart-click-in-each-form` | partly held | a tooltip containing operator marks after text |  |
| `test_a_tooltip_tag_opening_with_no_operator_marks_is_a_title[\u21c9Intake]` | Tooltip with a mark written against text is a title carried as written, target bundled | `rewriting/a-flowchart-click-in-each-form` | partly held | a tooltip opening with a mark against text |  |
| `test_a_tooltip_tag_opening_with_no_operator_marks_is_a_title[checks]` | Tooltip naming no declared preset is a title carried as written, target bundled | `reference/a-click-tooltip-selects-presets-as-a-link-title`, `rewriting/a-flowchart-click-in-each-form` | held |  | approved |
| `test_a_class_label_states_its_link_s_operator` | Class label stating the dispatch mark dispatches its link target | `reference/a-class-diagram-link-reads-its-class-label-and-a-class-with-none-carries-no-operator` | held |  | approved |
| `test_a_second_link_on_one_element_is_refused_naming_both_lines[click]` | Second click on one node refused naming its line and the earlier line | `reference/a-second-click-on-one-node-is-refused` | held |  | refused |
| `test_a_second_link_on_one_element_is_refused_naming_both_lines[class-link]` | Class link then click on one class refused naming both lines | `reference/a-second-class-diagram-link-on-one-class-is-refused` | partly held | a click following a class link line (fixture repeats link lines) |  |
| `test_a_node_text_stating_a_refused_combination_is_refused[\xac \u21c9]` | Click on node whose text states a refused mark combination refused naming the click (deferral, blank, dispatch) | `dispatch/a-click-on-a-node-whose-text-writes-a-blank-between-the-deferral-and-dispatch-marks-is-refused` | held |  | refused |
| `test_a_node_text_stating_a_refused_combination_is_refused[\xac\u21c9]` | Click on node whose text states a refused mark combination refused naming the click (deferral against dispatch) | `deferral/a-click-on-a-node-whose-text-writes-the-deferral-mark-against-the-dispatch-mark-is-refused` | held |  | refused |
| `test_a_node_text_stating_a_refused_combination_is_refused[\u21c9\u2afd]` | Click on node whose text states a refused mark combination refused naming the click (dispatch and parallel) | `parallel-dispatch/a-click-on-a-node-whose-text-opens-with-two-dispatch-marks-is-refused` | held |  | refused |
| `test_a_node_text_stating_a_refused_combination_is_refused[\u21c9\u21b3]` | Click on node whose text states a refused mark combination refused naming the click (dispatch against composition) | `dispatch/a-click-on-a-node-whose-text-writes-the-dispatch-mark-against-the-composition-mark-is-refused` | held |  | refused |
| `test_a_node_text_stating_a_refused_combination_is_refused[\u2afd\u21b3]` | Click on node whose text states a refused mark combination refused naming the click (parallel against composition) | `composition/a-click-on-a-node-whose-text-writes-the-parallel-mark-against-the-composition-mark-is-refused` | held |  | refused |
| `test_a_click_s_directive_and_target_refusals_name_the_click[whole-document]` | Composing click naming a whole document refused naming the directive click | `composition/a-composing-click-naming-a-whole-document-is-refused` | held |  | refused |
| `test_a_click_s_directive_and_target_refusals_name_the_click[composed-and-deferred]` | Section composed and deferred by two clicks refused naming the directive click | `composition/a-section-composed-and-deferred-in-one-step-is-refused` | partly held | the click form and the directive click naming (fixture uses links) |  |
| `test_a_click_s_directive_and_target_refusals_name_the_click[remote]` | Dispatching click to a remote address refused naming the link click | `dispatch/a-dispatched-link-naming-a-remote-address` | partly held | the click form and the link click naming (fixture uses a link) |  |
| `test_a_click_s_directive_and_target_refusals_name_the_click[missing]` | Dispatching click to a missing document fails E_TARGET_NOT_FOUND naming the link click | `inclusion/operators-keep-the-absent-target-refusal` | partly held | the click form and the link click naming (fixture uses a link) |  |
| `test_a_click_s_directive_and_target_refusals_name_the_click[silent]` | Dispatching click to a silent document refused naming the link click | `dispatch/a-dispatching-click-naming-a-document-that-declares-nothing-is-refused` | held |  | refused |
| `test_an_ordinary_click_carrying_the_pick_token_is_refused_naming_it` | Ordinary click carrying the pick token refused naming the click | `deferral/an-ordinary-click-carrying-the-pick-token-is-refused` | held |  | refused |
| `test_a_deferring_composing_click_carrying_no_tooltip_publishes_no_title` | Deferring composing click with no tooltip publishes its contribution link with no title | `composition/a-deferring-composing-click-carrying-no-tooltip-publishes-no-title` | held |  | refused |
| `test_a_gantt_click_carrying_a_tooltip_is_refused` | Gantt click carrying a tooltip refused naming its line, nothing published | `reference/a-gantt-click-carrying-a-tooltip-is-refused` | held |  | refused |
