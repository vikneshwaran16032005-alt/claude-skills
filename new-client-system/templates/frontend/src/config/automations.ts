import type { LucideIcon } from "lucide-react";

export type AutomationStatus = "draft" | "active" | "paused";

export type Automation = {
  slug: string;
  title: string;
  description: string;
  icon: LucideIcon;
  status: AutomationStatus;
};

// Add automations here. Each entry will appear in the sidebar and on the
// /dashboard/automations index. The /dashboard/automations/[slug] route reads
// the matching entry by slug.
//
// Example:
//
// import { FileText } from "lucide-react";
//
// export const automations: Automation[] = [
//   {
//     slug: "invoice",
//     title: "Send invoice",
//     description: "Generate a PDF invoice and send it via email.",
//     icon: FileText,
//     status: "active",
//   },
// ];
export const automations: Automation[] = [];

export function getAutomation(slug: string): Automation | undefined {
  return automations.find((a) => a.slug === slug);
}
