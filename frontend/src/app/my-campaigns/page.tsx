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
  
  // Mock data - replace with actual API call
  const campaigns: Campaign[] = [
    {
      id: 1,
      name: 'Spring 2026 Enrollment Drive',
      status: 'Active',
      type: 'Email',
      startDate: '2026-01-15',
      endDate: '2026-03-31',
      budget: 15000,
      leads: 245,
      owner: 'You'
    },
    {
      id: 2,
      name: 'Financial Aid Awareness',
      status: 'Active',
      type: 'Multi-Channel',
      startDate: '2026-01-20',
      endDate: '2026-02-28',
      budget: 25000,
      leads: 180,
      owner: 'You'
    },
  ];

  const columns: Column<Campaign>[] = [
    {
      key: 'name',
      title: 'Campaign Name',
      sortable: true,
      render: (value) => (
        <div className="text-sm font-medium text-gray-900">{value}</div>
      )
    },
    {
      key: 'status',
      title: 'Status',
      sortable: true,
      render: (value) => (
        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
          {value}
        </span>
      )
    },
    {
      key: 'type',
      title: 'Type',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value}</span>
      )
    },
    {
      key: 'startDate',
      title: 'Duration',
      sortable: false,
      render: (value, row) => (
        <span className="text-sm text-gray-500">
          {row.startDate} - {row.endDate}
        </span>
      )
    },
    {
      key: 'budget',
      title: 'Budget',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">${value.toLocaleString()}</span>
      )
    },
    {
      key: 'leads',
      title: 'Leads',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value}</span>
      )
    }
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">My Campaign List</h1>
          <p className="text-gray-600 mt-1">Manage your assigned campaigns</p>
        </div>
        <button className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
          <Plus className="w-5 h-5" />
          New Campaign
        </button>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search campaigns..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Filter className="w-5 h-5" />
            Filter
          </button>
        </div>
      </div>

      {/* Campaign List */}
      <TableArchive
        data={campaigns}
        columns={columns}
        itemsPerPage={10}
        onRowClick={(row) => console.log('Clicked:', row)}
        emptyMessage="No campaigns found"
      />
    </div>
  );
}
