# Initial timing run — exploratory, not accepted

Run `artifacts/eda/shared/2026-10-05-ad040a7` was executed from a clean
implementation checkout. Its frozen 160 event/control outcomes are retained
for auditability, not promoted as physical arrivals.

Review found 231 apparent raw−fit−residual tolerance exceedances caused solely
by binary floating-point cancellation at the 0.00002 m boundary. Independent
exact-decimal checks found zero strict exceedances. The initial report's
exceedance counts are incorrect and must not be cited. A regression-backed
decimal comparison replaces this implementation without changing the tolerance,
detector settings, inputs or observed source values.

Baseline-ineligible rows also serialized uncomputed search maximum gaps as blank
CSV cells. The corrected implementation explicitly emits `unknown`.

The early DART 21418 candidate conflicts with NOAA's approximate 25-minute
tsunami recording description. Follow-up evidence must include the first-hour
waveform and preserve that approximate reference rather than inventing an exact
onset. DART gap interiors and IOC QC extremes also trigger source-level checks.

The canonical report will be regenerated from the corrected committed code.
This initial bundle stays immutable and is excluded from release authority.
Local MLflow run: `cac45b0855954dbe86c7d458ed652481`.
