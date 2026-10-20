# Validation Record — I00:E04:W04

> Measured 2026-10-20 against `i00/e04/main` at `626b00a` and the delivery branch above it.

## The Behaviour Measured Before the Design Was Built To It

Each run below used the delivery build against a scratch tree, before any change to the repository.

**Consolidation and re-traversal.** A tree of `guide.md` (sections `Alpha` and `Beta`, each marking a dependency), `detail.md` marking `guide.md` whole, and `extra.md` marked only from `Beta`:

```
prosiform --root source 'guide.md#alpha'
```

The bundle carried `detail`, `extra` and `guide` — the whole of `guide.md` once, and `extra.md`, which only the part the entry did not select had marked. Consolidation and the re-traversal of the widened region both hold on the base.

**Determinism.** The same tree with three entry references given in two orders:

```
prosiform --root source 'guide.md#beta' 'extra.md' 'guide.md#alpha' > a.out
prosiform --root source 'guide.md#alpha' 'guide.md#beta' 'extra.md' > b.out
cmp a.out b.out
```

`cmp` reported no difference. The entry line named `extra`, `Alpha` and `Beta` in bundle order under both.

**The data-loss defect.** `guide.md` marking `detail.md`, which marks `guide.md`, with `extra.md` marked from `Beta`:

```
prosiform --root source --output source/extra.md 'guide.md'
```

Exited 0, and `source/extra.md` afterwards held the bundle. The source the run had read as a dependency was gone. Reproduced, then fixed; the same run now exits 2 with `E_INVALID_USAGE` and leaves the file as it was.

**The resolution the output check performed.** `source/alias.md` a symbolic link to `real.md` beside the source tree:

```
prosiform --root source --diagnostics json --output real.md 'alias.md'
```

Exited 2 with `E_INVALID_USAGE`: the `.resolve()` in `sources()` had crossed the link and claimed `real.md` as an input source, although the run would never read it. It now exits 1 with `E_SOURCE_SYMLINK`, the policy the reference meets first.

**Structural ancestors.** `grep -ril ancestor src/ checks/ fixtures/` returned nothing. Selecting a subsection alone emitted its own heading and body and no ancestor heading, so no run on this base produces a section present only as a heading-only ancestor.

**Ancestor promotion, the half that holds.** A document whose subsection marks a second document, which marks the first document's section:

```
prosiform --root source 'guide.md#detail' 'guide.md#gamma'
```

The named section arrived with its heading and body, subsuming the subsection that had been selected alone. The run differed from the criterion's expected bundle by exactly one line: the heading-only ancestor of the subsection no reference named.

## The Instrument Behind Each Criterion

| Criterion | Instrument | Verdict |
| --- | --- | --- |
| AC3 | `consolidation/a-child-then-its-whole-document`, `consolidation/a-subsection-and-its-section` | Met |
| AC9 | `determinism/entry-references-in-source-order`, `determinism/entry-references-in-another-order`, `determinism/groups-in-root-relative-path-order` | Met |
| AC10 | `ancestor-promotion/a-link-to-a-heading-only-ancestor`, `awaiting = "I00:E09:W02"` | Not met; the state the criterion turns on cannot arise on this base |

The two determinism fixtures declare one expected bundle between them: the files are byte-identical, which is the criterion stated as an artifact rather than as a comparison a runner performs.

## What Each Command Returned

```
PROSIFORM_BUILD="uv run --project .../src --frozen prosiform" make check
```

| Target | Output |
| --- | --- |
| `lock-check` | `Resolved 22 packages in 0.84ms` |
| `lint` | `All checks passed!` |
| `format-check` | `30 files already formatted` |
| `typecheck` | `Success: no issues found in 29 source files` |
| `test` | `362 passed in 0.18s` |
| `harness` | `239 passed in 0.49s` |
| `corpus` | `corpus check: 104 fixture(s), 101 pass, 0 fail, 3 awaited, 0 unexpected pass` |
| `layout` | `layout check: 3 tree(s) present` |
| `tables` | `table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table` |
| `links` | `link check: every reference in 6 document(s) resolved` |
| `vocabulary` | `vocabulary check: 34 contract term(s) marked ... every one defined in docs/glossary.md` |

The base held 96 fixtures, 94 passing and 2 awaited. The row adds eight fixtures and one marker.

## A Note on the Cache

`.ruff_cache` was removed before `make lint` was trusted, as the brief requires after a structural change. No file was moved or renamed, so the cache's premise held either way, and the lint result is the same with and without it.
