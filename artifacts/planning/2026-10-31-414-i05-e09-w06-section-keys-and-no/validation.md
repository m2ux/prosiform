# Validation — W06 Section Keys and No Chaining

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w06-section-keys-and-no` on branch `i05/e09/w06-section-keys-and-no`, at branch head `444fe9ab` unless a section names another revision. The build under test was named by `PROSIFORM_BUILD` as `env PYTHONPATH=<worktree>/src <venv>/pf`, the same form the continuous-integration job supplies.

The worktree's own `src/.venv` holds no installed package, so the interpreter and the installed tools came from the sibling worktree `.worktrees/i05/e09/w02-key-and-self-mock/src/.venv`, with `PYTHONPATH` naming this worktree's `src`. The build is therefore this branch's `prosiform` package run by a locked environment of the same revision. `make lock-check` needs network and did not run here; no dependency file changed on this branch.

The design pin is `827b66fcd837ec6a9e203a82a1c86fc5ec2b60bb`, which `README.md` names. Every fixture declares `Link classification and resource handling — The substitution mapping`.

## T1 — The three fixtures pass against the build

**Ran:** `make corpus`'s target, `checks/corpus.py`, at branch head `444fe9ab`.

**Observed:** exit `0`, `361 fixture(s), 361 pass, 0 fail, 0 awaited, 0 unexpected pass`. The count rose from 358, which is the three this row lands:

```text
mock/a-document-key-and-a-section-key-together: pass
mock/a-fragment-key-redirects-one-section: pass
mock/a-substitute-that-is-a-key-is-not-redirected-again: pass
```

AC3, AC12 and AC14 each have the fixture the epic names, and each fixture was rendered from a run against the pinned build before its expected bundle was written, rather than written against a prediction.

## T2 — A section key redirects one section and leaves the rest real

**Ran:** the fixture `a-fragment-key-redirects-one-section`, and manually `pf -d json -m rules.md#escalation=stand-in.md guide.md` over the same tree.

**Observed:** exit `0`, one bundle, one `W_MOCK_SUBSTITUTED`:

```text
{"severity": "warning", "message": "the reference 'rules.md#escalation' is redirected to the substitute 'stand-in.md#escalation', where it would have resolved to 'rules.md#escalation'", "code": "W_MOCK_SUBSTITUTED", "resolved": "stand-in.md#escalation", "source": "rules.md#escalation", "location": {"file": "guide.md", "line": 5, "column": 1}}
```

The bundle carries `# Rules` with its `## Escalation`, from the real document, and `# Stand-in` with its `### Escalation`, from the substitute. The whole-document link is rewritten to `#rules` and the escalation link to `#escalation-1`, the ordinal the substitute's own heading took. That pair is what makes AC3 a statement about the key rather than about the tree: the same run without `-m` bundles `rules.md` twice under one heading and warns `W_COINCIDENT_HEADING`.

**The one warning and not two** is the lookup working as W01 stated it: the key is `("rules.md", "escalation")`, so the whole-document reference names no key and is unredirected.

## T3 — Both keys of one document serve their references

**Ran:** the fixture `a-document-key-and-a-section-key-together`, and the same invocation manually.

**Observed:** exit `0`, two `W_MOCK_SUBSTITUTED`, one per key, in the order the two links are written:

```text
"the reference 'rules.md' is redirected to the substitute 'rules-copy.md' ..."
"the reference 'rules.md#escalation' is redirected to the substitute 'escalation-copy.md#escalation' ..."
```

The bundle carries `# Rules Copy` and `# Escalation Copy`, and neither `rules.md` nor its `## Escalation` appears. This is AC14, and it is the fixture that decides the lookup's order. Asking the document-wide key first would give the escalation link `rules-copy.md#escalation` and bundle `escalation-copy.md` for nothing, so the fixture fails on a lookup that asks them the other way round.

**Stashing the row's test additions does not change this fixture's result**, because the mechanism is W01's. What the fixture adds is the observation, not the code.

## T4 — A substitute that is a key is read from disk

**Ran:** the fixture `a-substitute-that-is-a-key-is-not-redirected-again`, and the same invocation manually.

**Observed:** exit `0`, one `W_MOCK_SUBSTITUTED` for `a.md`, and one `W_MOCK_UNUSED` naming `b.md`:

```text
{"severity": "warning", "message": "the mapping key 'b.md' names no reference the run resolved, so it substitutes nothing", "code": "W_MOCK_UNUSED", "source": "b.md", ...}
```

The bundle carries `# B`. `c.md` is not opened, and no bundle or group names it. That is AC12 in both halves: the substitute is material, and the key naming it is reported unused rather than followed.

**The same tree with both links written** — `guide.md` linking `a.md` and `b.md` — gives `# B` and `# C`, each from its own link, and two `W_MOCK_SUBSTITUTED`. So the `b.md` key is unused because nothing linked it, not because its substitution was suppressed. The mapping is consulted once per reference, which is the rule the fixture pins.

## T5 — The unit cases state the section's precedence and the substitute's section

**Ran:** `src/tests/test_mock.py`, 45 cases at `444fe9ab`, of which 5 are new.

**Observed:** pass. The cases that decide this row:

- `test_a_section_key_serves_no_other_section_of_its_document` — a section key redirects the section it names and leaves the document's other sections real, and is then unserved.
- `test_a_section_keys_substitute_section_is_the_one_the_run_reads` — a substitute carrying `#advised` is the section `rules.md#escalation` compiles, because the redirect replaces the reference rather than only its path.
- `test_a_section_key_leaves_the_rest_of_its_document_real` — end to end: the bundle carries the real `# Rules` and its body, and the substitute's `## Escalation`.
- `test_a_document_key_and_a_section_key_of_it_both_serve_their_references` — both substitutes bundled, neither real document.
- `test_a_substitute_that_is_also_a_key_is_read_from_disk` — the warning pair and the bundle, in one run.

The then-existing cases this row relies on rather than adds are `test_a_fragment_key_takes_the_section_it_names` and `test_a_document_key_covers_every_fragment_of_its_document`, which W01 landed.

## T6 — The remaining lookups the row reasoned about

**Ran:** manual runs against the pinned build, over trees built for each case.

**Observed:**

- **A substitute carrying a section** — `-m rules.md#escalation=stand-in.md#advised` compiles `stand-in.md`'s `## Advised`, and the link is rewritten to `#advised`. The substitute's section is the whole, as the design states.
- **A substitute lacking the section its key names** — `-m rules.md#escalation=stand-in.md` where `stand-in.md` has no `## Escalation` exits `1` with `E_TARGET_NOT_FOUND`, `resolved` naming `stand-in.md` and the chain `["guide.md", "stand-in.md#escalation"]`. The section the reference named is read against the substitute's document, and its absence is a defect rather than a silent whole-document read.
- **A fragment-only link inside a redirected document** — `stand-in.md` linking `#escalation` resolves against `stand-in.md` and is not redirected, which is the substitute's document resolving its own section.
- **A key naming a section of the substitute's own path** — `-m rules.md#escalation=stand-in.md#escalation -m stand-in.md#escalation=other.md#escalation` compiles `stand-in.md#escalation` and reports the second key unused. The single-application rule holds at the section level as well as at the document level.
- **A whole-document link under a section key only** — `-m rules.md#escalation=stand-in.md` with a link to `rules.md` bundles the real document and reports the key unused when no section link exists.

## T7 — Every target of `make check`, run by its own command

**Ran:** each target of `make check`, in the Makefile's order, by the command the Makefile names, substituting the sibling worktree's venv binaries for `uv run --project src --frozen`, which needs network to resolve the environment. `PYTHONPATH` named this worktree's `src`, so the build under test was this branch's.

**Observed:** exit `0` throughout, except where a note says otherwise.

- `lock-check` — **not run.** `uv lock --check` resolves the environment, and the sandbox has no network. No dependency file changed on this branch.
- `lint` — `All checks passed`. `format-check` — `72 files already formatted`. `typecheck` — `Success: no issues found in 70 source files`.
- `test` — `1355 passed in 42.67s`, up from the 1342 W01 recorded, the difference being this row's five cases and W02's and W04's landed on the epic base.
- `harness` — `985 passed in 31.21s`.
- `authoring` — `0 finding(s)` over `59 document(s)`.
- `corpus` — `361 fixture(s), 361 pass`.
- `smoke` — the installed command is named on the path, independent of the working directory and of this repository.
- `layout` — `4 tree(s) present`. `tables` — `21 command(s) and 8 declaration(s)`.
- `links --online` — `every reference in 212 document(s) resolved`.
- `vocabulary` — `46 contract term(s) ... on 827b66fcd837ec6a9e203a82a1c86fc5ec2b60bb`, every one defined in `docs/glossary.md`.
- `invocation` — `30 statement(s)`, each held to the build.
- `conformance` — `305 clause(s)`, `55 covered by no fixture`, `0 declaration(s) naming no clause`, `0 declared code(s) the build reports nowhere`, `0 reported code(s) the contract declares nowhere`.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — every procedure in `59 document(s)` under `example/work-planner/` writes its steps as sub-sections.

## T8 — What this row changed, and what it did not

**Ran:** a read of the branch diff against `8734a799`.

**Observed:** the diff is three fixture directories and `src/tests/test_mock.py`. `src/prosiform/closure.py` is untouched.

That is the row's scope as the epic's review settled it: W01 owns the exact-then-bare lookup and AC14's mechanism, and W06 owns what a section key means and the fixtures that make the precedence observable. Writing a second lookup here would have given one rule two implementations. The one code-adjacent question the row answered is whether anything else needed to change for a section key to work, and the manual runs in T2, T3, T4 and T6 show it did not: `Substitution.key` asks `(path, fragment)` then `(path, None)`, `substitute` takes the substitute's fragment where the key carries one and keeps the reference's where it does not, `served_key` marks the exact key served, and `inside` consults `key` on the authored identity. Each of those was already stated and tested by W01.

## T9 — Delivery

**Ran:** `gh api` against the pull request, `i05/e09/main` and #414.

**Observed:** recorded in the change list and the pull request. The base is `i05/e09/main`, never `main`.
