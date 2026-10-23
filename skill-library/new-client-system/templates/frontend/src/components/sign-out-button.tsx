"use client";

import { signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

export function SignOutButton() {
  return (
    <Button
      variant="outline"
      size="sm"
      onClick={() => signOut({ redirectTo: "/login" })}
      className="hairline font-mono text-[11px] uppercase tracking-wider"
    >
      <LogOut className="h-3.5 w-3.5" />
      Sign out
    </Button>
  );
}
