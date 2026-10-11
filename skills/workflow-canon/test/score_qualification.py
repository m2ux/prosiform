"""Reconcile completed live-agent findings with the blinded fixture reference.

Source-location matching records which independently confirmed finding covers
each planted construct; it does not replace the independent semantic judgment.
"""

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_common import digest, read_json, write_json
from audit_state import gate


def covers(finding, expected, state):
    criterion = state['criteria'][expected['criterion']]
    entries = {criterion['title']}
    if expected['criterion'].startswith('ap:'):
        entries.add(expected['criterion'].removeprefix('ap:'))
    elif expected['criterion'].startswith('dp:'):
        entries.add(re.sub(r'^\d+\.\s+', '', criterion['title']))
    # Both forms name the exact captured entry; an ordinal alone is insufficient.
    if finding['entry'] not in entries:
        return False
    location = finding['location']
    if expected['source'] not in location:
        return False
    if expected['category'] == 'whole-element-invariant':
        return True
    if expected['address'] in location:
        return True
    match = re.search(re.escape(expected['source']) + r':(\d+)', location)
    return bool(match and expected['lines'][0] <= int(match[1]) <= expected['lines'][1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    base = Path(args.out).resolve()
    reference = Path(__file__).resolve().parent / 'fixtures/audit-qualification/expected-outcomes.json'
    assert digest(reference.read_bytes()) == read_json(base / 'reference-identity.json')['expected_sha256']
    expected = read_json(reference)
    results = []
    for case in read_json(base / 'coordinator-cases.json'):
        state = read_json(Path(case['run']) / 'audit-state.json')
        status = gate(state)
        assert status['complete'], case['run'] + ': incomplete current coverage'
        assert set(state['criteria']) == set(expected['criteria'])
        outcomes = expected['findings'] if case['fixture'] == 'seeded' else []
        matches = {item['id']: [finding['id'] for finding in status['findings']
                               if covers(finding, item, state)] for item in outcomes}
        assert all(len(ids) == 1 for ids in matches.values()), (case['run'], matches)
        matched = [ids[0] for ids in matches.values()]
        assert len(set(matched)) == len(matched) == len(status['findings']), case['run']
        results.append({'run': str(Path(case['run']).relative_to(base)),
                        'snapshot': state['snapshot'], 'complete': True,
                        'rows': status['rows'], 'criteria': status['criteria'],
                        'cells': status['cells'], 'applicable': sum(
                            value['status'] == 'A' for value in state['mappings'].values()),
                        'findings': len(status['findings']), 'conformance': status['conformance'],
                        'reference_matches': matches})
    write_json(base / 'qualification-results.json', {
        'reference_sha256': digest(reference.read_bytes()), 'cases': results,
        'scope': 'Controlled four-criterion live qualification; full-canon semantic audits are separate.'})
    print(len(results), 'complete cases reconcile to the fixed reference')


if __name__ == '__main__':
    main()
