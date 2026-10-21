# Source

The Python build of prosiform.

It implements the behavioural contract and is held to it by the [fixture corpus](../fixtures/README.md).

Installing it puts the `prosiform` command on the path, declared by `[project.scripts]` and entered at `prosiform.cli:main`. The command carries the option set the contract declares, writes its response or its bundle to standard output and its diagnostics to standard error, and returns the exit status its outcome names.

`prosiform.delivery` is the wrapper a calling agent reaches the command through. It runs the entry point as a process, buffers the whole of standard output, reads the outcome from the process status rather than from the presence of Markdown, and holds the buffered bundle against the response limit the transport declares. A limit it cannot carry the bundle within is a delivery failure that withholds the document rather than cutting it, and the transport names that limit, since the build's own output budget is not universally safe for agent delivery.

## Environment

`pyproject.toml` declares the supported Python version and the build's dependencies. `uv.lock` records the exact version and hash of every package those dependencies resolve to, so two checkouts install the same tree.

```bash
cd src
uv sync --frozen
```

`--frozen` installs what the lockfile records and resolves nothing, so a dependency change reaches an environment only by way of a lockfile change. `uv sync --check` reports an environment whose versions have drifted from the lockfile. `uv lock` rewrites the lockfile after an edit to `pyproject.toml`, and `uv lock --check` reports a lockfile that no longer describes the declared dependencies. `make tables` holds the tables below to what `pyproject.toml` and the [`Makefile`](../Makefile) declare, in both directions, so a dependency added or dropped and a command added or retired reach this document on the change that makes it.

| Declared | Value | Why |
| --- | --- | --- |
| Python | `>=3.13` | The version the environment is created with and the one continuous integration runs. |
| [`markdown-it-py`](https://pypi.org/project/markdown-it-py/) | `==4.2.0` | The parser the `skill-markdown-v1` profile is configured on. Its `commonmark` preset with the `table` and `strikethrough` rules enabled gives the profile's pipe tables and double-tilde strikethrough; its typographer stays off, which is the profile's disabled typographic substitution; it leaves source task-list markers as text rather than generating checkbox HTML; and it emits raw HTML as its own token, which is what lets the build refuse it. |

`mdurl` is resolved as `markdown-it-py`'s own dependency. The profile needs no parser plugin, so `mdit-py-plugins` is not declared: pipe tables and strikethrough are core rules of the parser, and preserving task-list markers means leaving the plugin that renders them out.

## Packaging

The wheel carries [`docs/glossary.md`](../docs/glossary.md) at `prosiform/docs/glossary.md`, so the vocabulary the tool's diagnostics use travels with an installed build rather than only with the source tree.

```bash
uv build --wheel
```

`make smoke` builds that wheel, installs it into a throwaway environment and invokes the command by name from a directory unrelated to this repository, so the packaging metadata is held to producing an installable build with a resolvable entry point on every change rather than at release time.

## Checks

The build's tests and static checks are named commands, run from the repository root alongside [the checks the repository carries](../checks/README.md). Each tool is declared in the `dev` dependency group and pinned by the lockfile, so the version that checks a change on a working copy is the version that checks it in continuous integration.

| Command | Runs |
| --- | --- |
| `make test` | `pytest` over `tests/`. A run that collects no test exits 5, so a suite that discovers nothing fails. |
| `make harness` | `pytest` over `../checks/tests`, which validates every fixture manifest the corpus holds and exercises the runner that decides a fixture's result. The corpus is not this build, so it carries its own commands. |
| `make corpus` | `../checks/corpus.py` over every fixture the corpus holds, against the build `PROSIFORM_BUILD` names. This build reaches it as its console entry point, `prosiform`, so the corpus runs against the build a change produces rather than against the package it imports. |
| `make lint` | `ruff check` over the package, its tests and `checks/`. |
| `make format-check` | `ruff format --check` over those same files. Formatting is reported, not applied. |
| `make typecheck` | `mypy` in strict mode over those same files. |
| `make lock-check` | `uv lock --check`, which exits nonzero when `uv.lock` does not describe the dependency list `pyproject.toml` declares. A dependency edited without relocking fails here rather than at the next install. |

| Declared | Value | Why |
| --- | --- | --- |
| [`pytest`](https://pypi.org/project/pytest/) | `==9.1.1` | Discovers and reports the suite, and exits nonzero on a failure and on an empty discovery alike. |
| [`ruff`](https://pypi.org/project/ruff/) | `==0.17.1` | The linter and the formatter in one tool, so one declared configuration governs both. |
| [`mypy`](https://pypi.org/project/mypy/) | `==2.4.0` | The type checker, run in strict mode. |
| [`jsonschema`](https://pypi.org/project/jsonschema/) | `==4.26.0` | Validates a fixture manifest against the corpus schema, which is a published schema language rather than a validator written here. |
| [`types-jsonschema`](https://pypi.org/project/types-jsonschema/) | `==4.26.0.20261006` | The annotations `jsonschema` does not ship, which strict mode requires. |

`tests/test_profile.py` holds the build's configured parser to the clauses the declared profile rests on: pipe tables, double-tilde strikethrough, task-list markers preserved as source text and protected from a reference definition that would turn one into a link, typographic substitution off, raw HTML recognized as a token of its own, Markdown suffixes classified case-insensitively, and each recognized unsupported dependency or section-naming construct refused while the prose, the code span and the escape that resemble one pass untouched.

`tests/test_source.py` holds the transport-metadata scan to the frontmatter policy in both of its directions: one leading byte-order mark removed and a second left as content, a block closed by three hyphens or by three dots and by neither an indented delimiter nor one carrying a trailing space, CRLF terminators recognized, a YAML example inside a code block and a thematic break below the first line left alone, an opener no line closes failing, and the line of the file every location in the stripped content maps back to.

`tests/test_bundle.py` holds the bundle's structure to the clauses the file group rests on: the heading one path generates and the suffix it drops, the escaping that keeps that heading literal, the slug a destination is generated from and the ordinal a repeated one takes, the region a parse exposes for each block with the bytes its source wrote inside it and one blank line between it and the next, a title the path already names absorbed and one it does not kept and shifted, and a shift beyond the sixth level refused.

`tests/test_grouping.py` holds the names a merged group writes to the clauses the grouping rules rest on: a directory slug and a document stem emitted in title case, the trailing word of a stem the group's own heading already states dropped, the shortest run of a path that tells two contributing documents apart measured after the segments they share, the members the `Overview` section carries a subsection for — each with content above the grouping depth, and each the arrangement emits nothing else from — and the group a document belongs to read from the deepest directory segment a rule names.

`tests/test_closure.py` holds a reference to the path identity the resolution sequence gives it, step by step and in both directions: the components split before any escape is decoded, an escape validated as a percent and two hexadecimal digits, one decoding and no second, a separator or a control character a segment decodes to refused, `.` and `..` normalized against the directory the reference is written in, a path walking above the allowed source root refused, a scheme and an authority classified rather than resolved, a drive letter read as a path rather than as a scheme, and a fragment looked up as the exact text it decoded to.

`tests/test_cli.py` holds the command to its grammar, its two streams and its exit statuses. It carries the cases the corpus cannot reach: a response whose text belongs to this build rather than to the contract, a write the stream refuses, the status a request this build cannot carry out returns, and the publication the corpus observes only through standard output — a named output file written through one rename, left untouched by a failing run, and written by no validation-only run.

`tests/test_delivery.py` holds the wrapper to never returning a bundle the transport did not carry whole: a bundle within the limit delivered and one at it delivered too, a bundle over it withheld with no part of the document and no summary anywhere in the result, a limit of nothing refused, every failing status the contract names read as a failure whatever standard output carried, and three end-to-end runs of the installed entry point through the wrapper. A corpus fixture reaches none of them: the runner drives the command, and the process status, the buffer and the transport's limit are the layer above it.

`tests/test_candidate.py` holds the candidate-validation pass to failing. A validation pass nobody can break reports a guarantee nobody has, so each invariant is given a candidate or a provenance record that disagrees with the other and the invariant it names is asserted: a missing selected region, a region no range accounts for, a destination reaching another heading, a definition that survived emission, literal bracketed text read as a link, a rewritten link showing other text, reformatted bytes, a repaired code example, a heading at another level, and a range recorded twice. The corpus cannot reach any of them: no source document makes a working build disagree with its own record.

## Layout

| Path | Holds |
| --- | --- |
| `pyproject.toml` | The project definition: the supported Python version, the dependencies, the package data and the tool configuration. |
| `uv.lock` | The exact resolved version and hash of every package. |
| `prosiform/` | The package. |
| `tests/` | The build's tests. |
