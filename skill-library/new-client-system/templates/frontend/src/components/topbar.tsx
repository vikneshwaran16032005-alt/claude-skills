"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { Fragment } from "react";

export function Topbar({ userEmail }: { userEmail?: string | null }) {
  const pathname = usePathname();
  const segments = pathname.split("/").filter(Boolean);

  return (
    <header className="sticky top-0 z-20 flex h-12 items-center justify-between gap-4 border-b border-border bg-background/80 px-6 backdrop-blur-md">
      <nav className="flex items-center gap-1 font-mono text-xs text-muted-foreground">
        {segments.length === 0 ? (
          <span className="text-foreground">~</span>
        ) : (
          segments.map((seg, i) => {
            const href = "/" + segments.slice(0, i + 1).join("/");
            const isLast = i === segments.length - 1;
            return (
              <Fragment key={href}>
                {i > 0 && (
                  <span className="select-none text-border-strong">/</span>
                )}
                {isLast ? (
                  <span className="text-foreground">{seg}</span>
                ) : (
                  <Link
                    href={href}
                    className="hover:text-foreground transition-colors"
                  >
                    {seg}
                  </Link>
                )}
              </Fragment>
            );
          })
        )}
      </nav>

      {userEmail && (
        <span className="hairline hidden rounded-sm bg-surface px-2 py-1 font-mono text-[11px] text-muted-foreground sm:inline">
          {userEmail}
        </span>
      )}
    </header>
  );
}
