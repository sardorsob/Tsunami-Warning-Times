# Missingness profile run notes

This is the first bounded T-002D EDA slice. It distinguishes source blanks,
absent expected timestamps, structural not-applicable fields, deliberate
quarantine, unknown metadata, and whole-asset unavailability. It performs no
imputation, timestamp snapping, arrival picking, or station promotion.

Pooled MCAR is not supported by the observed station/time concentration. MAR is
only a possible conditional analysis assumption; MNAR cannot be excluded without
publisher outage, telemetry, maintenance, or QC evidence.
