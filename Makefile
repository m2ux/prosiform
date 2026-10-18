# The repository's checks, one target each.
#
# Every target exits nonzero when its check fails, so the target that failed
# names the check that failed. `make check` runs the set and stops at the
# first failure. Continuous integration calls these same targets.
#
# The Python tools come from the build's locked development dependency group:
# `uv run --frozen` installs what `prototype/uv.lock` records and resolves
# nothing. The three repository checks depend on the standard library alone
# and run under `python3` directly.

UV_RUN := uv run --project prototype --frozen
TOOL_CONFIG := prototype/pyproject.toml
PYTHON_SOURCES := prototype/src prototype/tests checks

.PHONY: check test lint format-check typecheck lock-check layout links vocabulary

check: lock-check lint format-check typecheck test layout links vocabulary

test:
	cd prototype && uv run --frozen pytest

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

links:
	python3 checks/links.py --online

vocabulary:
	python3 checks/vocabulary.py
