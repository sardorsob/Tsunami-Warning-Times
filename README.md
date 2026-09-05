# Pacific Tsunami Warning Time

One tsunami crosses a shared ocean, but bathymetry, geography, observation, and
warning systems leave Pacific communities with radically different amounts of
usable time.

This repository is the research, data, and browser-experience workspace for a
PacificVis 2027 visual data story. The intended result is a guided scientific
narrative: begin with a naive distance-only ring, reveal a bathymetry-shaped
modeled arrival field, compare it with DART and tide-gauge observations, and
then explain what those timings do—and do not—say about community warning time.

## Current status

The repository is in the **feasibility phase**. No historical event, station,
community set, or travel-time product is yet an accepted project fact. See the
[feasibility research](docs/research/feasibility.md), [project contract](context/PROJECT.md),
and [handover](context/HANDOVER.md) before beginning implementation.

The current browser shell deliberately displays that unresolved state. It does
not contain a simulated wave, operational warning information, or reportable
scientific result.

## Local setup

Requirements:

- Python 3.12
- Node.js 24.18.0 (pinned because the test and build toolchain has a narrower
  support range than Vite alone)
- `uv` 0.11.26
- npm 11.16.0

```bash
uv sync
npm install
```

Start the browser shell:

```bash
npm run dev
```

Run the repository gate:

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
npm run check
```

## Repository map

```text
app/                    React, TypeScript, and Vite browser experience
artifacts/              Generated outputs and provenance records
context/                Scope, decisions, scientific contracts, tasks, handover
data/                   Ignored raw/interim/processed working data
docs/                   Public concept, competition, methods, and research notes
pipeline/               Reusable Python pipeline code
public/data/             Generated, web-ready static assets
tests/                  Python contract and pipeline tests
```

Start with [AGENTS.md](AGENTS.md) for repository rules. The data pipeline remains
intentionally dependency-light until the event feasibility and source-format
checks determine which geospatial libraries are actually needed.

## Safety and interpretation

This project is retrospective research and visual communication. It must not be
used for real-time tsunami detection, forecasting, evacuation, or emergency
decision-making. Follow official local authorities for current warnings.

## License

No repository license has been selected. Do not assume reuse rights for project
code, narrative, or derived assets until the owner records that decision.
