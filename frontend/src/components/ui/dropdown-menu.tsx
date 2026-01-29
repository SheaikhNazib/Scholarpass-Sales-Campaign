'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface DropdownMenuProps {
  children: React.ReactNode;
}

const DropdownContext = React.createContext<{
  open: boolean;
  setOpen: (open: boolean) => void;
}>({ open: false, setOpen: () => {} });

export function DropdownMenu({ children }: DropdownMenuProps) {
  const [open, setOpen] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <DropdownContext.Provider value={{ open, setOpen }}>
      <div className="relative inline-block text-left" ref={containerRef}>
        {children}
      </div>
    </DropdownContext.Provider>
  );
}

export function DropdownMenuTrigger({ asChild, children }: { asChild?: boolean; children: React.ReactNode }) {
  const { open, setOpen } = React.useContext(DropdownContext);
  
  const handleClick = () => {
    setOpen(!open);
  };

  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement, {
      onClick: handleClick, 
      "aria-expanded": open
    } as React.DOMAttributes<HTMLElement>);
  }

  return (
    <button type="button" onClick={handleClick} aria-expanded={open}>
      {children}
    </button>
  );
}

export function DropdownMenuContent({ className, children, align = "end" }: { className?: string; children: React.ReactNode; align?: "start" | "end" }) {
  const { open } = React.useContext(DropdownContext);

  if (!open) return null;

  return (
    <div
      className={cn(
        "absolute z-50 mt-2 w-56 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none",
        align === "end" ? "right-0" : "left-0",
        className
      )}
    >
      <div className="py-1" role="menu" aria-orientation="vertical">
        {children}
      </div>
    </div>
  );
}

export function DropdownMenuItem({ asChild, children, className, onClick }: { asChild?: boolean; children: React.ReactNode; className?: string; onClick?: () => void }) {
  const { setOpen } = React.useContext(DropdownContext);

  const handleClick = () => {
    if (onClick) onClick();
    setOpen(false);
  };

  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement, {
      className: cn("block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer w-full text-left", className),
      onClick: handleClick
    } as React.DOMAttributes<HTMLElement>);
  }

  return (
    <button
      className={cn("block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left", className)}
      role="menuitem"
      onClick={handleClick}
    >
      {children}
    </button>
  );
}

export function DropdownMenuLabel({ children, className }: { children: React.ReactNode; className?: string }) {
   return <div className={cn("px-4 py-2 text-sm font-semibold text-gray-900", className)}>{children}</div>;
}

export function DropdownMenuSeparator({ className }: { className?: string }) {
    return <div className={cn("-mx-1 my-1 h-px bg-gray-100", className)} />;
}
