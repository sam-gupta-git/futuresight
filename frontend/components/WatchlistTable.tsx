"use client";

import type { Signal } from "@/lib/apiClient";

export function WatchlistTable({ signals }: { signals: Signal[] }) {
  return <div className="overflow-x-auto rounded border border-slate-700"><table className="min-w-full text-sm"><thead className="bg-slate-900 text-left text-slate-300"><tr><th className="px-3 py-2">symbol</th><th className="px-3 py-2">price</th><th className="px-3 py-2">signal</th><th className="px-3 py-2">confidence</th><th className="px-3 py-2">timestamp</th></tr></thead><tbody>{signals.map((s) => <tr key={s.id} className="border-t border-slate-800"><td className="px-3 py-2">{s.symbol}</td><td className="px-3 py-2">{s.price.toFixed(2)}</td><td className="px-3 py-2">{s.signal_type}</td><td className="px-3 py-2">{(s.confidence * 100).toFixed(1)}%</td><td className="px-3 py-2">{new Date(s.created_at).toLocaleString()}</td></tr>)}</tbody></table></div>;
}
