import { Badge } from "./Badge";
import { getTrustConfig } from "../lib/trust";

export function TrustBadge({ state, label }) {
  const config = getTrustConfig(state);
  return <Badge tone={config.tone}>{label || config.label}</Badge>;
}
