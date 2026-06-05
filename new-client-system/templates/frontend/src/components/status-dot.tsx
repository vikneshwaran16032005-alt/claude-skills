import { cn } from "@/lib/utils";
import type { AutomationStatus } from "@/config/automations";

type Variant = AutomationStatus | "danger" | "neutral";

const COLOR: Record<Variant, string> = {
  active: "bg-status-active",
  draft: "bg-status-draft",
  paused: "bg-status-paused",
  danger: "bg-status-danger",
  neutral: "bg-status-neutral",
};

const RING: Record<Variant, string> = {
  active: "ring-status-active/25",
  draft: "ring-status-draft/25",
  paused: "ring-status-paused/25",
  danger: "ring-status-danger/25",
  neutral: "ring-status-neutral/25",
};

export function StatusDot({
  status = "neutral",
  className,
  size = "sm",
}: {
  status?: Variant;
  className?: string;
  size?: "sm" | "md";
}) {
  const dim = size === "md" ? "h-2 w-2" : "h-1.5 w-1.5";
  return (
    <span
      aria-hidden
      className={cn(
        "inline-block shrink-0 rounded-full ring-4",
        dim,
        COLOR[status],
        RING[status],
        status === "active" && "animate-pulse-soft",
        className,
      )}
    />
  );
}
