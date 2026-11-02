# W03 Validation

The checks the [work item](w03.md) names, run against `invocation.md` at branch `i09/e02/w03-placement-stated-in-the`, commit `09dc41ee`.

## T1 Placement read against the pinned design

**Coverage:** AC5.

The pinned design is [design.md at b7e5a449](https://github.com/m2ux/prosiform/blob/b7e5a449996cf5c8b4ee24839508339ef55ded95/artifacts/planning/2026-10-17-prosiform-v1/design.md#grouping), the commit the README's profile badge names.

| Guide sentence (Conversion metadata) | Design clause | Agrees |
| --- | --- | --- |
| "a file's `group` pair places its own sections wherever a parent bundles it" | A file places its own sections: "a linked document's sections are placed by its own pair wherever a parent bundles it" | ✓ |
| "the parent's pair places the parent's sections where a further link bundles the parent in turn" | A file places its own sections: "a parent's pair places the parent's sections where a further reference bundles the parent in turn" | ✓ |
| "A named group nests inside the division of the document whose link placed its first member, and each enclosing division pushes its headings one level deeper" | Nested groups: "A named group stands inside the division holding the document whose reference placed its first member … Every heading of a nested group sits one level deeper for each division enclosing it" | ✓ |
| "a group whose first member is an entry stands at the top level" | Nested groups: "a group whose first member is an entry stands at the top level of the bundle" | ✓ |
| "A heading pushed past H6 fails the run with `E_HEADING_DEPTH_OVERFLOW`" | Nested groups: "a heading pushed beyond H6 fails as Depth overflow states"; Depth overflow: "Fail with `E_HEADING_DEPTH_OVERFLOW`" | ✓ |

The build agrees: the grouping fixtures `a-file-places-its-own-sections`, `an-intermediate-group-nests-inside-its-parent` and `a-nested-group-pushing-a-heading-past-the-sixth-fails` pass in `make corpus` (T2). The remedy — link the shared library from a shallower division or keep its headings shallow — is guidance, not a contract clause, and follows from the refusal the user chose on 2026-11-02.

**Result:** ✓

## T2 make check

**Coverage:** AC5.

`PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i09/e02/w03-placement-stated-in-the/src --frozen pf' make check` at `09dc41ee` exited 0. Within it:

- `make links` resolved every reference in 237 documents, the pinned design's `#grouping` anchor among them.
- `make invocation` matched every documented option, exit status and required statement against the build's help output.
- `make vocabulary`, `make conformance`, `make independence`, `make corpus` (427 fixtures) and the mock scenarios passed.

**Result:** ✓
