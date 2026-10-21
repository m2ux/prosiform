# Analysis

## Why these three and not the other seven

The epic held ten outstanding rows. The question put to the reading was which of them genuinely impair the experience of someone invoking the tool, so that the prototype initiative could be delivered without carrying work its product does not need.

The distribution settles most of it. `src/pyproject.toml` packages `prosiform` and one glossary file. Nothing under `checks/`, nothing under `fixtures/` and nothing in the design record on the `engineering` branch is installed, so a defect in any of them is read by this repository and by a second implementor and by no user of the build.

That places W25, W26, W28, W38 and W39 outside the reading at once: each changes a repository check. W36 changes the design record. W27 is the one close case, because the build does report `E_INVALID_GROUP_RULE` where the design's clause implies the usage code — but the run refuses the rule, and the message names the defect in it, so what is wrong is the code's category and the corpus's coverage of it rather than anything the person at the command line is misled by.

The remaining three were reproduced against the base rather than read from their issues.

## Reproductions

Each was run against `313e1f2`, the base at the time of the reading, with `uv run --project src --frozen prosiform`.

### An autolink ends the run

A single-document source whose body carries `<https://example.com/profile>`:

```text
E_UNEXPECTED_INTERNAL_ERROR: unexpected internal error: Unrewritable('the parser read 1 use(s) against the 0 the emission can edit in place')
status 4
```

No bundle is produced. The construct is ordinary CommonMark and the profile names it as core syntax the build supports.

### A member is emitted nowhere

A root carrying `index.md`, which references `docs/alpha.md` and `docs/beta.md`, where `alpha.md`'s whole content is `# Alpha`.

Under `--group docs:1` the member takes a subsection and its title is carried by that subsection's heading. Under `--group docs:2` the same member is emitted nowhere at all, and the entry's reference to it is rewritten to the group:

```text
# Docs

## Overview

### Beta

Beta has a paragraph of its own.

# index

See [Alpha](#docs) and [Beta](#beta).
```

The run exits 0. A selected document is absent from the bundle and the reference naming it points at the group heading, so the arrangement decides whether content is carried rather than only where it sits.

### A newline spelling is rewritten

A source whose every line is terminated CRLF bundles to one whose every line is terminated LF, including the paragraphs no rewrite reached. The run exits 0 and carries no diagnostic about it. The design's parser clause requires untouched content to keep its original bytes and its newline spelling, and normalising line endings is not among the declared transformations.

## What the reading leaves standing

Two of the three fail silently. A user asked the tool to bundle, got exit 0, and received a bundle that had lost a document or had every line rewritten. That is the property that makes them one unit of work: not that they share a component, which they do not, but that each is a case where the run's success is not evidence that the bundle is right.
