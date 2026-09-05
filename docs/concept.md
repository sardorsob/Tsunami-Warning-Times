# Concept

## Thesis

One tsunami crosses a shared ocean, but bathymetry, geography, observation, and
warning systems leave Pacific communities with radically different amounts of
usable time.

The wave is the mechanism; unequal time is the subject. The experience should be
a scientific explorable narrative, not a dashboard and not a cinematic disaster
simulation.

## Discovery sequence

1. Show a simple distance-only ring and ask which of two similarly distant
   communities receives the wave first.
2. Reveal bathymetry and replace the ring with the modeled travel-time front.
3. Activate selected DART buoys and tide gauges at their observed arrivals.
4. compare modeled and observed arrivals with directly labeled residuals.
5. Resolve the result into four to six synchronized community panels while
   separating physical travel time from actionable warning time.
6. Offer limited time scrubbing only after the guided result is clear.

## Visual direction

Aim for an **instrumented ocean**: part hydrographic chart, part observation log,
part scientific explainer. The active front comes from a measured or modeled
travel-time field—not particles, noise, a sine wave, or any other decorative
effect. Do not encode amplitude unless a suitable amplitude dataset supports it.

Modeled fields are continuous, subdued cyan/blue-gray linework. Observations are
discrete amber events. Residuals use an accessible zero-centered treatment,
uncertainty has a non-color cue, and missing data is explicit. Important values,
units, time standard, and station IDs remain visible without hover.

## Experience guardrails

- Guided first, exploratory second.
- One event and a small evidence chain.
- Discovery through comparison, not manufactured drama.
- D3/SVG for the authored Pacific geography and charts when the first figure
  needs it; a narrow WebGL threshold renderer only after the static proof works.
- Native controls and CSS before additional interaction or animation libraries.
- Every animated state has a reduced-motion static equivalent.
