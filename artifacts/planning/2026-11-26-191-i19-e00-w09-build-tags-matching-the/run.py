"""Run the releases check over a repository: run.py CHECKS-DIRECTORY REPOSITORY."""

import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import releases  # noqa: E402

releases.ROOT = Path(sys.argv[2])
sys.exit(releases.main())
