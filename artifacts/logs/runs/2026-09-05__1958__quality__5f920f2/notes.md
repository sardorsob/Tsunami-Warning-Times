# Normalization and data-quality run notes

## Disposition

Ready for independent scientific-data review. The two offline builds are
byte-identical and all input assets passed their recorded SHA-256 gates.

## Adaptive finding

The first profile found `9999.00000` in named DART measurement fields. No
publisher documentation found during the source audit establishes its precise
meaning. The pipeline therefore does not relabel it as NoData: it quarantines
all 90 affected source rows as `unexpected_sentinel`, retains their source and
line identity in `rejected_record.csv`, and rebuilds the candidate tables.

## Limits

The NCTR continuous field remains blocked without a proxy. NCTR scalar source
coefficients are coverage evidence only. Saipan and Valparaíso remain blocked,
and Pago Pago has both null values and an incomplete requested time window.
Unknown horizontal and vertical datums remain explicit rather than inferred.
