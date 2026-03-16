import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = { title: "FutureSight", description: "Trading analytics and scanning dashboard" };

const nav = [
  { href: "/watchlist", label: "Watchlist" },
  { href: "/alerts", label: "Alerts" },
  { href: "/trades", label: "Trades" },
  { href: "/analytics", label: "Analytics" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en"><body><main className="mx-auto max-w-6xl p-6"><h1 className="mb-4 text-2xl font-bold">FutureSight</h1><nav className="mb-6 flex gap-4 text-sm">{nav.map((item) => <Link key={item.href} href={item.href}>{item.label}</Link>)}</nav>{children}</main></body></html>
  );
}
