"""Integrity and deterministic replay, not legal validation or authentication."""
import argparse
import hmac
import json
import re
from pathlib import Path
from . import __version__
from .engine import calculate, compare, evidence
from .factor_r import factor_r


def verify(record):
    if not isinstance(record, dict):
        raise ValueError('Evidence record must be an object')
    payload = dict(record)
    digest = payload.pop('evidence_sha256', None)
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ValueError('Invalid or missing SHA-256 digest')
    if not hmac.compare_digest(digest, evidence(payload)):
        return {'integrity': False, 'replay': 'not_attempted'}
    if payload.get('engine_version') != __version__:
        return {'integrity': True, 'replay': 'unsupported_version_or_external_response'}
    status = payload.get('status')
    try:
        if status == 'experimental_estimate':
            expected = calculate(payload['inputs'])
        elif status == 'historical_experimental_classification':
            expected = factor_r(payload['inputs'])
        elif status == 'hypothetical_comparison':
            expected = compare([s['inputs'] for s in payload['scenarios']])
        else:
            return {'integrity': True, 'replay': 'unsupported_record'}
    except (ValueError, TypeError, KeyError, ArithmeticError):
        return {'integrity': True, 'replay': 'invalid_inputs'}
    return {'integrity': True, 'replay': 'match' if hmac.compare_digest(expected['evidence_sha256'], digest) else 'mismatch'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    args = parser.parse_args()
    try:
        if args.record.stat().st_size > 5 * 1024 * 1024:
            raise ValueError('Record exceeds 5 MiB')
        result = verify(json.loads(args.record.read_text(encoding='utf-8')))
        print(json.dumps(result))
        return 0 if result['replay'] == 'match' else 2
    except (OSError, ValueError, TypeError, ArithmeticError):
        print(json.dumps({'integrity': False, 'replay': 'invalid_record'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
