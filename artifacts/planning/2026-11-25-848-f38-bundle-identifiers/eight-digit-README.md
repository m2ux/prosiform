# F38 Bundle Identifiers

Preset-qualified bundle names use a 8-character SHA-256 prefix. Canonical selection matching and collision refusal govern every entry folder, dispatched filename and rewritten link.

## Retrospective Scope

The implementation and observing checks precede tracker registration. Target: main. Base 684437c06; candidate f41769e7cd7e763ad5182efc835b0e4d64cddaac. The candidate is an unreleased change to the pf 0.34.0 build.

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
- [Candidate](https://github.com/m2ux/prosiform/commit/f41769e7cd7e763ad5182efc835b0e4d64cddaac)

## Eight-Character Revision

The operator requests a shorter qualifier after the initial twelve-character candidate. [Source tests](eight-digit-source-tests.log), [708-fixture corpus](eight-digit-corpus.log), [focused preset/publication cases](eight-digit-preset-tests.log) and [types](eight-digit-types.log) verify the eight-character candidate. Earlier twelve-character checks remain retained at their original revision.

[Draft PR #849](https://github.com/m2ux/prosiform/pull/849) remains open; its Development relation is verified from both ends and board18 reads In Progress.
