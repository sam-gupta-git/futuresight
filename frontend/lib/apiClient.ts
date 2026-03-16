export type Signal = { id: string; symbol: string; signal_type: string; price: number; confidence: number; created_at: string };
export type AlertRow = { id: string; symbol: string; alert_type: string; message: string; timestamp: string };
export type Trade = { id: string; symbol: string; instrument_type: string; entry_price: number; exit_price: number | null; quantity: number; entry_time: string; exit_time: string | null; strategy: string; pnl: number; r_multiple: number; notes: string };
export type AnalyticsPoint = { metric: string; value: number; timestamp: string };
export type NewsItem = { title: string; source: string; summary: string; url: string; published_at: string; symbols: string[] };
export type QuoteData = { symbol: string; price: number; change_pct: number; sparkline: number[] };

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return (await res.json()) as T;
}

export const apiClient = {
  getWatchlist: () => getJson<Signal[]>("/watchlist"),
  getAlerts: () => getJson<AlertRow[]>("/alerts"),
  getTrades: () => getJson<Trade[]>("/trades"),
  getAnalytics: () => getJson<AnalyticsPoint[]>("/analytics"),
  getNews: (params?: { symbols?: string[]; topics?: string[] }) => {
    const s = params?.symbols?.join(",") ?? "";
    const t = params?.topics?.join(",") ?? "";
    return getJson<NewsItem[]>(`/news?symbols=${encodeURIComponent(s)}&topics=${encodeURIComponent(t)}`);
  },
  getQuotes: (symbols: string[]) => {
    const s = symbols.join(",");
    return getJson<QuoteData[]>(`/market/quotes?symbols=${encodeURIComponent(s)}`);
  },
};
