# W02 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| Candidate preservation (`candidate.py`) compares a code example with its click destinations taken out (`undestined`), and `carrying` counts a click line among the lines the bundle edits. | Blocking: preservation compares the fence's lines and content byte for byte, so it rejected every correct rewritten bundle with `E_UNEXPECTED_INTERNAL_ERROR`. The brief allows this fix. Holding each destination to its assigned anchor stays with W03 (AC7). |
| `clicked` locates the destination from the line's end, not from its start (physical length less fence-line length, plus offset). | The two are the same arithmetic where the fence line is the trailing text of the physical line. Measuring from the end also holds where the parser expands a tab in the leading indent, because the text after a destination is never expanded. |
| The `bundle.py` module docstring states that a code example keeps every byte but a diagram's click destinations, and adds a paragraph on the rewrite. | The docstring stated that a code example keeps its bytes, which a rewritten click destination contradicts. |

## Held

| Change | Reason |
| --- | --- |
| W03 will need `candidate.references` to compare the diagram destinations the bundle publishes with the anchors their uses were assigned. | Preservation now leaves the destination characters out, so until W03 lands no check holds them. W03's work item already owns this (AC7). It is recorded here so W03 knows preservation was narrowed to make room for it. |
