# Checks

The checks that hold the repository's own claims true. Each has a named command in the [Makefile](../Makefile) that runs it from the repository root and returns a nonzero status when it fails, so a developer and a continuous-integration job invoke the same name.

| Check | Command | Asserts | Fails on |
| --- | --- | --- | --- |
| `layout.py` | `make layout` | The repository holds a tree for the fixture corpus, one for the Python build and one for documentation. | A tree that holds no tracked file. |
| `links.py` | `make links` | Every reference the README carries resolves. | A path that does not exist, a fragment no heading generates, a git ref or path absent from the engineering branch, or a remote address that does not answer. |
| `vocabulary.py` | `make vocabulary` | The shipped glossary and the contract carry one vocabulary between them. | A term the design marks as a contract term and `docs/glossary.md` does not define, a marked term the glossary names as deliberately not used, or a definition neither the design marks nor an acceptance criterion uses. |
| `manifests.py` | `make corpus` | Every fixture the corpus holds is a fixture the manifest schema describes. | A manifest leaving out one of the five declarations, carrying a field the schema does not describe, naming an error code outside the catalogue, or naming a path the fixture does not hold. |
| `runner.py` | `make corpus` | A fixture's run against the build under test produces the result its manifest declares. | A differing exit status, standard output differing in any byte, or a diagnostic missing, extra, out of order, or carrying another value in a field the manifest declares. |

`make check` runs these five alongside the Python build's tests and static checks, in one pass over the repository.

The first three are standalone Python 3 scripts with no dependency beyond the standard library, run under `python3` directly. `manifests.py` and `runner.py` are the corpus's own modules rather than commands of their own, and `make corpus` runs the suite in [`tests/`](tests) that exercises both.

`manifests.py` is the manifest reader and validator: it reads [`fixtures/manifest.schema.json`](../fixtures/manifest.schema.json) through `jsonschema` from the locked development group and applies it to every fixture. `runner.py` reads its validation from that same module, so a manifest is checked the same way wherever it is read.

`runner.py` runs one fixture. It reads the manifest, invokes the build under test against the fixture's source tree, and compares the run's standard output, exit status and diagnostics with what the manifest declares. The build is named by configuration — the environment variable `PROSIFORM_BUILD` holds its command line — and invoked as a subprocess, so the module imports no package, names no module and names no language, and the production build runs the same corpus through a runner of its own. There is no default build: an unset variable raises rather than returning a verdict, so a fixture is never reported as holding against a build that never ran. The runner supplies the allowed source root and asks for diagnostics as data, which the contract's command line spells `--root DIR` and `--diagnostics json`, so a code is compared as a value rather than as prose.

A mismatch names the expectation that differed and locates the difference inside it. Standard output is compared as bytes and reported by byte offset, line and column, each window spelling its control bytes, so a CRLF against an LF reads as a difference rather than as two identical lines. Diagnostics are compared in order on the fields the manifest declares: one missing, one extra, a pair in the wrong order, and a field carrying another value are each reported as what they are, and a diagnostic carrying more than the manifest declares matches. `PROSIFORM_BUILD_TIMEOUT` bounds a run in seconds, and a run that exceeds it fails the fixture.

`links.py` reaches addresses outside this repository only with `--online`, and the named command supplies it: without the flag a remote reference counts as unresolved, so an offline run of this README cannot pass. References into this repository's own branches resolve through git, so they need no network. An issue, a pull request or a project board is read through `gh api` with the caller's credentials, because a private repository answers an unauthenticated request with 404.

`vocabulary.py` takes the contract's term inventory from the contract itself: the design italicises a term where it first uses it, and the glossary must define each one. It reads the design and the epic criteria from the branch and path the README's Design link names, which a checkout reaches as `origin/engineering`, so no path into a dated planning folder is written in a check. Superseding that folder changes the README's link, and `links.py` holds that link to resolving.

`manifests.py` takes the error-code catalogue from the schema and the schema from the corpus, so the one declaration of a code is the one both builds read. A test holds that catalogue to the design's own text, collecting every `E_`-prefixed code the design carries and requiring the schema to enumerate exactly those.

The scripts are linted, formatted and type checked with the Python build's tools, which `make lint`, `make format-check` and `make typecheck` run over `checks/` alongside the package.
