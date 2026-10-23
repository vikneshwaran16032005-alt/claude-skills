import { auth } from "@/auth";
import { automations } from "@/config/automations";
import { StatusDot } from "@/components/status-dot";

export default async function DashboardPage() {
  const session = await auth();
  const handle = session?.user?.email?.split("@")[0] ?? "there";

  const total = automations.length;
  const active = automations.filter((a) => a.status === "active").length;
  const draft = automations.filter((a) => a.status === "draft").length;

  const now = new Date().toISOString().slice(0, 19).replace("T", " ");

  return (
    <div className="flex flex-col gap-10">
      {/* hero */}
      <header className="relative sweep flex flex-col gap-1 pt-2">
        <div className="text-mono-label text-muted-foreground">
          {"// overview"}
        </div>
        <h1 className="text-3xl font-medium tracking-tight">
          Welcome back, {handle}
        </h1>
        <p className="text-sm text-muted-foreground">
          The control surface for your automations.
        </p>
      </header>

      {/* stats */}
      <section className="grid grid-cols-1 gap-px overflow-hidden rounded-md border border-border bg-border sm:grid-cols-3">
        <Stat label="total" value={total} />
        <Stat label="active" value={active} dotted="active" />
        <Stat label="drafts" value={draft} dotted="draft" />
      </section>

      {/* empty state */}
      {total === 0 && (
        <section className="flex flex-col gap-2">
          <div className="text-mono-label text-muted-foreground">
            {"// getting started"}
          </div>
          <div className="hairline rounded-md bg-background">
            <div className="flex flex-col gap-2 px-5 py-12 text-center">
              <p className="font-mono text-xs text-muted-foreground">
                no automations yet
              </p>
              <p className="font-mono text-[11px] text-border-strong">
                drop one into src/config/automations.ts to populate the sidebar
              </p>
            </div>
            <div className="border-t border-border px-5 py-2 font-mono text-[10px] tracking-wider text-border-strong">
              STATUS · IDLE
            </div>
          </div>
        </section>
      )}

      {/* activity */}
      {total > 0 && (
        <section className="flex flex-col gap-2">
          <div className="flex items-baseline justify-between">
            <div className="text-mono-label text-muted-foreground">
              {"// recent activity"}
            </div>
            <div className="font-mono text-[10px] tracking-wider text-border-strong">
              live · {now}
            </div>
          </div>
          <div className="hairline rounded-md bg-background">
            <div className="flex items-center gap-3 px-5 py-12">
              <StatusDot status="neutral" />
              <p className="font-mono text-xs text-muted-foreground">
                no events recorded · automations will report runs here as they
                fire
              </p>
            </div>
            <div className="border-t border-border px-5 py-2 font-mono text-[10px] tracking-wider text-border-strong">
              STATUS · IDLE — 00:00:00
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

function Stat({
  label,
  value,
  dotted,
}: {
  label: string;
  value: number;
  dotted?: "active" | "draft";
}) {
  return (
    <div className="flex flex-col gap-3 bg-background px-6 py-7">
      <div className="flex items-center gap-2">
        {dotted && <StatusDot status={dotted} />}
        <span className="text-mono-label text-muted-foreground">{label}</span>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="font-mono font-tabular text-4xl font-medium tracking-tight text-foreground">
          {value.toString().padStart(2, "0")}
        </span>
        <span className="font-mono text-xs text-border-strong">/ total</span>
      </div>
    </div>
  );
}
