'use client';

import * as React from "react"
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  TrendingUp, 
  ListChecks,
  Megaphone,
  Target,
} from 'lucide-react';
import {
  Sidebar,
} from "@/components/ui/sidebar"

interface MenuItem {
  title: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const menuItems: MenuItem[] = [
  {
    title: 'Dashboard',
    href: '/',
    icon: LayoutDashboard,
  },
  {
    title: 'My Opportunity Pipeline List',
    href: '/my-opportunity-pipelines',
    icon: Target,
  },
  {
    title: 'Opportunity Pipeline List',
    href: '/opportunity-pipelines',
    icon: TrendingUp,
  },
  {
    title: 'My Campaign List',
    href: '/my-campaigns',
    icon: ListChecks,
  },
  {
    title: 'Campaign List',
    href: '/campaigns',
    icon: Megaphone,
  },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const pathname = usePathname();

  return (
    <Sidebar {...props}>
      <div className="flex h-full flex-col gap-4">
        {/* Header */}
        <div className="flex h-16 items-center border-b px-6">
           <h1 className="text-xl font-bold text-primary-600">
            ScholarPASS
          </h1>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto py-4">
           <nav className="grid gap-1 px-4 text-sm font-medium">
             {menuItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                return (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={`flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary-600 ${
                            isActive ? "bg-gray-100 text-primary-600" : "text-gray-500"
                        }`}
                    >
                        <Icon className="h-4 w-4" />
                        {item.title}
                    </Link>
                )
             })}
           </nav>
        </div>

        {/* Footer */}
        <div className="p-4 border-t">
           <div className="text-xs text-gray-500">
            © 2026 ScholarPASS
          </div>
        </div>
      </div>
    </Sidebar>
  )
}
