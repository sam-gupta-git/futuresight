import { RiskBanner } from "@/components/RiskBanner";
import { TradeTable } from "@/components/TradeTable";
import { apiClient } from "@/lib/apiClient";

export default async function TradesPage() {
  const trades = await apiClient.getTrades();
  return <section className="space-y-3"><h2 className="text-xl font-semibold">Trades</h2><RiskBanner /><TradeTable trades={trades} /></section>;
}
