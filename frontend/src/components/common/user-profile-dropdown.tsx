'use client';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User, LogOut } from "lucide-react";
import React from 'react';

interface UserData {
  name: string;
  email: string;
  avatar?: string;
  role?: string;
  lastLogin?: string;
}

interface MenuItem {
    label: string;
    icon: React.ComponentType<{ className?: string }>;
    onClick: () => void;
}

interface UserProfileDropdownProps {
  user: UserData;
  menuItems: MenuItem[];
  onLogout: () => void;
}

export function UserProfileDropdown({ user, menuItems, onLogout }: UserProfileDropdownProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="flex items-center gap-2 focus:outline-none">
          <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
             {user.avatar ? (
                 <img src={user.avatar} alt={user.name} className="h-full w-full object-cover" />
             ) : (
                 <User className="h-5 w-5 text-gray-500" />
             )}
          </div>
          <div className="hidden md:block text-left">
            <p className="text-sm font-medium text-gray-700">{user.name}</p>
            <p className="text-xs text-gray-500">{user.role}</p>
          </div>
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{user.name}</p>
            <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        {menuItems.map((item, index) => {
            const Icon = item.icon;
            return (
                <DropdownMenuItem key={index} onClick={item.onClick}>
                    <Icon className="mr-2 h-4 w-4" />
                    <span>{item.label}</span>
                </DropdownMenuItem>
            )
        })}
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={onLogout}>
          <span className="flex items-center">
            <LogOut className="mr-2 h-4 w-4" />
            Log out
          </span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
