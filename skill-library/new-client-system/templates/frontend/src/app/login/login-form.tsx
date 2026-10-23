"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { signIn } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight } from "lucide-react";

export function LoginForm() {
  const params = useSearchParams();
  const errorParam = params.get("error");
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const errorMessage =
    errorParam === "AccessDenied"
      ? "Only @{{CLIENT_DOMAIN}} email addresses can sign in."
      : errorParam
        ? "Something went wrong. Please try again."
        : null;

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitting(true);
    await signIn("resend", { email, redirectTo: "/dashboard" });
  }

  return (
    <div className="w-[380px] max-w-full">
      {/* brand */}
      <div className="mb-5 flex items-center gap-2">
        <span className="grid h-6 w-6 place-items-center rounded-sm bg-primary text-primary-foreground">
          <span className="block h-1.5 w-1.5 rounded-[1px] bg-primary-foreground" />
        </span>
        <span className="text-sm font-medium tracking-tight">{{CLIENT_NAME}}</span>
      </div>

      <div className="hairline rounded-md bg-surface">
        <div className="flex items-baseline justify-between border-b border-border px-5 py-2">
          <span className="text-mono-label text-muted-foreground">
            {"// sign in"}
          </span>
          <span className="font-mono text-[10px] tracking-wider text-border-strong">
            v1
          </span>
        </div>

        <div className="px-5 pb-5 pt-5">
          <h1 className="text-xl font-medium tracking-tight">
            Sign in to {{CLIENT_NAME}}
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Enter your{" "}
            <span className="font-mono text-foreground">@{{CLIENT_DOMAIN}}</span>{" "}
            email — we&apos;ll send a magic link.
          </p>

          <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-3">
            <label className="flex flex-col gap-1.5">
              <span className="text-mono-label text-muted-foreground">
                email
              </span>
              <Input
                type="email"
                required
                autoComplete="email"
                placeholder="you@{{CLIENT_DOMAIN}}"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="hairline h-9 rounded-sm bg-background font-mono text-sm"
              />
            </label>

            {errorMessage && (
              <p className="font-mono text-xs text-destructive">
                ! {errorMessage}
              </p>
            )}

            <Button
              type="submit"
              disabled={submitting || !email}
              className="mt-1 h-9 rounded-sm font-medium"
            >
              {submitting ? "Sending..." : "Send magic link"}
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </form>
        </div>

        <div className="flex items-center justify-between border-t border-border px-5 py-2 font-mono text-[10px] tracking-wider text-border-strong">
          <span>{{CLIENT_DOMAIN}} · internal</span>
          <span>↵ to submit</span>
        </div>
      </div>
    </div>
  );
}
