"""Pytest plugin: write each collected test as its node id and the case it runs.

Load with `-p collect_items` and name the output file in W06_ITEMS. A case is
the test function with its parameter values, so a case keeps its identity when
the position-numbered part of a node id (`entries0`, `arguments2`) shifts
after an earlier case of the same list is removed.
"""

import json
import os


def pytest_collection_modifyitems(session, config, items):
    cases = []
    for item in items:
        callspec = getattr(item, "callspec", None)
        params = sorted(callspec.params.items()) if callspec else []
        cases.append(
            {
                "id": item.nodeid.split("::", 1)[1],
                "case": repr((item.originalname, params)),
            }
        )
    with open(os.environ["W06_ITEMS"], "w") as handle:
        json.dump(cases, handle, indent=1, ensure_ascii=False)
