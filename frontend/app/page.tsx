import Link from "next/link";

export default function HomePage() {
  return <div className="space-y-4"><p className="text-slate-300">Real-time trading signals, alerts, trade log, and analytics.</p><ul className="list-disc pl-5 text-slate-200"><li><Link href="/watchlist">Watchlist</Link></li><li><Link href="/alerts">Alerts</Link></li><li><Link href="/trades">Trades</Link></li><li><Link href="/analytics">Analytics</Link></li></ul></div>;
}
