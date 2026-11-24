import unittest
from fisco_open.engine import calculate, compare, evidence
from fisco_open.factor_r import factor_r
from fisco_open.verify import verify
from test_engine import BASE
from test_factor_r import BASE_R


class EvidenceVerification(unittest.TestCase):
    def test_replay(self):
        s = {'name': 'synthetic', 'revenue': '100', 'costs': '10', 'expenses': '0', 'taxes': '1', 'other_obligations': '0', 'implementation_cost': '0', 'eligibility_confirmed': True}
        for result in (calculate(BASE), factor_r(BASE_R), compare([s])):
            self.assertEqual(verify(result), {'integrity': True, 'replay': 'match'})

    def test_tampered_and_rehashed(self):
        r = calculate(BASE)
        r['estimated_das_brl'] = '0.00'
        self.assertFalse(verify(r)['integrity'])
        del r['evidence_sha256']
        r['evidence_sha256'] = evidence(r)
        self.assertEqual(verify(r), {'integrity': True, 'replay': 'mismatch'})

    def test_unknown_version(self):
        r = {'engine_version': 'future', 'status': 'experimental_estimate'}
        r['evidence_sha256'] = evidence(r)
        self.assertEqual(verify(r)['replay'], 'unsupported_version_or_external_response')

    def test_malformed(self):
        for r in ([], {}, {'evidence_sha256': 'z' * 64}):
            with self.assertRaises(ValueError):
                verify(r)
