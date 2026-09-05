# Project Instructions

This repository supports a PacificVis 2027 scientific visual story. It is a
research and communication artifact, not an operational warning system.

## Start here

Before changing data, analysis, narrative state, or visualization code, read:

1. `context/PROJECT.md`
2. `context/HANDOVER.md`
3. `context/DECISIONS.md`
4. the active block in `context/TASKS.md`
5. the directly relevant scientific contract or research note

For hazard or geospatial work, follow the Catastrophe Modeling & GeoAI workflow
profile and select one narrow domain skill for the current stage. Repository or
pipeline changes also use the geospatial SWE standards. Do not stack unrelated
skills or tools.

## Non-negotiable scientific rules

- The historical tsunami remains unresolved until the feasibility gate in
  `docs/research/feasibility.md` is accepted and a decision is recorded.
- Keep modeled arrival, observed first deviation, maximum wave, bulletin issue,
  public alert, and evacuation times as separate fields and concepts.
- Never call rupture-to-arrival duration “actionable warning time” without
  evidence for the alert or warning-system timestamps being compared.
- Record source URL, publisher, retrieval date, terms, version, checksum,
  units, temporal reference, datum, CRS, coordinate order, processing, and
  missingness. Use the explicit value `unknown` instead of a blank.
- Never overwrite a CRS, infer a vertical datum, or repair/drop spatial records
  silently. Log input/output counts and rejected records.
- Distinguish zero from NoData. Treat the antimeridian explicitly. Use UTC for
  internal timestamps only after each source time basis is verified.
- Generated data and figures are rebuilt by scripts and are not hand-edited.
  Raw downloaded scientific data stays out of Git unless its license, size, and
  reproducibility support committing it.

## Scope and implementation rules

- Keep every file under `context/`, including intentionally empty placeholders.
  Do not prune a context file because it has no content; `context/.gitignore`
  re-includes all descendants so they remain eligible for version control.
- Keep the first release to one event, one modeled arrival field, a small
  observational chain, four to six communities, one primary projection, one
  story clock, and one guided experience.
- Do not add a backend, live warning feed, machine-learning or Bayesian model,
  MapLibre/deck.gl, 3D globe, or elaborate audio without an evidence-backed
  decision in `context/DECISIONS.md`.
- Prefer static preprocessing and native browser features. Add D3, WebGL, or a
  scroll library only when the first data proof or interaction requires it.
- Keep narrative state explicit and deterministic. One module owns time.
  Renderer-specific code stays separate from React layout.
- Essential meaning must work without hover, sound, or animation. Support
  keyboard, touch, mobile, reduced motion, and a non-WebGL fallback.

## Verification

Run the smallest relevant checks, and run the full gate before handing off:

```bash
uv run ruff check .
uv run pyright
uv run pytest -q
uv run python -m pipeline.provenance artifacts/provenance/source-manifest.csv
npm run check
```

Do not commit, push, deploy, publish, or download large datasets unless the user
has authorized that action. Record observed verification evidence in
`context/HANDOVER.md`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
