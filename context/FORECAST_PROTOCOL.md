# Historical Event Protocol

## Purpose

Define how an authoritative modeled arrival product will be compared with a
retrospective observation set. This is an event-intelligence protocol, not an
operational forecast protocol.

## Required definitions before execution

- selected event identity and origin;
- model or travel-time product identity, producer, run/issue time, processing
  level, spatial support, units, datum, and uncertainty;
- whether the modeled product was available before arrivals or reconstructed
  afterward;
- observation sensor, sample interval, quality flags, time basis, datum, and
  arrival-pick rule;
- community selection rule and any alert/bulletin source used;
- distance-only reference equation and assumptions;
- residual convention: modeled arrival minus observed arrival, unless a recorded
  decision changes it.

## Comparison sequence

1. Freeze source records and checksums.
2. Validate event identity, time bases, units, CRS, coordinate order, and datums.
3. Create the distance-only reference independently of the modeled field.
4. Extract modeled values at station/community locations with a documented
   interpolation rule.
5. Obtain or reproduce observed arrival picks without inspecting model residuals
   to tune the method.
6. Compare paired values and preserve missing or rejected cases.
7. Review residuals, spatial hard cases, uncertainty, and alternative definitions.
8. Export only accepted fields and labels to the browser artifact.

## Stop conditions

Stop if event identity, time zone, units, CRS/order, vertical datum, product
availability timing, arrival definition, terms, or uncertainty that could reverse
the finding is unknown or contradictory.
