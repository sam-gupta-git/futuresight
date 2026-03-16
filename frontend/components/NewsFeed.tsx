"use client";

import { useEffect, useState } from "react";

import type { NewsItem } from "@/lib/apiClient";
import { apiClient } from "@/lib/apiClient";

interface NewsFeedProps {
  initialArticles: NewsItem[];
  symbols?: string[];
  topics?: string[];
}

function highlightSymbols(text: string, symbols: string[]): React.ReactNode {
  if (!symbols.length) return text;
  const pattern = new RegExp(`\\b(${symbols.map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})\\b`, "gi");
  const parts = text.split(pattern);
  return parts.map((part, i) =>
    symbols.some((s) => s.toLowerCase() === part.toLowerCase())
      ? <mark key={i} className="bg-amber-400/20 text-amber-300 rounded px-0.5">{part}</mark>
      : part
  );
}

export function NewsFeed({ initialArticles, symbols = [], topics = [] }: NewsFeedProps) {
  const [articles, setArticles] = useState<NewsItem[]>(initialArticles);

  useEffect(() => {
    const refresh = async () => {
      try {
        const fresh = await apiClient.getNews({ symbols, topics });
        setArticles(fresh);
      } catch {
        // keep stale data on error
      }
    };

    const id = setInterval(refresh, 60_000);
    return () => clearInterval(id);
  }, [symbols, topics]);

  return (
    <div className="space-y-3">
      {articles.map((article, i) => (
        <div key={article.url || i} className="rounded border border-slate-700 bg-slate-900 p-4 text-sm">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-slate-100 hover:text-blue-400 transition-colors"
          >
            {highlightSymbols(article.title, symbols)}
          </a>
          <div className="mt-1 text-xs text-slate-400">
            {article.source} &middot; {new Date(article.published_at).toLocaleString()}
          </div>
          <p className="mt-2 text-slate-300 leading-relaxed">
            {article.summary.length > 180 ? article.summary.slice(0, 180) + "…" : article.summary}
          </p>
          {article.symbols.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {article.symbols.map((sym) => (
                <span
                  key={sym}
                  className={`rounded px-1.5 py-0.5 text-xs font-mono ${
                    symbols.includes(sym)
                      ? "bg-amber-400/20 text-amber-300 border border-amber-400/30"
                      : "bg-slate-800 text-slate-400"
                  }`}
                >
                  {sym}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
