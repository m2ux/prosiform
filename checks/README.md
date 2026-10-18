# Checks

The checks that hold the repository's own claims true. Each is a standalone Python 3 script with no dependency beyond the standard library, run from the repository root and returning a nonzero status when it fails.

| Check | Asserts | Fails on |
| --- | --- | --- |
| `layout.py` | The repository holds a tree for the fixture corpus, one for the Python build and one for documentation. | A tree that holds no tracked file. |
| `links.py` | Every reference the README carries resolves. | A path that does not exist, a fragment no heading generates, a git ref or path absent from the engineering branch, or a remote address that does not answer. |
| `vocabulary.py` | The shipped glossary defines every contract term the design and the epic acceptance criteria use. | A term the planning record's glossary inventories, the design or a criterion uses, and `docs/glossary.md` does not define. |

```bash
python3 checks/layout.py
python3 checks/links.py --online
python3 checks/vocabulary.py
```

`links.py` reaches addresses outside this repository only with `--online`; without it, a remote reference counts as unresolved. References into this repository's own branches resolve through git, so they need no network. An issue, a pull request or a project board is read through `gh api` with the caller's credentials, because a private repository answers an unauthenticated request with 404.

`vocabulary.py` reads the design, the epic criteria and the term inventory from the `engineering` branch, which a checkout reaches as `origin/engineering`.

The commands that run the build's tests and static checks are a later task; these three move under that command when it exists.
