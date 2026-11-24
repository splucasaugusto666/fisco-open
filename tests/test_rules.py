import unittest
from fisco_open.engine import calculate, evidence
from fisco_open.factor_r import factor_r
from fisco_open.rules import catalog, describe
from test_engine import BASE
from test_factor_r import BASE_R

class RuleRegistry(unittest.TestCase):
    def test_unique_complete(self):
        rows = catalog()
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), 21)
        self.assertEqual(len(set(ids)), 21)
        self.assertTrue(all(r["status"] == "experimental" for r in rows))
        self.assertTrue(all(not r["source"]["historical_text_snapshot_verified"] for r in rows))

    def test_calculation_binding(self):
        for a in ("I","II","III","IV","V"):
            for rbt in ("1","180001","360001","720001"):
                result = calculate(dict(BASE, annex=a, rbt12=rbt))
                rule = describe(result["rule_id"], BASE["period"])
                self.assertEqual(rule["calculation"]["nominal_rate"], result["nominal_rate"])
                self.assertEqual(rule["jurisdiction"], result["jurisdiction"])
        result = factor_r(BASE_R)
        self.assertEqual(describe(result["rule_id"], BASE_R["period"])["calculation"]["threshold"], result["threshold"])

    def test_temporal_and_unknown(self):
        for id, period in (("BR-SN-I-2025-1","2026-01-01"),("BR-SN-I-2025-1","2024-12-31"),("missing","2025-01-01"),("BR-SN-I-2025-1","20250101")):
            with self.assertRaises(ValueError):
                describe(id, period)

    def test_digest_and_isolation(self):
        rule = describe("BR-SN-IV-2025-1", "2025-12-31")
        digest = rule.pop("rule_sha256")
        self.assertEqual(digest, evidence(rule))
        rule["conditions"]["annex"] = "invalid"
        self.assertEqual(describe("BR-SN-IV-2025-1", "2025-01-01")["conditions"]["annex"], "IV")
