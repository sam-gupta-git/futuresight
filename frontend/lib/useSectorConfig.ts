"use client";

import { useCallback, useEffect, useState } from "react";

export interface SectorConfig {
  id: string;
  name: string;
  symbols: string[];
  topics: string[];
}

const STORAGE_KEY = "futuresight_sectors";

const DEFAULT_SECTORS: SectorConfig[] = [
  { id: "natural-gas", name: "Natural Gas", symbols: ["NG"], topics: ["natural gas", "lng"] },
  { id: "oil", name: "Oil", symbols: ["CL", "BZ"], topics: ["oil", "crude", "petroleum"] },
  { id: "mining", name: "Mining", symbols: ["FCX", "NEM", "BHP"], topics: ["mining", "metals", "gold"] },
];

export function useSectorConfig() {
  const [sectors, setSectors] = useState<SectorConfig[]>(DEFAULT_SECTORS);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as SectorConfig[];
        if (Array.isArray(parsed) && parsed.length > 0) {
          setSectors(parsed);
        }
      }
    } catch {
      // use defaults
    }
    setHydrated(true);
  }, []);

  const persist = useCallback((updated: SectorConfig[]) => {
    setSectors(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }, []);

  const addSector = useCallback(
    (sector: Omit<SectorConfig, "id">) => {
      const id = sector.name.toLowerCase().replace(/\s+/g, "-") + "-" + Date.now();
      persist([...sectors, { ...sector, id }]);
    },
    [sectors, persist],
  );

  const updateSector = useCallback(
    (id: string, data: Omit<SectorConfig, "id">) => {
      persist(sectors.map((s) => (s.id === id ? { ...data, id } : s)));
    },
    [sectors, persist],
  );

  const removeSector = useCallback(
    (id: string) => {
      persist(sectors.filter((s) => s.id !== id));
    },
    [sectors, persist],
  );

  return { sectors, hydrated, addSector, updateSector, removeSector };
}
