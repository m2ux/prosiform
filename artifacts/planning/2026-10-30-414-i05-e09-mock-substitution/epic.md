## Overview

A link in a Markdown source names one document, and `pf` compiles whichever document sits at that path. This epic adds an invocation parameter that names a different document for one authored path, so a bundle can be built and exercised against stand-in material without editing the tree under test. The substitution is applied where resolution happens, so discovery, emission and validation read one answer.

## Problem

A caller who needs a bundle built against other material than the tree holds has no way to say so.

- **The only lever is editing the tree.**
  A test that needs a stand-in dependency copies the skill and edits the copy, so what it measures is a modified tree rather than the one that ships. Resolution is reached through `inside`, `resolvable`, `bundled` and `withholding_target` in [closure.py](https://github.com/m2ux/prosiform/blob/9851615028ea489c48f6b3fa5ddbe0d917438cf2/src/prosiform/closure.py), each call site in `cli.py`, `bundle.py` and `candidate.py` opens the authored path, and `entry` normalizes the command line's own references through `resolve` before any source is read.
- **A stand-in cannot be kept beside the work.**
  Test material that must not ship has nowhere to live, because every document the run reaches is one the shipped tree holds, and the closure follows links rather than a list a caller supplies.
- **A source's declared root excludes the stand-in.**
  A source's `prosiform.root` bounds every link it writes, so a fixture tree beside the skill rather than inside it is unreachable by the very document it would stand in for.
- **The gap is invisible in the run.**
  A bundle of stand-in material and a bundle of real material are the same kind of output, and nothing in a run's diagnostics says which documents it carried.

## Proposal

- **Substitution at a resolution seam.**
  `closure.inside` is where a link's own path is resolved, and the mapping is a parameter beside the `root` each call site already passes. Discovery, emission, the withheld-target check and candidate validation all reach `inside` through `resolvable`, `bundled` and `withholding_target`, so none carries a rule of its own. A positional reference and `-f` are normalized by `entry` before any source is read, and the mapping is applied there too, so the two paths agree.
- **Redirect, not overlay.**
  The substitute becomes the target outright. Its title, its `group` and `group-depth`, its `root` and its own links are the ones the run uses, and the bundle reads as if the author had written the substitute's path in the link. One file owns each identity.
- **A repeatable option.**
  `-m ORIGINAL=ALTERNATIVE` is given once per substitution. Both sides are working-directory-relative references read by the existing reference grammar, so percent decoding, `..` normalization and the Markdown-suffix requirement are unchanged.
- **Neither side is bounded by the writing source's root.**
  A mapping entry is an invocation parameter rather than authored content, so it resolves from the invocation working directory the way a positional entry does. A fixture tree outside the root of the skill it exercises is the case the feature exists for.
- **Matched on normalized identity.**
  A key is the identity a link normalizes to, so `./rules.md` and `rules.md` name one key. A key carrying a fragment redirects that section alone and beats a key naming the whole document, and a key without one covers the document and every fragment of it.
- **Every reference is redirected.**
  Positional entries, `-f`, and compiled, deferred, dispatched and parallel-dispatched targets alike, a reference its author's root admits and one it carries as a citation. A deferred destination in a mocked bundle names the substitute, because a later run follows the path the bundle published.
- **A redirected entry names its own output.**
  The derived filename follows the substitute, because the redirect is total.
- **Substitution is visible.**
  A warning per redirected target names the link's location, the identity it would have resolved to and the substitute. A key that matched nothing warns too, because a fixture that mocks nothing looks like a fixture that mocks something.
- **No chaining.**
  A substitute is material rather than another indirection. Its own links are matched against the mapping like any other document's, and a substitute that is also a key is not followed again.
- **A self-mock is refused.**
  A key whose sides normalize to one identity states nothing and reads as a substitution that took effect.
- **Proven end to end.**
  Every behaviour a fixture can observe lands as a corpus fixture in the same pull request as the code that makes it pass, so a fixture is written against working behaviour rather than against a prediction. The fixture names the design clause it encodes, so the design clause and its pin land ahead of the first one.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, invocation rules and pin | AC16, AC17 | | | |
| W01 | Mapping, option and identity | AC1, AC11, AC18 | W00 | | |
| W02 | Key and self-mock refusals | AC9, AC10, AC23 | W01 | | |
| W03 | Entry redirect and derived name | AC2, AC13 | W01 | | |
| W04 | Substitution warnings and check mode | AC7, AC8, AC19 | W01 | | |
| W05 | Withheld and dispatched targets | AC4 | W01 | | |
| W06 | Section keys and no chaining | AC3, AC12, AC14 | W01 | | |
| W07 | Substitute as a full source | AC5, AC6, AC20 | W01 | | |
| W08 | Example skill scenarios over the mechanism | AC21, AC22 | W04 | | |
| W09 | Documented option row | AC15 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** A link under the root naming a mocked identity compiles the substitute's document in place of the target, as the corpus fixture `fixtures/mock/a-mocked-dependency-is-compiled` shows.
- [ ] **AC2.** A positional entry naming a mocked identity compiles the substitute document and the run derives its output filename from the substitute, as the corpus fixture `fixtures/mock/a-redirected-entry-derives-its-name-from-the-substitute` shows.
- [ ] **AC3.** A mapping key carrying a fragment redirects that section alone and leaves the rest of its document real, as the corpus fixture `fixtures/mock/a-fragment-key-redirects-one-section` shows.
- [ ] **AC4.** A withheld link's target is redirected, and the destination the bundle publishes for it is the substitute's working-directory-relative path, as the corpus fixture `fixtures/mock/a-deferred-target-is-redirected` shows.
- [ ] **AC5.** A substitute declaring a group and depth contributes to that merged group, as the corpus fixture `fixtures/mock/a-substitute-declaring-a-group-joins-it` shows.
- [ ] **AC6.** A substitute declaring a root bounds its own outgoing links by that root, as the corpus fixture `fixtures/mock/a-substitute-root-bounds-its-own-links` shows.
- [ ] **AC7.** A redirected target raises `W_MOCK_SUBSTITUTED` naming the link's location, the identity it resolved from and the substitute, as the corpus fixture `fixtures/mock/a-substitution-warns-with-its-target` shows.
- [ ] **AC8.** A mapping key that matched no reference raises `W_MOCK_UNUSED` and the run publishes its bundle with exit status 0, as the corpus fixture `fixtures/mock/an-unused-key-warns-and-publishes` shows.
- [ ] **AC9.** Mapping keys normalizing to one identity are refused as invalid usage, as the corpus fixture `fixtures/mock/a-duplicate-key-is-refused` shows.
- [ ] **AC10.** A key and value normalizing to one identity are refused as invalid usage, as the corpus fixture `fixtures/mock/a-self-mock-is-refused` shows.
- [ ] **AC11.** A mocked identity is reachable from a source whose declared root excludes the substitute's path, as the corpus fixture `fixtures/mock/a-substitute-outside-the-writing-root-is-reachable` shows.
- [ ] **AC12.** A substitute whose own path is a mapping key compiles from disk rather than being redirected again, as the corpus fixture `fixtures/mock/a-substitute-that-is-a-key-is-not-redirected-again` shows.
- [ ] **AC13.** A referrer `-f` names is redirected, and the fragment-only entry resolves against the substitute, as the corpus fixture `fixtures/mock/a-redirected-referrer-carries-its-entry` shows.
- [ ] **AC14.** A key naming a whole document and a key naming one of its sections both serve their references, the narrower one taking precedence, as the corpus fixture `fixtures/mock/a-document-key-and-a-section-key-together` shows.
- [ ] **AC15.** The option, its effect and its accepted form appear in `invocation.md` and agree with the command's own help output, as `make invocation` shows.
- [ ] **AC16.** The bundling rules state that a mapping entry redirects each reference naming its key, and state which references are redirected, as an inspection of `invocation.md` shows.
- [ ] **AC17.** The design states the mapping as a thing deciding what a reference names, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.

- [ ] **AC18.** A mapping key naming a document that does not exist compiles its substitute and publishes, where the same run without the mapping fails with `E_TARGET_NOT_FOUND`, as the corpus fixture `fixtures/mock/a-key-naming-an-absent-document-is-substituted` shows.
- [ ] **AC19.** A mapping applies under `-c`, which publishes nothing and reports the substitution warning, as the corpus fixture `fixtures/mock/a-mocked-check-publishes-nothing` shows.
- [ ] **AC20.** A mapping value carrying a parent segment reads the substitute above the working directory, as the corpus fixture `fixtures/mock/a-substitute-outside-the-writing-root-is-reachable` shows.
- [ ] **AC21.** The example skill's plan mode bundles against a stub artifact supplied by a mapping and no edit to the skill tree, with the stub standing where the real artifact's heading stood, as `make mock-scenarios` shows.
- [ ] **AC22.** The example skill's `conventions.md` is redirected to a document naming a fake `gh`, and the bundle carries the fake as the command the agent is told to run, as `make mock-scenarios` shows.
- [ ] **AC23.** A mapping key carrying no document, as `#section` does, is refused as invalid usage, as the corpus fixture `fixtures/mock/a-fragment-only-key-is-refused` shows.

## Open Questions

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) — the design decisions, the fixture inventory and the independent row pairs.
