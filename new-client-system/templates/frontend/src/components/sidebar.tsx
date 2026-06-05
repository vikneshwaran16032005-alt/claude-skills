"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutGrid, Settings } from "lucide-react";
import { automations } from "@/config/automations";
import { cn } from "@/lib/utils";
import { StatusDot } from "@/components/status-dot";
import { Kbd } from "@/components/kbd";

type SidebarProps = {
  userEmail?: string | null;
};

export function Sidebar({ userEmail }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="relative flex h-screen w-64 shrink-0 flex-col border-r border-border bg-sidebar">
      {/* brand */}
      <div className="flex h-12 items-center justify-between border-b border-border px-4">
        <Link href="/dashboard" className="flex items-center gap-2 group">
          <span className="grid h-5 w-5 place-items-center rounded-sm bg-primary text-primary-foreground">
            <span className="block h-1.5 w-1.5 rounded-[1px] bg-primary-foreground" />
          </span>
          <span className="text-sm font-medium tracking-tight">{{CLIENT_NAME}}</span>
        </Link>
        <Kbd>⌘K</Kbd>
      </div>

      {/* nav */}
      <nav className="flex-1 overflow-y-auto px-3 py-5">
        <SectionLabel>{"// Overview"}</SectionLabel>
        <ul className="mb-6 flex flex-col gap-0.5">
          <li>
            <NavItem
              href="/dashboard"
              label="Dashboard"
              icon={<LayoutGrid className="h-3.5 w-3.5" />}
              active={pathname === "/dashboard"}
            />
          </li>
        </ul>

        <SectionLabel>{"// Automations"}</SectionLabel>
        <ul className="flex flex-col gap-0.5">
          {automations.map((a) => {
            const href = `/dashboard/automations/${a.slug}`;
            const active = pathname === href;
            return (
              <li key={a.slug}>
                <Link
                  href={href}
                  className={cn(
                    "group flex items-center gap-2.5 rounded-sm px-2.5 py-1.5 text-sm transition-colors",
                    "text-muted-foreground hover:bg-accent hover:text-foreground",
                    active &&
                      "border border-border bg-accent-soft text-foreground",
                    !active && "border border-transparent",
                  )}
                >
                  <StatusDot status={a.status} />
                  <span className="truncate flex-1">{a.title}</span>
                  <span
                    className={cn(
                      "font-mono text-[10px] tracking-wider text-border-strong opacity-0 transition-opacity",
                      active && "opacity-100",
                    )}
                  >
                    {a.slug}
                  </span>
                </Link>
              </li>
            );
          })}
          <li className="mt-1">
            <Link
              href="/dashboard/automations"
              className={cn(
                "block rounded-sm border border-transparent px-2.5 py-1.5 font-mono text-[10px] uppercase tracking-[0.18em] transition-colors",
                "text-muted-foreground hover:text-foreground",
                pathname === "/dashboard/automations" && "text-foreground",
              )}
            >
              view all →
            </Link>
          </li>
        </ul>
      </nav>

      {/* footer */}
      <div className="border-t border-border px-3 py-3">
        <NavItem
          href="/dashboard/settings"
          label="Settings"
          icon={<Settings className="h-3.5 w-3.5" />}
          active={pathname.startsWith("/dashboard/settings")}
        />
        {userEmail && (
          <div className="mt-3 flex items-center gap-2 px-2.5">
            <span className="grid h-5 w-5 shrink-0 place-items-center rounded-full bg-accent font-mono text-[10px] uppercase text-muted-foreground">
              {userEmail.slice(0, 1)}
            </span>
            <span className="truncate font-mono text-[11px] text-muted-foreground">
              {userEmail}
            </span>
          </div>
        )}
      </div>
    </aside>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="px-2.5 pb-2 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
      {children}
    </div>
  );
}

function NavItem({
  href,
  label,
  icon,
  active,
}: {
  href: string;
  label: string;
  icon?: React.ReactNode;
  active?: boolean;
}) {
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-2.5 rounded-sm px-2.5 py-1.5 text-sm transition-colors",
        "text-muted-foreground hover:bg-accent hover:text-foreground",
        active
          ? "border border-border bg-accent-soft text-foreground"
          : "border border-transparent",
      )}
    >
      {icon && <span className="text-muted-foreground">{icon}</span>}
      <span>{label}</span>
    </Link>
  );
}
