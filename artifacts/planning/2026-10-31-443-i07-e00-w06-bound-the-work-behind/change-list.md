# Change List — W06 Bound the Work Behind the Byte Budget

> Delivery record · 2026-10-31

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| `SCALAR_DIGITS = 65_536` declared beside the budgets | Source | A byte budget bounds the work its bytes can ask for only where that work is bounded. One scalar canonicalising in quadratic time was enough to spend minutes inside a budget it never crossed | `src/prosiform/limits.py` |
| A scalar beyond the ceiling refused with `E_RESOURCE_LIMIT` | Source | The ceiling is what makes the byte budget the bound it claims to be; a refusal is reachable in a fraction of a second where canonicalising the same scalar took sixteen | `src/prosiform/metadata.py` |
| Kind resolution separated from canonicalisation | Source | The ceiling has to be held before the cost is paid, so `_kind` classifies and builds nothing and `_canonical` reads what is already bounded | `src/prosiform/metadata.py` |
| The ceiling stated in the page the budgets are read on | Docs | The ceiling is part of what a byte budget means rather than an option, so it belongs where the budgets are stated and not in the options table | `docs/validation.md` |
| `cli.undeclared_root` names the declaring source and the root as written | Source | The walk reports the segment it refused; a reader of a bare path in a closure cannot tell which document declared it or what it wrote | `src/prosiform/cli.py` |
| `cli.root_remedy` states the remedy for each of the three codes the walk raises | Source | The action differs between a missing directory, a link the no-follow walk declines and a permission fault, so one remedy would misdirect two of the three | `src/prosiform/cli.py` |
| The work item's Test row delivered as five cases | Test | The row asks for a run at the bound completing within it, and a run over a reference declaring a missing root reporting the reference, the root and a remedy | `src/tests/test_metadata.py`, `src/tests/test_file_roots.py` |

No finding moved between tasks, no task was created, closed or renumbered, and no criterion changed. The epic's disposition already carried findings 35 and 36 to W06, and the work item's Test row already named both cases, so the plan as written was followed.

Epic delivery was recorded against the plan: row `W06` on [#443](https://github.com/m2ux/prosiform/issues/443) links [#471](https://github.com/m2ux/prosiform/pull/471), merged at `46700605`, with Done ticked, and `AC13` and `AC14` are ticked there, each on the evidence the pull request's Test Plan cites.

## A finding wider than the row states

Finding 35 names a base-prefixed integer. Probing the neighbouring notations found the float exponent costs the same quadratic time in `_finite_float`, on a branch no ceiling over integers reaches: 4.17s at 800,000 digits against 9.15s for hex and 0.001s for decimal. The repair bounds the work rather than the notation, so the float branch is covered by the same ceiling and the same code.

Recorded here rather than amended in the epic: the row names one case, and the defect it describes is the family the case belongs to.

## Held

| Held | Why |
| --- | --- |
| A corpus fixture for the scalar ceiling | The case is reachable through a fixture's source tree and exit status, so a fixture would hold it. It is not taken here because `fixtures/` is W10's component by the epic's own planning, and adding one would collide with a sibling delivery. The case is held in `src/tests`, where it runs on every `make test`; the corpus belongs to W10 |
| A corpus `message_contains` on the root fixture | The same reason: `fixtures/cli/an-allowed-source-root-naming-no-directory` states the code and would state the message and remedy beside it, but `fixtures/` is not this task's area |
| A ninth budget option for the ceiling | The ceiling states what a byte budget means rather than a preference an author sets. An option would invite raising it past what a run can afford, which is the defect |
| A timeout instead of a digit ceiling | A timeout makes the outcome depend on the machine the run is on, which contradicts the deterministic bound every other budget keeps |
| Making the costly notations linear rather than bounded | A decimal conversion of a binary value is quadratic in the digits by construction; converting in chunks under a fixed precision trades exactness for speed and would change which keys are duplicate. The ceiling bounds the work without changing any value |

## Technical debt classified

| Debt | Class | Disposition |
| --- | --- | --- |
| `test_linked_bootstrap` needs network for `uv build` | Deferred, not this task's | The brief names it as reproducing on every settled branch and passing in CI. It does not import the changed modules |
| `make smoke` fails under `/tmp`'s atomic folder swap | Deferred, not this task's | Same standing; it fails before the build is exercised |
| `_finite_float` accumulates its exponent digit by digit | Fixed on this branch, trivially | The ceiling covers it, so the cost is bounded. Making it linear would change the exponent's exactness, so the bound is the right repair rather than a rewrite |
| `Decimal(int(...))` remains the integer's canonical form | Deferred to design, not blocking | It is exact, and exactness is what decides duplicate keys across notations. A ceiling bounds its cost; replacing it is a change no finding asks for |

Nothing blocking was found. The one trivial candidate inside the changed code — the float branch's accumulation — is bounded by the same ceiling the integer branch is, so it is delivered rather than deferred.

## Placement needs

None. No new initiative, epic or task was needed, and nothing was found that needs a home outside this pull request.
