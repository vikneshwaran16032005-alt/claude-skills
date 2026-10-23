import { defineConfig } from "@trigger.dev/sdk";

export default defineConfig({
  project: process.env.TRIGGER_PROJECT_REF ?? "proj_REPLACE_ME",
  // Every automation lives under ./src/automations/<slug>/, and any task.ts
  // it exports is auto-discovered. To add a new automation, drop a new folder
  // here with a task that calls schemaTask({ id: "...", ... }).
  dirs: ["./src/automations"],
  maxDuration: 300,
  retries: {
    enabledInDev: false,
    default: {
      maxAttempts: 3,
      factor: 2,
      minTimeoutInMs: 1000,
      maxTimeoutInMs: 30000,
      randomize: true,
    },
  },
  build: {
    external: ["@react-pdf/renderer"],
  },
});
