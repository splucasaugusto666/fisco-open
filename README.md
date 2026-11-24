# FISCO OPEN

**Pay what you owe. Never more.**

Independent experimental Brazilian tax intelligence and profit simulation. Not affiliated with Receita Federal. [Português](README.pt-BR.md).

## Quickstart (Python 3.10+, no runtime dependencies)

```sh
python -m fisco_open calculate examples/commerce.json
python -m fisco_open compare examples/scenarios.json
python -m fisco_open upstream
python -m unittest discover -s tests -v
```

Version `0.1.0a1` — research preview, not a tax filing tool. Historical 2025 estimates for ordinary domestic single-revenue Simples scenarios, Annexes I, II and V, first four bands only. Eligibility and scope conditions must be confirmed externally. No PGDAS-D parity, no current-year or professional validation. Scenario ranking uses supplied amounts, not inferred eligibility. No unknown taxes represented as zero.

## Official RTC integration

Two local HTTP adapters, tested against mock services only. See [upstream guide](docs/upstream.md) for pinned references and actual service instructions. The upstream response is deliberately marked unvalidated; the deployed commit is not attested. DANFSe is inventoried but not implemented. No official source code is bundled.

## Architecture

```text
JSON inputs → scope validation → Decimal estimate → evidence digest
           → hypothetical financial comparison → evidence digest
           → loopback RTC HTTP adapter → unvalidated upstream response
```

Evidence digests detect changes to serialized records; they do not prove correctness or identity. Keep inputs local; output includes sensitive inputs when supplied. Never publish real tax records.

## Roadmap

- Independent accountant review, verified current-period rules, annex III/IV and revenue segregation.
- Run pinned official services, validate request/response schemas and add differential fixtures.
- Expand geography/regimes, reform simulation, rule specification, API and MCP.

MIT; see LICENSE and NOTICE. Contributions with official sources and reproducible tests welcome. No official endorsement implied.
