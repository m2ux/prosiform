"""Measure actual corpus inventories, matrices and bounded assignment coverage."""

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_common import cell_index, write_json
from audit_dispatch import packet, packet_content, plan_assignments
from audit_inventory import inventory
from audit_state import gate
from audit_surface import save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', required=True)
    parser.add_argument('--engine', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out)
    budgets = {'context_tokens': 258400, 'reserve_tokens': 20000, 'safety_tokens': 30000,
               'output_tokens': 12000, 'work_seconds': 600, 'slots': 3, 'bytes_per_token': 1,
               'calibration': {'map': {'output_tokens_per_item': 80, 'seconds_per_item': 2,
                                       'evidence': 'Bounded structural sizing experiment; no semantic execution claim'}}}
    results = []
    for name, target in (
            ('mvw', 'corpus/specimens/mvw'),
            ('routine-conformance', 'corpus/specimens/routine-conformance/routines/measured-pass.yaml')):
        started = time.monotonic()
        state = inventory(args.corpus, args.engine, {'paths': [target]}, 'specimen-coordinator')
        assert {row['type'] for row in state['rows'].values()} == {'workflow', 'activity', 'routine', 'technique'}
        assert any(row['kind'] == 'relationship' for row in state['rows'].values())
        assert any('/routines/' in row['source'] for row in state['rows'].values())
        if name == 'routine-conformance':
            sites = [row for row in state['rows'].values() if
                     row.get('relationship', {}).get('address', '').startswith('instance/')]
            assert any('/counting/' in row['address'] or '/counting/' in
                       row.get('relationship', {}).get('address', '') for row in sites)
            assert len({tuple(row['sources']) for row in sites}) > 1
            assert any(row['origin'] == 'consumer' and '/activities/' in row['source']
                       for row in state['rows'].values())
        run = out / name
        # Both specimens receive all four required documents and full cell views.
        save(state, run)
        initial = gate(state)
        assert not initial['mapping_ready'] and not initial['complete']
        assert initial['unknown'] == initial['rows'] * initial['criteria']
        planned = plan_assignments(state, 'map', budgets)
        owned = [item for job in planned['assignments'] for item in state['assignments'][job]['items']]
        assert len(owned) == len(set(owned)) and set(owned) == set(cell_index(state))
        index = cell_index(state)
        for job in planned['assignments']:
            assignment = state['assignments'][job]
            payload = packet_content(state, assignment, index)
            size = len(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True).encode())
            assert size <= assignment['estimate']['input_tokens_estimate'] * budgets['bytes_per_token']
        packet(state, planned['assignments'][0])
        save(state, run)
        result = {'specimen': name, 'target': target, 'snapshot': state['snapshot'],
                  'corpus_revision': state['identity']['corpus'], 'engine_revision': state['identity']['engine'],
                  'rows': len(state['rows']), 'criteria': len(state['criteria']), 'cells': len(owned),
                  'types': dict(Counter(row['type'] for row in state['rows'].values())),
                  'dispatch': planned, 'elapsed_seconds': round(time.monotonic() - started, 3),
                  'audit_complete': False, 'scope': 'Structural corpus qualification; semantic cells remain unresolved'}
        results.append(result)
        print(json.dumps({key: value for key, value in result.items() if key != 'dispatch'}), flush=True)
        print(json.dumps({key: value for key, value in planned.items() if key != 'assignments'}), flush=True)
    write_json(out / 'results.json', results)


if __name__ == '__main__':
    main()
