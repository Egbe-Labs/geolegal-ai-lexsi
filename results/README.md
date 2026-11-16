# Results status

`geolegal_baseline_test.json` is the first actual Tiny Aya inference produced in Google Colab. It is preserved unchanged as an **exploratory smoke test**, not a held-out evaluation prediction and not a validated benchmark result.

Its outer artifact is valid JSON. Its `response` uses the legacy `DECISION:/EXPLANATION:` text format rather than the current structured JSON contract. The deterministic extractor recognizes the closed label for pipeline compatibility, but the artifact is permanently excluded from scored metrics because it has no reviewed scenario ID or legally reviewed answer key.

`baseline_predictions.jsonl` is populated only by executing the Colab baseline notebook. `baseline_metrics.json` must report no scored items until evaluation answer keys are `LEGAL_REVIEWED`.
