'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  TrendingUp, 
  ListChecks,
  Megaphone,
  Target,
  ChevronRight
} from 'lucide-react';

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

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-white shadow-lg">
      <div className="h-full flex flex-col">
        {/* Logo/Header */}
        <div className="px-6 py-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-primary-600">
            ScholarPASS
          </h1>
          <p className="text-sm text-gray-500 mt-1">Sales Campaign</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center px-4 py-3 rounded-lg transition-all duration-200
                  ${isActive 
                    ? 'bg-primary-50 text-primary-700 font-semibold' 
                    : 'text-gray-700 hover:bg-gray-50 hover:text-primary-600'
                  }
                `}
              >
                <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-primary-600' : 'text-gray-500'}`} />
                <span className="flex-1 text-sm">{item.title}</span>
                {isActive && (
                  <ChevronRight className="w-4 h-4 text-primary-600" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            © 2026 ScholarPASS
          </div>
        </div>
      </div>
    </aside>
  );
}
