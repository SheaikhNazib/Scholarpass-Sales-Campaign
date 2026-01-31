'use client';

import * as React from 'react';
import { PanelLeft } from 'lucide-react';
import { cn } from '@/lib/utils';

const SidebarContext = React.createContext<{
  open: boolean;
  setOpen: (open: boolean) => void;
  toggleSidebar: () => void;
}>({
  open: true,
  setOpen: () => {},
  toggleSidebar: () => {},
});

export function useSidebar() {
  return React.useContext(SidebarContext);
}

export function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(true);

  const toggleSidebar = React.useCallback(() => {
    setOpen((prev) => !prev);
  }, []);

  return (
    <SidebarContext.Provider value={{ open, setOpen, toggleSidebar }}>
      <div className="flex min-h-screen w-full bg-gray-100/40 dark:bg-gray-800/40">
        {children}
      </div>
    </SidebarContext.Provider>
  );
}

export function Sidebar({ className, children }: { className?: string; children?: React.ReactNode }) {
  const { open } = useSidebar();
  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-10 overflow-y-auto border-r bg-white transition-all duration-300 ease-in-out md:translate-x-0 dark:bg-gray-950",
        open ? "w-64" : "w-16",
        "-translate-x-full md:translate-x-0",
        className
      )}
    >
      {children}
    </aside>
  );
}

export function SidebarInset({ className, children }: { className?: string; children: React.ReactNode }) {
  const { open } = useSidebar();
  return (
    <div
      className={cn(
        "flex flex-col flex-1 transition-all duration-300 ease-in-out",
        open ? "md:ml-64" : "md:ml-16",
        className
      )}
    >
      {children}
    </div>
  );
}

export function SidebarTrigger({ className }: { className?: string }) {
  const { toggleSidebar } = useSidebar();
  return (
    <button
      onClick={toggleSidebar}
      className={cn("p-2 rounded-md hover:bg-gray-100", className)}
    >
      <PanelLeft className="w-5 h-5" />
      <span className="sr-only">Toggle Sidebar</span>
    </button>
  );
}
