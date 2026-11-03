# Validation

Evidence for the check that a heading answers one member, observed at branch head `906e92c2` of `i10/e03/w01-a-destination-answers-one`.

## A heading answering two members fails

Covers `AC2`. `test_a_heading_answering_two_members_of_a_group_fails` in `src/tests/test_candidate.py` records a heading of a built candidate's merged group as answering a target of a second document. Validation raises `Invalid` under the invariant `one destination answers one member`, and the failure names the heading, the group and both documents. Validation raises before anything is published. Result: pass.

## A correctly built merged group passes

`test_a_variant_heading_answers_its_own_document` and `test_a_merged_heading_one_document_contributes_answers_that_member` build merged groups with the grouping arrangement and hold every heading to one member; `test_a_candidate_whose_merged_headings_each_answer_one_member_validates` runs the whole validation pass over a built candidate recorded as merged. Result: pass.

## The repository checks

`make check`, run with the build under test named by `PROSIFORM_BUILD`, covers lint, types, the unit tests, the 504-fixture corpus, invocation, conformance and independence. Result: pass, exit 0.
