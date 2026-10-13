# Canon Map

How each home is enumerated, and where a judgement already made is recorded.

## Unit Inventory

Read the enumeration from the home at the commit audited, with [List units](canon-context.md#list-units).

| Home | Unit |
|------|------|
| Anti-Patterns | One `##` family; each `###` entry inside it |
| Design Principles | One `##` |
| Convention Conformance | One `##` |
| Guards | One registry entry in `guards/guards.ts` |

- Read the catalog through its last family. Appended entries share that family, so its title is not the end of the list.
- The catalog's first family binds when the change edits a canon home: `anti-patterns.md`, `design-principles.md`, or `convention-conformance.md`. Otherwise it is `not-applicable`, with that reason.

## Prior Judgments

An entry can fire against an instance a surface has already judged. Read that surface before hand-walking an entry whose registry line claims the check.

| Authority | Where | Records |
|-----------|-------|---------|
| A guard's exemption surface | In the guard or a module it shares — `EXEMPT_DATA_IDS` in `src/schema/identifiers.ts`; the kind and pipeline sets in `guards/check-prism-lens-reachability.ts` | Instances the check excuses, each with a reason |
| Triage ledgers | `ledgers/binding-fidelity-triage.json` and `ledgers/section-framing-triage.json` on the corpus tree | A verdict and a rationale per finding. Binding-fidelity stamps the corpus commit |
| Reasoned exemption lists | `walks/option-coverage.json` on the corpus tree | Options a walk need not reach, under the reason that covers them |

`EXEMPT_DATA_IDS` is compiled into the Zod variable schema and the published JSON schemas.

## File Kinds

Author and Audit establish applicability through the shared [matrix contract](change-surface.md#applicability). The complete [unit inventory](#unit-inventory) supplies the matrix and supplemental obligations.

- **Fires-on line.**
  Each entry, principle and convention section names the constructs it reads. A unit reaches only the file kinds its line names, resolved through [List Units for a Construct](audit-mode.md#list-units-for-a-construct).
- **A unit carrying no line.**
  It is walked by the rule governing its family. The Creation Rules exempt two families from the line: the catalog's `##` family headings, and the Creation Rules themselves, which bind as the [first family](#unit-inventory) does.
- **An unavailable lookup.**
  Where the command cannot run, or a home carries no fires-on lines, the walk is the full unit-file product and the report names that, so a narrowed walk is never read as a full one.
- **Coverage.**
  Fires-on narrows which files a unit is carried against. Every cell of the full product stays in the coverage the report accounts for.
