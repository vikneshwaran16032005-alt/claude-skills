import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { Sidebar } from "@/components/sidebar";
import { Topbar } from "@/components/topbar";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  if (!session?.user) redirect("/login");

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <Sidebar userEmail={session.user.email} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar userEmail={session.user.email} />
        <main className="relative min-h-0 flex-1 overflow-y-auto bg-grid">
          <div className="mx-auto w-full max-w-6xl px-8 py-10">
            <div className="animate-enter">{children}</div>
          </div>
        </main>
      </div>
    </div>
  );
}
