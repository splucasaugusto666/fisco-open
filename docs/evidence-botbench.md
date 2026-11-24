# Evidence verification and BOTBench seed

Run from the repository root:

```sh
python -m fisco_open calculate examples/commerce.json > evidence.json
python -m fisco_open.verify evidence.json
python -m unittest discover -s tests -v
```

Integrity checks the record's canonical SHA-256 digest. Replay independently reruns the current version of the deterministic application and checks whether the result matches. A modified output whose digest was recomputed can still fail replay. Neither check establishes identity, truth of user-supplied inputs, legal eligibility, or official approval. Historical/unknown engine versions and external RTC responses cannot be replayed by this verifier.

BOTBench seed uses exact rational arithmetic (Fraction) with separate tables, 5 annexes × 4 bands × 3 revenue-history points × 4 monthly revenue values = 240 synthetic subcases. It checks the implemented historical 2025 gross estimate with the specified final-cent rounding; it does not reproduce PGDAS-D allocation or official RTC results. Source: LC 123/2006 art. 18 and annexes I–V. Some synthetic combinations are arithmetic boundary stress cases rather than real company histories. No independent professional review or benchmark against third-party software has been completed.

Local execution: 19 unittest methods passed, including the 240 subcases. Remote CI required before merge.
