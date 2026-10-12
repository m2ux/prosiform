# Definition Scope

The definition files, contracts and references that authoring and canon audits resolve on this project.

## Scope

- **Base ref.**  The ref the change is measured against.
- **Surface files.**
  `workflow.yaml`, `activities/`, `techniques/`, `routines/`, `resources/`, READMEs of the target.
- **Construct ids.**
  - The ids the surface writes, resolved beside its paths: the bare kind of each definition file on it, the paths of the fields those files declare, and `resource` or `readme` for its supporting material.
  - A listing covers the queried id and the ids above it, so a kind named alone leaves the units keyed to its fields unlisted.
  - They narrow the unit side of the walk through [file kinds](canon-map.md#file-kinds).
  - A surface the catalog keys on nowhere, such as walk records, ledgers and fixtures, carries no id and is judged against the contracts its own consumers enforce.
- **Touched.**
  Definition paths whose bytes differ from the base ref, each the whole file. Hunks discover membership.
- **I/O contract.**
  - Technique `## Inputs` / `## Outputs`, including nested component and artifact declarations.
  - Activity inputs, outputs, and step binds that name those ids.
  - Routine parameters, outputs, internals, nested reference sites and technique arguments.
  - Renames, additions, removals, optionality flips, and type or shape changes.
- **Reference.**
  - `techniques[]`, step `technique` / `technique.name`, Protocol `Apply` / `::` / a markdown link to an op, or a resource or README cite that resolves to the op file.
  - Sweep the workflows tree. Resolve each to a file path.
  - Resolve routine references and their full instantiation chains, graph entries, ancestors and shared resources through [surface identity](change-surface.md#identity).
- **Closure.**
  Affected elements and supporting sources reached through callers, consumers, invoked definitions and inherited contracts, including unchanged files across workflow boundaries.
- **Change surface.**  Touched ∪ closure. The header reports the two subsets separately.
- **Consumers.**
  - References other workflows hold into the target. Always computed.
  - A consumer joins the change surface when the file it names is on it.
  - Start from [Find consumers](canon-context.md#find-consumers), then resolve binds and Apply links.
- **Reference workflows.**  Siblings of similar type, as convention conformance requires.
- **Prior residual.**
  - `unread` paths in the latest findings register in the shared [planning record](planning.md).
  - Reconcile captured identities through [freshness](change-surface.md#freshness-and-resume). A deleted path remains a base-side obligation when the selected comparison includes it.
  - Reading starts at the residual. The walk follows [audit rules](audit-mode.md#rules). Paths a stop leaves unread are the next residual.
- **Second entry.**
  - Where a graph gives one activity two entry points, both are on the surface.
  - Read each outcome against the state that entry arrives in. Take entries from every graph that includes the activity.

Hunk lines are not the surface. A unit read from a hunk is not `walked`. A referencer stays on the surface when its bind site was not edited.
