"use client";

import { useSyncExternalStore } from "react";
import { useTheme } from "next-themes";
import { Monitor, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const ORDER = ["light", "dark", "system"] as const;
type ThemeName = (typeof ORDER)[number];

function nextTheme(theme: ThemeName | undefined): ThemeName {
  const idx = ORDER.indexOf((theme ?? "system") as ThemeName);
  return ORDER[(idx + 1) % ORDER.length];
}

const subscribe = () => () => {};
const useMounted = () =>
  useSyncExternalStore(
    subscribe,
    () => true,
    () => false,
  );

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme();
  const mounted = useMounted();

  const current = (mounted ? (theme ?? "system") : "system") as ThemeName;
  const Icon =
    current === "light" ? Sun : current === "dark" ? Moon : Monitor;

  return (
    <Button
      variant="ghost"
      size="icon-sm"
      aria-label={`Theme: ${current}. Click to cycle.`}
      onClick={() => setTheme(nextTheme(current))}
      className={cn(
        "hairline rounded-sm bg-transparent text-muted-foreground hover:text-foreground",
        className,
      )}
    >
      <Icon className="h-3.5 w-3.5" />
    </Button>
  );
}
