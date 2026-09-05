# Tōhoku Data Pipeline and EDA Design

- Date: 2026-09-04
- Tier: Full
- Primary lane: retrospective event forecast/intelligence
- Domain owner: geospatial data engineering
- Review state: approved by project owner on 2026-09-05

## Outcome

Build a reproducible data-proof workflow for the provisional 11 March 2011
Tōhoku event. The workflow will acquire the broad source set requested by the
project owner, preserve raw evidence and provenance, normalize only interpretable
records, run inspectable exploratory analysis, and publish every conclusion and
next action in Markdown.

This work proves whether the event and source bundle can support the later visual
story. It does not yet freeze the event, select story communities, or produce an
operational-warning claim.

## Approved choices

- Include the NCTR field and six coastal-gauge candidates in the initial proof,
  in addition to USGS metadata, NCEI TTT contours, and four DART records.
- Put reusable acquisition, transformation, validation, and analysis logic in
  ordinary Python modules.
- Keep command-line entry points thin and independently runnable.
- Use a marimo notebook as an inspectable, reactive view over analysis-ready
  artifacts. The notebook must not own unique transformations.
- Generate canonical Markdown reports containing evidence, results,
  interpretation, limitations, takeaways, and next steps.
- Track meaningful EDA runs in both a portable file bundle and project-local
  MLflow. Deterministic download/ETL steps require run bundles but not separate
  MLflow runs.

## Source boundary

The first proof owns only these source classes:

| Source class | Planned coverage | Promotion requirement |
| --- | --- | --- |
| Event identity | Reviewed USGS machine record | Exact event ID, origin, coordinates, depth, precision, terms, checksum |
| Travel-time contours | NCEI TTT layer 17 | Query, feature count, `HOURS`, EPSG:4326 metadata, coordinate order, validity, antimeridian review |
| Model field | NCTR Tōhoku source/field | Exact asset, variables, units, grid, time step, longitude convention, coefficients, processing level, terms |
| Open-ocean observations | Four DART stations | Two near-field and two far-field records chosen before residual inspection; station identity, coordinates, cadence, UTC, gaps, units, datum notes |
| Coastal observations | Six candidate communities | Saipan, Adak, one Hawaiʻi station, Crescent City, Pago Pago, and one Chilean station; exact station IDs and raw URLs resolved before acquisition |

A source may be downloaded yet remain quarantined. Only records whose identity,
terms, units, time basis, spatial reference, datum implications, and missingness
are adequate for the intended comparison may enter analysis-ready outputs.

## Architecture

The smallest maintainable implementation is a script-first Python package with
one thin notebook:

```text
config/tohoku-data-proof.toml
pipeline/acquisition.py
pipeline/normalize.py
pipeline/eda.py
scripts/acquire_tohoku.py
scripts/build_tohoku_data.py
scripts/run_tohoku_eda.py
notebooks/tohoku_eda.py
tests/fixtures/
tests/test_acquisition.py
tests/test_normalize.py
tests/test_eda.py
```

Begin with one acquisition module. Split source adapters into separate modules
only when incompatible protocols or formats make the single file difficult to
test. Configuration uses TOML so Python 3.12 can read it without another parser.

The marimo notebook reads the same processed tables and metric artifacts used by
the report generator. Opening it never triggers network downloads. Expensive or
mutable work stays behind explicit command-line steps.

## Data flow

```text
authoritative endpoint
  -> source discovery and contract review
  -> atomic raw download in data/raw/
  -> checksum and provenance record
  -> source-specific parse and quarantine
  -> normalized tables in data/interim/
  -> validated analysis-ready artifacts in data/processed/
  -> reusable EDA functions
  -> marimo views + compact figures/tables
  -> Markdown reports + run bundle + MLflow EDA record
  -> independent scientific review
```

Raw, interim, processed, and local MLflow storage remain outside Git. Small
schemas, run metadata, metrics, rejection summaries, reports, and curated figures
may be tracked when their task accepts them.

## Canonical records

Normalized data will expose explicit grains instead of a single mixed table:

- `source_asset`: one row per retrieved file or API response;
- `ttt_contour`: one feature per source contour part with `hours` and geometry;
- `model_field_index`: one row per NCTR variable/grid/time asset before any
  optional array-to-table reduction;
- `station`: one row per deployment or gauge identity;
- `observation`: one row per station sample, retaining source time and derived
  UTC separately;
- `arrival_pick`: one row per station, method configuration, and sensitivity run;
- `rejected_record`: one row per rejected asset, feature, station, or sample with
  a stable reason code.

Keys, units, temporal reference, coordinate order, CRS, vertical reference,
NoData representation, and missingness are mandatory schema metadata. Unknown
values remain explicit and block affected comparisons.

## Acquisition behavior

- Use HTTPS endpoints from approved provenance rows only.
- Apply finite timeouts and bounded retries to transient failures.
- Download to a temporary file, validate non-empty content and expected media or
  signature, compute SHA-256, then atomically move it into the raw cache.
- Never overwrite an existing raw asset whose checksum differs. Quarantine and
  report the conflict.
- Record request parameters, response metadata, byte count, retrieval time,
  checksum, and local path.
- Treat every source independently. A blocked NCTR field must not erase valid TTT
  or observation evidence, but it blocks claims requiring the field.
- Unit tests use local fixtures. Live endpoint checks are explicit integration
  commands and never run implicitly in the normal unit-test suite.

## Normalization and quality gates

Each stage writes accounting evidence: input, accepted, rejected, and output
counts. The quality report covers:

- event/source identity and cross-source consistency;
- schema, types, grain, keys, duplicates, and unexpected sentinel values;
- source and UTC time ranges, monotonicity, cadence changes, gaps, and precision;
- station identifiers, deployment coordinates, coordinate order, and coverage;
- CRS, geometry types, validity, empty geometry, extent, contour values, and
  antimeridian behavior;
- model variables, dimensions, grid orientation, units, time step, NoData, and
  longitude convention;
- water-level raw/fitted/residual fields, units, vertical-reference notes,
  missingness, and robust outliers;
- join coverage and any many-to-many expansion;
- per-source terms and redistribution status.

No CRS, datum, unit, or timestamp is guessed. Repair is deterministic, recorded,
and limited to cases justified by source documentation.

## EDA contract

The EDA is descriptive and diagnostic. It will produce:

1. a dataset and source inventory with success/quarantine coverage;
2. TTT contour counts, `HOURS` distribution, spatial extent, multipart structure,
   and geographic spot checks;
3. NCTR variable/dimension/grid/time summaries and field usability findings;
4. per-station temporal coverage, cadence segments, gaps, missingness, and robust
   water-level summaries;
5. raw/fitted/residual agreement checks where all fields exist;
6. arrival-pick sensitivity across predeclared baseline, threshold, persistence,
   and gap-handling settings;
7. manually checked picks independent of modeled residuals;
8. source-distance, modeled arrival, observed first deviation, uncertainty, and
   join coverage for candidate locations;
9. counterexamples and hard cases, not only visually appealing pairs; and
10. a promote, revise, or reject recommendation for Tōhoku and each source class.

The first pass is a fixed core profile. After that pass, an EDA decision ledger
records the finding that raised each new question, the follow-up check chosen,
its evidence, and its disposition. This makes the exploration adaptive without
making it outcome-driven: gaps, cadence shifts, outliers, geometry behavior, and
source conflicts may branch the analysis, while station selection and baseline
arrival-pick settings stay frozen before modeled residuals are inspected.

Arrival-pick parameters are frozen before model residuals are inspected for
selection. Sensitivity analysis may compare methods, but the chosen method cannot
be optimized to make the model look accurate.

## Markdown and run artifacts

Three intentionally empty canonical report files are created during planning:

- `context/ACQUISITION_REPORT.md`
- `context/DATA_QUALITY_REPORT.md`
- `context/EDA_REPORT.md`

Their producing scripts will populate them only when the owning task runs. Every
populated report includes the command, run ID, Git SHA, input source IDs and
checksums, output checksums, counts/rates, findings, interpretation, limitations,
takeaways, unresolved questions, and next steps.

Each meaningful execution also writes
`artifacts/logs/runs/<YYYY-MM-DD__HHMM__tag__gitsha>/` with `meta.json`,
`config.json`, `inputs.json`, `outputs.json`, `metrics.json`, and `notes.md`.
The EDA task records the same run ID, parameters, metrics, artifacts, data
references, Git SHA, and disposition in project-local MLflow.

## Dependencies and deliberate deferrals

Dependencies are pinned only after T-002A confirms the real file formats. The
likely minimum is pandas/numpy for tables, xarray plus the demonstrated NetCDF
engine for the NCTR field, Shapely/pyproj for geometry checks, matplotlib or
Altair for figures, marimo for the notebook, and MLflow's smallest sufficient
local package for the experiment ledger.

DVC, a workflow engine, PostGIS, distributed compute, a backend, and cloud
storage are deferred. Add DVC only if measured size, mutability, or collaboration
makes URL-plus-checksum reconstruction inadequate.

## Verification

- TDD for acquisition, parsing, normalization, quality rules, and EDA metrics.
- Synthetic and tiny recorded fixtures cover malformed responses, time/cadence
  boundaries, NoData/zero, geometry/coordinate order, antimeridian cases,
  duplicate keys, and partial-source failure.
- Two identical runs must produce matching checksums for deterministic outputs.
- `marimo check` and a headless notebook execution must pass.
- Generated Markdown must reconcile with machine-readable metrics.
- Three contours, all ten observation records, and at least three reported values
  receive manual source checks.
- Ruff, Pyright, Pytest, provenance validation, frontend checks, and Graphify
  update remain green.
- An independent scientific reviewer must accept T-002E before T-003 begins.

## Commit boundaries

1. Planning/context/specification commit.
2. Tested acquisition and source-contract implementation commit.
3. Acquired/normalized evidence and data-quality report commit, excluding raw
   and bulky processed data.
4. EDA, marimo, Markdown results, and reviewer-accepted handoff commit.

Push, publication, deployment, large unbounded downloads, and source-contact
messages remain separately authorized actions.
