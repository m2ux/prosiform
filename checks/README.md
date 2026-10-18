# Checks

The checks that hold the repository's own claims true. Each is a standalone Python 3 script with no dependency beyond the standard library, and each has a named command in the [Makefile](../Makefile) that runs it from the repository root and returns a nonzero status when it fails. A developer and a continuous-integration job invoke the same name.

| Check | Command | Asserts | Fails on |
| --- | --- | --- | --- |
| `layout.py` | `make layout` | The repository holds a tree for the fixture corpus, one for the Python build and one for documentation. | A tree that holds no tracked file. |
| `links.py` | `make links` | Every reference the README carries resolves. | A path that does not exist, a fragment no heading generates, a git ref or path absent from the engineering branch, or a remote address that does not answer. |
| `vocabulary.py` | `make vocabulary` | The shipped glossary defines every contract term the design and the epic acceptance criteria use. | A term the planning record's glossary inventories, the design or a criterion uses, and `docs/glossary.md` does not define. |

`make check` runs these three alongside the Python build's tests and static checks, in one pass over the repository.

`links.py` reaches addresses outside this repository only with `--online`, and the named command supplies it: without the flag a remote reference counts as unresolved, so an offline run of this README cannot pass. References into this repository's own branches resolve through git, so they need no network. An issue, a pull request or a project board is read through `gh api` with the caller's credentials, because a private repository answers an unauthenticated request with 404.

`vocabulary.py` reads the design, the epic criteria and the term inventory from the `engineering` branch, which a checkout reaches as `origin/engineering`.

The scripts are linted, formatted and type checked with the Python build's tools, which `make lint`, `make format-check` and `make typecheck` run over `checks/` alongside the package.
