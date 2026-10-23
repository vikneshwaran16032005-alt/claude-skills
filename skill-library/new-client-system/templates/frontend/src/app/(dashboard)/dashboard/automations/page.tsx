import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { automations } from "@/config/automations";
import { StatusDot } from "@/components/status-dot";

export default function AutomationsIndexPage() {
  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-1">
        <div className="text-mono-label text-muted-foreground">
          {"// automations"}
        </div>
        <div className="flex items-baseline justify-between">
          <h1 className="text-3xl font-medium tracking-tight">All automations</h1>
          <span className="font-mono text-xs text-muted-foreground">
            {automations.length.toString().padStart(2, "0")} total
          </span>
        </div>
      </header>

      <div className="hairline overflow-hidden rounded-md bg-background">
        <div className="grid grid-cols-[auto_1fr_auto_auto] items-center gap-4 border-b border-border px-5 py-2 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
          <span className="w-2" />
          <span>name</span>
          <span>slug</span>
          <span className="pr-1">›</span>
        </div>
        <ul>
          {automations.map((a) => (
            <li key={a.slug} className="border-b border-border last:border-b-0">
              <Link
                href={`/dashboard/automations/${a.slug}`}
                className="group grid grid-cols-[auto_1fr_auto_auto] items-center gap-4 px-5 py-4 transition-colors hover:bg-accent-soft"
              >
                <StatusDot status={a.status} />
                <div className="flex min-w-0 flex-col gap-0.5">
                  <span className="truncate text-sm text-foreground">
                    {a.title}
                  </span>
                  <span className="truncate text-xs text-muted-foreground">
                    {a.description}
                  </span>
                </div>
                <span className="font-mono text-[11px] tracking-wider text-border-strong group-hover:text-muted-foreground">
                  {a.slug}
                </span>
                <ChevronRight className="h-3.5 w-3.5 text-border-strong transition-transform group-hover:translate-x-0.5 group-hover:text-foreground" />
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
