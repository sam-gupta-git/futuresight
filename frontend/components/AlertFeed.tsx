"use client";

import { useEffect, useMemo, useState } from "react";

import type { AlertRow } from "@/lib/apiClient";
import { supabase } from "@/lib/supabaseClient";

export function AlertFeed({ initialAlerts }: { initialAlerts: AlertRow[] }) {
  const [alerts, setAlerts] = useState<AlertRow[]>(initialAlerts);

  useEffect(() => {
    const channel = supabase.channel("alerts").on("postgres_changes", { event: "INSERT", schema: "public", table: "alerts" }, (payload) => {
      setAlerts((prev) => [payload.new as AlertRow, ...prev]);
    }).subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const sorted = useMemo(() => [...alerts].sort((a, b) => +new Date(b.timestamp) - +new Date(a.timestamp)), [alerts]);

  return <div className="space-y-2">{sorted.map((a) => <div key={a.id} className="rounded border border-slate-700 bg-slate-900 p-3 text-sm"><div className="font-semibold">{a.symbol} - {a.alert_type}</div><div>{a.message}</div><div className="text-xs text-slate-400">{new Date(a.timestamp).toLocaleString()}</div></div>)}</div>;
}
