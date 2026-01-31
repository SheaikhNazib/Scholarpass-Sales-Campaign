"use client";

import { useAuthStore } from "@/actions/auth/store";
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
import { Bell, CreditCard, Settings, Shield, User } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React from "react";

type Props = {
  children: React.ReactNode;
};

export default function DashboardLayout({ children }: Props) {
  const router = useRouter();
  const user = useUserInfo();
  const { logout } = useAuthStore();

  const userData = {
    name: user ? `${user.firstName} ${user.lastName}` : "No User",
    email: user?.email || "no email",
    avatar: user?.profilePicture || undefined,
    role: "Super Admin",
    lastLogin: "2 hours ago",
  };

  // Menu items with their respective actions
  const menuItems = [
    {
      label: "Profile",
      icon: User,
      onClick: () => {
        router.push("/dashboard/profile");
      },
    },
    {
      label: "Account Security",
      icon: Shield,
      onClick: () => {
        router.push("/dashboard/security");
      },
    },
    {
      label: "Settings",
      icon: Settings,
      onClick: () => {
        router.push("/dashboard/settings");
      },
    },
    {
      label: "Notifications",
      icon: Bell,
      onClick: () => {
        router.push("/dashboard/notifications");
      },
    },
    {
      label: "Billing",
      icon: CreditCard,
      onClick: () => {
        router.push("/dashboard/billing");
      },
    },
  ];

  return (
    <div className="h-full">
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset className="flex flex-col h-full w-full">
          <header className="flex justify-between h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12 border-b border-gray-200 bg-white shadow-sm px-4">
            <div className="flex items-center gap-2">
              <SidebarTrigger className="-ml-1" />
              <Separator
                orientation="vertical"
                className="mr-2 h-4"
              />
              <DashboardBreadcrumb />
            </div>

            <div className="flex items-center">
              <div className="hidden md:block">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <button
                      type="button"
                      className="font-semibold border-0 shadow-none bg-transparent px-4 py-2 rounded-lg cursor-pointer focus:outline-none text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-all duration-200"
                    >
                      Quick Actions
                    </button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="bg-white border border-gray-200 shadow-lg rounded-xl"
                  >
                    <DropdownMenuItem asChild className="hover:bg-blue-50 hover:text-blue-700 cursor-pointer">
                      <Link href="/dashboard/create-task">Quick Task</Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild className="hover:bg-blue-50 hover:text-blue-700 cursor-pointer">
                      <Link href="/dashboard/create-task">Meeting</Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild className="hover:bg-blue-50 hover:text-blue-700 cursor-pointer">
                      <Link href="/dashboard/employee-attendance">Check In/Out</Link>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
              <div className="px-4">
                <UserProfileDropdown
                  user={userData}
                  menuItems={menuItems}
                  onLogout={() => {
                    logout();
                  }}
                />
              </div>
            </div>
          </header>
          <div className="flex flex-1 flex-col min-h-0 bg-gradient-to-br from-slate-50 to-gray-50">
            <div className="overflow-y-auto overflow-x-hidden flex-1 px-6 py-6">
              {children}
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider>
    </div>
  );
}
