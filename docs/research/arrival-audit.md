# Tōhoku timing audit protocol

Frozen before executing real-data picks on 2026-10-05. Purpose: test whether
the accepted records support reproducible timing, including failure cases.
The ten station IDs remain fixed. All eight settings per station are reported.

## Measurement contract

DART uses the publisher's residual in metres of water column. Coastal records
have no verified tidal residual: median-centered raw metres are run as an
explicitly **unsupported raw-water-level control**, never as a physical arrival.
No polynomial tide fit is extrapolated from the short coastal baseline. No
absolute water levels are compared across datums. The DART residual fit is
retrospective and its fitting window is unknown; it cannot establish real-time
detection or warning lead time.

NOAA describes residual-versus-threshold detection and a 3 cm North Pacific
reference threshold, but its algorithm uses predicted tides at 15-second
sampling. Our archival sensitivity diagnostic is different and does not
reproduce instrument trigger time. Sources checked 2026-10-05:
- https://www.ndbc.noaa.gov/dart/algorithm.shtml
- https://www.ndbc.noaa.gov/dart/system.shtml
- https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/tsunamis/travel-time-maps

## Frozen rules

- Baseline: 2 or 4 hours immediately before earthquake origin; median center
  and 1.4826 × median absolute deviation (MAD), no fitted predictive model.
- Threshold: max(5 × baseline scaled MAD, 0.03 or 0.05 m); both signs count.
- Persistence: 60 or 120 elapsed seconds of consecutive above-threshold valid
  samples; at least two samples. The reported timestamp is the run's first
  sample, with a separate confirmation timestamp. Persistence across accepted
  DART sampling intervals is only sampled persistence, not proof of continuous
  exceedance between readings.
- Baseline gate: at least six valid observations, at least 90% temporal support,
  no interval (including window boundaries) above 900 s for DART or 120 s for
  coastal. Temporal support sums min(interval, 900/60 s) between valid samples
  and both boundaries, divided by baseline duration; this is a support score,
  not an expected-grid completeness rate. Require a recent baseline sample.
- Search: origin to +30 h, retaining only source-supported timestamps. Gaps
  above the declared maximum, retained blanks, and explicit IOC bad flags reset
  persistence. No interpolated sample, threshold crossing, or missing tail.
- Bracket: last below-threshold valid sample to first above-threshold sample,
  only when the intervening interval satisfies the gap rule. Otherwise the
  lower bound is unknown. This is sampling support, not a confidence interval.
- Pre-origin control: apply the identical detector over the last hour before
  origin, estimating its baseline from the preceding 2/4 h. This window is
  disjoint from its fitted baseline. A control crossing rejects automatic
  promotion; absence of one is not validation of a tsunami onset.
  An evaluable quiet window also requires the baseline support/gap criteria
  over the entire search window. Empty or truncated searches are explicitly
  `incomplete_search`. A candidate may be shown despite incomplete later
  coverage, but any earlier invalid sample or excessive gap blocks the screen.
- Sensitivity: retain no-detection and ineligible settings; never compute a
  stable consensus from successful settings alone. All eight must detect, all
  controls must be evaluable and quiet, maximum spread 300 s, and supporting
  interval <= the reported uncertainty. Even then require manual scientific
  validation independent of modeled times before any physical-arrival release.
- Maximum wave is not estimated. Source-distance is WGS84 ellipsoidal distance
  as a descriptive approximation with station horizontal datum unknown; it
  cannot supply speed-derived arrival. Published hourly TTT linework is not a
  station arrival surface. Station modeled arrival therefore stays unavailable
  unless a separate validated extraction method/product is accepted.

## Adaptive sequence and acceptance

Profile first; record observation → question → follow-up → evidence → decision.
Check long DART intervals against quarantined raw-line accounting; compare
raw minus fitted to residual; inspect QC-flagged extremes; inspect candidates
and controls in local windows; retain source time and sample identity. These
findings may reject the method or narrow release scope. Changes to settings
require a new protocol version and explicit exploratory label. They cannot be
selected from modeled agreement. No story/community selection occurs here.

T-002E can accept descriptive source/coverage/geometry evidence while issuing
revise for arrival comparisons. Any restricted release must say so in a
machine-readable allowed-use list; downstream Stage B needs an explicit
arrival-comparison permission, not merely a release file's existence.
