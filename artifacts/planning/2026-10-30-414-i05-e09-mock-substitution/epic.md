## Overview

A link in a Markdown source names one document, and `pf` compiles whichever document sits at that path. This epic adds an invocation parameter that names a different document for one authored path, so a bundle can be built and exercised against stand-in material without editing the tree under test. The substitution is applied where resolution happens, so discovery, emission and validation read one answer.

## Problem

A caller who needs a bundle built against other material than the tree holds has no way to say so.

- **The only lever is editing the tree.**
  A test that needs a stand-in dependency copies the skill and edits the copy, so what it measures is a modified tree rather than the one that ships. The eleven resolution call sites across [candidate.py](https://github.com/m2ux/prosiform/blob/9851615028ea489c48f6b3fa5ddbe0d917438cf2/src/prosiform/candidate.py), [bundle.py](https://github.com/m2ux/prosiform/blob/9851615028ea489c48f6b3fa5ddbe0d917438cf2/src/prosiform/bundle.py) and [cli.py](https://github.com/m2ux/prosiform/blob/9851615028ea489c48f6b3fa5ddbe0d917438cf2/src/prosiform/cli.py) each read the path from disk, and the invocation states nothing that a different document is meant.
- **A stand-in cannot be kept beside the work.**
  Test material that must not ship has nowhere to live, because every document the run reaches is one the shipped tree holds, and the closure follows links rather than a list a caller supplies.
- **The gap is invisible in the run.**
  A bundle of stand-in material and a bundle of real material are the same kind of output, and nothing in a run's diagnostics says which documents it carried.

## Proposal

- **Substitution at the resolution seam.**
  `closure.inside` is the one function every stage reaches resolution through, and the mapping is a parameter beside the `root` each call site already passes. No stage carries a rule of its own, so discovery, emission, candidate validation, the withheld-target check and entry normalization cannot disagree.
- **Redirect, not overlay.**
  The substitute becomes the target outright. Its title, its `group` and `group-depth`, its `root` and its own links are the ones the run uses, and the bundle reads as if the author had written the substitute's path in the link. One file owns each identity.
- **A repeatable option.**
  `-m ORIGINAL=ALTERNATIVE` is given once per substitution. Both sides are working-directory-relative references read by the existing reference grammar, so percent decoding, `..` normalization and the Markdown-suffix requirement are unchanged.
- **Neither side is bounded by the writing source's root.**
  A mapping entry is an invocation parameter rather than authored content, so it resolves from the invocation working directory the way a positional entry does. A fixture tree outside the root of the skill it exercises is the case the feature exists for.
- **Matched on normalized identity.**
  A key is the identity a link normalizes to, so `./rules.md` and `rules.md` name one key. A key carrying a fragment redirects that section alone, and a key without one covers the whole document and every fragment of it.
- **Every reference is redirected.**
  Positional entries, `-f`, and compiled, deferred, dispatched and run-set targets alike. A deferred destination in a mocked bundle names the substitute, because a later run follows the path the bundle published.
- **A redirected entry names its own output.**
  The derived filename follows the substitute, because the redirect is total.
- **Substitution is visible.**
  A warning per redirected target names the link's location, the identity it would have resolved to and the substitute. A key that matched nothing warns too, because a fixture that mocks nothing looks like a fixture that mocks something.
- **No chaining.**
  A substitute is material rather than another indirection. Its own links are matched against the mapping like any other document's, and a substitute that is also a key is not followed again.
- **A self-mock is refused.**
  A key whose sides normalize to one identity states nothing and reads as a substitution that took effect.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W01 | The resolution seam and its identity | AC1, AC5, AC6 | | | |
| W02 | Option grammar and its refusals | AC9, AC10 | W01 | | |
| W03 | Redirected entry derives its own name | AC2 | W02 | W04 | |
| W04 | Substitution warnings on the run | AC7, AC8 | W02 | W03 | |
| W05 | Withheld and dispatched targets redirected | AC4 | W02 | W06 | |
| W06 | Keys scoped to one section | AC3 | W03 | W05 | |
| W07 | Bundling rules state the substitution | AC11 | W04, W05, W06 | | |

## Acceptance Criteria

- [ ] **AC1.** A link under the root naming a mocked identity compiles the substitute's document in place of the target, as the corpus fixture `fixtures/mock/a-mocked-dependency-is-compiled` shows.
- [ ] **AC2.** A positional entry naming a mocked identity compiles the substitute document, and the output filename derived for that run names the substitute, as the corpus fixture `fixtures/mock/a-redirected-entry-derives-its-name-from-the-substitute` shows.
- [ ] **AC3.** A mapping key carrying a fragment redirects that section alone and leaves the rest of the document real, as the corpus fixture `fixtures/mock/a-fragment-key-redirects-one-section` shows.
- [ ] **AC4.** A withheld link's target is redirected, and the destination the bundle publishes for it is the substitute's working-directory-relative path, as the corpus fixture `fixtures/mock/a-deferred-target-is-redirected` shows.
- [ ] **AC5.** A substitute declaring a group and depth contributes to that merged group, as the corpus fixture `fixtures/mock/a-substitute-declaring-a-group-joins-it` shows.
- [ ] **AC6.** A substitute declaring a root bounds its own outgoing links by that root, as the corpus fixture `fixtures/mock/a-substitute-root-bounds-its-own-links` shows.
- [ ] **AC7.** A redirected target raises `W_MOCK_SUBSTITUTED` naming the link's location, the identity it resolved from and the substitute, as the corpus fixture `fixtures/mock/a-substitution-warns-with-its-target` shows.
- [ ] **AC8.** A mapping key that matched no reference raises `W_MOCK_UNUSED` and the run publishes its bundle with exit status 0, as the corpus fixture `fixtures/mock/an-unused-key-warns-and-publishes` shows.
- [ ] **AC9.** A mapping whose keys normalize to one identity, or whose key and value normalize to one identity, fails with `E_INVALID_USAGE` and exit status 2, as the corpus fixtures `fixtures/mock/a-duplicate-key-is-refused` and `fixtures/mock/a-self-mock-is-refused` show.
- [ ] **AC10.** The option, its effect and its default appear in `invocation.md` and agree with the command's own `-h` output, as `make invocation` shows.
- [ ] **AC11.** The bundling rules state that a mapping entry redirects each reference naming its key, and state which references are redirected, as an inspection of `invocation.md` and the design shows.

## Open Questions

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) — the design decisions and the independent row pairs.
