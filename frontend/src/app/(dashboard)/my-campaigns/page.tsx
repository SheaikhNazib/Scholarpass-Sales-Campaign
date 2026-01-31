'use client';

import { useState } from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';

interface Campaign {
  id: number;
  name: string;
  status: string;
  type: string;
  startDate: string;
  endDate: string;
  budget: number;
  leads: number;
  owner: string;
}

export default function MyCampaigns() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);

  // Mock data
  const campaigns: Campaign[] = [
    {
      id: 1,
      name: 'Summer Sale 2024',
      status: 'Active',
      type: 'Email Campaign',
      startDate: '2024-06-01',
      endDate: '2024-08-31',
      budget: 5000,
      leads: 250,
      owner: 'John Doe',
    },
    {
      id: 2,
      name: 'Black Friday Promo',
      status: 'Planning',
      type: 'Social Media',
      startDate: '2024-11-15',
      endDate: '2024-11-30',
      budget: 8000,
      leads: 450,
      owner: 'Jane Smith',
    },
    {
      id: 3,
      name: 'New Product Launch',
      status: 'Completed',
      type: 'Multi-Channel',
      startDate: '2024-01-15',
      endDate: '2024-03-15',
      budget: 12000,
      leads: 890,
      owner: 'Mike Johnson',
    },
  ];

  const columns: Column<Campaign>[] = [
    { key: 'name', title: 'Campaign Name' },
    { key: 'status', title: 'Status' },
    { key: 'type', title: 'Type' },
    { key: 'startDate', title: 'Start Date' },
    { key: 'endDate', title: 'End Date' },
    { key: 'budget', title: 'Budget', render: (value) => `$${value}` },
    { key: 'leads', title: 'Leads' },
    { key: 'owner', title: 'Owner' },
  ];

  const filtered = campaigns.filter((campaign) =>
    campaign.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Campaigns</h1>
          <p className="text-gray-600 mt-1">Manage your sales campaigns</p>
        </div>
        <button className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
          <Plus size={20} />
          New Campaign
        </button>
      </div>

      {/* Search and Filter Bar */}
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search campaigns..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
          />
        </div>
        <button
          onClick={() => setFilterOpen(!filterOpen)}
          className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <Filter size={20} />
          Filter
        </button>
      </div>

      {/* Filter Panel */}
      {filterOpen && (
        <div className="p-4 bg-white border border-gray-300 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600">
                <option>All Status</option>
                <option>Active</option>
                <option>Planning</option>
                <option>Completed</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600">
                <option>All Types</option>
                <option>Email Campaign</option>
                <option>Social Media</option>
                <option>Multi-Channel</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Owner
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600">
                <option>All Owners</option>
                <option>John Doe</option>
                <option>Jane Smith</option>
                <option>Mike Johnson</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <TableArchive
          data={filtered}
          columns={columns}
          onRowClick={(row) => console.log('Campaign clicked:', row)}
        />
      </div>
    </div>
  );
}
