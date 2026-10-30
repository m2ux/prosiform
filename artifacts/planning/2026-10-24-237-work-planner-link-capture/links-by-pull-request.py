"""Write the pull-request link snapshot the work-planner scripts read.

Usage:
  python3 links-by-pull-request.py --repo owner/name --pulls prs.json --out links.json
      [--query-out pr-links-query.graphql] [--batch 90] [--no-run]

prs.json holds pull requests as JSON lines, as the skill's sync.py reads them. The output is the
array of {repo, number, closingIssuesReferences: [{repo, number}]} its --links input expects.

The relation is read from the pull request end so the snapshot covers exactly the pull requests
that were collected, including one whose title names no epic. A pulled relation that cannot be
read is reported and the run exits 1, matching the skill's rule that incomplete evidence is a
blocker rather than a partial result.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

QUERY = """  {alias}: pullRequest(number: {number}) {{
    number
    closingIssuesReferences(first: 50) {{ nodes {{ number repository {{ nameWithOwner }} }} }}
  }}"""


def pull_records(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def query_file(repo: str, numbers: list[int], path: Path) -> Path:
    owner, name = repo.split('/')
    body = '\n'.join(QUERY.format(alias=f'p{n}', number=n) for n in numbers)
    path.write_text(f'query {{\n  repository(owner: "{owner}", name: "{name}") {{\n{body}\n  }}\n}}\n')
    return path


def read_batch(path: Path) -> dict:
    out = subprocess.run(['gh', 'api', 'graphql', '-F', f'query=@{path}'],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f'graphql read failed: {out.stderr.strip()[:400]}')
    return json.loads(out.stdout)['data']['repository']


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--pulls', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--query-out', default='pr-links-query.graphql')
    parser.add_argument('--batch', type=int, default=90)
    parser.add_argument('--no-run', action='store_true')
    args = parser.parse_args()

    numbers = [p['number'] for p in pull_records(args.pulls)]
    if not numbers:
        sys.exit('no pull requests in the supplied collection')

    rows, unreadable = [], []
    for start in range(0, len(numbers), args.batch):
        batch = numbers[start:start + args.batch]
        path = query_file(args.repo, batch, Path(args.query_out))
        if args.no_run:
            print(f'query written: {path}')
            continue
        repository = read_batch(path)
        for n in batch:
            node = repository.get(f'p{n}')
            if node is None:
                unreadable.append(n)
                continue
            rows.append({
                'repo': args.repo,
                'number': n,
                'closingIssuesReferences': [
                    {'repo': i['repository']['nameWithOwner'], 'number': i['number']}
                    for i in node['closingIssuesReferences']['nodes']
                ],
            })

    if args.no_run:
        return 0
    Path(args.out).write_text(json.dumps(rows, indent=2) + '\n')
    print(f'{len(rows)} pull request(s) read, {sum(len(r["closingIssuesReferences"]) for r in rows)} link(s)')
    for n in unreadable:
        print(f'pull request {n}: issue links unreadable')
    return 1 if unreadable else 0


if __name__ == '__main__':
    sys.exit(main())
