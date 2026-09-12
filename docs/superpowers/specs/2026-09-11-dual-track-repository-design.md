# PacificVis 2027 Dual-Track Repository Design

- Date: 2026-09-11
- Scope: repository architecture, analytical ownership, and delivery roadmap
- Primary paper target: PacificVis 2027 Conference Paper Track
- Parallel creative target: PacificVis 2027 Visual Data Storytelling Contest
- Review state: conceptual design approved by the project owner; written design
  self-reviewed and awaiting final owner review

## Outcome

Keep one repository while producing two materially different PacificVis 2027
submissions from a governed scientific foundation:

1. a conference paper whose contribution is an uncertainty-aware visual
   analytics method using statistical and machine-learning models to investigate
   tsunami timing discrepancies across multiple events and stations; and
2. an original visual data story whose contribution is a guided, single-event
   Tōhoku narrative implemented in `app/` and supported by descriptive evidence.

The two lanes may share authoritative source acquisition, provenance,
normalization, schemas, and reviewed data-quality facts. They do not share a
thesis, model-derived result, final figure, narrative sequence, interaction
design, or submission claim.

## Confirmed targets and dates

The official PacificVis 2027 calls establish these working deadlines:

| Target | Deadline | Working interpretation |
| --- | --- | --- |
| Conference Paper abstract | 2026-11-02 AoE | Register title, abstract, authors, and keywords |
| Conference Paper manuscript | 2026-11-09 AoE | Submit an original full paper of up to 9+2 pages |
| Conference Paper first decision | 2026-12-16 AoE | Begin revision or decide on the VisNotes fallback |
| VisNotes fallback | 2027-01-04 AoE | Use only if the work is better supported as a narrower paper |
| Visual Data Storytelling entry | 2027-02-01 AoE | Submit the original browser story and 150-word abstract |

Authoritative pages, verified on 2026-09-11:

- <https://pacificvis2027.github.io/contribute/conference-papers/>
- <https://pacificvis2027.github.io/contribute/short-papers/>
- <https://pacificvis2027.github.io/contribute/paper-submission-guidelines/>
- <https://visstory.github.io/2027/>

The paper deadline is the first critical path. The storytelling lane may define
its contribution and protect its originality before November, but substantial
story production follows the paper submission.

## Product definitions

### Shared scientific foundation

The shared foundation owns facts and reusable scientific contracts:

- source discovery, credentials policy, acquisition, checksums, and provenance;
- immutable raw assets and reproducible normalized tables;
- event, station, observation, arrival-definition, unit, time, datum, CRS, and
  missingness contracts;
- source-factual quality checks and descriptive coverage summaries;
- explicit rejection, blocker, and unknown-metadata accounting; and
- versioned release manifests naming the exact tables and checksums a lane may
  consume.

The current Tōhoku acquisition, normalization, and missingness work belongs to
this foundation. Shared does not mean that every dataset must feed both products.
A release manifest names its allowed consumers.

### Conference paper

The paper asks:

> How can uncertainty-aware visual analytics and statistical learning reveal
> systematic discrepancies among modeled and observed tsunami arrival times?

The paper lane owns:

- a multi-event, multi-station analytical corpus;
- a predeclared target, data split, baseline, leakage policy, and evaluation
  protocol;
- statistical and machine-learning models, calibration, uncertainty,
  sensitivity, ablation, and out-of-event or out-of-station validation;
- an original visual analytics method or system that helps a researcher examine
  discrepancy structure and uncertainty;
- paper-only experiment tracking, figures, tables, interpretation, and
  manuscript text;
- an AI-assistance ledger sufficient to prepare the conference-required
  disclosure for generated text, figures, images, or code; and
- the scientific claim that is evaluated for the Conference Paper Track.

Machine learning is the analytical engine, not the submission contribution by
itself. The primary contribution remains visualization or visual analytics.

### Visual data story

The story asks:

> How did one tsunami produce radically different arrival-time experiences
> around the Pacific, and why is distance alone misleading?

The storytelling lane owns:

- one reviewed Tōhoku event and a small source-supported observation chain;
- story-only descriptive EDA used to select defensible contrasts;
- an original narrative thesis, scene order, pacing, visual language, and
  interaction design;
- compact static story exports consumed only by `app/`;
- the accessible guided website, reduced-motion and non-WebGL fallbacks, and
  submission abstract; and
- the story's descriptive claims and direct source explanations.

The app does not expose paper-model predictions, feature importance, model
selection, paper ablations, paper figures, or the paper's visual analytics
method. It remains a story rather than a model demonstration or exploratory
dashboard.

## Originality firewall

The firewall is semantic and technical. Folder names alone are insufficient.

| Surface | Shared | Paper only | Story only |
| --- | --- | --- | --- |
| Public source bytes and checksums | Yes | May consume | May consume |
| Normalized source-faithful tables | Yes | May consume approved release | May consume approved release |
| Missingness and data-quality facts | Yes | May cite | May cite |
| Multi-event feature engineering | No | Yes | No |
| Statistical/ML model outputs | No | Yes | No |
| Uncertainty method and evaluation | No | Yes | No |
| Paper figures and tables | No | Yes | No |
| Narrative scenes and authored pacing | No | No | Yes |
| Story visual encodings and interactions | No | No | Yes |
| App-ready static exports | No | No | Yes |

Rules:

1. Paper code may import shared modules but never story modules.
2. Story analysis may import shared modules but never paper modules.
3. `app/` consumes only story-export manifests under `app/public/data/`.
4. A shared release may contain source-factual derived fields, including a
   reviewed transparent arrival pick, but no fitted paper-model result.
5. A result becomes paper-only as soon as it depends on paper features, fitted
   parameters, model selection, cross-validation, calibration, or the paper's
   uncertainty method.
6. A result becomes story-only as soon as it encodes narrative selection,
   scene-specific framing, annotation, pacing, or story presentation state.
7. Final paper and story figures are independently designed and generated.
8. `context/ORIGINALITY.md` records both contribution statements, the overlap
   matrix, related-publication disclosures, submission dates, and publication
   gates.
9. A finished story is not publicly deployed before its contest submission
   without an explicit originality review and owner decision.
10. Once the contribution statements are stable, contact the paper and contest
    chairs for a written track-compatibility opinion before submitting both.

Chair contact is a later externally authorized action; repository preparation
does not send messages.

## Repository organization

Preserve the existing shared pipeline and add explicit analytical lanes:

```text
pipeline/                         shared acquisition and normalization modules
analysis/
  paper/                          statistical/ML and visual-analytics analysis
  story/                          descriptive story-selection analysis
scripts/
  *.py                            existing shared EDA and release entry points
  paper/                          paper experiment and evaluation entry points
  story/                          story-analysis and export entry points
notebooks/
  *.py                            existing views over shared EDA artifacts
  paper/                          paper experiment and diagnostic views
  story/                          story-only exploratory views
tests/
  test_*.py                       existing shared data and release contracts
  paper/                          paper analysis and evaluation behavior
  story/                          story analysis and export behavior
artifacts/
  provenance/                     shared source inventory
  releases/                       reviewed shared release manifests
  eda/missingness/                current shared data-quality evidence
  eda/paper/                      paper-only analytical evidence
  eda/story/                      story-only analytical evidence
  models/paper/                   tracked compact model metadata when approved
  logs/runs/                      portable runs with an explicit lane field
paper/
  manuscript/                     paper source and bibliography
  figures/                        final paper-only generated figures
  supplemental/                   stable paper supplements
app/                              visual-story website
  src/                            story layout and renderer implementation
  public/data/                    story-export manifests and compact assets only
context/
  *.md                            existing shared contracts and reports
  paper/                          paper question, protocol, EDA, model, and report
  story/                          story brief, EDA, storyboard, and release report
  TASKS.md                        master dependencies and deadline view
  DECISIONS.md                    cross-lane decisions
  HANDOVER.md                     current status across all lanes
  ORIGINALITY.md                  contribution and overlap ledger
  AI_USAGE.md                     human-reviewed AI assistance and disclosure log
```

Every existing file under `context/` remains tracked. A root context file that
is superseded by a lane-specific document becomes a durable index or historical
record; it is not deleted merely because its content moved.

The existing top level of `pipeline/`, `scripts/`, `notebooks/`, `tests/`, and
`context/` is the shared lane. This is an explicit ownership rule, not an
accident of history. Do not introduce `shared/` wrapper directories merely for
symmetry: that would churn stable commands and invalidate recorded artifact
paths without improving the scientific boundary. New work that is specific to
a submission must enter the corresponding `paper/` or `story/` directory.
All analytical notebooks are Marimo views over tested Python modules or
script-generated artifacts. A notebook may support adaptive exploration, but a
metric or transformation used in a claim must live in testable code and be
reconciled to a Markdown report.

Migration is intentionally limited:

- existing acquisition and normalization modules remain in `pipeline/`;
- the current missingness profiler, script, notebook, tests, artifacts, EDA
  report, and portable run bundle stay at their recorded paths and are
  designated shared evidence;
- historical generated outputs are never copied or moved merely to match the
  new directory shape; their checksums and recorded paths remain valid;
- `public/data/` moves to `app/public/data/` when the Vite configuration is
  updated, because it is application input rather than scientific evidence;
- pending story tasks are retagged as story work rather than rewritten from
  scratch; and
- no monorepo framework, backend, workflow engine, duplicate environment, or
  second repository is introduced.

## Shared release interface

Each downstream lane reads a reviewed release manifest rather than locating
arbitrary processed files. The interface contains:

- release ID and allowed consumer lanes;
- Git SHA and producing run ID;
- source-manifest and configuration checksums;
- table paths, schemas, grains, row counts, and SHA-256 values;
- temporal, unit, datum, CRS, and missingness semantics;
- rejected and blocked records that remain in denominators;
- known limitations and prohibited interpretations; and
- the task/reviewer disposition that authorizes consumption.

Changing a field's meaning creates a new release ID. Correcting an
implementation without changing meaning may rebuild the same candidate, but a
reviewed checksum change is always recorded. Neither lane reads another lane's
artifacts through the shared interface.

## Data and experiment flow

```text
authoritative sources
  -> shared acquisition and provenance
  -> shared normalization and quality review
  -> reviewed release manifest
       |-> paper corpus expansion
       |    -> frozen protocol
       |    -> statistical/ML experiments
       |    -> uncertainty-aware visual analytics
       |    -> evaluation -> manuscript
       |
       `-> one-event story bundle
            -> story-only descriptive EDA
            -> narrative and visual design
            -> compact story exports -> app/
```

Project-local MLflow uses separate experiments for `paper-*` and `story-*`.
Shared deterministic processing continues to use portable run bundles; shared
EDA may also use MLflow when it constitutes a meaningful analytical run. Every
portable run and MLflow record includes `lane = shared|paper|story`.

Paper hypothesis generation and confirmatory evaluation are recorded
separately. The final test split, model-selection rule, and primary metrics are
frozen before final model comparison. Story exploration remains adaptive, but
every branch records the observed finding that motivated it.

## Roadmap

### Phase 1 — Repository and shared-data seam, 2026-09-11 through 2026-09-18

- migrate the approved structure without changing scientific values;
- create the master roadmap and originality ledger;
- reclassify T-002D as shared EDA and keep it in progress;
- finish source-factual cadence, gap, arrival-definition, spatial, and join
  checks required by both lanes; and
- review and freeze the first shared release interface under T-002E.

### Phase 2 — Paper framing and corpus expansion, 2026-09-19 through 2026-09-30

- define the paper contribution, hypotheses, users/tasks, and related-work gap;
- select additional event and station candidates under the same source gates;
- define targets, statistical assumptions, leakage controls, baselines, data
  splits, uncertainty metrics, and evaluation criteria; and
- write the frozen analysis and evaluation protocol before final comparisons.

The story lane may refine its one-paragraph contribution statement and source
inventory during this phase, but does not reuse paper exploration.

### Phase 3 — Paper experiments and method, 2026-10-01 through 2026-10-18

- build and test the multi-event paper corpus;
- run statistical and machine-learning baselines;
- evaluate calibration, sensitivity, missingness, and cross-event or
  cross-station generalization;
- implement the uncertainty-aware visual analytics method; and
- record selections, rejections, and negative findings.

An explicit checkpoint on 2026-10-15 decides whether the evidence still
supports a full Conference Paper or should target VisNotes instead.

### Phase 4 — Paper evaluation and submission, 2026-10-19 through 2026-11-09

- complete quantitative and visual-analytics evaluation;
- freeze paper claims, figures, and reproducibility materials;
- complete internal scientific, statistical, visualization, and originality
  review;
- register the abstract by 2026-11-02; and
- submit the Conference Paper by 2026-11-09.

### Phase 5 — Story discovery and design, 2026-11-10 through 2026-12-15

- run story-only descriptive EDA on the frozen single-event release;
- select a narrative thesis without paper-model evidence;
- build the storyboard, visual grammar, static proof, and accessibility plan;
- test the intended distance-versus-arrival contrast; and
- freeze the story's scene interfaces before full app production.

### Phase 6 — Paper decision and story production, 2026-12-16 through 2027-01-25

- respond to the Conference Paper decision and complete a conditional revision;
- if rejected, decide by 2026-12-18 whether a scoped VisNotes submission is
  scientifically honest and achievable by 2027-01-04;
- build the story app with deterministic data and narrative state;
- complete mobile, keyboard, touch, reduced-motion, non-WebGL, and source-trace
  checks; and
- audit the paper/story overlap again after both artifacts exist.

### Phase 7 — Story submission, 2027-01-26 through 2027-02-01

- freeze the story and its source manifest;
- complete functional, trustworthiness, accessibility, and originality review;
- prepare the 150-word abstract without revealing a message the story must carry
  itself; and
- submit the directly runnable browser story by 2027-02-01.

## Task organization

`context/TASKS.md` remains the master dependency ledger.

- Completed task IDs remain unchanged as historical evidence.
- T-002D and T-002E are labeled `shared` and close the common Tōhoku data proof.
- Existing pending T-003 through T-005 are labeled `story` and retain their
  history, acceptance criteria, and dependencies.
- New paper tasks use `P-001`, `P-002`, and subsequent IDs.
- Lane-specific task details live in `context/paper/TASKS.md` and
  `context/story/TASKS.md`; the master ledger holds only status, dependency,
  deadline, and evidence links.
- At most one task per lane is active. A shared blocker may block both lanes;
  a paper-only or story-only blocker cannot silently block the other lane.

## Verification and enforcement

The migration adds the smallest useful automated controls:

1. an import-fence test rejects paper-to-story and story-to-paper Python imports;
2. a story-export test rejects paper artifact paths in `app/public/data/`;
3. release-manifest validation checks lane, checksums, schemas, counts, and
   reviewer disposition;
4. generated reports reconcile with their lane's machine-readable metrics;
5. paper runs record frozen split/protocol identifiers, seeds, parameters,
   metrics, artifacts, Git SHA, and selection decisions;
6. story exports remain deterministic and source-traceable; and
7. every substantive EDA or experiment records results, interpretation,
   limitations, decisions, and next steps in the lane's Markdown report; and
8. the existing full repository gate and Graphify update remain required.

Manual review verifies that paper and story contribution statements, final
figures, results, prose, and public claims remain materially distinct.

## Failure and change handling

- If the shared release changes, each lane records whether it accepts the new
  release; neither consumer silently advances.
- If the paper needs a new source, it enters through shared acquisition and
  quality gates but is marked `paper` unless separately approved for the story.
- If story EDA discovers a scientific data defect, the defect is fixed in the
  shared implementation and both lanes receive a new reviewed release.
- If story EDA merely discovers a narrative contrast, it stays story-only.
- If the paper produces an appealing model result, it remains paper-only even if
  it would improve the story.
- If either submission's originality status becomes ambiguous, stop publication
  and seek written guidance from the relevant chairs.

## Deliberate deferrals

Do not add separate repositories, duplicated raw caches, a monorepo framework,
DVC, a workflow orchestrator, a backend, distributed training, deep learning, or
a model registry during the migration. Add a dependency only when an approved
paper or story task demonstrates the need.

The first paper baseline should be the simplest statistically defensible model.
More complex machine learning follows only when it improves an agreed evaluation
criterion or reveals a scientifically useful discrepancy structure.

## Commit boundaries

1. Commit this approved architecture design.
2. Commit the task/context and directory migration with enforcement tests.
3. Complete and commit the reviewed shared release.
4. Commit paper tasks in reproducible experiment-sized units.
5. Commit story tasks in data-proof, visual-proof, and production-sized units.

Push, public deployment, conference submission, chair contact, new credentialed
downloads, and large multi-event acquisition remain separately authorized.
