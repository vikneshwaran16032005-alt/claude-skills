import "dotenv/config";
import { Composio } from "@composio/core";

/**
 * One-time: connect Gmail + Google Drive for COMPOSIO_USER_ID.
 *
 *   npx tsx scripts/connect-composio.ts
 *
 * - Ensures a Composio-managed auth config exists for each toolkit.
 * - Skips toolkits already ACTIVE for this user.
 * - Prints the OAuth URL and waits up to 10 minutes for each toolkit.
 *
 * Adjust the TOOLKITS list below to match the integrations your automations
 * need (e.g. add "SLACK", "NOTION", "HUBSPOT", "GITHUB", etc.).
 */

const TOOLKITS = ["GMAIL", "GOOGLEDRIVE"] as const;

async function main() {
  const apiKey = process.env.COMPOSIO_API_KEY;
  const userId = process.env.COMPOSIO_USER_ID;
  if (!apiKey) throw new Error("Missing COMPOSIO_API_KEY in env");
  if (!userId) throw new Error("Missing COMPOSIO_USER_ID in env");

  const composio = new Composio({ apiKey });

  for (const toolkit of TOOLKITS) {
    console.log(`\n→ Connecting ${toolkit} for ${userId}…`);

    const existing = await composio.connectedAccounts
      .list({ userIds: [userId], toolkitSlugs: [toolkit.toLowerCase()] } as never)
      .catch(() => null as never);
    const active = pickActive(existing);
    if (active) {
      console.log(`  ✓ ${toolkit} already ACTIVE (id=${active.id})`);
      continue;
    }

    const authConfigId = await ensureAuthConfig(composio, toolkit);
    console.log(`  Using auth config ${authConfigId}`);

    const linkFn =
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (composio.connectedAccounts as any).link ?? composio.connectedAccounts.initiate;
    const conn = await linkFn.call(composio.connectedAccounts, userId, authConfigId);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const redirect = (conn as any).redirectUrl ?? (conn as any).redirect_url;
    if (redirect) {
      console.log(`  Open this URL to authorize ${toolkit}:`);
      console.log(`  ${redirect}`);
      console.log(`  (Waiting up to 10 minutes — finish the OAuth flow in your browser.)`);
    } else {
      console.log(`  Connection initiated: ${JSON.stringify(conn)}`);
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    if (typeof (conn as any).waitForConnection === "function") {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const finalConn = await (conn as any).waitForConnection(600_000);
      console.log(`  ✓ ${toolkit} connected (id=${finalConn.id})`);
    } else {
      console.log(`  (No waitForConnection helper — verify manually in the Composio dashboard.)`);
    }
  }

  console.log("\nAll done.");
}

function pickActive(listResp: unknown): { id: string } | null {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const items = (listResp as any)?.items ?? (listResp as any)?.data ?? [];
  if (!Array.isArray(items)) return null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return items.find((c: any) => c?.status === "ACTIVE") ?? null;
}

async function ensureAuthConfig(composio: Composio, toolkit: string): Promise<string> {
  const slug = toolkit.toLowerCase();
  const existing = await composio.authConfigs
    .list({ toolkit: slug } as never)
    .catch(() => null as never);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const items = (existing as any)?.items ?? (existing as any)?.data ?? [];
  if (Array.isArray(items) && items.length > 0) {
    return items[0].id;
  }
  const created = await composio.authConfigs.create(toolkit, {
    type: "use_composio_managed_auth",
  } as never);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const id = (created as any)?.id ?? (created as any)?.authConfigId;
  if (!id) throw new Error(`Failed to create auth config for ${toolkit}: ${JSON.stringify(created)}`);
  return id;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
