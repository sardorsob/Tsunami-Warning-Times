import { access } from "node:fs/promises";

const requiredOutputs = ["dist/index.html", "dist/data/README.md"];

await Promise.all(requiredOutputs.map((path) => access(new URL(`../${path}`, import.meta.url))));
console.log(`Verified ${requiredOutputs.length} required build outputs.`);
