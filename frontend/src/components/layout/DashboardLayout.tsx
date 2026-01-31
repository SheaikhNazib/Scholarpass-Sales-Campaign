"use client";

import { useRouter, usePathname } from "next/navigation";
import React, { useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { AppSidebar } from "@/components/app-sidebar";
import { DashboardBreadcrumb } from "@/components/breadcrumb/dashboard-breadcrumb";
import { UserProfileDropdown } from "@/components/common/user-profile-dropdown";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import useUserInfo from "@/hooks/useUserInfo";
import { Bell, CreditCard, Settings, Shield, User, LogOut } from "lucide-react";
import Link from "next/link";

type Props = {
  children: React.ReactNode;
};

export default function DashboardLayout({ children }: Props) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, isLoading, user, logout } = useAuth();
  const userInfo = useUserInfo();

  // Check if we're on an auth page
  const isAuthPage = pathname === '/login' || pathname === '/register';
  // Redirect to login when user is not authenticated and not on auth pages
  React.useEffect(() => {
    if (!isAuthPage && !isLoading && !isAuthenticated) {
      router.push(`/login?redirect=${pathname}`);
    }
  }, [isAuthPage, isLoading, isAuthenticated, pathname, router]);

  // If on auth page, just render children without sidebar
  if (isAuthPage) {
    return <div className="h-full">{children}</div>;
  }

  // If loading, show loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If not authenticated (and not loading), don't render layout
  if (!isAuthenticated) {
    return null;
  }

  // Prefer authenticated user info when available
  const userData = {
    name: user ? `${(user as any).first_name || ''} ${(user as any).last_name || ''}`.trim() || (userInfo ? `${userInfo.firstName} ${userInfo.lastName}`.trim() : 'User') : (userInfo ? `${userInfo.firstName} ${userInfo.lastName}`.trim() : 'User'),
    email: (user as any)?.email || userInfo?.email || 'no email',
    avatar: (user as any)?.profile_picture_url || userInfo?.profilePicture || undefined,
    role: (user as any)?.primary_role_id ? `role-${(user as any).primary_role_id}` : 'User',
    lastLogin: 'Just now',
  };

  const menuItems: Array<{
    label: string;
    icon: React.ComponentType<{ className?: string }>;
    onClick: () => void;
  }> = [
    // {
    //   label: "Profile",
    //   icon: User,
    //   onClick: () => {
    //     router.push("/dashboard/profile");
    //   },
    // },
    // {
    //   label: "Account Security",
    //   icon: Shield,
    //   onClick: () => {
    //     router.push("/dashboard/security");
    //   },
    // },
    // {
    //   label: "Settings",
    //   icon: Settings,
    //   onClick: () => {
    //     router.push("/dashboard/settings");
    //   },
    // },
    // {
    //   label: "Notifications",
    //   icon: Bell,
    //   onClick: () => {
    //     router.push("/dashboard/notifications");
    //   },
    // },
    // {
    //   label: "Billing",
    //   icon: CreditCard,
    //   onClick: () => {
    //     router.push("/dashboard/billing");
    //   },
    // },
  ];

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div className="h-full">
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset className="flex flex-col h-full w-full">
          <header className="flex justify-between h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 border-b bg-white px-4">
            <div className="flex items-center gap-2">
              <DashboardBreadcrumb />
            </div>

            <div className="flex items-center">
              <div className="hidden md:block">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <button
                      type="button"
                      className="font-semibold border-0 shadow-none bg-transparent px-4 py-2 rounded cursor-pointer focus:outline-none text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Quick Actions
                    </button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem asChild>
                      <Link href="/my-campaigns">My Campaigns</Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild>
                      <Link href="/my-opportunity-pipelines">Opportunities</Link>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
              <div className="px-4">
                <UserProfileDropdown
                  user={userData}
                  menuItems={menuItems}
                  onLogout={handleLogout}
                />
              </div>
            </div>
          </header>
          <div className="flex flex-1 flex-col min-h-0 bg-gray-50/50">
            <div className="overflow-y-auto overflow-x-hidden flex-1 px-4 py-4">
              {children}
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}
