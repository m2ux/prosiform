# Joins

Pairs of independent rows that do not share a pull request, and why.

- E09:W02 and E09:W03 take separate pull requests: W02 decides what the mapping refuses before any source is read, and W03 resolves the entry and referrer and derives the run's output name.
- E09:W02 and E09:W04 take separate pull requests: W04 emits the substitutions a run performed, which a refused run never reaches.
- E09:W02 and E09:W05 take separate pull requests: W05 redirects the targets a run resolves without compiling, and its fixtures all publish.
- E09:W02 and E09:W06 take separate pull requests: W06 changes the lookup a mapping performs, and W02 refuses a mapping before that lookup runs.
- E09:W02 and E09:W07 take separate pull requests: W07 derives a source's settings and root from its bytes, which a refused run never captures.
- E09:W03 and E09:W04 take separate pull requests: W03 changes the document a run is built from, and W04 changes what the run reports about it.
- E09:W03 and E09:W05 take separate pull requests: W05 has no diagnostic of its own and W03 publishes under another name.
- E09:W03 and E09:W06 take separate pull requests: W06 redirects a section within a document, and W03 redirects the document a run starts from.
- E09:W03 and E09:W07 take separate pull requests: W07 changes which group a substitute joins and which root bounds its links, neither of which the entry's own path decides.
- E09:W04 and E09:W05 take separate pull requests: W05 changes what a withheld reference resolves to, and W04 has no compiled target to report.
- E09:W04 and E09:W06 take separate pull requests: W06 changes the lookup that records a substitution, and W04 reads the record rather than performing the lookup.
- E09:W04 and E09:W07 take separate pull requests: W07 changes a source's metadata and root, and W04 reports the substitution that stands in front of it.
- E09:W05 and E09:W06 take separate pull requests: W06 redirects compiled targets by section, and W05 redirects the targets a run resolves without compiling.
- E09:W05 and E09:W07 take separate pull requests: W07 governs the substitute's outgoing links, and W05 governs the link that reaches it.
- E09:W06 and E09:W07 take separate pull requests: W07 reads the substitute's own declarations, which W06 never inspects because it ends at the reference the source wrote.
- E09:W02 and E09:W08 take separate pull requests: W08 consumes a mapping that already works, and W02 refuses the two shapes that state nothing.
- E09:W03 and E09:W08 take separate pull requests: W08 redirects artifact links inside the tree, and W03 redirects the document a run starts from.
- E09:W05 and E09:W08 take separate pull requests: W08 compiles the targets its mapping names and W05 withholds them.
- E09:W06 and E09:W08 take separate pull requests: W08 redirects whole artifacts, and W06 redirects a section within one.
- E09:W07 and E09:W08 take separate pull requests: W07 decides which group a substitute joins, and W08 leaves every stub in the group its own metadata declares.
