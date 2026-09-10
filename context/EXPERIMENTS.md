# Experiment Ledger

## 2026-09-09 — T-002D missingness slice

- Portable run: `2026-09-09__1749__missingness__7b6d386`
- Git SHA: `7b6d386`; working tree recorded as clean
- MLflow experiment/run: `tohoku-eda` /
  `3ea475f7045e48c9a1a87af913f807e0`; finished successfully in ignored local
  store `.mlflow/mlruns`
- Input fingerprint: `710dc48719a3f6362635b59cff2663887c43c5484ea9d15f6d3d12a4635d97d4`
- Disposition: preliminary missingness slice; retain T-002D as in-progress and
  freeze station selection
- Method: deterministic descriptive profiling with no random seed, imputation,
  timestamp snapping, arrival picking, or model-guided selection
- Result: 1,049 raw-value blanks among 143,655 retained observations; 2,276
  strict unavailable coastal positions among 23,040 expected positions; 2,156
  unavailable positions under the sample-density view; 17 of 18 source assets
  approved
- Artifacts: `context/EDA_REPORT.md`, `artifacts/eda/missingness/`, and the
  six-file portable run bundle
- Decision: pooled MCAR is not supported; causal MAR/MNAR classification remains
  unresolved without publisher evidence

Future meaningful T-002D runs use the same portable-bundle and project-local
MLflow pairing. Deterministic acquisition and normalization runs retain portable
bundles only; they do not need separate MLflow runs.
