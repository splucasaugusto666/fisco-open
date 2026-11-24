"""Rule-bound evidence envelope; not a signature or legal attestation."""
import argparse
import hmac
import json
from pathlib import Path
from .engine import evidence
from .verify import verify
from .rules import describe, PROTOCOL
from . import __version__

SCHEMA = "fisco-open/evidence-envelope/0.1"

def bind(record):
    """Bind a replayable historical calculation to its descriptive rule revision."""
    result = verify(record)
    if result != {"integrity": True, "replay": "match"}:
        raise ValueError("A matching deterministic replay is required")
    if record.get("status") not in ("experimental_estimate", "historical_experimental_classification"):
        raise ValueError("Only rule-backed historical calculations can be bound")
    rule = describe(record["rule_id"], record["inputs"]["period"])
    envelope = {"schema": SCHEMA, "engine_version": __version__, "rule_protocol": PROTOCOL,
                "calculation": record, "rule": rule,
                "limitations": ["Rule metadata is experimental, not a verified historical legal snapshot",
                                "No professional validation, official parity, signature or input attestation"]}
    # Copy the record so callers cannot alter the returned envelope through the original object.
    envelope = json.loads(json.dumps(envelope, ensure_ascii=False, allow_nan=False))
    return {**envelope, "envelope_sha256": evidence(envelope)}

def verify_envelope(record):
    if not isinstance(record, dict):
        raise ValueError("Expected envelope object")
    payload = dict(record)
    digest = payload.pop("envelope_sha256", None)
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid envelope digest")
    if not hmac.compare_digest(digest, evidence(payload)):
        return {"integrity": False, "binding": "not_attempted"}
    if payload.get("schema") != SCHEMA or payload.get("engine_version") != __version__ or payload.get("rule_protocol") != PROTOCOL:
        return {"integrity": True, "binding": "unsupported_version"}
    try:
        expected = bind(payload["calculation"])
    except (ValueError, TypeError, KeyError, ArithmeticError):
        return {"integrity": True, "binding": "invalid_calculation"}
    return {"integrity": True, "binding": "match" if hmac.compare_digest(expected["envelope_sha256"], digest) else "mismatch"}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["bind", "verify"])
    p.add_argument("file", type=Path)
    a = p.parse_args()
    try:
        if a.file.stat().st_size > 5 * 1024 * 1024:
            raise ValueError("Input exceeds 5 MiB")
        record = json.loads(a.file.read_text(encoding="utf-8"))
        out = bind(record) if a.command == "bind" else verify_envelope(record)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if a.command == "bind" or out["binding"] == "match" else 2
    except (OSError, ValueError, TypeError, KeyError, ArithmeticError):
        print(json.dumps({"error": "Invalid or unsupported evidence"}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
