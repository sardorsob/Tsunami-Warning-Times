# Independent shared EDA and data-proof review

Date: 2026-10-05. Checker: independent Codex agent
`arrival_final_checker`, separate from the Maker. Primary lane: retrospective
event intelligence. Review process: direct Workflow Core scientific/code review,
with `geo-data-engineering`, `swe-devops-standards`, and `evident-charts`.

## Disposition

**ACCEPT the descriptive and diagnostic T-002D audit. REVISE the data proof for
physical-arrival comparisons.** No Critical or Important implementation finding
remains after the corrections below. This acceptance does not validate a tsunami
onset, promote a station/community, or unblock story Stage B.

Reviewed implementation: `16e4c23..c98a9c2`, concentrating on the shared audit
and its corrective commits. The previously reviewed Stage A atlas was not
re-reviewed. Final evidence is `artifacts/eda/shared/2026-10-05-final`; its
implementation SHA is `c98a9c2`, and `context/EDA_RUN.json` explicitly selects it.
The scientific summary is identical to the corrected `2026-10-05-2e29de3`
summary; the final changes repair a figure annotation and canonical-viewer
selection. The earlier exploratory artifacts remain superseded evidence.

## Independent verification

- Read the frozen protocol, five-task implementation plan, T-002D/T-002E task
  blocks, and data, spatial, forecast, and validation contracts. Queried Graphify
  before tracing the source implementation.
- Final focused command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest
  -q -p no:cacheprovider tests/test_eda.py tests/test_eda_report.py
  --basetemp=/tmp/arrival-final-checker-c98a9c2` — **19 passed in 5.16 s**.
  The notebook needs a local kernel socket; the first sandboxed export was
  blocked by `PermissionError` at socket bind, and the authorized local-socket
  rerun passed. This was an execution restriction, not a notebook defect.
- The integration check independently rebuilt two scratch bundles and verified
  byte-identical outputs, overwrite refusal, and the populated notebook. Its
  stale-folder fixture verifies selection through the canonical pointer.
- Recomputed every final bundle checksum: **28/28 inputs** and **24/24 stable
  outputs** match. All **62 raw-trace records** match their archived path and
  one-based raw line exactly. The canonical Markdown is byte-identical to the
  final report. The MLflow receipt names run
  `6e42c1bfb21a49c8be204cda94c0c386`; the tracking receipt is explicitly outside
  the deterministic manifest.
- Reconciled **10 stations, 160 event/control settings, 143,655 accepted
  observations, 4,380 contour parts, and 62,988 vertices**. No sensitivity CSV
  cell is blank. Every station modeled-arrival field is `unavailable`; every
  physical-arrival state remains unvalidated or unsupported raw water level.

The coordinator owns the full repository gate, final clean-tree evidence,
MLflow store reconciliation, release creation, and canonical task updates.
This Checker independently ran the focused gate above, not the entire frontend
and Python repository gate.

## Source traces and scientific interpretation

1. **DART 21418's early candidate is supported as a threshold crossing only.**
   In `data/raw/ncei/dart/dart21418_20110301to20110320_meter.txt`, line 1895
   records 05:48:30 UTC and residual -0.00535 m; line 1896 records 05:48:45 UTC,
   source time `70.242188`, and residual 0.02200 m. Against the frozen
   two-hour median -0.02156 m and 0.03 m threshold, the centered excursion is
   0.04356 m. Line 1900 supports confirmation at 05:49:45. The candidate is
   140.88 seconds after the verified origin; the eight settings span
   140.88–155.88 seconds. The
   [NOAA NCTR event page](https://nctr.pmel.noaa.gov/honshu20110311/), independently
   opened on 2026-10-05 and present in the checksummed cached HTML, describes
   first tsunami recording at this buoy at approximately 25 minutes. The
   early crossing must not become a physical-arrival claim. Neither its cause
   nor a replacement exact arrival timestamp is established here.
2. **DART 32401's failed support screen is justified despite stable picks.**
   Raw file `dart32401_20110301to20110320_meter.txt` lines 1292 and 1294 record
   2011-03-11 09:59 and 10:15 UTC. Line 1293 contains `9999.00000` in the raw
   and residual fields at 10:00 and is the normalized rejection
   `dart-32401-line-001293`. The retained interval is 960 seconds, exceeding
   the frozen 900-second limit. The later candidate's local bracket does not
   erase that earlier gap; `earlier_support_complete` is false and its screen
   fails even though its setting spread is only 210 seconds.
3. **Saipan's baseline rejection follows the unsnapped source timestamps.**
   `data/raw/ntwc/saipan/saip_A_2011.070` lines 298 and 299 retain
   `20110311045159` and `20110311045400`, a 121-second interval. It exceeds the
   frozen 120-second maximum inside the event baseline. The first setting's
   support score is 0.966528, but the separate maximum-gap criterion fails.
   All eight event settings remain ineligible; none is silently dropped.
4. **Valparaíso's source extremes and flags remain visible.** Independent
   counting in `data/raw/ioc/valparaiso/valp_rad_20110311_20110314.json` finds
   140 flagged rows. The 0 m record at 2011-03-12 01:30 has `out_of_range=T`;
   the 6.222 m maximum at 06:20 has `exceeded_neighbours=T`. They remain in
   descriptive profiles while QC flags exclude them from detector use. Zero
   is not silently reclassified as missing.

## Strengths

Accepted accounting anchors the processed tables, and accepted source hashes
anchor all 17 acquired raw assets. The blocked continuous NCTR field remains in
the 18-asset denominator. Duplicate/orphan/semantic checks precede analysis.
All eight event settings and eight disjoint controls survive for every station.
Baseline and search support, early gaps, blanks, and explicit bad QC flags have
separate effects; incomplete controls cannot establish a quiet window.

The detector consumes no modeled arrival. Coastal raw levels remain unsupported
controls, and no nearest-contour extraction, datum inference, imputation,
timestamp snapping, or station selection was introduced. Candidate, lower
sampling bound, confirmation, source time, and event elapsed time are separate.
Staged publication refuses an existing bundle. The notebook displays generated
evidence rather than owning a second calculation path.

## Findings resolved during review

- **Important — false residual disagreement counts.** Original
  `pipeline/eda_audit.py:64`–69 used binary subtraction and a strict 0.00002 m
  boundary, reporting 8 + 8 + 3 + 212 = 231 exceedances. Independent decimal
  arithmetic on all four DART station tables found a maximum exactly
  0.00002 m and zero strict exceedances. The corrected comparison at
  `pipeline/eda_audit.py:64`–74 and its regression test resolve the finding.
  All final profiles now report zero exceedances; no detector setting changed.
- **Minor — unavailable search statistics became blank/zero.** Original early
  baseline returns omitted `search_max_gap_seconds`, yielding 12 empty CSV
  cells, while an unevaluated search had coverage 0. Initialization at
  `pipeline/eda.py:143`–144 now uses `unknown`, and the CSV writer at
  `pipeline/eda_report.py:39` supplies explicit missing-field values. Final
  sensitivity output contains no blank cells.
- **Minor — waveform annotation crossed the peak.** The intermediate 21418
  waveform ran through its NOAA-reference label. Data-derived headroom and
  annotation positions at `pipeline/eda_report.py:199`–215 resolve the
  collision in the final rendered PNG. The approximate reference remains
  explicitly distinguished from an exact pick.
- UTF-8 text reads were made explicit. The final canonical pointer also avoids
  choosing an old run merely because its directory sorts last; the populated
  notebook regression test verifies this behavior.

## Presentation caveats and declined judgments

The Checker viewed the two initial PNGs and the intermediate/final waveform.
Recovered message: these are diagnostic crossings, and a stable early crossing
can conflict with independent tsunami evidence. Final waveform labels are
legible at native size and do not collide with the signal. The coordinator's
separate image-only review owns the additional fresh visual pass.

The trusted scratch-renderer chart check on final code reports **3 figures,
0 failures, 4 warnings** at the 600-pixel report preset: small text in each
figure (smallest 7.6 pixels), plus a source-prefix warning for the waveform.
The waveform actually names NOAA/NCEI and NOAA/PMEL/NCTR in its footer, so the
last warning is a checker syntax convention, not missing attribution. The
small-text warning is real: these diagnostic figures need sufficiently wide
display or larger text before use as compact publication/mobile figures.
This is a **Minor remaining presentation limitation** of the restricted audit,
not permission to claim publication readiness. CSV alternatives remain present.

This review declines to certify physical tsunami onsets, the early signal's
cause, calibrated arrival uncertainty, maximum waves, absolute cross-datum
levels, public-warning performance, modeled-minus-observed residuals, final
community selection, or story Stage B. Their required source/method/uncertainty
gates are not met. A passing screen is not manual scientific validation.
Publication/redistribution terms and a new model extraction method were not
re-adjudicated; prior restrictions remain in force.

The release interface must therefore allow descriptive source/coverage/geometry
and diagnostic inspection only, explicitly set arrival-comparison permission
false, and retain the approximate-reference conflict and presentation caveats.
Existence of a release file must not be treated as arrival capability.
