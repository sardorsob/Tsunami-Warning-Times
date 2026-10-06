# Shared audit figure review

Canonical run: `artifacts/eda/shared/2026-10-05-final`, implementation `c98a9c2`.
Review scope: three generated diagnostics, not public/mobile story scenes.

## Deterministic checks

Ran the trusted figure renderer through evident-charts `check_chart.py` in a
scratch location. Report preset: three figures, zero failures, four warnings.
Three warnings concern text below 12 px when shrunk to 600 px width (minimum
7.6 px); use at least 1000 px for this analytical preview. The fourth is a
source-prefix heuristic: the early-waveform footer names NOAA/NCEI and
NOAA/PMEL/NCTR but does not start with `Source:`. No source is absent.

## Fresh image-only Checker

One fresh-context round at 1000 px: no P0/P1 findings. The reviewer saw only the
three PNGs, user request and report destination. Recovered messages agree with
diagnostic scope and the approximate-versus-exact timing distinction.

Scores (story / honesty / polish / fit): setting status 4/5/4/5;
DART candidates 4/5/4/4; early-crossing check 5/5/5/5.

Retained P2/P3 follow-ups before standalone publication:

- Improve the Saipan count's readability against its hatch.
- Consider omitting unused legend categories (the present fixed vocabulary
  deliberately makes failed outcome types visible).
- Print candidate ranges directly when exact near-origin times are the message;
  CSV and the early-crossing panel currently provide the detailed evidence.
- Add event identity/date to each independently circulated figure. In this
  report the shared caption is: **2011 Tōhoku; reviewed USGS origin
  2011-03-11 05:46:24.120 UTC**. Config and source contract retain that reference.

The image-only reviewer did not certify computed values, source accuracy, CVD
measurements or data exclusions. The separate scientific Checker verifies those
data paths. No reviewed chart is promoted as an app asset by this receipt.
