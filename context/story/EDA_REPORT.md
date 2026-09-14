# Visual-Story EDA Report

## Status

No story EDA run has been executed and no visual finding has been accepted.
The design was approved in conversation on 2026-09-14; its written specification
is awaiting project-owner review. Existing missingness results remain shared
evidence in `context/EDA_REPORT.md` rather than being copied here.

## Reporting contract

This is the canonical interpretation surface for story-only exploratory plots.
Scripts generate factual run sections; reviewers add dispositions through the
documented review workflow. Every plot entry records:

```text
observation -> question -> follow-up -> result -> disposition -> storyboard implication
```

Allowed dispositions are `retain`, `revise`, `branch`, `promote`, and `reject`.
Every entry also names its candidate build or release, command, input and output
hashes, units, projection or time basis, assumptions, limitations, artifact
paths, and reviewer status.

## Current evidence boundary

- Preliminary maps may use the accepted T-002C2 build.
- Published NCEI travel-time contours are not a continuous arrival field.
- Arrival comparisons wait for the shared arrival-pick and T-002E release gates.
- Unknown datum values remain explicit and block incompatible comparisons.
- No paper-only model, selection result, method, or figure is permitted.

## Next action

After the project owner approves the written design, prepare the implementation
plan for T-003A. Do not record a finding here until a script-generated artifact
and its verification evidence exist.
