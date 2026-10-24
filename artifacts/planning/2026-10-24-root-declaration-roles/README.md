# The `root` Declaration: Three Roles, One of Them Questionable

> Note · Created 2026-10-24

## What This Records

A question asked while restoring `main`: whether the `prosiform.root` declaration is needed at all. It is, but for one of the three roles it plays, and the third is the one that keeps causing wrong documents. This note separates the roles with runs against the build, so the decision about the third can be taken separately from the other two.

## The Three Roles

The declaration is read in three places, and they answer different questions.

| Role | What it decides | Verdict |
| --- | --- | --- |
| Output identity | The derived filename, the group's heading text, and the group order | Needed |
| Containment | Which paths a document may name at all | Needed |
| Link spelling | Which spelling of a path finds a document | Questionable |

## Evidence

Two sources in one directory, differing only in the declared root. Each run publishes from `rules/`.

```text
rules/a.md declares root: "."
rules/a.md declares root: ".."
```

| Declared root | Derived filename | First heading |
| --- | --- | --- |
| `"."` | `a.bundle.md` | `# A` |
| `".."` | `rules_a.bundle.md` | `# Rules` |

Neither publishes a relative path for a link. Every compiled link is a bare `#slug` inside the bundle, so there is no relative root *in the output* for a link to be relative to. The relative path appears in exactly one place: the destination the build writes when a run is asked for a derived output file.

The second and third roles are visible in what a link finds. Under `root: ".."`, with `rules/codex.md` present:

| Link written in `rules/a.md` | Outcome |
| --- | --- |
| `[Codex](rules/codex.md)` | resolves |
| `[Codex](codex.md)` | fails with `E_TARGET_NOT_FOUND` |

So a link inside `rules/` is spelled as if written from the parent, not as the file's own reader sees it.

## Why the Third Role Is the Questionable One

The build already resolves a link carrying a parent segment from the file that writes it. That is the ordinary understanding of a relative link, and it is what makes containment enforceable without also dictating spelling:

```text
[Target](../artifacts/epic.md)   resolves from modes/
[Target](../../secret.md)        refused: above the declared root
```

With that in place, a root's path job is to bound the result, not to prefix it. A declaration that still prefixes a link without a parent segment leaves two spellings for one document in the same directory, and the wrong one fails at compile time rather than at review.

## How It Arose

Two commits on `main` attempted to "simplify" the worked examples from `rules/codex.md` to `codex.md`, and both were wrong:

- `3d549a2` — `common.md`, `rules/agents.md` → `agents.md`
- `a7862b5` — `agents.md`, `rules/codex.md` → `codex.md`

The build rejects each of those links. Neither was noticed because `corpus` failed first and `make check` stops at the first failing target, so `links` never ran. The mistake is a reasonable one to make by hand: the spelling looks like an ordinary relative link.

## What Is Not Recorded Here

No change is proposed. Removing the third role would touch 40 declarations, 253 fixtures and the invocation contract, which is a larger change than the one that surfaced the question, and it needs a decision about whether a link without a parent segment should resolve from the file or from the root. The two roles that are needed are unaffected either way.

The immediate consequence of the question is already in [PR #244](https://github.com/m2ux/prosiform/pull/244): `checks/links.py` now resolves a parent-segment link from its file, as the build does, so the link check no longer reports a document the build accepts as broken.
