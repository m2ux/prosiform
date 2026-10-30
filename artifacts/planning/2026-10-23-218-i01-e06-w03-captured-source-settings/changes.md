# Delivery Decisions

- Capture each source's immutable conversion settings from the same read as its body. Preserve exact BOM/delimiter recognition and physical coordinates; enforce raw source budgets before UTF-8 or YAML decoding.
- Retain normally opened deferred sources in the read/index/capture caches, independently of the contributing-reference set. This closes the observed duplicate reads, missing byte accounting and missing publication rechecks for deferred-only files. Capture the first-read inclusion chain for every source.
- Pin the build's declared design to the published W03 snapshot at `a35cb50522c509cd79f57f53095f8d2481eb722d`. This is the full contract for this delivered stage: existing CLI grouping plus validated captured metadata. The new runtime codes are declared and fixtured; conformance remains bidirectional. W01's complete target contract remains in draft review #220. W04 owns grouping behavior and CLI retirement.
- Preserve the installation term *entry point* in the snapshot's CLI paragraph. The existing vocabulary check previously found it in acceptance-criterion files beside the established design.
- No deferred technical debt or arising standalone issue was found in this unit.
