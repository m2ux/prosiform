# Scoping the Clause Coverage Work

The uncovered list, grouped by what states each clause, and the disposition each group takes.

## The Measurement on This Base

`make conformance` on `i00/e11/w32-every-behavioural-clause-reached` at its base commit `8cd9534` closes:

```text
conformance report: 253 clause(s) the design states, 64 covered by no fixture,
0 declaration(s) naming no clause; 30 declared name(s) reached, 0 unfixturable,
3 installation claim(s) no run observes
```

Issue [#169](https://github.com/m2ux/prosiform/issues/169) states 253 and 66, and 57 gaps against 9 non-behavioural sections. The figure moved to 64 because W24 and W30 and the base merge each brought fixtures that named clauses nothing had named. The split within it moved too: eleven of the 64, not nine, belong to the three sections that state no behaviour a run can produce, because each of those sections' own heading is a clause beside its bullets. The behavioural remainder is 53.

## What States the Uncovered Clauses

| Group | Clauses | Disposition |
| --- | --- | --- |
| The three non-behavioural sections and their bullets | 11 | Told apart from the gaps, so they leave the uncovered list |
| Clauses the corpus already exercises without naming | 33 | Declared on the fixture that establishes each |
| Clauses no fixture in the corpus reaches | 4 | A fixture apiece |
| Clauses no source tree and one invocation can state | 16 | Recorded with the reason, in the shape an installation claim takes |

### The Non-Behavioural Sections

`Design status`, `Implementation verification and residual policy detail` and `Upstream follow-up reference` state what the project has decided, what remains to be proven after implementation is authorized, and what an upstream contribution would say. None states an outcome a run can produce, so none will ever carry a fixture, and each is listed for exactly the reason every genuine gap is listed. Eleven clauses: the three headings and the eight bullets under two of them.

### Clauses the Corpus Already Exercises

Thirty-three clauses are established by a fixture that does not name them. A bundle every fixture publishes is one Markdown document with one heading per group; a run every failing fixture performs resolves its entry references first; the two entries one delivery fixture names in reverse path order are reported in path order. The work is a declaration apiece on the manifest of the fixture that already states it, which is why the corpus's reach is understated rather than absent.

### Clauses No Fixture Reaches

Four clauses the corpus states nothing about:

- `CLI contract — --help`, the usage response naming the defaults and the exit statuses.
- `Markdown and source-heading profile — Core syntax`, the constructs the profile supports carried through one bundle.
- `Link classification and resource handling — Unsupported local-document syntax`, a raw HTML link naming a local document refused rather than silently dropped.
- `Heading-only structural ancestors — Named titles`, a title the file heading absorbed not emitted again as the structural ancestor of a selected subsection.

### Clauses No Source Tree Can State

Sixteen clauses state something other than an outcome of one run against one tree:

- **Two headings carry no rule of their own.**
  `Input and output contract` and `Resolution sequence` open straight onto the rules beneath them.
- **Six state how a build identifies and edits source spans.**
  `Parser and source-preserving edits` and its `Parsing authority`, `Source positions`, `Source model`, `Edits` and `Validation` rules bind the means. What the means must produce is stated by the invariants, which carry their own clauses and their own fixtures.
- **Three state what a project does rather than what a run does.**
  `Mandatory parser viability gates` names when its gates apply, `Explicitly linked source structure` states how sources are to be authored, and `Adversarial acceptance fixtures` instructs that a corpus be written.
- **One states a distinction inclusion does not decide.**
  `Explicitly linked source structure — Reading versus execution` holds that availability is not authorization, which no bundle's bytes can show.
- **One states an internal record.**
  `Heading-only structural ancestors — Provenance` requires ancestry be recorded apart from selected content; its effects are the depth and deduplication rules, each already reached.
- **Three bind the caller's wrapper rather than the tool.**
  `Agent delivery contract` and its `Response limit` and `Broken pipes` rules state what a transport must do with a run's output, which a fixture declaring a tree and an invocation cannot reach.

## The Shape a Recorded Reason Takes

The declared surface already lists an installation claim no run observes with the reason it is unreachable and what would make it observable. A clause no source tree can state takes that entry shape: its name, the reason, and the run that would observe it where one can be named. Nothing is maintained beside the report, so a clause that comes to be reached leaves the listing by leaving its declaration.

## The Defect the Fourth Fixture Found

The fixture carrying every construct the profile supports is the first in the corpus to run an autolink, and an autolink ends the run in an internal error. The corpus states the run the contract requires and marks the fixture as awaiting [I00:E11:W37](https://github.com/m2ux/prosiform/issues/181), which delivers it. The clause is reached by the fixture that declares it, and the build's fault is tracked where it belongs.

## Whether This Is One Pull Request

It is. The declarations are one line apiece on manifests the report itself holds true — a declaration naming no clause fails the report — and the four fixtures are small. The two component groups, the corpus and the conformance report, change disjoint files.
