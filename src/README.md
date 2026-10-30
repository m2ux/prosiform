## Entry points

### Command line

Installing the package provides `pf`, declared in `[project.scripts]` as `prosiform.cli:main`. It accepts the contract's options, writes its bundles into a folder of the run's own, named for its entry with the `.bundles` suffix, in the working directory or the folder `-o` names, writes the guide a bare `pf` prints and informational responses to standard output, writes diagnostics to standard error, and returns the outcome's exit status.

## Environment

### Setup

`pyproject.toml` declares the supported Python version and dependencies. `uv.lock` pins every resolved package's version and hash.

```bash
cd src
uv sync --frozen
```

`--frozen` installs from the lockfile without resolving dependencies.

### Dependency maintenance

- `uv sync --check` detects environment drift from the lockfile.
- `uv lock` updates the lockfile after dependency changes.
- `uv lock --check` checks the lockfile against declared dependencies.
- `make tables`, run from the repository root, checks documentation dependency and command tables against `pyproject.toml` and the [`Makefile`](../Makefile), including additions and removals.

### Runtime dependencies

| Declared | Value | Why |
| --- | --- | --- |
| Python | `>=3.13` | Required Python version; also used in continuous integration. |
| [`markdown-it-py`](https://pypi.org/project/markdown-it-py/) | `==4.2.0` | Markdown parser for the `skill-markdown-v4` profile. |
| [`ruamel.yaml`](https://yaml.dev/doc/ruamel.yaml/) | `==0.18.16` | Safe event parsing for bounded YAML metadata decoding. |

The parser uses the `commonmark` preset with core `table` and `strikethrough` rules enabled. Typographic substitution is off, task-list markers remain text, and raw HTML produces tokens the build can reject. No parser plugin is required. `mdurl` is a transitive dependency of `markdown-it-py`.

The metadata decoder consumes the pure Python YAML event stream, checks collection depth before building nodes, and applies YAML 1.2 Core scalar resolution. Node identities keep tag-aware key equality, including collection keys. Aliases, custom tags and merge keys fail before construction. The decoder accepts a byte span from a captured source; source-reader integration supplies that span.

## Packaging

### Wheel

From `src`, build the wheel with:

```bash
uv build --wheel
```

The wheel includes [`docs/glossary.md`](../docs/glossary.md) at `prosiform/docs/glossary.md`, making diagnostic vocabulary available with the installed package.

### Installation check

`make smoke`, run from the repository root, builds the wheel, installs it in a temporary environment, and invokes `pf` from outside the repository. This checks packaging and entry-point resolution on every change.

## Checks

### Commands

Run these from the repository root alongside the [repository checks](../checks/README.md). Development tools are pinned in `uv.lock` for consistent local and CI runs.

| Command | Runs |
| --- | --- |
| `make test` | `pytest` over `src/tests/`; empty discovery fails with exit status 5. |
| `make harness` | `pytest` over `checks/tests/` and `evals/diagram-following/`, validating fixture manifests, the corpus runner and the diagram-following corpus, its scorer, its runner against a stub agent, and its report over recorded results. |
| `make corpus` | `checks/corpus.py` over every fixture against the command in `PROSIFORM_BUILD`. Use `pf` to test this build's console entry point. |
| `make lint` | `ruff check` over the package, its tests, `checks/` and `evals/`. |
| `make format-check` | `ruff format --check` over the same files; reports formatting without applying it. |
| `make typecheck` | Strict `mypy` over the same files. |
| `make lock-check` | `uv lock --check`; fails if the lockfile disagrees with declared dependencies. |

### Development dependencies

| Declared | Value | Why |
| --- | --- | --- |
| [`pytest`](https://pypi.org/project/pytest/) | `==9.1.1` | Test discovery and execution; failures and empty discovery return nonzero. |
| [`ruff`](https://pypi.org/project/ruff/) | `==0.17.1` | Linting and formatting under one configuration. |
| [`mypy`](https://pypi.org/project/mypy/) | `==2.4.0` | Strict type checking. |
| [`jsonschema`](https://pypi.org/project/jsonschema/) | `==4.26.0` | Fixture-manifest validation against the corpus schema. |
| [`types-jsonschema`](https://pypi.org/project/types-jsonschema/) | `==4.26.0.20261006` | Type annotations for `jsonschema`. |

## Test coverage

Paths below are relative to `src/`.

### Markdown profile

`tests/test_profile.py` checks tables, strikethrough, literal task-list markers (including reference-definition collisions), disabled typographic substitution, raw HTML recognition, and case-insensitive Markdown suffixes. Unsupported dependency and section-naming constructs are rejected; lookalikes in prose, code spans, and escapes pass through.

### Source metadata

`tests/test_source.py` checks frontmatter closed by three hyphens or three dots, CRLF handling, unterminated blocks, and original line locations after stripping. It removes one leading byte-order mark, preserves a second, and leaves code-block YAML and nonleading thematic breaks intact. Indented delimiters and delimiters with trailing spaces do not close frontmatter.

### Bundle structure

`tests/test_bundle.py` checks path-derived headings, suffix removal, literal escaping, destination slugs, and duplicate ordinals. It verifies source-byte preservation and one blank line between blocks, absorption of titles matching the path, shifts of retained headings, and refusal beyond level six.

### Grouping

`tests/test_grouping.py` checks title-cased directory and document names, redundant trailing-word removal, shortest distinguishing paths after shared segments, the `Overview` subsection each member takes — including one the arrangement emits nothing else from — and group selection from the deepest matching directory.

### Reference resolution

`tests/test_closure.py` checks splitting before decoding, valid percent escapes, exactly one decoding pass, and rejection of decoded separators or control characters. It also covers relative-path normalization, source-root confinement, scheme and authority classification, drive-letter paths, and exact decoded-fragment lookup.

### Command interface

`tests/test_cli.py` checks option grammar, the guide a bare `pf` prints, output streams, exit statuses, implementation-specific responses, and write failures. A run's bundles are written into a folder of its own under the folder `-o` names, or the working directory, under their joined derived names; the folder is published through one rename, an existing run folder keeps its bytes on failure, validation-only runs write nothing, and `-o -` is invalid usage.

### Candidate validation

`tests/test_candidate.py` supplies inconsistent candidates and provenance records to verify rejection of:

- Missing selected regions, unaccounted regions, and duplicate ranges.
- Destinations targeting the wrong heading and surviving reference definitions.
- Literal bracketed text interpreted as links and rewritten links with altered text.
- Reformatted bytes, repaired code examples, and incorrect heading levels.

These tests exercise internal inconsistencies that source documents cannot induce in a working build.

## Layout

| Path | Holds |
| --- | --- |
| `pyproject.toml` | Python requirement, dependencies, package data, and tool configuration. |
| `uv.lock` | Resolved package versions and hashes. |
| `prosiform/` | Implementation package. |
| `tests/` | Implementation tests. |
