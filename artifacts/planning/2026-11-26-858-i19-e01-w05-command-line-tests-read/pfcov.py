"""A build for the corpus runner: pf under coverage, one context per fixture.

The fixture is found from the working directory the runner sets: the
nearest directory holding manifest.toml. Its path under fixtures/ is the
context; a run in a temporary copy (a fault fixture) is named by the copy's
directory name and mapped back to its identity afterwards.
"""

import os
import sys
from pathlib import Path

import coverage

DATA = os.environ["W05_COVERAGE_DATA"]


def fixture_identity(start: Path) -> str:
    for directory in (start, *start.parents):
        if (directory / "manifest.toml").is_file():
            parts = directory.parts
            if "fixtures" in parts:
                at = len(parts) - 1 - parts[::-1].index("fixtures")
                return "/".join(parts[at + 1 :])
            return "copy:" + directory.name
    return "unknown"


context = fixture_identity(Path.cwd())
cov = coverage.Coverage(
    data_file=DATA, data_suffix=True, source=["prosiform"], context=context
)
cov.start()
status = 2
try:
    from prosiform.cli import main

    status = main(sys.argv[1:])
except SystemExit as exit_:
    status = exit_.code if isinstance(exit_.code, int) else 1
finally:
    cov.stop()
    cov.save()
sys.exit(status)
