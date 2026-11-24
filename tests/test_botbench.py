"""BOTBench seed: independent rational-arithmetic oracle, not official parity."""
from fractions import Fraction
import unittest
from fisco_open.engine import calculate
from test_engine import BASE

# LC 123/2006, annexes I-V, first four bands. Rates in basis points.
# Source: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm
ROWS = {
    'I': [(400,0),(730,5940),(950,13860),(1070,22500)],
    'II': [(450,0),(780,5940),(1000,13860),(1120,22500)],
    'III': [(600,0),(1120,9360),(1350,17640),(1600,35640)],
    'IV': [(450,0),(900,8100),(1020,12420),(1400,39780)],
    'V': [(1550,0),(1800,4500),(1950,9900),(2050,17100)],
}
LIMIT_CENTS = [0,18000000,36000000,72000000,180000000]


def brl(cents):
    return f'{cents // 100}.{cents % 100:02d}'


class BOTBench(unittest.TestCase):
    def test_all_bands_boundaries(self):
        for annex, rows in ROWS.items():
            for i, (bps, deduction) in enumerate(rows):
                lo, hi = LIMIT_CENTS[i] + 1, LIMIT_CENTS[i+1]
                for rbt in (lo, (lo+hi)//2, hi):
                    for revenue in (0, 1, 1234567, 8000000):
                        with self.subTest(annex=annex, band=i+1, rbt=rbt, revenue=revenue):
                            exact = revenue * (Fraction(bps,10000) - Fraction(deduction*100,rbt))
                            expected = int(exact + Fraction(1,2))
                            result = calculate(dict(BASE,annex=annex,rbt12=brl(rbt),revenue=brl(revenue)))
                            self.assertEqual(result['estimated_das_brl'],brl(expected))
