"""Put the check scripts on the import path.

`checks/` is a directory of scripts rather than a package, so a test
reaches one by name once that directory is importable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
