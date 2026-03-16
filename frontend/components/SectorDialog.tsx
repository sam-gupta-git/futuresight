"use client";

import { useState, useEffect } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import type { SectorConfig } from "@/lib/useSectorConfig";

interface SectorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  sector?: SectorConfig;
  onSave: (data: Omit<SectorConfig, "id">) => void;
}

export function SectorDialog({ open, onOpenChange, sector, onSave }: SectorDialogProps) {
  const [name, setName] = useState("");
  const [symbols, setSymbols] = useState("");
  const [topics, setTopics] = useState("");

  useEffect(() => {
    if (open) {
      setName(sector?.name ?? "");
      setSymbols(sector?.symbols.join(", ") ?? "");
      setTopics(sector?.topics.join(", ") ?? "");
    }
  }, [open, sector]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !symbols.trim()) return;
    onSave({
      name: name.trim(),
      symbols: symbols.split(",").map((s) => s.trim()).filter(Boolean),
      topics: topics.split(",").map((t) => t.trim()).filter(Boolean),
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{sector ? "Edit Sector" : "Add Sector"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Name</label>
            <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Natural Gas" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Symbols</label>
            <Input value={symbols} onChange={(e) => setSymbols(e.target.value)} placeholder="e.g. NG, CL, BZ" />
            <p className="text-xs text-muted-foreground">Comma-separated ticker symbols</p>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Topics</label>
            <Input value={topics} onChange={(e) => setTopics(e.target.value)} placeholder="e.g. oil, crude, petroleum" />
            <p className="text-xs text-muted-foreground">Comma-separated keywords for news filtering</p>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={!name.trim() || !symbols.trim()}>
              {sector ? "Save" : "Add"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
