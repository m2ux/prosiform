# The repository's checks, one target each.
#
# Every target exits nonzero when its check fails, so the target that failed
# names the check that failed. `make check` runs the set and stops at the
# first failure. Continuous integration calls these same targets.
#
# The Python tools come from the build's locked development dependency group:
# `uv run --frozen` installs what `prototype/uv.lock` records and resolves
# nothing. The corpus checks read `jsonschema` from that same group, so they
# run through it; the layout, table, link and vocabulary checks depend on the
# standard library alone and run under `python3` directly.
#
# `make corpus` runs the corpus against a build named by configuration:
# `PROSIFORM_BUILD` holds that build's command line, and the target fails
# without one, so a fixture is never reported as holding against a build that
# never ran.
#
# Every target below is named by a command table in one of the repository's
# READMEs, which `make tables` holds true in both directions.

UV_RUN := uv run --project prototype --frozen
TOOL_CONFIG := prototype/pyproject.toml
PYTHON_SOURCES := prototype/src prototype/tests checks

.PHONY: check test harness corpus lint format-check typecheck lock-check layout tables links vocabulary

check: lock-check lint format-check typecheck test harness corpus layout tables links vocabulary

test:
	cd prototype && uv run --frozen pytest

harness:
	$(UV_RUN) pytest --config-file $(TOOL_CONFIG) --rootdir . checks/tests

corpus:
	$(UV_RUN) python checks/corpus.py

lint:
	$(UV_RUN) ruff check --config $(TOOL_CONFIG) $(PYTHON_SOURCES)

format-check:
	$(UV_RUN) ruff format --check --config $(TOOL_CONFIG) $(PYTHON_SOURCES)

typecheck:
	$(UV_RUN) mypy --config-file $(TOOL_CONFIG) $(PYTHON_SOURCES)

lock-check:
	cd prototype && uv lock --check

layout:
	python3 checks/layout.py

tables:
	python3 checks/tables.py

links:
	python3 checks/links.py --online

vocabulary:
	python3 checks/vocabulary.py
