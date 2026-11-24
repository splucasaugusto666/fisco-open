import unittest
from decimal import localcontext
from fisco_open.factor_r import factor_r
from fisco_open.engine import calculate, evidence
from test_engine import BASE

BASE_R = {'period':'2025-11-01','fs12':'28000','rbt12r':'100000',
          'confirmed_subject_to_factor_r':True,'confirmed_full_12_month_history':True}

class FactorR(unittest.TestCase):
    def test_threshold(self):
        for fs, annex in [('27999.99','V'),('28000','III'),('28000.01','III')]:
            with self.subTest(fs=fs):
                self.assertEqual(factor_r(dict(BASE_R,fs12=fs))['annex'],annex)
    def test_zero_cases(self):
        for fs,rb,ratio,annex in [('0','0','0.01','V'),('1','0','0.28','III'),('0','1','0.01','V')]:
            r=factor_r(dict(BASE_R,fs12=fs,rbt12r=rb))
            self.assertEqual((r['factor_r'],r['annex']),(ratio,annex))
    def test_reject(self):
        for key,value in [('period','2026-01-01'),('fs12','-1'),('rbt12r','NaN'),('confirmed_subject_to_factor_r',False),('confirmed_full_12_month_history',False)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                factor_r(dict(BASE_R,**{key:value}))
    def test_evidence_and_context(self):
        with localcontext() as ctx:
            ctx.prec=3
            r=factor_r(dict(BASE_R,fs12='27999.99'))
        self.assertEqual(r['annex'],'V')
        digest=r.pop('evidence_sha256'); self.assertEqual(digest,evidence(r))
    def test_annex_golden(self):
        for annex,expected in [('III','9830.00'),('IV','7885.00')]:
            r=calculate(dict(BASE,annex=annex))
            self.assertEqual(r['estimated_das_brl'],expected)
            if annex=='IV': self.assertTrue(any('CPP' in x for x in r['limitations']))
