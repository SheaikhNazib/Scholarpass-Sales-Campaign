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
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center border-b border-gray-200 px-6 bg-white">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-500 bg-clip-text text-transparent">
              ScholarPASS
            </h1>
            <p className="text-xs text-gray-600 mt-0.5 font-medium">Sales Campaign</p>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto py-6">
           <nav className="grid gap-1 px-3 text-sm font-medium">
             {menuItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                return (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={`flex items-center gap-3 rounded-xl px-4 py-3 transition-all duration-200 ${
                            isActive 
                              ? "bg-blue-500 text-white font-semibold shadow-md shadow-blue-200" 
                              : "text-gray-700 hover:bg-blue-50 hover:text-blue-700 hover:shadow-sm"
                        }`}
                    >
                        <Icon className={`h-5 w-5 ${isActive ? 'text-white' : 'text-gray-500'}`} />
                        {item.title}
                    </Link>
                )
             })}
           </nav>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 bg-white">
           <div className="text-xs text-gray-500">
            © 2026 ScholarPASS
          </div>
        </div>
      </div>
    </Sidebar>
  )
}
