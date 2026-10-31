# Validation — W06 Bound the Work Behind the Byte Budget

> Evidence · 2026-10-31

Every case below was run in the worktree `.worktrees/i07/e00/w06-bound-the-work-behind`, at branch `i07/e00/w06-bound-the-work-behind`, cut from `i07/e00/main` at `23882b7d` and fast-forwarded onto it at `de694350`. The branch merged as [#471](https://github.com/m2ux/prosiform/pull/471) into `i07/e00/main` at `46700605`.

The build under test is named `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. Tooling ran under the sandbox by absolute path; `git fetch` and `git push` ran unsandboxed.

## Baseline, before any change

Both faults were reproduced against the branch as cut, before a line was edited, so a case that reports a ceiling only after the repair would prove nothing.

## Finding 35 — the byte bound does not bound decoder work

**The case the finding records.** A source of 1,048,558 bytes — inside the default `-B` of 1,048,576 — holding one frontmatter field whose value is `0x` followed by 1,048,536 hex digits.

**Before the fix**, the run accepted the source and canonicalised the scalar in full:

```
1048558 source bytes, 1048536 hex digits in one scalar
16.114s  accepted
```

Sixteen seconds inside a budget it never crossed. The bound exists to protect a run from material it cannot handle, and a source of one megabyte held material it handled in quadratic time.

**The stage.** Timing the conversions the decoder makes separates them:

| Conversion | 100,000 digits | 400,000 digits | 800,000 digits |
| --- | --- | --- | --- |
| `int(text, 16)` | 0.0001s | 0.0004s | 0.0006s |
| `Decimal(int(text, 16))` | 0.148s | 2.38s | 9.50s |
| `str(int(text, 16))` | 0.023s | 0.124s | 0.293s |

The binary conversion is linear; converting that binary value to a decimal one is what is quadratic. `metadata._scalar` performed it at `Decimal(int(value, 8 if value.startswith("0o") else 16))`.

**A second site the finding does not name.** A float's exponent is accumulated digit by digit in `_finite_float` as `power = power * 10 ** len(chunk) + int(chunk)`, which is the same quadratic growth in the same function, on the branch a ceiling over integers does not reach. Measured end to end on the tree before the change, at a fixed source size:

| Notation, 400,002 characters of literal | Time |
| --- | --- |
| `0x` + hex | 2.549s |
| `1e` + exponent | 1.188s |
| `1.` + fraction, no exponent | 0.201s |
| decimal | 0.195s |

At 800,000 characters the same run took 9.648s for hex and 4.165s for the exponent, against 0.205s and 0.209s for the two linear notations.

**After the fix**, the same 1,048,558-byte source, with the same scalar:

```
0.215s  InvalidMetadata: one int scalar carries 1048538 characters, more than the
65536 a scalar of this notation may carry, because its canonical form costs time
quadratic in its digits; write the same value in decimal or as a string, or keep
it within 65536 characters
```

Sixteen seconds became a fifth of a second, and the run reports which construct crossed and what to write instead.

**Each notation at the byte budget, on the changed tree:**

| Notation | Outcome | Time |
| --- | --- | --- |
| `0x` + hex, 1,048,538 characters | `E_RESOURCE_LIMIT` | 0.216s |
| `0o` + octal, 1,048,538 characters | `E_RESOURCE_LIMIT` | 0.218s |
| `1e` + exponent, 1,048,538 characters | `E_RESOURCE_LIMIT` | 0.221s |
| decimal, 1,048,536 characters | accepted | 0.223s |

**The ceiling's figure.** One costly scalar at each candidate ceiling, and the worst a megabyte can then ask for:

| Ceiling | One scalar | Scalars in a megabyte | Worst total |
| --- | --- | --- | --- |
| 4,096 | 0.36 ms | 255 | 0.09s |
| 16,384 | 5.49 ms | 63 | 0.35s |
| 65,536 | 63.48 ms | 15 | 0.95s |

65,536 is declared because the shipped tests carry scalars of 5,002 and 20,000 characters, so a smaller ceiling would refuse sources the repository already reads, and the worst case at the byte budget stays under a second.

**What the ceiling must not touch.** The shipped cases the corpus and the tests already read, each asserted beside the ceiling:

| Case | Result |
| --- | --- |
| `other: "9" * 5000` (`test_large_integer`) | read, unchanged |
| `0x` + `f` * 5000 against `0x` + `F` * 5000 (`test_extreme_canonical_duplicates`) | still duplicate, unchanged |
| `1e` + `9` * 5000 against `1.0e` + `9` * 5000 | still duplicate, unchanged |
| `prosiform: {group: rules, group-depth: 0x2}` (`test_core_integer_depth`) | resolves to 2, unchanged |
| A `group-depth` of 5,001 hex digits | still refused by the 1–6 range rule, not by the ceiling: it is inside the ceiling, so the schema decides it as before |

## Finding 36 — a root-not-found diagnostic reports a bare path segment

**The break.** A source whose frontmatter declares `prosiform: {root: "missing"}`, in a directory holding no `missing`.

**Before the fix**, the diagnostic carried the segment the walk refused and nothing else:

```json
{"severity": "error", "message": "missing", "code": "E_ROOT_NOT_FOUND", "reference": "a.md", "chain": ["a.md"], "location": {"file": "a.md", "line": 2, "column": 19}}
```

Rendered as text:

```
E_ROOT_NOT_FOUND: missing
  reference: a.md
  chain: a.md
  location: a.md:2:19
```

`missing` states neither which source declared the root, nor what that source wrote, nor what a reader does. A closure of any size leaves a reader unable to tell which document to open.

A nested declaration was worse: `prosiform: {root: "library/../absent"}` reported `library`, a segment of a root that was itself a path expression, so the message named neither the root nor a directory that exists anywhere.

**After the fix:**

```json
{"severity": "error", "message": "the source 'a.md' declares prosiform.root 'missing', which the walk cannot reach: missing", "code": "E_ROOT_NOT_FOUND", "reference": "a.md", "remedy": "declare a root the declaring document's directory carries, or remove prosiform.root to bind the invocation working directory", "chain": ["a.md"], "location": {"file": "a.md", "line": 2, "column": 19}}
```

The nested declaration reports the whole root as written:

```json
{"message": "the source 'docs/b.md' declares prosiform.root 'library/../absent', which the walk cannot reach: library"}
```

The three codes the same walk can raise each carry a remedy of their own, because the action differs: a missing directory, a link the no-follow walk declines, and a permission fault.

**What did not move.** The original location, the reference, the code and the chain are unchanged, and `test_missing_or_non_directory_root_has_original_location` still passes for both a missing directory and a root naming a regular file.

## Cases that ship with the fix

Each case below failed on the tree before the change and passes after it.

| Case | File | Before |
| --- | --- | --- |
| `test_one_scalar_beyond_the_ceiling_is_refused_inside_the_byte_budget` | `src/tests/test_metadata.py` | 16.114s, accepted |
| `test_a_scalar_whose_canonical_form_is_quadratic_has_a_ceiling` | `src/tests/test_metadata.py` | no ceiling to cross |
| `test_a_scalar_within_the_ceiling_is_read` | `src/tests/test_metadata.py` | passed; holds the shipped shapes unchanged |
| `test_a_missing_root_names_the_declaring_source_the_root_and_a_remedy` | `src/tests/test_file_roots.py` | `KeyError: 'remedy'` |
| `test_a_root_absent_from_the_working_directory_names_that_binding` | `src/tests/test_file_roots.py` | `KeyError: 'remedy'` |

The two metadata ceiling cases cannot be run against the unmodified tree at all, because they import `SCALAR_DIGITS` and it does not exist there. Their failure before the repair is therefore recorded as the behaviour they assert, measured above and reproduced with a standalone script against both trees.

## Checks run

Run on the branch head, each target invoked directly:

| Target | Result |
| --- | --- |
| `make lock-check` | pass |
| `make lint` | All checks passed |
| `make format-check` | 34 files already formatted |
| `make typecheck` | no issues in 34 source files |
| `make test` | 1306 passed, 13 errors |
| `make harness` | pass |
| `make authoring` | 0 findings |
| `make corpus` | 349 fixtures, 349 pass, 0 fail, 0 awaited |
| `make smoke` | fail: `E_PUBLICATION_FAILED`, `hatchling` unfetchable |
| `make layout` | 4 trees present |
| `make tables` | 21 commands and 8 declarations |
| `make vocabulary` | 44 terms, every one defined |
| `make steps` | 59 documents, every procedure a sub-section |
| `make invocation` | 29 statements |
| `make conformance` | 0 declarations naming no clause, 0 codes unreported |
| `make independence` | pass |

`make test`'s thirteen errors are all in `test_linked_bootstrap`, which runs `uv build --wheel` and needs network for `hatchling`:

```
cause: Failed to fetch: https://pypi.org/simple/hatchling/
cause: dns error: failed to lookup address information: Temporary failure in name resolution
```

The brief names that case, and `make smoke`'s `E_PUBLICATION_FAILED`, as reproducing on every settled branch and passing in CI. Neither imports the changed modules; `test_metadata` and `test_file_roots` pass, and the full suite passes with `test_linked_bootstrap` excluded:

```
$ uv run --frozen pytest -q --ignore=tests/test_linked_bootstrap.py
1306 passed
```

## Review of neighbouring behaviour

| Behaviour | Held by |
| --- | --- |
| A decimal integer of any length a byte budget admits is still read | `test_a_scalar_within_the_ceiling_is_read`, `test_large_integer` |
| A float without an exponent is still read whole | `test_a_scalar_within_the_ceiling_is_read` |
| Duplicate keys across notations are still duplicate | `test_extreme_canonical_duplicates`, `test_core_key_types_are_distinct` |
| The boxed-integer depth values `0x2` and `0o2` still resolve to 2 | `test_core_integer_depth` |
| A root the walk reaches is unaffected | `test_library_root_outside_source_and_fragment_self_reference`, `test_root_walk_checks_symlinks_before_parent_segments` |
| A symlinked or inaccessible root is still refused under its own code | `test_a_source_reached_through_a_link_is_refused_before_any_output_check` |
| The original location of a root fault is unchanged | `test_missing_or_non_directory_root_has_original_location` |
