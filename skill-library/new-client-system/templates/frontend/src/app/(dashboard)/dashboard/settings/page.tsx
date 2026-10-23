import { auth } from "@/auth";
import { SignOutButton } from "@/components/sign-out-button";
import { ThemeToggle } from "@/components/theme-toggle";

export default async function SettingsPage() {
  const session = await auth();

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-1">
        <div className="text-mono-label text-muted-foreground">{"// settings"}</div>
        <h1 className="text-3xl font-medium tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground">
          Manage your account and appearance.
        </p>
      </header>

      <section className="hairline rounded-md bg-background">
        <SectionHead>{"// account"}</SectionHead>
        <Row label="email">
          <span className="font-mono text-sm">{session?.user?.email}</span>
        </Row>
        <Row label="domain" last>
          <span className="font-mono text-sm text-muted-foreground">
            @{{CLIENT_DOMAIN}} (allowed)
          </span>
        </Row>
      </section>

      <section className="hairline rounded-md bg-background">
        <SectionHead>{"// appearance"}</SectionHead>
        <Row label="theme" last>
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs text-muted-foreground">
              click to cycle · light → dark → system
            </span>
            <ThemeToggle />
          </div>
        </Row>
      </section>

      <section className="hairline rounded-md bg-background">
        <SectionHead>{"// session"}</SectionHead>
        <Row label="sign out" last>
          <SignOutButton />
        </Row>
      </section>
    </div>
  );
}

function SectionHead({ children }: { children: React.ReactNode }) {
  return (
    <div className="border-b border-border px-5 py-2 text-mono-label text-muted-foreground">
      {children}
    </div>
  );
}

function Row({
  label,
  children,
  last,
}: {
  label: string;
  children: React.ReactNode;
  last?: boolean;
}) {
  return (
    <div
      className={`grid grid-cols-[140px_1fr] items-center gap-4 px-5 py-4 ${
        last ? "" : "border-b border-border"
      }`}
    >
      <span className="text-mono-label text-muted-foreground">{label}</span>
      <div className="flex items-center justify-between gap-4">{children}</div>
    </div>
  );
}
