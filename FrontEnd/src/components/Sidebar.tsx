import React from 'react';
import { cn } from '../lib/utils';

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ReactNode;
}

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  items: SidebarItem[];
}

export default function Sidebar({ activeTab, onTabChange, items }: SidebarProps) {
  return (
    <aside className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <h1 className="text-xl font-bold">Optimización de Atraque</h1>
      </div>
      <nav className="mt-6">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => onTabChange(item.id)}
            className={cn(
              'w-full flex items-center space-x-3 px-6 py-4 text-sm font-medium transition-colors',
              activeTab === item.id
                ? 'bg-gray-800 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
            )}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}