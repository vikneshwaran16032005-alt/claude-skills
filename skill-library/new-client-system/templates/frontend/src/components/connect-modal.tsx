"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Check, ExternalLink, Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { StatusDot } from "@/components/status-dot";
import {
  checkAuthAction,
  startAuthAction,
} from "@/app/(dashboard)/dashboard/automations/connect-actions";

// Friendly labels — duplicated here so it stays a client module.
// Keep in sync with src/lib/composio.ts → TOOLKIT_LABELS.
const TOOLKIT_LABELS: Record<string, string> = {
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

type ToolkitState = {
  toolkit: string;
  status: "missing" | "connecting" | "active";
  error?: string;
};

export function ConnectModal({
  open,
  toolkits,
  onAllConnected,
  onCancel,
}: {
  open: boolean;
  toolkits: string[];
  onAllConnected: () => void;
  onCancel: () => void;
}) {
  const [states, setStates] = useState<ToolkitState[]>(() =>
    toolkits.map((t) => ({ toolkit: t, status: "missing" })),
  );
  // Reset states whenever the requested toolkits change (modal reopens with a
  // new list) — handled during render per React's "store info from previous
  // render" pattern, not in an effect.
  const [prevToolkits, setPrevToolkits] = useState(toolkits);
  if (prevToolkits !== toolkits) {
    setPrevToolkits(toolkits);
    setStates(toolkits.map((t) => ({ toolkit: t, status: "missing" })));
  }
  const pollRef = useRef<number | null>(null);

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      window.clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  const refresh = useCallback(async () => {
    const res = await checkAuthAction(toolkits);
    if (!res.ok) return;
    setStates((prev) =>
      prev.map((s) => {
        const remoteMissing = res.missing.includes(s.toolkit);
        if (!remoteMissing) return { ...s, status: "active" };
        // keep "connecting" if we previously kicked off OAuth
        return s.status === "connecting" ? s : { ...s, status: "missing" };
      }),
    );
  }, [toolkits]);

  // Poll Composio while the modal is open. This effect *is* "subscribe to
  // external state" — exactly what effects are for — but the new strict React
  // rule still flags the transitive setState via refresh().
  useEffect(() => {
    if (!open) {
      stopPolling();
      return;
    }
    // eslint-disable-next-line react-hooks/set-state-in-effect
    refresh();
    pollRef.current = window.setInterval(refresh, 2000);
    return stopPolling;
  }, [open, refresh, stopPolling]);

  // When everything flips active, fire the callback exactly once.
  const allActive = states.length > 0 && states.every((s) => s.status === "active");
  const firedRef = useRef(false);
  useEffect(() => {
    if (allActive && !firedRef.current) {
      firedRef.current = true;
      stopPolling();
      // small delay so the user gets to see the checkmark land
      const t = window.setTimeout(() => onAllConnected(), 600);
      return () => window.clearTimeout(t);
    }
    if (!open) firedRef.current = false;
  }, [allActive, open, onAllConnected, stopPolling]);

  async function connect(toolkit: string) {
    setStates((prev) =>
      prev.map((s) =>
        s.toolkit === toolkit
          ? { ...s, status: "connecting", error: undefined }
          : s,
      ),
    );
    const res = await startAuthAction(toolkit);
    if (!res.ok) {
      setStates((prev) =>
        prev.map((s) =>
          s.toolkit === toolkit ? { ...s, status: "missing", error: res.error } : s,
        ),
      );
      return;
    }
    // Open the OAuth flow in a new tab. The user completes it externally;
    // our 2s poll detects when status flips to ACTIVE.
    window.open(res.redirectUrl, "_blank", "noopener,noreferrer");
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(o) => {
        if (!o) onCancel();
      }}
    >
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="text-base">Connect your accounts</DialogTitle>
          <DialogDescription>
            This automation needs access to the services below. Sign in to each
            one — we&apos;ll detect when you&apos;re done and continue.
          </DialogDescription>
        </DialogHeader>

        <ul className="mt-2 flex flex-col">
          {states.map((s, i) => (
            <li
              key={s.toolkit}
              className={`flex items-center justify-between gap-3 py-3 ${
                i === states.length - 1 ? "" : "border-b border-border"
              }`}
            >
              <div className="flex min-w-0 items-center gap-3">
                <StatusDot status={s.status === "active" ? "active" : "draft"} />
                <div className="flex min-w-0 flex-col">
                  <span className="truncate text-sm text-foreground">
                    {TOOLKIT_LABELS[s.toolkit] ?? s.toolkit}
                  </span>
                  <span className="truncate font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                    {s.status === "active"
                      ? "connected"
                      : s.status === "connecting"
                        ? "waiting for OAuth…"
                        : s.error
                          ? `error · ${s.error}`
                          : "not connected"}
                  </span>
                </div>
              </div>

              {s.status === "active" ? (
                <span className="inline-flex h-7 w-7 items-center justify-center rounded-sm border border-border text-status-active">
                  <Check className="h-3.5 w-3.5" />
                </span>
              ) : s.status === "connecting" ? (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="hairline font-mono text-[11px] uppercase tracking-wider"
                  onClick={() => connect(s.toolkit)}
                >
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  Re-open
                </Button>
              ) : (
                <Button
                  type="button"
                  size="sm"
                  className="rounded-sm font-mono text-[11px] uppercase tracking-wider"
                  onClick={() => connect(s.toolkit)}
                >
                  Connect
                  <ExternalLink className="h-3.5 w-3.5" />
                </Button>
              )}
            </li>
          ))}
        </ul>

        <div className="mt-2 flex items-center justify-between gap-3">
          <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            polling · 2s
          </span>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={onCancel}
            className="font-mono text-[11px] uppercase tracking-wider"
          >
            Cancel
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
