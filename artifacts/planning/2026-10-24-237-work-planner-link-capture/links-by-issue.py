"""Read every issue's Development links in one batched tracker call.

Usage:
  python3 links-by-issue.py --repo owner/name --issues issues.json --out links-by-issue.json
      [--query-out links-query.graphql] [--batch 90] [--no-run]

issues.json is every issue as `gh api --paginate "repos/{owner}/{repo}/issues?state=all&per_page=100"`
returns it, the pages' arrays one after another. Pull requests among them are skipped.

The output maps each issue number to the pull requests its Development field holds, each as its
repository, number and state. A field that could not be read is reported and the run exits 1: an
unread field is missing evidence, never an empty link set.

The query travels to the tracker by file. A GraphQL variable is a literal dollar sign, which this
workspace's shell rules deny, so a query composed as an argument cannot be sent at all. Building
that file by hand for one initiative costs a call per issue; building it here costs one call per
batch of --batch issues.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

QUERY = """  {alias}: issue(number: {number}) {{
    number
    closedByPullRequestsReferences(first: 50) {{
      nodes {{ number state repository {{ nameWithOwner }} }}
    }}
  }}"""


def pages(path: str) -> list:
    """A paginated REST response: JSON arrays written one after another."""
    text, decoder, items, i = Path(path).read_text(), json.JSONDecoder(), [], 0
    while True:
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            return items
        page, i = decoder.raw_decode(text, i)
        items.extend(page)


def issues_only(path: str) -> list[dict]:
    return [i for i in pages(path) if 'pull_request' not in i]


def query_file(repo: str, numbers: list[int], path: Path) -> Path:
    owner, name = repo.split('/')
    body = '\n'.join(QUERY.format(alias=f'i{n}', number=n) for n in numbers)
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
    parser.add_argument('--issues', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--query-out', default='links-query.graphql')
    parser.add_argument('--batch', type=int, default=90)
    parser.add_argument('--no-run', action='store_true')
    args = parser.parse_args()

    numbers = [i['number'] for i in issues_only(args.issues)]
    if not numbers:
        sys.exit('no issues in the supplied collection')

    links, unreadable = {}, []
    for start in range(0, len(numbers), args.batch):
        batch = numbers[start:start + args.batch]
        path = query_file(args.repo, batch, Path(args.query_out))
        if args.no_run:
            print(f'query written: {path}')
            continue
        repository = read_batch(path)
        for n in batch:
            node = repository.get(f'i{n}')
            if node is None:
                unreadable.append(n)
                continue
            links[str(n)] = [
                {'repo': p['repository']['nameWithOwner'], 'number': p['number'], 'state': p['state']}
                for p in node['closedByPullRequestsReferences']['nodes']
            ]

    if args.no_run:
        return 0
    Path(args.out).write_text(json.dumps(links, indent=2, sort_keys=True) + '\n')
    print(f'{len(links)} issue(s) read, {sum(len(v) for v in links.values())} link(s)')
    for n in unreadable:
        print(f'issue {n}: Development field unreadable')
    return 1 if unreadable else 0


if __name__ == '__main__':
    sys.exit(main())
