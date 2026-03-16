"use client";

import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { SectorCard } from "@/components/SectorCard";
import { SectorDialog } from "@/components/SectorDialog";
import type { SectorConfig } from "@/lib/useSectorConfig";
import { useSectorConfig } from "@/lib/useSectorConfig";

export function SectorGrid() {
  const { sectors, hydrated, addSector, updateSector, removeSector } = useSectorConfig();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingSector, setEditingSector] = useState<SectorConfig | undefined>();

  const handleEdit = (sector: SectorConfig) => {
    setEditingSector(sector);
    setDialogOpen(true);
  };

  const handleAdd = () => {
    setEditingSector(undefined);
    setDialogOpen(true);
  };

  const handleSave = (data: Omit<SectorConfig, "id">) => {
    if (editingSector) {
      updateSector(editingSector.id, data);
    } else {
      addSector(data);
    }
  };

  const handleRemove = (id: string) => {
    if (window.confirm("Remove this sector?")) {
      removeSector(id);
    }
  };

  if (!hydrated) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Sector Dashboard</h2>
        <Button size="sm" onClick={handleAdd}>
          <Plus className="mr-1.5 h-4 w-4" />
          Add Sector
        </Button>
      </div>
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))" }}
      >
        {sectors.map((sector) => (
          <SectorCard
            key={sector.id}
            sector={sector}
            onEdit={() => handleEdit(sector)}
            onRemove={() => handleRemove(sector.id)}
          />
        ))}
      </div>
      <SectorDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        sector={editingSector}
        onSave={handleSave}
      />
    </div>
  );
}
