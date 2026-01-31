'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight, Home } from 'lucide-react';

export function DashboardBreadcrumb() {
  const pathname = usePathname();
  const segments = pathname.split('/').filter(Boolean);

  return (
    <nav className="flex" aria-label="Breadcrumb">
      <ol className="inline-flex items-center space-x-1 md:space-x-3">
        <li className="inline-flex items-center">
          <Link href="/" className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-blue-600">
            <Home className="w-4 h-4 mr-2 mb-1" />
            <span className="self-center">Dashboard</span>
          </Link>
        </li>
        {segments.map((segment, index) => {
          const href = `/${segments.slice(0, index + 1).join('/')}`;
          const isLast = index === segments.length - 1;
          const title = segment.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

          return (
            <li key={segment}>
              <div className="flex items-center">
                <ChevronRight className="w-4 h-4 text-gray-400" />
                {isLast ? (
                  <span className="ml-1 text-sm font-medium text-gray-500 md:ml-2">
                    {title}
                  </span>
                ) : (
                  <Link href={href} className="ml-1 text-sm font-medium text-gray-700 hover:text-blue-600 md:ml-2">
                    {title}
                  </Link>
                )}
              </div>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
