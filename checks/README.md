# Checks

The checks that hold the repository's own claims true. Each is a standalone Python 3 script with no dependency beyond the standard library, and each has a named command in the [Makefile](../Makefile) that runs it from the repository root and returns a nonzero status when it fails. A developer and a continuous-integration job invoke the same name.

| Check | Command | Asserts | Fails on |
| --- | --- | --- | --- |
| `layout.py` | `make layout` | The repository holds a tree for the fixture corpus, one for the Python build and one for documentation. | A tree that holds no tracked file. |
| `links.py` | `make links` | Every reference the README carries resolves. | A path that does not exist, a fragment no heading generates, a git ref or path absent from the engineering branch, or a remote address that does not answer. |
| `vocabulary.py` | `make vocabulary` | The shipped glossary and the contract carry one vocabulary between them. | A term the design marks as a contract term and `docs/glossary.md` does not define, a marked term the glossary names as deliberately not used, or a definition neither the design marks nor an acceptance criterion uses. |

`make check` runs these three alongside the Python build's tests and static checks, in one pass over the repository.

`links.py` reaches addresses outside this repository only with `--online`, and the named command supplies it: without the flag a remote reference counts as unresolved, so an offline run of this README cannot pass. References into this repository's own branches resolve through git, so they need no network. An issue, a pull request or a project board is read through `gh api` with the caller's credentials, because a private repository answers an unauthenticated request with 404.

`vocabulary.py` takes the contract's term inventory from the contract itself: the design italicises a term where it first uses it, and the glossary must define each one. It reads the design and the epic criteria from the branch and path the README's Design link names, which a checkout reaches as `origin/engineering`, so no path into a dated planning folder is written in a check. Superseding that folder changes the README's link, and `links.py` holds that link to resolving.

The scripts are linted, formatted and type checked with the Python build's tools, which `make lint`, `make format-check` and `make typecheck` run over `checks/` alongside the package.
