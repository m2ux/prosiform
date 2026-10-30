# W02 Validation

## Revision

Task commits 95d7064 and 482741d on i01/e06/w02-bounded-metadata-decoder, based on cd3d8e6. Governing W01 contract: 91eecd4, delivered by PR #219 into i01/e06/engineering. W02 delivers the decoder seam; W03 connects source reading.

## Schema and coordinates

The final targeted metadata suite passes all 80 cases. AC2 covers absent/empty metadata, string fields, paired settings, group/depth grammar, reserved keys and Core typing. AC4 covers physical code-point locations, BOM, CRLF, tabs, Unicode, syntax/reader errors and duplicate related locations in text and JSON. The out-of-range Unicode escape regression verifies column 11, including parser cleanup.

## Resource and adversarial cases

AC3 tests source-byte boundaries before decoding, collection-depth boundaries and a 10,000-level unterminated input rejected at the configured depth. Alias/custom-tag/merge-key rejection, tag-kind mismatch, YAML 1.1 rejection, duplicate scalar/sequence/map keys, map-order-independent equality and distinct bool/int/float keys pass. Numeric cases include 5,000-digit integers, hexadecimal keys and exponents.

## Static and regression checks

Lint, format, strict mypy and dependency lock checks pass. The complete Python run passed 879 tests on 95d7064; 609 harness tests pass. The final scanner-mark correction adds one targeted regression and all 80 metadata cases pass on 482741d, with strict mypy passing again.

## Repository checks

Corpus, wheel smoke, layout, dependency tables, online links, vocabulary, invocation, conformance and independence pass against the task build. The corpus holds 252 fixtures. These verify existing runtime behavior; W02 does not claim runtime metadata integration.

## Review

Independent review ran fifteen additional adversarial cases, all passing after corrections. Review corrected budget messages, ReaderError position, invalid Unicode escape handling and scanner-mark preservation. No deferred debt.

## Plan changes

No task or epic scope changes. The main implementation base is distinct from W01's engineering contract base; both draft reviews remain open until epic completion.

## Merged revision verification

PR [#221](https://github.com/m2ux/prosiform/pull/221) merged exact head 482741dd5bbe196351ac05c7921151b187abfad2 into i01/e06/main as 5375a66c6335ef45fb8e0dfe70c4f6579147d51c. Fresh target protection returned not protected, active rules were empty, and reviews were empty. The [remote Checks run](https://github.com/m2ux/prosiform/actions/runs/39904611362) completed successfully before merge.

At merged revision 5375a66, the named metadata instrument ran again in the epic-base worktree: all 80 tests pass. AC2, AC3 and AC4 are verified on this revision and recorded complete; W02 is Done.

Draft [#222](https://github.com/m2ux/prosiform/pull/222) presents the Python epic base to main. Its Development relation to epic #218 was created with addCloseIssueReferences and read back with complete pagination. Draft #220 retains the engineering contract review. Epic #218 remains open and In Progress. W03 is next; it has not been started in this delivery session.
