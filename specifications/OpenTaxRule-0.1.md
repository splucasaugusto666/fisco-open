# OpenTaxRule Protocol 0.1 — experimental registry

## Motivation and prior art
Rules as Code predates this project. See OECD, *Cracking the code* (2020), https://www.oecd.org/en/publications/cracking-the-code_3afe6ba5-en.html and the EU interoperability discussion https://interoperable-europe.ec.europa.eu/collection/eugovtech/document/rules-code-open-approach. OpenFisca is an established precedent; this registry does not claim scientific novelty or compatibility. Our narrower research question: can an independently inspectable rule description link a bounded Brazilian tax estimate to source, coverage and reproducible tests without mistaking software scope for statutory validity?

## Contract
Each entry identifies a rule, protocol version, revision, jurisdiction, regime, kind, implementation status, inclusive **software-supported** date interval, source URL and provision, conditions, whitelisted operator and parameters, exclusions and test references. The supported interval is not a representation of the full legal validity interval. Source URLs point to official consolidated texts; historical immutable snapshots have not been verified. No arbitrary code execution, eval or executable expressions from documents. Only the existing Python operators are used. This is a descriptive view over the existing tables, not an independent validation or a standalone DSL interpreter.

Lookup requires exact ID and ISO date. Missing, ambiguous or unsupported requests fail closed. Rule digest is SHA-256 of the record serialized with the current engine's sorted-key, compact UTF-8 JSON convention. It is not a digital signature or a normative text hash. Released alpha evidence is unchanged; this registry adds a separately retrievable rule digest. The original evidence does not embed it.

## Usage
```sh
python -m fisco_open.rules
python -m fisco_open.rules --id BR-SN-I-2025-1 --period 2025-11-01
python -m unittest discover -s tests -v
```

## Research gates
1. Capture official historical source snapshots and record access dates and document digests.
2. Separate statutory validity, implementation coverage, and review dates. Preserve superseded rules; disallow overlapping applicable versions without explicit precedence.
3. Establish independent legal review; run official differential fixtures. A hash or passing test alone does not establish legal correctness.
4. Bind immutable rule revisions to versioned evidence with backward compatibility.
5. Measure coverage by supported operations, dates and jurisdictions, not just count of entries.
6. Evaluate portability against established rules-as-code tools before claiming interoperability.

The initial 21 entries cover 20 partial Simples bands and one factor R classification, historical 2025 only. No new tax calculation or 2026 coverage is introduced.
