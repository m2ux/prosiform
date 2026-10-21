# Reading a declaration against the words it is entitled to use

How the independence check tells a word that names something from a word any sentence needs, what it does with inflections, plurals, hyphenation and proper nouns in a path, and what the rule reports over the corpus as it stands.

## The question

A positive rule reports the words a claim states that the contract does not. Its risk is the opposite of the inventory's: an inventory lets through what it fails to name, and a vocabulary reports what it fails to admit. Ordinary English is most of a fixture description, so a rule that cannot tell `panic` from `beside` reports half the corpus.

Three readings of "a word that names something" were measured against the corpus.

- **A word's form.** A name carries a mark prose does not — a dotted suffix, a path separator, an underscore, camel case, an option's leading dashes. It catches `bundle.rs`, `__main__`, `ValueError` and an invented flag, and misses every lower-case term the inventory held: `module`, `package`, `wheel`, `panic`, `traceback`. Form alone bounds nothing.
- **A word's membership of English.** A general word list admits `module`, `package`, `wheel`, `panic`, `crate`, `cargo` and `maven`, each an ordinary English word, so the terms most likely to arrive are the ones it lets through. A dictionary is the wrong source for this distinction.
- **A word's presence in the contract.** The design is 11,480 words of the contract's own prose, the glossary defines 43 terms, and the manifest schema and the documented invocation declare 50 interface names. None of them states `module`, `package`, `wheel`, `panic` or `traceback`, and all of them state the English a clause is written in. This is the reading the check takes.

## The rule

A claim states a word; the word is admitted when one of the sources below states it, and reported otherwise.

| Source | What it contributes |
| --- | --- |
| The design's prose | Every word the design writes in lower case, its code spans and link destinations apart. |
| The design's clause names | Every word of every clause the design states, whatever its case, so a manifest quoting `Adversarial acceptance fixtures` quotes the design. |
| `docs/glossary.md` | Every word of every term the glossary defines. |
| The contract's declared names | The error codes, the warning codes, the severities, the exit statuses and the documented options, each read as its words. |
| `docs/corpus-vocabulary.md` | The words the corpus's own declarations and the report's entries add: the English a sentence is written in, the names Markdown and its encodings carry, the documents the examples are built from, and the words a report entry uses about itself. |

Nothing is refused by name. A term is therefore not reached by spelling it differently: `pyproject`, a build's own function name and a flag one implementation invented are each reported by being absent from the vocabulary rather than present on a list.

### Case decides what the design states

The design names two builds in its status and parser sections, so reading it case-blind would admit `Python` and `Rust` into the corpus's vocabulary. The stating side is therefore not case-folded: **a word the design writes only capitalised names a product, a language or a build rather than stating a term of the contract.** The reading side is folded, so a claim writing `Python` states the word `python` and is reported.

The cost is that an initialism the corpus legitimately uses — `ASCII`, `ATX`, `CRLF`, `TOML`, `YAML`, `URL`, `UTF` — is not stated by the design either, and is registered instead. That is the right place for it: a name is admitted by being written down.

### Inflection, plurals and hyphenation

A word stands for its inflections, so one source word admits each form a sentence needs:

- a plural, including `-ies` to `-y` and the `-es` of a sibilant;
- a past tense and a present participle, with the doubled consonant of `filled` and `emitting` resolved;
- an adverb in `-ly`.

The resolution is applied to both sides and the candidate forms are compared as sets, so `blockquotes` in the design admits `blockquote` in a claim and `pipe` does not admit `pip`. Derivation is not inflection: `citation` is not admitted by `cite`, and a derived form the design does not write is registered.

A hyphenated compound is read as its parts, so `root-relative` is `root` and `relative`, and `rust-based` reports `rust`. A single letter names nothing and is not a word; a letter carrying a sign is one, so `c++` and `c#` are reported and the `a` of a sentence is not.

### Proper nouns in a path, and the tree a declaration names

A path is not prose. A fixture's source tree and the bytes it expects back are the input a run consumes and the output it reproduces, and the paths, reference texts and arguments a manifest declares name that same tree. `manifests.py` already holds each of them to the files the fixture carries, so this check reads them as the tree they name rather than as words. A proper noun in a path is therefore not read at all — `modes/plan-mode.md` states nothing about the contract.

A path *written into a description* is prose like any other, and its words are read. A code span in a claim quotes the fixture's own tree, so a span's contents are read no further than a path is.

### What is left outside the bound

- **An argument naming an option the contract does not declare** is not reported. The corpus carries a fixture whose declaration is exactly that — an undeclared option refused as invalid usage — so an option rule would have to admit the case it exists to catch. The contract refuses the invented flag at run time, which is where that bound belongs.
- **A term the glossary names as deliberately not used** is admitted where the design's prose also writes the word: the design writes `include` and `branches` in their ordinary senses. `make vocabulary` holds the design's *marked* terms to that table, which is the bound that rules on a term of art; this check rules on vocabulary.

## The run over the corpus

The rule was run over the corpus as it stands — 233 fixtures and the conformance report as it renders — and every word it reported was given a verdict. No word was reported for a term the contract states, and no fixture declaration was changed.

| Words reported | Verdict | Disposition |
| --- | --- | --- |
| 77 ordinary English words (`beside`, `kept`, `although`, `three`, `told`, …) | A word any sentence needs that the design has no occasion to write. | Registered under Ordinary English. |
| 23 names of markup, encodings and address forms (`ascii`, `atx`, `setext`, `crlf`, `toml`, `yaml`, `url`, `backtick`, `brace`, …) | A name the Markdown the contract binds carries, which the design writes only capitalised or not at all. | Registered under Markup, encodings and formats. |
| 6 names of documents the corpus's examples carry (`alpha`, `beta`, `checklist`, `diagram`, `workspace`, `column`) | A proper noun of the corpus's own source trees, written into a description. | Registered under the documents the corpus's examples carry. |
| 27 words a declaration or a report entry uses about itself (`clause`, `conformance`, `unfixturable`, `installation`, `runner`, `uncovered`, …) | The corpus and the report saying what they are doing. | Registered under what the corpus and the report state about themselves. |
| 0 | A word naming a build, a language, a library or the machinery of packaging. | None found. |

`make independence` is clean over the corpus with the register in place, which is the observation AC37 asks for.

## The inventory's 60 terms, against the rule

Each of the 60 terms the retired inventory held — 25 languages and runtimes, 20 of the machinery of modules and packaging, 10 of the wording a build gives its own fault, and the 5 shapes it matched — was put into a claim and read against the repository's own vocabulary. The demonstration is recorded in [validation](validation.md); 59 are reported and one is not.

`crate` is stated by the design, in the sentence that leaves the production build's slugging component unchosen. The vocabulary therefore admits it, and so does AC36 by its own terms: the word is one the design states. Keeping a one-term refusal list beside the vocabulary would be the two-rules condition this work ends, so the word is admitted and the design's naming of a build's packaging is raised as its own work.
