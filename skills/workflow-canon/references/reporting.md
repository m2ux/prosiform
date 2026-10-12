# Reporting

Severity, row shapes, and which report the run owes.

## Report Context

Read this section before selecting a report layout.

### Bands

| Band | Holds | Target |
|---|---|---|
| **Live** | The definition misbehaves as it stands — a value read before its producer runs, a bind of the wrong value, a gate option that reaches no path | Zero, every pass |
| **Contract** | The defect propagates while the run still works — a second home for an owned fact, a constraint with no structural backing, a citation whose home lacks the claim | Zero, every pass |
| **Hygiene** | Contained to the prose it sits in | A falling ratchet against the prior pass |

State each band's count. The verdict is Live and Contract. Text a fix writes is checked within its pass, so a pass reports no finding its own fixes made.

### Severity

Severity ranks urgency inside a band. The band says whether the finding gates.

| Severity | Fires when |
|----------|-----------|
| `Critical` | Schema-invalid or structurally broken. Must not be committed. Every guard failure is Critical. |
| `High` | An entry fires on a construct the change ships, and the defect propagates |
| `Medium` | An entry fires and the defect stays in that construct |
| `Low` | Hygiene with no consumer consequence |

The [dispatch phases](audit-dispatch.md#phases) own finding confirmation. An unmeasured guard records `blocked` coverage; the [canon check conventions](canon-context.md#canon-check-conventions) define its exit statuses.

### Finding Rows

| Column | Carries |
|--------|---------|
| ID | Stable within the report |
| Band | `Live`, `Contract`, or `Hygiene` |
| Severity | The scale above |
| Entry | As the catalog's entry-identity rule states. A principle by the title its file uses: an anchor that embeds the section ordinal breaks when a principle is inserted ahead of it |
| Location | File and field, at the depth the evidence sits |
| Evidence | The construct Detect keys on, quoted or named. A closure-only file says which contract it references |
| Origin | The value [Attribution](audit-mode.md#attribution) assigns. A `known` row stays out of the decision surface |
| Fix | The action the entry prescribes, in one line |

A row whose Evidence cannot name a construct is not a finding. Evidence and Location cite any construct in a change-surface file.

### Coverage Ledger

The generated [coverage state](change-surface.md#artifacts) accounts for every row–criterion cell, inventory, file read and supplemental obligation. The findings report summarizes divergences and links to that complete ledger.

| Column | Carries |
|--------|---------|
| Home | The criteria home |
| Unit | The section title or anchor, as the home spells it |
| Status | `not-applicable` with the unit's own reason, or `blocked` with what prevented the walk |

Derive unknown, unverified, unevaluated and supplemental residuals from current state. Preserve each residual's identifiers. Display counts summarize those lists.

### File Coverage

Independent of the unit ledger: every unit can be `walked` while the surface stays unopened.

| Disposition | Means |
|-------------|-------|
| `read` | The whole file was inspected |
| `unread` | Anything else |

A scan hit is `read` only when the file was then inspected whole. A scan is evidence for a finding, not a path disposition. `read` and `unread` sum to the enumeration; where they do not, the report states the list that was walked.

List the `unread` paths. While any remain, the header's status is the [coverage header](#coverage-header). An existence claim over a list that still has `unread` paths says so on the finding.

### Coverage Header

Use `finished` only when the shared [completion predicate](change-surface.md#completion) holds; otherwise use `in progress`. Include the captured generation, row and AP/DP counts, verified applicability, applicable-cell evaluations, unread sources and unresolved supporting obligations. Every count reconciles to the generated state.

## Which Report

Inside workflow-authoring or workflow-design, use [Workflow Reports](#workflow-reports). Otherwise use the [Standalone](#standalone) layout. Stored artifacts follow the shared [planning guide](planning.md).

## Standalone

In the chat, or in a file the user named:

~~~markdown
# Canon Audit — `{target}`

**Status:** in progress | finished · **Base ref:** `{ref}` · **Snapshot:** `{hash}` · **Coverage:** N rows × N AP/DP criteria — N of N mappings independently verified, N of N applicable cells evaluated · **Change surface:** N files (touched: N · context: N · consumers: N) · **Guards:** clean | N findings | N unmeasured

**Verdict:** Live N · Contract N · Hygiene N, at that coverage. Residual: N unknown mappings · N unverified mappings · N unevaluated applicable cells · N unverified inventory items · N supporting obligations · N unread files. Live and Contract converge to zero over the coverage measured. Hygiene ratchets against the prior pass's N.

| Band | Open | Known | Prior pass |
|------|-----:|------:|-----------:|
| Live | N | N | N |
| Contract | N | N | N |
| Hygiene | N | N | N |

## Change Surface

| Path | How it joined |
|------|----------------|
| `{path}` | touched |
| `{path}` | closure — references `{contract-path}` |
| `{path}` | consumer of a change-surface file |

## Findings

| ID | Band | Severity | Entry | Location | Evidence | Origin | Fix |
|----|------|----------|-------|----------|----------|--------|-----|

## Coverage

[Complete coverage ledger]({run}/audit-coverage.md)

| Home | Unit | Status |
|------|------|--------|
| `{home}` | `{unit}` | not-applicable — `{reason}` |

## File Coverage

read N · unread N.

| Disposition | Paths |
|-------------|-------|
| `unread` | `{path}` |

## Finding Confirmations

| Finding | Outcome | Reason |
|---------|---------|--------|
| `{id}` | `{outcome}` | `{what reproduced}` |

## Known
~~~

Omit an empty section. Order findings Critical → High → Medium → Low. Link the entry; the report holds no criteria prose. Known repeats the Findings columns for rows whose Origin is `known`, and the band table counts them apart from Open. Prior pass carries the previous report's figure; every other header count reconciles against the generated ledger. Status is the [coverage header](#coverage-header). Live or Contract at zero over partial coverage is a statement about that part. A Live or Contract count that rose says a fix moved a defect.

## Workflow Reports

That run's guide owns the layout:

| Artifact | Guide, on the corpus tree |
|----------|---------------------------|
| `findings-register.md` | `corpus/workflow-authoring/resources/findings-register.md` |
| `compliance-review.md` / `post-update-review.md` | `corpus/workflow-design/resources/compliance-report.md` |
| per-pass `*-findings.md` | `corpus/workflow-design/resources/findings-satellite.md` |

Fetch the guide's `## Template` and fill it. Persist through the activity's `manage-artifacts::write-artifact` step.
