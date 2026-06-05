import { Suspense } from "react";
import { LoginForm } from "./login-form";

export default function LoginPage() {
  return (
    <div className="relative flex min-h-screen items-center justify-center bg-background p-6">
      <div className="pointer-events-none absolute inset-0 bg-grid" />
      <div className="relative z-10 animate-enter">
        <Suspense>
          <LoginForm />
        </Suspense>
      </div>
    </div>
  );
}
