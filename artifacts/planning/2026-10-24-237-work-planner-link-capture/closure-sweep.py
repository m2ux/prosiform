"""Report closed issues whose closure their own evidence does not support.

Usage:
  python3 closure-sweep.py --issues issues.json --links links-by-issue.json
      [--repo owner/name] [--only 49,63,66]

issues.json is every issue as `gh api --paginate "repos/{owner}/{repo}/issues?state=all&per_page=100"`
returns it, the pages' arrays one after another. links-by-issue.json is what links-by-issue.py
writes: each issue's Development pull requests.

An issue is reported when it is closed as completed while an acceptance criterion is unticked, or
while a Development-linked pull request has not merged. The state reason and each link are printed
with the finding, because an issue closed after another issue took its work is legitimate and looks
identical to an unproven closure from the criteria alone.

An issue stating no acceptance criteria at all is listed separately: it is closed unproven, but a
body written before the body template carried criteria is a different question from one the current
template failed to satisfy, and the two are triaged apart.

Exit 0 when every closure is supported, 1 when any is not. The skill's closure.py gates one issue
against fresh evidence; this reports the repository-wide condition that gate cannot see.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TICKED = re.compile(r'^- \[[xX]\] \*\*AC\d+\.\*\*', re.M)
UNTICKED = re.compile(r'^- \[ \] \*\*AC(\d+)\.\*\*', re.M)
MERGED = 'MERGED'


def pages(path: str) -> list:
    text, decoder, items, i = Path(path).read_text(), json.JSONDecoder(), [], 0
    while True:
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            return items
        page, i = decoder.raw_decode(text, i)
        items.extend(page)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--issues', required=True)
    parser.add_argument('--links', required=True)
    parser.add_argument('--only', default='')
    args = parser.parse_args()

    issues = [i for i in pages(args.issues) if 'pull_request' not in i]
    links = json.loads(Path(args.links).read_text())
    only = {int(n) for n in args.only.split(',') if n.strip()}

    findings, uncriteria = 0, 0
    for issue in sorted(issues, key=lambda i: i['number']):
        if only and issue['number'] not in only:
            continue
        if issue['state'] != 'closed':
            continue
        body = issue.get('body') or ''
        reasons = []
        unticked = UNTICKED.findall(body)
        if unticked:
            reasons.append('criteria unticked: ' + ', '.join(f'AC{n}' for n in unticked))
        elif not TICKED.search(body):
            uncriteria += 1
            continue
        for pr in links.get(str(issue['number']), []):
            if pr['state'] != MERGED:
                reasons.append(f'#{pr["number"]} {pr["state"].lower()}, not merged')
        if not reasons:
            continue
        findings += 1
        reason = issue.get('state_reason') or 'unspecified'
        print(f'#{issue["number"]} closed as {reason}: {issue["title"]}')
        for r in reasons:
            print(f'  {r}')
    print(f'sweep: {findings} closure(s) unsupported by their own evidence, '
          f'{uncriteria} closed stating no acceptance criteria')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
