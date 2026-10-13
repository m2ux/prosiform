"""Prepare blinded live-agent runs and reconcile their actual typed returns."""

import argparse
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'scripts'))
from audit_common import digest, read_json, write_json
from audit_dispatch import packet, plan_assignments
from audit_inventory import inventory
from audit_state import bind, gate
from audit_surface import main as cli, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('init', 'refresh', 'plan', 'submit', 'status'))
    parser.add_argument('--out', required=True)
    parser.add_argument('--engine')
    parser.add_argument('--round', type=int, default=1)
    parser.add_argument('--mode', choices=('author', 'audit', 'all'), default='all')
    parser.add_argument('--phase', choices=('map', 'inventory', 'verify', 'evaluate', 'obligations'))
    parser.add_argument('--actor')
    parser.add_argument('--receipts')
    args = parser.parse_args()
    out = Path(args.out).resolve()
    fixtures = HERE / 'fixtures' / 'audit-qualification'
    if args.operation == 'init':
        cases = []
        for repeat in (1, 2):
            for mode in ('author', 'audit'):
                for label, fixture in (('a', 'clean'), ('b', 'seeded')):
                    run = out / f'round-{repeat}' / f'{mode}-{label}'
                    root = fixtures / fixture
                    spec = {**read_json(root / 'scope.json'), 'qualification_mode': mode, 'repeat': repeat}
                    state = inventory(root, args.engine, spec, '/root')
                    save(state, run)
                    command = [sys.executable, str(fixtures / 'check.py'), str(root), args.engine]
                    check = subprocess.run(command, capture_output=True, text=True)
                    output = run / 'fixture-guard.txt'
                    output.write_text(check.stdout + check.stderr)
                    assert check.returncode == 0, output.read_text()
                    write_json(run / 'check-observation.json', {'command': command, 'cwd': str(HERE),
                                                               'exit_code': check.returncode, 'output': str(output)})
                    cases.append({'run': str(run), 'round': repeat, 'mode': mode,
                                  'fixture': fixture, 'cells': len(state['rows']) * len(state['criteria'])})
        write_json(out / 'coordinator-cases.json', cases)
        write_json(out / 'reference-identity.json', {'expected_sha256': digest((fixtures / 'expected-outcomes.json').read_bytes()),
                                                   'scope': 'Controlled four-criterion live-agent qualification, separate from real corpus conformance'})
        print(json.dumps(cases, indent=2))
        return
    cases = [case for case in read_json(out / 'coordinator-cases.json')
             if case['round'] == args.round and (args.mode == 'all' or case['mode'] == args.mode)]
    if args.operation == 'refresh':
        for case in cases:
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                assert cli(['refresh', '--run', case['run']]) == 0
        print(json.dumps({'refreshed': len(cases)}))
    elif args.operation == 'plan':
        assert args.actor and args.phase
        budgets = {'context_tokens': 258400, 'reserve_tokens': 20000, 'safety_tokens': 30000,
                   'output_tokens': 16000, 'work_seconds': 600, 'slots': 1, 'bytes_per_token': 1,
                   'calibration': {args.phase: {'output_tokens_per_item': 256, 'seconds_per_item': 3,
                                              'evidence': 'Initial required-work pilot caps. Measure the first assignment before releasing the remainder; host context comes from session token telemetry.'}}}
        calibration = out / 'calibration.json'
        if calibration.exists() and args.phase in read_json(calibration):
            budgets['calibration'][args.phase] = read_json(calibration)[args.phase]
        queue = []
        for case in cases:
            run = Path(case['run'])
            state = read_json(run / 'audit-state.json')
            plan = plan_assignments(state, args.phase, budgets)
            for job in plan['assignments']:
                bind(state, job, args.actor)
            save(state, run)
            for job in plan['assignments']:
                destination = run / 'packets' / args.phase / (job + '.json')
                write_json(destination, packet(state, job))
                queue.append({'run': str(run), 'packet': str(destination), 'phase': args.phase,
                              'mode': case['mode'], 'assignment': job, 'actor': args.actor,
                              'check_observation': str(run / 'check-observation.json') if args.phase == 'obligations' else None})
        path = out / f'round-{args.round}' / f'{args.mode}-{args.phase}-queue.json'
        write_json(path, queue)
        print(json.dumps({'queue': str(path), 'assignments': len(queue)}, indent=2))
    elif args.operation == 'submit':
        assert args.receipts
        submitted = []
        for path in sorted(Path(args.receipts).glob('*.json')):
            wrapper = read_json(path)
            run = wrapper.pop('run')
            assert any(case['run'] == run for case in cases), 'Receipt belongs to another case'
            accepted = Path(run) / 'worker-results' / wrapper['assignment'] / (wrapper['attempt'] + '.json')
            if accepted.exists():
                assert read_json(accepted) == wrapper, 'Immutable receipt content changed'
                continue
            receipt = out / 'incoming' / path.name
            write_json(receipt, wrapper)
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                result = cli(['submit', '--run', run, '--receipt', str(receipt)])
            if result:
                raise RuntimeError(str(path) + ': receipt rejected')
            submitted.append({'file': str(path), 'assignment': wrapper['assignment'], 'actor': wrapper['actor']})
        write_json(out / f'round-{args.round}' / f'{args.mode}-submission-latest.json', submitted)
        print(json.dumps({'submitted': len(submitted)}, indent=2))
    else:
        print(json.dumps([{**case, 'status': gate(read_json(Path(case['run']) / 'audit-state.json'))}
                          for case in cases], indent=2))


if __name__ == '__main__':
    main()
