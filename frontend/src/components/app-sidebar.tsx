'use client';

import * as React from "react"
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Image from 'next/image';
import {
  LayoutDashboard,
  TrendingUp,
  ListChecks,
  Megaphone,
  Target,
  Settings,
  Users,
  ShieldCheck,
  ChevronDown,
  ChevronRight,
  ChevronLeft,
} from 'lucide-react';
import {
  Sidebar,
  useSidebar,
} from "@/components/ui/sidebar"
import { useAuth } from '@/hooks/useAuth';

interface MenuItem {
  title: string;
  href?: string;
  icon: React.ComponentType<{ className?: string }>;
  items?: {
    title: string;
    href: string;
    icon: React.ComponentType<{ className?: string }>;
  }[];
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
  const { user } = useAuth();
  const { open, toggleSidebar } = useSidebar();
  const [isAdminOpen, setIsAdminOpen] = React.useState(true);

  const isAdmin = user?.primary_role_name === 'Super Admin' || user?.username === 'superadmin';

  const items = [...menuItems];

  if (isAdmin) {
    items.push({
      title: 'Admin Settings',
      icon: Settings,
      items: [
        {
          title: 'Users',
          href: '/admin/users',
          icon: Users,
        },
        {
          title: 'User Roles',
          href: '/admin/roles',
          icon: ShieldCheck,
        },
      ],
    });
  }

  return (
    <Sidebar {...props}>
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center border-b px-6 justify-between">
          <Link href="/" className="flex items-center gap-3 cursor-pointer">
            <Image
              src="/logo.png"
              alt="ScholarPASS Logo"
              width={32}
              height={32}
              className="h-8 w-8"
            />
            {open && (
              <h1 className="text-xl font-bold text-primary-600">
                ScholarPASS
              </h1>
            )}
          </Link>
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-md hover:bg-gray-100 transition-colors"
            title={open ? "Collapse sidebar" : "Expand sidebar"}
          >
            {open ? (
              <ChevronLeft className="h-5 w-5 text-gray-500" />
            ) : (
              <ChevronRight className="h-5 w-5 text-gray-500" />
            )}
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto py-4">
          <nav className="grid gap-1 px-4 text-sm font-medium">
            {items.map((item, idx) => {
              const Icon = item.icon;
              const hasSubItems = item.items && item.items.length > 0;
              const isActive = item.href ? pathname === item.href : false;

              if (hasSubItems) {
                return (
                  <div key={item.title} className="grid gap-1">
                    <button
                      onClick={() => setIsAdminOpen(!isAdminOpen)}
                      className="flex items-center justify-between gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-primary-600"
                      title={item.title}
                    >
                      <div className="flex items-center gap-3">
                        <Icon className="h-4 w-4 flex-shrink-0" />
                        {open && <span>{item.title}</span>}
                      </div>
                      {open && (
                        isAdminOpen ? (
                          <ChevronDown className="h-4 w-4" />
                        ) : (
                          <ChevronRight className="h-4 w-4" />
                        )
                      )}
                    </button>
                    {isAdminOpen && open && (
                      <div className="ml-4 grid gap-1 border-l pl-2">
                        {item.items?.map((subItem) => {
                          const SubIcon = subItem.icon;
                          const isSubActive = pathname === subItem.href;
                          return (
                            <Link
                              key={subItem.href}
                              href={subItem.href}
                              className={`flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary-600 ${isSubActive ? "bg-gray-100 text-primary-600" : "text-gray-500"
                                }`}
                              title={subItem.title}
                            >
                              <SubIcon className="h-4 w-4 flex-shrink-0" />
                              {subItem.title}
                            </Link>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              }

              return (
                <Link
                  key={item.href || item.title}
                  href={item.href!}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary-600 ${isActive ? "bg-gray-100 text-primary-600" : "text-gray-500"
                    }`}
                  title={item.title}
                >
                  <Icon className="h-4 w-4 flex-shrink-0" />
                  {open && <span>{item.title}</span>}
                </Link>
              )
            })}
          </nav>
        </div>

        {/* Footer */}
        {open && (
          <div className="p-4 border-t">
            <div className="text-xs text-gray-500">
              © 2026 ScholarPASS
            </div>
          </div>
        )}
      </div>
    </Sidebar>
  )
}
