The Python implementation of prosiform, checked against the behavioural contract by the [fixture corpus](../fixtures/README.md).

## Entry points

### Command line

Installing the package provides `prosiform`, declared in `[project.scripts]` as `prosiform.cli:main`. It accepts the contract's options, writes responses and bundles to standard output, writes diagnostics to standard error, and returns the outcome's exit status.

### Agent delivery

`prosiform.delivery` runs the command as a process and buffers standard output. It determines success from the exit status and checks the complete bundle against the transport's response limit. An oversized bundle is withheld as a delivery failure. Each transport declares its limit; the build's output budget alone cannot guarantee delivery.

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
- `make tables`, run from the repository root, checks README dependency and command tables against `pyproject.toml` and the [`Makefile`](../Makefile), including additions and removals.

### Runtime dependencies

| Declared | Value | Why |
| --- | --- | --- |
| Python | `>=3.13` | Required Python version; also used in continuous integration. |
| [`markdown-it-py`](https://pypi.org/project/markdown-it-py/) | `==4.2.0` | Markdown parser for the `skill-markdown-v1` profile. |

The parser uses the `commonmark` preset with core `table` and `strikethrough` rules enabled. Typographic substitution is off, task-list markers remain text, and raw HTML produces tokens the build can reject. No parser plugin is required. `mdurl` is a transitive dependency of `markdown-it-py`.

## Packaging

### Wheel

From `src`, build the wheel with:

```bash
uv build --wheel
```

The wheel includes [`docs/glossary.md`](../docs/glossary.md) at `prosiform/docs/glossary.md`, making diagnostic vocabulary available with the installed package.

### Installation check

`make smoke`, run from the repository root, builds the wheel, installs it in a temporary environment, and invokes `prosiform` from outside the repository. This checks packaging and entry-point resolution on every change.

## Checks

### Commands

Run these from the repository root alongside the [repository checks](../checks/README.md). Development tools are pinned in `uv.lock` for consistent local and CI runs.

| Command | Runs |
| --- | --- |
| `make test` | `pytest` over `src/tests/`; empty discovery fails with exit status 5. |
| `make harness` | `pytest` over `checks/tests/`, validating fixture manifests and the corpus runner. |
| `make corpus` | `checks/corpus.py` over every fixture against the command in `PROSIFORM_BUILD`. Use `prosiform` to test this build's console entry point. |
| `make lint` | `ruff check` over the package, its tests, and `checks/`. |
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

`tests/test_grouping.py` checks title-cased directory and document names, redundant trailing-word removal, shortest distinguishing paths after shared segments, and group selection from the deepest matching directory.

### Reference resolution

`tests/test_closure.py` checks splitting before decoding, valid percent escapes, exactly one decoding pass, and rejection of decoded separators or control characters. It also covers relative-path normalization, source-root confinement, scheme and authority classification, drive-letter paths, and exact decoded-fragment lookup.

### Command interface

`tests/test_cli.py` checks option grammar, output streams, exit statuses, implementation-specific responses, and write failures. Named output files are published through one rename, preserved on failure, and never written by validation-only runs.

### Delivery limits

`tests/test_delivery.py` checks delivery below and at the transport limit, complete withholding above it (including summaries), rejection of a zero limit, and failure statuses regardless of standard output. Three end-to-end tests run the installed entry point through the wrapper. The corpus drives the command directly, so wrapper behaviour needs separate tests.

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
