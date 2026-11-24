# Evidence Envelope 0.1

An additive protocol linking a deterministic historical calculation to the corresponding OpenTaxRule descriptive revision. The alpha calculation format and public tag are unchanged. The envelope includes schema, engine version, rule protocol, full original calculation, full rule metadata and limitations. SHA-256 covers the canonical serialized payload (sorted keys, compact separators, UTF-8); the envelope digest itself is excluded.

Verification first checks integrity, then rebuilds the envelope from a fresh deterministic replay and date-specific rule lookup. An altered rule with a recalculated digest fails binding. Unknown versions are not silently accepted. Economic comparisons and external RTC responses are excluded because they are not supported rule-backed calculations.

Usage:
```sh
python -m fisco_open calculate examples/commerce.json > calculation.json
python -m fisco_open.proof bind calculation.json > envelope.json
python -m fisco_open.proof verify envelope.json
```

A successful binding demonstrates consistency with the installed engine and descriptive registry, not authenticity, legal correctness, historical source snapshot verification or official parity. A different engine can manufacture consistent records; independent signatures, immutable versioned source archives and professional review are future requirements. Inputs and results can contain private fiscal data; never publish real envelopes.
