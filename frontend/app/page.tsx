import Link from "next/link";

import { NewsFeed } from "@/components/NewsFeed";
import { apiClient } from "@/lib/apiClient";

const SYMBOLS = ["NVDA", "SPY", "AAPL"];
const TOPICS = ["options", "futures"];

export default async function HomePage() {
  let articles = await apiClient.getNews({ symbols: SYMBOLS, topics: TOPICS }).catch(() => []);

  return (
    <div className="space-y-6">
      <p className="text-slate-300">Real-time trading signals, alerts, trade log, and analytics.</p>
      <ul className="list-disc pl-5 text-slate-200">
        <li><Link href="/watchlist">Watchlist</Link></li>
        <li><Link href="/alerts">Alerts</Link></li>
        <li><Link href="/trades">Trades</Link></li>
        <li><Link href="/analytics">Analytics</Link></li>
      </ul>
      <div>
        <h2 className="mb-3 text-lg font-semibold text-slate-100">Market News</h2>
        <NewsFeed initialArticles={articles} symbols={SYMBOLS} topics={TOPICS} />
      </div>
    </div>
  );
}
