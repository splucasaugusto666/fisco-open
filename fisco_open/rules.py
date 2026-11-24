"""OpenTaxRule 0.1: descriptive registry for the existing historical engine.
Not an interpreter for arbitrary legislative expressions or an official rule source.
"""
import argparse
from copy import deepcopy
from datetime import date
import json
from .engine import TABLE, LIMITS, ASSUMPTIONS, SOURCE, evidence
from .factor_r import SOURCE as FACTOR_SOURCE

PROTOCOL = "0.1"
START, END = "2025-01-01", "2025-12-31"

def catalog():
    rows = []
    for annex, bands in TABLE.items():
        for i, (rate, deduction) in enumerate(bands):
            rows.append({
                "id": f"BR-SN-{annex}-2025-{i+1}",
                "protocol": PROTOCOL, "revision": 1,
                "jurisdiction": "BR", "regime": "Simples Nacional",
                "kind": "gross_das_estimate", "status": "experimental",
                "supported_from": START, "supported_through": END,
                "source": {"url": SOURCE, "provision": f"LC 123/2006 art. 18, Annex {annex}",
                           "historical_text_snapshot_verified": False},
                "conditions": {"annex": annex, "rbt12_gt": str(LIMITS[i-1]) if i else "0",
                               "rbt12_lte": str(LIMITS[i]), "required_confirmations": list(ASSUMPTIONS)},
                "calculation": {"operator": "gross_das_v1", "nominal_rate": rate, "deduction_brl": deduction,
                                "rounding": "final_cent_half_up"},
                "exclusions": ["special treatments", "revenue segregation", "allocation parity",
                               "professional validation", "current-period coverage"] + (
                               ["employer CPP outside DAS"] if annex == "IV" else []),
                "tests": ["tests/test_botbench.py", "tests/test_rules.py"]
            })
    rows.append({
        "id": "BR-SN-FATOR-R-2025", "protocol": PROTOCOL, "revision": 1,
        "jurisdiction": "BR", "regime": "Simples Nacional",
        "kind": "factor_r_classification", "status": "experimental",
        "supported_from": START, "supported_through": END,
        "source": {"url": FACTOR_SOURCE, "provision": "Res. CGSN 140/2018 art. 26; LC 123 art. 18",
                   "historical_text_snapshot_verified": False},
        "conditions": {"required_confirmations": ["confirmed_subject_to_factor_r",
                                                  "confirmed_full_12_month_history"]},
        "calculation": {"operator": "factor_r_v1", "threshold": "0.28",
                        "zero_both_or_payroll_only_zero": "0.01", "zero_revenue_positive_payroll": "0.28"},
        "exclusions": ["activity eligibility", "partial history", "professional validation", "current-period coverage"],
        "tests": ["tests/test_factor_r.py", "tests/test_rules.py"]
    })
    return sorted(rows, key=lambda x: x["id"])

def describe(rule_id, period):
    if not isinstance(period, str) or len(period) != 10:
        raise ValueError("Expected ISO date YYYY-MM-DD")
    d = date.fromisoformat(period)
    if d.isoformat() != period:
        raise ValueError("Noncanonical date")
    found = [r for r in catalog() if r["id"] == rule_id and r["supported_from"] <= period <= r["supported_through"]]
    if len(found) != 1:
        raise ValueError("Unknown rule, unsupported period or ambiguous match")
    rule = deepcopy(found[0])
    return {**rule, "rule_sha256": evidence(rule)}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--id")
    p.add_argument("--period")
    a = p.parse_args()
    if bool(a.id) != bool(a.period):
        p.error("--id and --period must be used together")
    try:
        result = describe(a.id, a.period) if a.id else {"protocol": PROTOCOL, "rules": catalog()}
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
