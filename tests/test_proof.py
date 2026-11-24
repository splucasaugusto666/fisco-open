import unittest
from fisco_open.engine import calculate, evidence, compare
from fisco_open.factor_r import factor_r
from fisco_open.proof import bind, verify_envelope
from test_engine import BASE
from test_factor_r import BASE_R

class ProofEnvelope(unittest.TestCase):
    def test_replay_and_rule_binding(self):
        for result in (calculate(BASE), factor_r(BASE_R)):
            p = bind(result)
            self.assertEqual(p["rule"]["id"], result["rule_id"])
            self.assertEqual(verify_envelope(p), {"integrity": True, "binding": "match"})

    def test_tampered_rule(self):
        p = bind(calculate(BASE))
        p["rule"]["source"]["provision"] = "fabricated"
        self.assertEqual(verify_envelope(p)["integrity"], False)
        p.pop("envelope_sha256")
        p["envelope_sha256"] = evidence(p)
        self.assertEqual(verify_envelope(p)["binding"], "mismatch")

    def test_rehashed_calculation(self):
        p = bind(calculate(BASE))
        c = p["calculation"]
        c["estimated_das_brl"] = "0.00"
        c.pop("evidence_sha256")
        c["evidence_sha256"] = evidence(c)
        p.pop("envelope_sha256")
        p["envelope_sha256"] = evidence(p)
        self.assertEqual(verify_envelope(p)["binding"], "invalid_calculation")

    def test_unsupported_version(self):
        p = bind(calculate(BASE))
        p["schema"] = "future"
        p.pop("envelope_sha256")
        p["envelope_sha256"] = evidence(p)
        self.assertEqual(verify_envelope(p)["binding"], "unsupported_version")

    def test_original_unchanged(self):
        record = calculate(BASE)
        p = bind(record)
        record["estimated_das_brl"] = "0.00"
        self.assertEqual(verify_envelope(p)["binding"], "match")

    def test_reject_non_rule_comparison(self):
        s = {"name":"synthetic","revenue":"100","costs":"10","expenses":"0","taxes":"1","other_obligations":"0","implementation_cost":"0","eligibility_confirmed":True}
        with self.assertRaises(ValueError):
            bind(compare([s]))
