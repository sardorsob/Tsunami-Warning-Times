# Artifacts

`provenance/` contains tracked source and processing evidence. Large generated
figures and tables belong under ignored `generated/` paths until a task curates
them. `logs/runs/` holds compact, portable run bundles; keep metadata and small
evidence tracked while referencing large inputs/outputs by checksum and location.

Every reportable artifact must record its producing command, Git commit, input
source IDs and checksums, output checksum, units, CRS/time basis where relevant,
and review disposition. Generated artifacts are never hand-edited.

For T-002, each meaningful execution writes
`logs/runs/<YYYY-MM-DD__HHMM__tag__gitsha>/` containing `meta.json`,
`config.json`, `inputs.json`, `outputs.json`, `metrics.json`, and `notes.md`.
The acquisition, data-quality, and EDA summaries are rendered into the canonical
Markdown report paths named in `context/TASKS.md`.
