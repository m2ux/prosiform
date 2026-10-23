# The repository's checks, one target each.
#
# Every target exits nonzero when its check fails, so the target that failed
# names the check that failed. `make check` runs the set and stops at the
# first failure. Continuous integration calls these same targets.
#
# The Python tools come from the build's locked development dependency group:
# `uv run --frozen` installs what `src/uv.lock` records and resolves
# nothing. The corpus, invocation, conformance and independence checks reach
# the build under test through the corpus runner, and the last two read the
# corpus through the manifest reader beside it, which reads `jsonschema` from
# that same group, so the four run through it. The link check reads source
# metadata through that environment. The smoke, layout, table and
# vocabulary checks depend on the standard library alone and run under
# `python3` directly.
#
# `make smoke` is the one check that does not run the build from this
# checkout: it builds the wheel, installs it into a throwaway environment and
# invokes the command by name from a directory of its own, which is how a
# caller reaches an installed entry point.
#
# `make conformance` reads the design, the corpus and the build under test:
# it reports which clause of the contract each fixture exercises, which
# clauses no fixture reaches, which declared code and exit status the corpus
# reaches, and whether the codes the build reports for itself are the codes
# the contract declares. `make independence` reads the same three and that
# report, and fails on a declaration or an entry stating a word the
# contract's vocabulary does not hold.
#
# `make corpus` runs the corpus against a build named by configuration:
# `PROSIFORM_BUILD` holds that build's command line, and the target fails
# without one, so a fixture is never reported as holding against a build that
# never ran. `make invocation` reads the documented invocation against that
# same build's own help output, `make conformance` reads the codes it reports
# and `make independence` reads that report, and each fails without a build
# for the same reason.
#
# Every target below is named by a command table in one of the repository's
# documents, which `make tables` holds true in both directions.

UV_RUN := uv run --project src --frozen
TOOL_CONFIG := src/pyproject.toml
PYTHON_SOURCES := src/prosiform src/tests checks

.PHONY: check test harness corpus smoke lint format-check typecheck lock-check layout tables links vocabulary invocation conformance independence

check: lock-check lint format-check typecheck test harness corpus smoke layout tables links vocabulary invocation conformance independence

test:
	cd src && uv run --frozen pytest

harness:
	$(UV_RUN) pytest --config-file $(TOOL_CONFIG) --rootdir . checks/tests

corpus:
	$(UV_RUN) python checks/corpus.py

smoke:
	python3 checks/smoke.py

lint:
	$(UV_RUN) ruff check --config $(TOOL_CONFIG) $(PYTHON_SOURCES)

format-check:
	$(UV_RUN) ruff format --check --config $(TOOL_CONFIG) $(PYTHON_SOURCES)

typecheck:
	$(UV_RUN) mypy --config-file $(TOOL_CONFIG) $(PYTHON_SOURCES)

lock-check:
	cd src && uv lock --check

layout:
	python3 checks/layout.py

tables:
	python3 checks/tables.py

links:
	$(UV_RUN) python checks/links.py --online

vocabulary:
	python3 checks/vocabulary.py

invocation:
	$(UV_RUN) python checks/invocation.py

conformance:
	$(UV_RUN) python checks/conformance.py

independence:
	$(UV_RUN) python checks/independence.py
