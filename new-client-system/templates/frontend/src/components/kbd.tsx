import { cn } from "@/lib/utils";

export function Kbd({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <kbd
      className={cn(
        "inline-flex h-5 min-w-5 items-center justify-center rounded-sm border border-border bg-surface px-1",
        "font-mono text-[10px] font-medium tracking-wider text-muted-foreground",
        className,
      )}
    >
      {children}
    </kbd>
  );
}
