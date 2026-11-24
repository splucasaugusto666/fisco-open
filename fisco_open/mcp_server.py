"""Optional local stdio MCP adapter. No filing, network services or eligibility inference."""
from typing import Any
from mcp.server.fastmcp import FastMCP
from .engine import calculate, compare
from .factor_r import factor_r
from .rules import describe
from .proof import bind, verify_envelope
from . import __version__

server = FastMCP("FISCO OPEN")

def _run(fn, *args):
    try:
        return {"ok": True, "result": fn(*args)}
    except (ValueError, TypeError, KeyError, ArithmeticError):
        # Do not echo confidential inputs into errors.
        return {"ok": False, "error": "invalid_or_unsupported_input",
                "instruction": "Check required fields, externally confirmed conditions and historical 2025 scope. Do not infer an amount or eligibility."}

@server.tool()
def get_coverage() -> dict[str, Any]:
    """Return actual experimental scope before calculating; never imply current legal coverage."""
    return {"engine_version": __version__, "status": "research_preview",
            "period": "2025", "annexes": ["I","II","III","IV","V"],
            "bands_per_annex": 4, "maximum_rbt12_brl": "1800000",
            "official_parity": False, "professional_validation": False,
            "limitations": ["No 2026 calculation", "No automatic eligibility", "Annex IV DAS excludes employer CPP"]}

@server.tool()
def calculate_historical_tax(inputs: dict[str, Any]) -> dict[str, Any]:
    """Historical 2025 partial gross DAS estimate. Pass exact engine fields: period, annex, rbt12, revenue, assumptions. Decimal strings only. All six scope confirmations must be supplied explicitly; never invent them."""
    return _run(calculate, inputs)

@server.tool()
def classify_historical_factor_r(inputs: dict[str, Any]) -> dict[str, Any]:
    """Classify 2025 factor R with period, fs12, rbt12r and both explicit scope/history confirmations."""
    return _run(factor_r, inputs)

@server.tool()
def compare_financial_scenarios(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    """Rank externally supplied, externally confirmed admissible scenarios by net income. Same periods and no duplicate costs; no regime recommendation."""
    return _run(compare, scenarios)

@server.tool()
def describe_tax_rule(rule_id: str, period: str) -> dict[str, Any]:
    """Retrieve descriptive experimental rule metadata for an exact ID and ISO date."""
    return _run(describe, rule_id, period)

@server.tool()
def bind_tax_evidence(calculation: dict[str, Any]) -> dict[str, Any]:
    """Bind a replayable historical calculation to descriptive rule metadata; no legal attestation."""
    return _run(bind, calculation)

@server.tool()
def verify_tax_evidence(envelope: dict[str, Any]) -> dict[str, Any]:
    """Reproduce a rule-bound envelope; match is computational consistency, not truth or authenticity."""
    return _run(verify_envelope, envelope)

def main():
    server.run(transport="stdio")

if __name__ == "__main__":
    main()
