export type ProjectPhase = "feasibility" | "data-proof" | "prototype" | "production";

export interface ProjectStatus {
  readonly title: string;
  readonly phase: ProjectPhase;
  readonly selectedEvent: string | null;
  readonly thesis: string;
}

export const projectStatus: ProjectStatus = {
  title: "Pacific Tsunami Warning Time",
  phase: "feasibility",
  selectedEvent: null,
  thesis:
    "One tsunami crosses a shared ocean, but bathymetry, geography, observation, and warning systems leave Pacific communities with radically different amounts of usable time.",
};
