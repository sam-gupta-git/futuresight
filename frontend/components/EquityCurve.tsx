"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { AnalyticsPoint } from "@/lib/apiClient";

export function EquityCurve({ points }: { points: AnalyticsPoint[] }) {
  const curve = points.filter((p) => p.metric === "cumulative_pnl").map((p) => ({ time: new Date(p.timestamp).toLocaleTimeString(), value: p.value })).reverse();

  return <div className="h-72 rounded border border-slate-700 bg-slate-900 p-3"><ResponsiveContainer width="100%" height="100%"><LineChart data={curve}><XAxis dataKey="time" /><YAxis /><Tooltip /><Line type="monotone" dataKey="value" stroke="#38bdf8" dot={false} /></LineChart></ResponsiveContainer></div>;
}
