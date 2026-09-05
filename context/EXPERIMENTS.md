# Experiment Ledger

No analytical experiment or model run has been conducted. Repository setup,
source-feasibility research, and the data-proof design are not experiments.

When a meaningful run begins, record a file-based run bundle under
`artifacts/logs/runs/<YYYY-MM-DD__HHMM__tag__gitsha>/` with configuration, seeds
where relevant, source/version references, inputs, outputs, metrics, notes, and
the selection or rejection decision.

T-002D is a substantive data-science/EDA run. Record it in project-local MLflow
with the same run ID, parameters, metrics, artifact references, input source IDs
and checksums, Git SHA, and promote/revise/reject disposition. Deterministic
acquisition and normalization runs keep portable bundles only; they do not need
separate MLflow runs.
