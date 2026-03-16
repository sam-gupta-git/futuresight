import "./globals.css";
import type { ReactNode } from "react";
import { Inter } from "next/font/google";

import { cn } from "@/lib/utils";
import { SidebarLayout } from "@/components/SidebarLayout";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata = { title: "FutureSight", description: "Trading analytics and scanning dashboard" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={cn("dark font-sans", inter.variable)}>
      <body>
        <SidebarLayout>{children}</SidebarLayout>
      </body>
    </html>
  );
}
