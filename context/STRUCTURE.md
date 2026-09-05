# Repository Structure

| Path | Owner and rule |
| --- | --- |
| `app/` | Static React/TypeScript story; no secrets or scientific source parsing |
| `pipeline/` | Reusable, typed Python transformations and validation |
| `scripts/` | Thin command-line entry points; no unique scientific logic |
| `notebooks/` | Thin marimo EDA views over reusable pipeline outputs |
| `config/` | Reviewed, portable source/run configuration without secrets |
| `tests/` | Python behavior, data contracts, and spatial/temporal invariants |
| `data/raw/` | Ignored source cache; immutable after download |
| `data/interim/` | Ignored checkpoints with accounting and provenance |
| `data/processed/` | Ignored analysis-ready outputs |
| `public/data/` | Ignored generated web assets; never hand-edit |
| `artifacts/provenance/` | Tracked source inventory, contracts, and evidence |
| `artifacts/generated/` | Ignored generated figures/tables until explicitly curated |
| `artifacts/logs/runs/` | Portable run metadata, metrics, notes, and decisions |
| `graphify-out/` | Tracked durable knowledge graph/report; local extraction state ignored |
| `docs/` | Public-facing competition, concept, methodology, and research notes |
| `context/` | Canonical scope, decisions, tasks, validation, handover, and Markdown result reports; retain empty placeholders |

Large or awkward scientific formats are transformed into compact static web
assets. Any generated artifact that becomes reportable must be indexed here or
in a later artifact index with its producing command and source-manifest IDs.
