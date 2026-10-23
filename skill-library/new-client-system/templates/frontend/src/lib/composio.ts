import "server-only";
import { Composio } from "@composio/core";

let _client: Composio | null = null;

export function composio(): Composio {
  if (!_client) {
    if (!process.env.COMPOSIO_API_KEY) {
      throw new Error("Missing COMPOSIO_API_KEY");
    }
    _client = new Composio({ apiKey: process.env.COMPOSIO_API_KEY });
  }
  return _client;
}

export function composioUserId(): string {
  const id = process.env.COMPOSIO_USER_ID;
  if (!id) throw new Error("Missing COMPOSIO_USER_ID");
  return id;
}

export type ToolkitStatus = {
  toolkit: string;
  status: "active" | "missing";
  connectionId?: string;
};

/** Look up every toolkit's current status for the configured user. */
export async function getToolkitStatuses(
  toolkits: string[],
): Promise<ToolkitStatus[]> {
  const userId = composioUserId();
  const out: ToolkitStatus[] = [];
  for (const toolkit of toolkits) {
    const resp = await composio()
      .connectedAccounts.list({
        userIds: [userId],
        toolkitSlugs: [toolkit.toLowerCase()],
      } as never)
      .catch(() => null as never);
    const active = pickActive(resp);
    out.push(
      active
        ? { toolkit, status: "active", connectionId: active.id }
        : { toolkit, status: "missing" },
    );
  }
  return out;
}

/** Begin an OAuth flow for a toolkit. Returns the URL to open in a new tab. */
export async function startToolkitConnection(
  toolkit: string,
): Promise<{ redirectUrl: string; connectionId?: string }> {
  const userId = composioUserId();
  const authConfigId = await ensureAuthConfig(toolkit);

  const linkFn =
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (composio().connectedAccounts as any).link ??
    composio().connectedAccounts.initiate;
  const conn = await linkFn.call(composio().connectedAccounts, userId, authConfigId);

  const redirectUrl: string | undefined =
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (conn as any).redirectUrl ?? (conn as any).redirect_url;
  if (!redirectUrl) {
    throw new Error(`Composio did not return a redirect URL for ${toolkit}`);
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const connectionId: string | undefined = (conn as any).id;
  return { redirectUrl, connectionId };
}

function pickActive(listResp: unknown): { id: string } | null {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const items = (listResp as any)?.items ?? (listResp as any)?.data ?? [];
  if (!Array.isArray(items)) return null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return items.find((c: any) => c?.status === "ACTIVE") ?? null;
}

async function ensureAuthConfig(toolkit: string): Promise<string> {
  const slug = toolkit.toLowerCase();
  const existing = await composio()
    .authConfigs.list({ toolkit: slug } as never)
    .catch(() => null as never);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const items = (existing as any)?.items ?? (existing as any)?.data ?? [];
  if (Array.isArray(items) && items.length > 0) return items[0].id;

  const created = await composio().authConfigs.create(toolkit, {
    type: "use_composio_managed_auth",
  } as never);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const id = (created as any)?.id ?? (created as any)?.authConfigId;
  if (!id) {
    throw new Error(
      `Failed to create auth config for ${toolkit}: ${JSON.stringify(created)}`,
    );
  }
  return id;
}

/** Friendly labels for the modal. */
export const TOOLKIT_LABELS: Record<string, string> = {
  GMAIL: "Gmail",
  GOOGLEDRIVE: "Google Drive",
  GOOGLECALENDAR: "Google Calendar",
  SLACK: "Slack",
  NOTION: "Notion",
  GITHUB: "GitHub",
  HUBSPOT: "HubSpot",
  LINEAR: "Linear",
  AIRTABLE: "Airtable",
};
