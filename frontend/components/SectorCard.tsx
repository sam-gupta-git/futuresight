"use client";

import { Pencil, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Line, LineChart, ResponsiveContainer } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import type { NewsItem, QuoteData } from "@/lib/apiClient";
import { apiClient } from "@/lib/apiClient";
import type { SectorConfig } from "@/lib/useSectorConfig";

interface SectorCardProps {
  sector: SectorConfig;
  onEdit: () => void;
  onRemove: () => void;
}

export function SectorCard({ sector, onEdit, onRemove }: SectorCardProps) {
  const [quotes, setQuotes] = useState<QuoteData[]>([]);
  const [news, setNews] = useState<NewsItem[]>([]);

  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        const data = await apiClient.getQuotes(sector.symbols);
        setQuotes(data);
      } catch {
        // keep stale
      }
    };

    fetchQuotes();
    const id = setInterval(fetchQuotes, 120_000);
    return () => clearInterval(id);
  }, [sector.symbols]);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const data = await apiClient.getNews({ symbols: sector.symbols, topics: sector.topics });
        setNews(data);
      } catch {
        // keep stale
      }
    };

    fetchNews();
    const id = setInterval(fetchNews, 60_000);
    return () => clearInterval(id);
  }, [sector.symbols, sector.topics]);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-base font-semibold">{sector.name}</CardTitle>
        <div className="flex gap-1">
          <Button variant="ghost" size="icon" className="h-7 w-7" onClick={onEdit}>
            <Pencil className="h-3.5 w-3.5" />
          </Button>
          <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={onRemove}>
            <Trash2 className="h-3.5 w-3.5" />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Quotes */}
        <div className="space-y-2">
          {quotes.map((q) => (
            <div key={q.symbol} className="flex items-center gap-3">
              <Badge variant="secondary" className="font-mono text-xs">
                {q.symbol}
              </Badge>
              <span className="text-sm font-medium">${q.price.toFixed(2)}</span>
              <span className={`text-xs font-medium ${q.change_pct >= 0 ? "text-green-400" : "text-red-400"}`}>
                {q.change_pct >= 0 ? "+" : ""}
                {q.change_pct.toFixed(2)}%
              </span>
              <div className="ml-auto h-8 w-16">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={q.sparkline.map((v, i) => ({ i, v }))}>
                    <Line
                      type="monotone"
                      dataKey="v"
                      stroke={q.change_pct >= 0 ? "#4ade80" : "#f87171"}
                      dot={false}
                      strokeWidth={1.5}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          ))}
          {quotes.length === 0 && (
            <p className="text-xs text-muted-foreground">Loading quotes...</p>
          )}
        </div>

        <Separator />

        {/* News */}
        <ScrollArea className="h-48">
          <div className="space-y-2 pr-3">
            {news.map((article, i) => (
              <div key={article.url || i} className="text-sm">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-medium hover:text-primary transition-colors leading-tight line-clamp-2"
                >
                  {article.title}
                </a>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {article.source} &middot; {timeAgo(article.published_at)}
                </p>
              </div>
            ))}
            {news.length === 0 && (
              <p className="text-xs text-muted-foreground">Loading news...</p>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}
