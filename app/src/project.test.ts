import { describe, expect, it } from "vitest";

import { projectStatus } from "./project";

describe("project status", () => {
  it("keeps the historical event unresolved during feasibility work", () => {
    expect(projectStatus.phase).toBe("feasibility");
    expect(projectStatus.selectedEvent).toBeNull();
  });
});
