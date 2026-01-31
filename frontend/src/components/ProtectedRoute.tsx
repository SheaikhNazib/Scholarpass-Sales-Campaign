'use client';

import React, { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRoles?: string[];
}

export function ProtectedRoute({ children, requiredRoles }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  // If requiredRoles provided, check user's primary role id or name
  if (requiredRoles && requiredRoles.length > 0) {
    const hasRole = (() => {
      if (!user) return false;
      // primary_role_id may be number; requiredRoles may be names or ids
      const primaryRoleId = (user as any).primary_role_id;
      const primaryRoleName = (user as any).primary_role_name || (user as any).role;

      // Check by id
      if (primaryRoleId) {
        if (requiredRoles.includes(String(primaryRoleId))) return true;
      }

      // Check by name
      if (primaryRoleName) {
        if (requiredRoles.includes(String(primaryRoleName))) return true;
      }

      return false;
    })();

    if (!hasRole) {
      // Forbidden — redirect to home/dashboard
      router.push('/');
      return null;
    }
  }

  return <>{children}</>;
}

export default ProtectedRoute;
