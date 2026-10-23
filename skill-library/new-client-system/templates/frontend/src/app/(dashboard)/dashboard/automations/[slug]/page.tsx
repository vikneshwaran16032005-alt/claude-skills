import { notFound } from "next/navigation";
import { getAutomation } from "@/config/automations";
import { StatusDot } from "@/components/status-dot";

type Params = { params: Promise<{ slug: string }> };

export default async function AutomationDetailPage({ params }: Params) {
  const { slug } = await params;
  const automation = getAutomation(slug);
  if (!automation) notFound();

  const Icon = automation.icon;

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-4">
        <div className="text-mono-label text-muted-foreground">
          {"// automation"}
        </div>
        <div className="flex items-start gap-4">
          <div className="grid h-12 w-12 place-items-center rounded-md border border-border bg-background text-foreground">
            <Icon className="h-5 w-5" />
          </div>
          <div className="flex flex-col gap-1">
            <h1 className="text-3xl font-medium tracking-tight">
              {automation.title}
            </h1>
            <p className="text-sm text-muted-foreground">
              {automation.description}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 font-mono text-[10px] uppercase tracking-[0.18em]">
          <MetaPill label="slug" value={automation.slug} />
          <MetaPill
            label="status"
            value={automation.status}
            leading={<StatusDot status={automation.status} />}
          />
          <MetaPill label="runtime" value="trigger.dev" />
        </div>
      </header>

      <section className="hairline rounded-md bg-background">
        <SectionHead title={"// about"} />
        <div className="px-5 py-4 text-sm text-muted-foreground">
          Configuration and metadata for this automation will live here. Once
          the corresponding Trigger.dev task is registered, you can edit
          parameters, trigger runs manually, and inspect prior executions.
        </div>
      </section>

      <section className="hairline rounded-md bg-background">
        <SectionHead title={"// run history"} right="last 30 days" />
        <div className="flex flex-col items-center justify-center gap-2 px-5 py-16">
          <StatusDot status="neutral" />
          <p className="font-mono text-xs text-muted-foreground">
            no runs recorded yet
          </p>
        </div>
      </section>
    </div>
  );
}

function MetaPill({
  label,
  value,
  leading,
}: {
  label: string;
  value: string;
  leading?: React.ReactNode;
}) {
  return (
    <span className="inline-flex items-center gap-2 rounded-sm border border-border bg-background px-2 py-1 text-muted-foreground">
      <span className="text-border-strong">{label}</span>
      <span className="text-border-strong">·</span>
      {leading}
      <span className="text-foreground">{value}</span>
    </span>
  );
}

function SectionHead({ title, right }: { title: string; right?: string }) {
  return (
    <div className="flex items-center justify-between border-b border-border px-5 py-2">
      <span className="text-mono-label text-muted-foreground">{title}</span>
      {right && (
        <span className="font-mono text-[10px] tracking-wider text-border-strong">
          {right}
        </span>
      )}
    </div>
  );
}
