import Anthropic from "@anthropic-ai/sdk";

let _anthropic: Anthropic | null = null;
export function anthropic(): Anthropic {
  if (!_anthropic) {
    if (!process.env.ANTHROPIC_API_KEY) throw new Error("Missing ANTHROPIC_API_KEY");
    _anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _anthropic;
}

/**
 * Attempt to parse a JSON object out of a model response. Falls back to
 * extracting the first balanced `{...}` block if the model wrapped its
 * output in prose or fences.
 */
export function safeParseJson<T = Record<string, unknown>>(text: string): T | null {
  try {
    return JSON.parse(text) as T;
  } catch {
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start >= 0 && end > start) {
      try {
        return JSON.parse(text.slice(start, end + 1)) as T;
      } catch {
        return null;
      }
    }
    return null;
  }
}

/*
 * ─── Pattern: drafting a structured email with Claude ────────────────────
 *
 * Copy this into your automation folder (e.g. `src/automations/<slug>/draft.ts`)
 * and tailor `system`, the user payload, and the fallback to your domain.
 *
 *   import { anthropic, safeParseJson } from "@/src/shared/anthropic";
 *
 *   export type DraftedEmail = { subject: string; body: string };
 *
 *   export async function draftEmail(input: MyInputType): Promise<DraftedEmail> {
 *     const system = [
 *       "You write short, warm, professional emails on behalf of a business owner.",
 *       "Output strict JSON with keys `subject` and `body`. No markdown. No code fences.",
 *       "The body should be 3–5 sentences, plain text, no signature block.",
 *     ].join(" ");
 *
 *     const user = JSON.stringify({
 *       // ...domain-specific fields the model needs to write the email
 *     });
 *
 *     const resp = await anthropic().messages.create({
 *       model: "claude-sonnet-4-6",
 *       max_tokens: 600,
 *       system,
 *       messages: [{ role: "user", content: user }],
 *     });
 *
 *     const text = resp.content
 *       .map((b) => (b.type === "text" ? b.text : ""))
 *       .join("")
 *       .trim();
 *
 *     const parsed = safeParseJson<{ subject?: string; body?: string }>(text);
 *     if (!parsed || typeof parsed.subject !== "string" || typeof parsed.body !== "string") {
 *       return { subject: "Fallback subject", body: "Fallback body" };
 *     }
 *     return { subject: parsed.subject, body: parsed.body };
 *   }
 */
