# Change List

The plan changes the W03 delivery session applied and held.

## Applied

None. The rewrite W02 built already resolves each composed region against its source and keys each contribution by its directive's position, so W03 needed no code change beyond stating those rules in the composition module.

## Held

None.

## Notes

- **A dispatch inside a contribution points at its source's sub-section.**
  The contribution's dispatch link points at the dispatch sub-section the target's own file group carries, as W02's dispatch pass states. Once W08 drops the file group of a document reached by directives alone, that sub-section is absent, so W08 must give such a dispatch a sub-section of its own.
