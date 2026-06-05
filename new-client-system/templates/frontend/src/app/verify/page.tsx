import { Mail } from "lucide-react";

export default function VerifyPage() {
  return (
    <div className="relative flex min-h-screen items-center justify-center bg-background p-6">
      <div className="pointer-events-none absolute inset-0 bg-grid" />

      <div className="relative z-10 w-[380px] max-w-full animate-enter">
        <div className="mb-5 flex items-center gap-2">
          <span className="grid h-6 w-6 place-items-center rounded-sm bg-primary text-primary-foreground">
            <span className="block h-1.5 w-1.5 rounded-[1px] bg-primary-foreground" />
          </span>
          <span className="text-sm font-medium tracking-tight">{{CLIENT_NAME}}</span>
        </div>

        <div className="hairline rounded-md bg-surface">
          <div className="flex items-baseline justify-between border-b border-border px-5 py-2">
            <span className="text-mono-label text-muted-foreground">
              {"// verify"}
            </span>
            <span className="font-mono text-[10px] tracking-wider text-border-strong">
              waiting
            </span>
          </div>

          <div className="flex flex-col items-center gap-5 px-5 py-8 text-center">
            <div className="grid h-10 w-10 place-items-center rounded-sm border border-border bg-background text-foreground">
              <Mail className="h-4 w-4" />
            </div>
            <div className="flex flex-col gap-1">
              <h1 className="text-xl font-medium tracking-tight">
                Check your inbox
              </h1>
              <p className="text-sm text-muted-foreground">
                We sent a sign-in link. It expires in 24 hours.
              </p>
            </div>
            <span
              className="animate-loader-dots inline-flex items-center gap-1 font-mono text-xs text-muted-foreground"
              aria-label="waiting"
            >
              <span>·</span>
              <span>·</span>
              <span>·</span>
            </span>
          </div>

          <div className="border-t border-border px-5 py-2 font-mono text-[10px] tracking-wider text-border-strong">
            you can close this tab safely
          </div>
        </div>
      </div>
    </div>
  );
}
