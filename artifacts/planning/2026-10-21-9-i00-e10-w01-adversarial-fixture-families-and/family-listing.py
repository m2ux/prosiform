"""List each adversarial fixture family the design names and the fixtures that encode it.

The design lists its adversarial families as bold-led bullets under
`## Adversarial acceptance fixtures`, and a fixture states the clauses it
encodes in its manifest, so a family is represented when a manifest names it
as `Adversarial acceptance fixtures - <Family>`, optionally followed by the
case after a comma. The listing reads both and prints one line per family.

Usage: family-listing.py <design.md> <fixtures-dir>
"""

import re
import sys
from pathlib import Path

FAMILY_HEADING = "## Adversarial acceptance fixtures"
CLAUSE_PREFIX = "Adversarial acceptance fixtures "
BULLET = re.compile(r"\A- \*\*(?P<name>[^:*]+):\*\*")


def families(design: Path) -> list[str]:
    """The family names the design's adversarial section lists, in its order."""
    named: list[str] = []
    inside = False
    for line in design.read_text(encoding="utf-8").splitlines():
        if line.startswith(FAMILY_HEADING):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            found = BULLET.match(line)
            if found:
                named.append(found.group("name"))
    return named


def encoded(fixtures: Path) -> dict[str, list[str]]:
    """Each family a manifest names, against the fixture identities naming it."""
    held: dict[str, list[str]] = {}
    for manifest in sorted(fixtures.glob("*/*/manifest.toml")):
        identity = manifest.parent.relative_to(fixtures).as_posix()
        for line in manifest.read_text(encoding="utf-8").splitlines():
            clause = line.strip().strip(",").strip('"')
            if not clause.startswith(CLAUSE_PREFIX):
                continue
            named = clause[len(CLAUSE_PREFIX) :].lstrip("- —").split(",")[0]
            held.setdefault(named.strip(), []).append(identity)
    return held


def main() -> int:
    design, fixtures = Path(sys.argv[1]), Path(sys.argv[2])
    held = encoded(fixtures)
    missing = 0
    for family in families(design):
        identities = held.get(family, [])
        if identities:
            print("held      {0:<20} {1}".format(family, len(identities)))
            for identity in identities:
                print("              {0}".format(identity))
        else:
            missing += 1
            print("UNHELD    {0}".format(family))
    unknown = sorted(set(held) - set(families(design)))
    for name in unknown:
        print("UNNAMED   {0} is named by a manifest and by no design bullet".format(name))
    print("{0} family(ies) the design names, {1} held by no fixture".format(
        len(families(design)), missing))
    return 1 if missing or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
