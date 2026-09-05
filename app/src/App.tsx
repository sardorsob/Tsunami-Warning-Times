import { projectStatus } from "./project";

export function App() {
  return (
    <main>
      <p className="eyebrow">PacificVis 2027 · feasibility phase</p>
      <h1>{projectStatus.title}</h1>
      <p className="thesis">{projectStatus.thesis}</p>

      <section aria-labelledby="status-heading">
        <h2 id="status-heading">Research before rendering</h2>
        <p>
          The historical event has not been selected. The next gate is to verify one modeled
          travel-time field against usable DART and tide-gauge observations before building the
          visual story.
        </p>
        <dl>
          <div>
            <dt>Primary lane</dt>
            <dd>Historical event intelligence</dd>
          </div>
          <div>
            <dt>Current phase</dt>
            <dd>{projectStatus.phase}</dd>
          </div>
          <div>
            <dt>Selected event</dt>
            <dd>{projectStatus.selectedEvent ?? "Pending evidence"}</dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
