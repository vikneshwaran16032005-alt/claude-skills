"use server";

import {
  getToolkitStatuses,
  startToolkitConnection,
  type ToolkitStatus,
} from "@/lib/composio";

export async function checkAuthAction(
  toolkits: string[],
): Promise<
  | { ok: true; statuses: ToolkitStatus[]; missing: string[] }
  | { ok: false; error: string }
> {
  try {
    const statuses = await getToolkitStatuses(toolkits);
    const missing = statuses.filter((s) => s.status === "missing").map((s) => s.toolkit);
    return { ok: true, statuses, missing };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export async function startAuthAction(
  toolkit: string,
): Promise<{ ok: true; redirectUrl: string } | { ok: false; error: string }> {
  try {
    const { redirectUrl } = await startToolkitConnection(toolkit);
    return { ok: true, redirectUrl };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) };
  }
}
