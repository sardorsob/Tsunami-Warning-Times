# Shared EDA and scientific closure implementation plan

Authorized by the owner on 2026-10-05: complete T-002D and the reviews T-003A /
T-002E, inline on main, committing each verified unit. No story Stage B or app
implementation is included. Base: 16e4c23.

Spec: docs/superpowers/specs/2026-09-04-tohoku-data-pipeline-eda-design.md.
Scope authority also includes context/FORECAST_PROTOCOL.md, VALIDATION_PLAN.md,
spatial-contract.md, and the approved story Stage A specification.

## Global constraints

Primary lane: retrospective event intelligence; tier Full. Domain skill:
geo-data-engineering for audited shared inputs and release semantics;
analyze-data-quality for adaptive checks; cartography-geoviz and evident-charts
for rendered diagnostics. Superpowers execution/TDD/verification owns process;
Ponytail limits code to the existing pinned stack. Separate independent Checker.

Use accepted normalized bytes and verify their hashes against tracked evidence.
No download, imputation, timestamp snapping, inferred datum, continuous NCTR
proxy, station-to-nearest-contour arrival, or fitted paper model. Every candidate
station stays in denominators. Generated reports and figures come from code.
Freeze diagnostic settings before looking at timing discrepancies. A negative
feasibility finding is a legitimate result; T-002E can close with revise/reject
and a restricted interface, never a fabricated promotion.

### Task 1: Freeze diagnostic protocol and task boundaries

Produce config/tohoku-arrival-audit.toml and docs/research/arrival-audit.md.
Define fields, controls, completeness, sensitivity, precision, and limitations.
Commit before any detector is run on the real event. Interfaces: Task 2 reads
this protocol; Task 4 must report all combinations without optimizing them.
Verification: TOML parsing, protocol/source consistency, git diff --check.
Expected: explicit UTC/event identity and all 10 candidates; no selected result.

### Task 2: Implement shared audit and sensitivity core

Write tests first for checksum mismatch, orphan/duplicate records, gaps,
baseline completeness, persistence, unknown/no-detection, and timestamp
brackets. Implement pipeline/eda.py using existing CSV/UTC validation helpers.
Profile numeric distributions, raw-fit-residual agreement, source-QC flags,
cadence/gap intervals, geometry and joins. Diagnostic detection consumes no
modeled arrival. Interfaces: typed samples and audit results feed Task 3.
Verification: uv run pytest -q; uv run ruff check .; uv run pyright.
Expected: RED on missing behavior, then GREEN; real inputs reconcile unchanged.
Commit: feat(eda): audit timing support and threshold sensitivity.

### Task 3: Add report runner and thin notebook

Write integration tests first for deterministic output, input provenance and
overwrite refusal. Implement scripts/run_tohoku_eda.py and a thin read-only
Marimo view. Produce canonical Markdown, CSV/JSON evidence, control/sensitivity
figures, portable run bundle, and project-local MLflow. Keep raw data ignored.
Interfaces: Task 4 consumes these explicit outputs; Task 5 cites their hashes.
Verification: full Python checks, Marimo check/export, deterministic rerun.
Expected: all tests GREEN; notebook does not recompute or write analysis.
Commit: feat(eda): generate reproducible arrival audit evidence.

### Task 4: Execute and follow findings

Run from a clean implementation SHA. Inspect results and PNGs; investigate
triggered findings (e.g. gaps near candidates, pre-origin crossings, QC outliers,
coastal tides, DART field disagreement). Save the follow-up evidence and adaptive
ledger. Do not silently retune parameters. Trace at least three reported values
back to normalized/raw evidence. Generate all results and disposition text.
Verification: byte-identical stable outputs on second run; full gate; source
checks; chart checker and rendered review. Expected: honest finite results or
explicit unavailable/unsupported states, including negative controls.
Commit: data(eda): record adaptive timing audit results.

### Task 5: Independently review and close with an explicit disposition

The independent Stage A Checker can review the existing atlas while Tasks 1–4
run. A fresh final Checker reviews T-002D and T-002E code/evidence, using the
whole change range, protocol and current limitations. Coordinator handles fixes
and canonical status updates. Build a checksummed release decision describing
allowed consumers/uses and prohibited interpretations; promote arrival evidence
only if every applicable scientific gate passes. T-003B remains blocked on an
actual arrival-capable release. Update all affected context, preserving empty
files, refresh Graphify, run complete gates, commit the result.
Expected: reviewer acceptance or explicit revise/reject, never self-acceptance.
Commit: docs(eda): record independent data-proof disposition.

## Review focus

Candidate crossing versus physical arrival; no finite value for failed gates;
control-window training/test separation; baseline and local gap accounting;
all-station/all-setting denominators; raw coastal tides; unknown datum effects;
cadence changes and quarantined rows; raw-fit-residual consistency; integrity of
frozen input hashes; failure-safe output publication; independent release scope.
