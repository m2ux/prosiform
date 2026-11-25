# F38 Bundle Identifiers

Preset-qualified bundle names use a 12-character SHA-256 prefix. Canonical selection matching and collision refusal govern every entry folder, dispatched filename and rewritten link.

## Retrospective Scope

The implementation and observing checks precede tracker registration. Target: main. Base 684437c06; candidate e6816a23a957d247301dc33b260313f533ab9bfc. The candidate is an unreleased change to the pf 0.34.0 build.

## Evidence

| Artifact | Contents |
| --- | --- |
| [Issue](issue.md) | F38 defect, design and criteria |
| [Tests](test-results.md) | Source-bound verification and limits |
| [Source tests](source-tests.log) | Passing complete source suite |
| [Source-test count](source-test-count.log) | 2,324 collected cases |
| [Corpus](corpus.log) | 708 fixtures, all passing |
| [Collision tests](collision-tests.log) | 10 final publication cases, including a forced truncated-prefix collision |
| [Types](types.log) | 87 source files without type findings |
| [Pull request](pull-request.md) | Draft publication body |

- [F38 #848](https://github.com/m2ux/prosiform/issues/848)
- [Candidate](https://github.com/m2ux/prosiform/commit/e6816a23a957d247301dc33b260313f533ab9bfc)
