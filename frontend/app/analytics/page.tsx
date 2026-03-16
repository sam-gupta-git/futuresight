import { EquityCurve } from "@/components/EquityCurve";
import { apiClient } from "@/lib/apiClient";

export default async function AnalyticsPage() {
  const points = await apiClient.getAnalytics();
  const winRate = points.find((p) => p.metric === "win_rate")?.value ?? 0;
  const profitFactor = points.find((p) => p.metric === "profit_factor")?.value ?? 0;
  return <section className="space-y-3"><h2 className="text-xl font-semibold">Analytics</h2><div className="grid grid-cols-2 gap-3 text-sm"><div className="rounded border border-slate-700 bg-slate-900 p-3">Win Rate: {winRate.toFixed(2)}%</div><div className="rounded border border-slate-700 bg-slate-900 p-3">Profit Factor: {profitFactor.toFixed(2)}</div></div><EquityCurve points={points} /></section>;
}
