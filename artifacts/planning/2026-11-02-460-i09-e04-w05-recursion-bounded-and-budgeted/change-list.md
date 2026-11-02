# Change List

The plan changes the W05 delivery session applied and held.

## Applied

- **Delivery recorded.** [#574](https://github.com/m2ux/prosiform/pull/574) merged into `i09/e04/main` at `1c5a6987`. W05's row links it and is marked Done, `AC9` and `AC10` are ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change under Section Composition. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **W08 stopgap removed.**
  Placement no longer turns a directive inside a contribution into an inclusion, and the two `test_cli.py` cases that pinned it are gone.
- **Unmapped-pass counting.**
  Before destinations are assigned, composition counts only the generated headings toward `output-bytes`, since a link's published length is unknown there; the mapped pass counts every byte, so no figure exceeds the published bundle's.
- **No arising issues.**
