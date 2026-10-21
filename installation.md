# Installation

prosiform installs from the Python build in [`src/`](src/README.md):

```bash
pip install ./src
```

A working copy takes its environment from the lockfile, which records the exact version of every dependency a checkout installs:

```bash
cd src
uv sync --frozen
```

Installing the build puts the `prosiform` command on the path and ships the [glossary](docs/glossary.md) with the package, so an installed build carries the vocabulary its diagnostics use. The command is the entry point every caller depends on, and three properties are what make it one:

- **Named on the path.** The installation puts the one documented name in the environment's executable directory, so a caller writes `prosiform` and resolves nothing for itself.
- **Independent of the working directory.** A run's outcome follows from its options and the source root they name, and from nothing about where the process was started.
- **Independent of this repository.** The installed build reads nothing out of the tree it was built from, and the source root a caller names is the caller's own.

`make smoke` holds all three on every change: it builds the wheel, installs it into a throwaway environment, and bundles a reference from a source root outside this repository with the command resolved by name from a directory unrelated to it. `prosiform --version` reports the installed version and the `skill-markdown-v1` profile the build implements.
