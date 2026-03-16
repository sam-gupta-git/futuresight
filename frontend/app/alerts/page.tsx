import { AlertFeed } from "@/components/AlertFeed";
import { apiClient } from "@/lib/apiClient";

export default async function AlertsPage() {
  const alerts = await apiClient.getAlerts();
  return <section className="space-y-3"><h2 className="text-xl font-semibold">Alerts</h2><AlertFeed initialAlerts={alerts} /></section>;
}
