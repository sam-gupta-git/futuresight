"use client";

import type { Trade } from "@/lib/apiClient";

export function TradeTable({ trades }: { trades: Trade[] }) {
  return <div className="overflow-x-auto rounded border border-slate-700"><table className="min-w-full text-sm"><thead className="bg-slate-900 text-left text-slate-300"><tr><th className="px-3 py-2">symbol</th><th className="px-3 py-2">type</th><th className="px-3 py-2">entry</th><th className="px-3 py-2">exit</th><th className="px-3 py-2">qty</th><th className="px-3 py-2">pnl</th><th className="px-3 py-2">r</th><th className="px-3 py-2">strategy</th></tr></thead><tbody>{trades.map((t) => <tr key={t.id} className="border-t border-slate-800"><td className="px-3 py-2">{t.symbol}</td><td className="px-3 py-2">{t.instrument_type}</td><td className="px-3 py-2">{t.entry_price.toFixed(2)}</td><td className="px-3 py-2">{t.exit_price?.toFixed(2) ?? "-"}</td><td className="px-3 py-2">{t.quantity}</td><td className="px-3 py-2">{t.pnl.toFixed(2)}</td><td className="px-3 py-2">{t.r_multiple.toFixed(2)}</td><td className="px-3 py-2">{t.strategy}</td></tr>)}</tbody></table></div>;
}
