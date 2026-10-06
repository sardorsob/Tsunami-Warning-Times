# Independent Stage A Checker review

Date: 2026-10-05

Checker: independent `stage_a_checker` agent; Maker work reviewed at `16e4c23`.

Task: T-003A, preliminary diagnostic atlas only. No T-002D implementation,
arrival result, community promotion, paper output, or public scene was reviewed.

Initial disposition: **needs-fix** for the populated Marimo viewer (R1). The scientific
atlas and portable evidence are accepted within preliminary diagnostic scope.
Acceptance is not a publication-chart or production-scene approval.

## R1 — Populated notebook renders no visible content

The notebook passes `marimo check` and its HTML export exits successfully, but
the populated export contains eight cells with empty `text/plain` output.
`title_view`, `selector_view`, `boundary_view`, `figures_view`, and `decision_view`
are assigned and returned as dependency values without a display expression.
Consequently the title, selector, evidence warning, four figures, and decision
ledger are not visible. The empty-state callout works because `mo.stop` emits it;
that does not prove populated-state rendering.

Evidence: scratch session file
`/tmp/tsunami-stage-a-checker.J1dOdz/viewer/__marimo__/session/tohoku_storyboard_eda.py.json`.

Required fix: display the already-built views through one final layout cell or
explicit display expressions, and verify populated exported output actually
contains the selected run, four images, and ledger. Preserve the notebook's
read-only boundary. Recheck after the Maker fix before marking T-003A done.

## Reproducibility and provenance

Canonical atlas: `artifacts/eda/story/2026-09-16__0351__story-atlas__6c35d78/`.
Canonical bundle: `artifacts/logs/runs/2026-09-16__0351__story-atlas__6c35d78/`.

Independent scratch run:
`2026-10-05__stage-a-independent-checker__16e4c23`, local scratch MLflow run
`80eb00a42fa34add9026d732c828fd5d`.

All ten input file hashes and eleven portable output hashes reconcile with
files on disk. All eight independently rebuilt media files are byte-identical.
The decision ledger, inputs, configuration, and metrics are byte-identical.
Per-artifact manifest fields match after excluding only output paths,
generating command, and the distinct Checker Git identity.

| Artifact | SHA-256 |
| --- | --- |
| Pacific map PNG | `a3ec2a5206bc5593dae727a1003e5b1abbe6d49b156543755db454e046426fea` |
| Pacific map SVG | `d089a001dda9532ceb874fa42079c7d43971cb1d2ada93bca4cb3d9cf271f407` |
| Coverage PNG | `991e4d64bc615388b36949400a423f78c6568e4b30c3a0ef7ed7e6a8c9021dca` |
| Coverage SVG | `306132709fdc3dcbcd5d7c84322cab862e6f131307f8acb4d3ffba4fa98c3d70` |
| Station signals PNG | `48fd2793a08f012f9714f3a8ed6b814614cfd1ed2a8dac2aba91b7cd1f5f3482` |
| Station signals SVG | `a8bb88f4878d0d2cbb8eb52fe2d610e29b00b44e15c69630b0bf4f6a001efffe` |
| Distance/contour PNG | `9ed1767ab65b425e09fb243cdeabb29dd773a51f07f7a03528aabd7ca55c40a7` |
| Distance/contour SVG | `64d0ac653736f5776d728f9aa87ed2deba2fcfa0dcb16e763f0de46b2ec9684e` |

Observed metrics: ten stations; 143,655 source observations; 24,729 plotted
numeric points; 23,040 coverage-grid positions and 120 separate off-grid samples;
4,380 published contour parts; map 4,514 input and 4,543 output line parts;
distance comparison 885 input and 916 output parts; six range rings and nine
selected contour-hour classes. No arrival picks or residual comparison occur.

Independent source traces agree with the plotted geography: event latitude/
longitude `38.297, 142.373`; Hilo `19.7303, -155.0556`; Valparaíso
`-33.02767128, -71.62787275`. Source contour parts for hours 1, 6, and 24 are
8, 74, and 57. The normalized-source units and unknown station datums remain
explicit; positions support descriptive mapping, not inferred datum precision.

Coverage traces agree: Hilo 29/4,320 unavailable (99.3287% coverage), Pago Pago
1,319/4,320 (69.4676%), Saipan 796/1,440 strict unavailable (44.7222%) with 120
off-grid observations (53.0556% density). An independent scan of Saipan numeric
source observations confirms the maximum interval is 39,660 seconds, between
2011-03-11 12:07 and 23:08 UTC.

## Rendered-image review and chart checker

Skills applied: `cartography-geoviz`, `evident-charts` critique route, and
`marimo-notebook`; Workflow Core, Data Science, and Catastrophe profiles read.
Domain lane: retrospective event description; no forecast or loss estimate.

All four canonical PNGs were opened and inspected. Recovered messages match
their preliminary diagnostic questions:

- Pacific map: an event and mixed observational chain span the basin; projection
  is Pacific-centered Equal Earth, seam-spanning artifacts are absent, and the
  caption explicitly excludes a continuous field. The Tōhoku labels collide.
- Coverage: records differ in continuity and missingness mechanism; Saipan and
  Pago Pago dominate the visible gaps. Saipan's 24-hour source window differs
  from the other panels' 72-hour windows, with its own date ticks; bar length
  must not be interpreted as a common elapsed duration in a future public scene.
- Station signals: retained source points expose gaps and outliers. Coastal raw
  levels and DART residuals are labeled separately; local scales and the footer
  forbid amplitude comparisons. Saipan's gap stays open; no line bridges it.
- Shape diagnostic: geodesic ring shape differs from published contour shape.
  Panels use the same projection and extent, and explicitly state incompatible
  units, no speed conversion, and no station arrival assignment.

`evident-charts/scripts/check_chart.py` executed trusted scratch plotting code
with output confined to `/tmp`, using its `report` preset (600 px display width).
It reported **23 failures and 30 warnings**, not a clean chart-quality pass:

- 3 text-overlap failures: event versus DART 21418 on the basin map, and Crescent
  City 9419750 versus DART 46411 in both shape panels.
- 13 text-on-line failures across the spatial plots, including station labels
  on contextual coastlines/contours.
- 6 plot-area-height failures for the six coverage strips (7% of canvas each
  versus the generic 8% threshold). These strips encode time/status only; there
  is no quantitative vertical comparison, so this is a documented diagnostic
  layout exception rather than a scientific defect.
- 1 contour-contrast failure: effective basin contour contrast 1.45:1 against
  the background. Contextual linework is muted deliberately, but future scenes
  making the contours the message require stronger contrast.
- Warnings: 4 small-text findings at 600 px, 4 missing-source-label findings,
  4 ambiguous-label findings, 2 direct-label suggestions, 15 contrast warnings,
  and 1 deuteranopia color-distance warning. The latter compares range lines
  with station points, already distinguished by mark type. Source provenance
  exists in adjacent manifest/report metadata; public standalone exports need
  an explicit publisher/dataset source line.

The current approved atlas is analyst-facing exploratory evidence. Its recorded
`branch` disposition explicitly identifies clutter as a result, and no scene is
promoted. Therefore the label, typography, and contextual-contrast findings do
not invalidate the scientific diagnostic. They are mandatory follow-ups before
any affected rendering becomes a public scene. Extend the existing regional-
context branch to cover the Crescent City/DART pair as well as Tōhoku. No claim
is made that the existing figures are readable as complete charts at 600 px or
at thumbnail size. This Checker ran automated CVD checks and full-image review;
it did not repeat the Maker's full simulated-image montage.

## Commands and results

```bash
uv run pytest tests/story -q
uv run python -m pipeline.provenance artifacts/provenance/story-source-manifest.csv
uv run marimo check notebooks/story/tohoku_storyboard_eda.py
```

Results: 27 tests passed; one story source record validated; Marimo static check
passed. The root coordinator owns the final combined full repository gate.

Scratch atlas rebuild (outputs and MLflow remain outside the repository):

```bash
uv run python scripts/story/build_story_atlas.py \
  --processed-dir data/processed/tohoku/2026-09-09-valparaiso-reviewed-7576ffb-a \
  --missingness-config config/tohoku-missingness.toml \
  --missingness-summary artifacts/eda/missingness/missingness-summary.json \
  --coastline data/raw/natural-earth/ne_110m_coastline_v4.1.0.zip \
  --config config/story-atlas.toml \
  --decision-input config/story-atlas-decisions.toml \
  --artifact-dir /tmp/tsunami-stage-a-checker.J1dOdz/artifacts \
  --run-dir /tmp/tsunami-stage-a-checker.J1dOdz/run \
  --report /tmp/tsunami-stage-a-checker.J1dOdz/EDA_REPORT.md \
  --run-id 2026-10-05__stage-a-independent-checker__16e4c23 \
  --git-sha 16e4c23 --working-tree unknown \
  --mlflow-dir /tmp/tsunami-stage-a-checker.J1dOdz/mlruns \
  --mlflow-experiment stage-a-independent-checker

.venv/bin/python /tmp/tsunami-stage-a-checker.J1dOdz/reconcile.py
.venv/bin/python /Users/sobirov/.codex/skills/evident-charts/scripts/check_chart.py \
  /tmp/tsunami-stage-a-checker.J1dOdz/render_for_check.py --dest report --json
```

The rebuild and reconciliation passed. Chart-check exit code 1 has the findings
above. `render_for_check.py` only loads accepted atlas inputs and calls the four
plot functions with scratch output stems; no acquisition, MLflow, or repository
write occurs in the chart checker. A scratch-only reconciliation typo
(`arrival_hours` versus source `hours`) was corrected before its passing run;
the source tables and generated artifacts were never altered.

Notebook validation used an exact copy under a temporary viewer directory and
a read-only symlink to the canonical `artifacts` directory. Both empty and
populated exports exited 0. The empty-state callout appeared; populated output
was empty, producing R1. Exit status alone is insufficient for this criterion.

T-003B remains gated by the accepted shared release and its own scientific and
cartographic review. This receipt does not clear that gate or resolve the
unavailable continuous NCTR field.

## R1 independent recheck and final disposition

Maker fix reviewed at `7b87d6d` on 2026-10-05. The notebook now explicitly calls
`mo.output.replace` for its title, selector, evidence boundary, figure collection,
and ledger views. It retains the read-only boundary and introduces no scientific
calculation or artifact mutation.

The Checker copied the committed notebook to
`/tmp/tsunami-stage-a-recheck.2jTR0s/viewer.py`, linked only the existing canonical
`artifacts` directory, and exported it headlessly:

```bash
.venv/bin/marimo export html \
  /tmp/tsunami-stage-a-recheck.2jTR0s/viewer.py \
  -o /tmp/tsunami-stage-a-recheck.2jTR0s/viewer.html --no-include-code
.venv/bin/pytest tests/story/test_notebook_render.py tests/story/test_dependencies.py -q
.venv/bin/python /tmp/tsunami-stage-a-checker.J1dOdz/reconcile.py
```

The export exits 0. Inspection of actual exported cell outputs, excluding
notebook source, confirms the title, selector label, canonical run ID,
continuous-NCTR limitation, all four canonical figure titles, exactly four
`<img>` elements, and the adaptive decision ledger. There are no error outputs.
The four focused notebook/dependency tests pass. All ten input and eleven
output hashes still reconcile; all eight canonical figure bytes, decision
ledger, stable manifest fields, configuration, and metrics remain unchanged
from the independently rebuilt evidence above. R1 is resolved.

Final independent Checker disposition: **accepted for T-003A's preliminary
diagnostic scope; recommend T-003A `done`**. No blocking scientific or notebook
finding remains. The report-preset chart lint still has the recorded 23
failures and 30 warnings; this acceptance does not describe it as lint-clean.
The regional/label branch, contrast, readable public sizing, source labeling,
and clear handling of unequal coverage windows remain required before public
scene promotion. T-003B still requires its separately accepted shared release
and subsequent scientific/cartographic review.
