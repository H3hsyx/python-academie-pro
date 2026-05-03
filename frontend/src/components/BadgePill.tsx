import type { ReactNode } from "react";

type BadgePillProps = {
  children: ReactNode;
  tone?: "neutral" | "success" | "warning" | "danger";
};

export function BadgePill({ children, tone = "neutral" }: BadgePillProps) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}