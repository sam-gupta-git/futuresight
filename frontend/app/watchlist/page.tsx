import { WatchlistTable } from "@/components/WatchlistTable";
import { apiClient } from "@/lib/apiClient";

export default async function WatchlistPage() {
  const signals = await apiClient.getWatchlist();
  return <section className="space-y-3"><h2 className="text-xl font-semibold">Watchlist</h2><WatchlistTable signals={signals} /></section>;
}
