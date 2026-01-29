'use client';

import { useState } from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';

interface Opportunity {
  id: number;
  title: string;
  contactName: string;
  email: string;
  phone: string;
  companyName: string;
  status: string;
  expectedValue: number;
  score: number;
  closingDate: string;
  owner: string;
}

export default function MyOpportunityPipelines() {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Mock data - replace with actual API call
  const opportunities: Opportunity[] = [
    {
      id: 1,
      title: 'District Wide Implementation',
      contactName: 'John Smith',
      email: 'john.smith@abschools.edu',
      phone: '(555) 123-4567',
      companyName: 'ABC School District',
      status: 'Negotiation',
      expectedValue: 50000,
      score: 75,
      closingDate: '2024-03-15',
      owner: 'You'
    },
    {
      id: 2,
      title: 'University Partnership Q1',
      contactName: 'Sarah Johnson',
      email: 's.johnson@xyz.edu',
      phone: '(555) 987-6543',
      companyName: 'XYZ University',
      status: 'Proposal',
      expectedValue: 125000,
      score: 60,
      closingDate: '2024-04-01',
      owner: 'You'
    },
  ];

  const columns: Column<Opportunity>[] = [
    {
      key: 'title',
      title: 'Title',
      sortable: true,
      render: (value) => (
        <div className="flex flex-col">
          <span className="text-sm font-medium text-gray-900">{value}</span>
        </div>
      )
    },
    {
      key: 'contactName',
      title: 'Contact',
      sortable: true,
      render: (value, item) => (
        <div className="flex flex-col">
          <span className="text-sm text-gray-900">{value}</span>
          <span className="text-xs text-gray-500">{item.email}</span>
        </div>
      )
    },
    {
      key: 'companyName',
      title: 'Company',
      sortable: true,
    },
    {
      key: 'status',
      title: 'Status',
      sortable: true,
      render: (value) => (
        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
          {value}
        </span>
      )
    },
    {
      key: 'expectedValue',
      title: 'Exp. Value',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">${value.toLocaleString()}</span>
      )
    },
    {
      key: 'score',
      title: 'Score',
      sortable: true,
      render: (value) => (
        <div className="flex items-center gap-2">
           <div className="w-16 bg-gray-200 rounded-full h-1.5">
            <div 
              className={`h-1.5 rounded-full ${value >= 70 ? 'bg-green-500' : value >= 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
              style={{ width: `${value}%` }}
            ></div>
          </div>
          <span className="text-xs text-gray-600">{value}</span>
        </div>
      )
    },
    {
      key: 'closingDate',
      title: 'Closing Date',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-500">{value}</span>
      )
    }
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Sales Opportunities</h1>
          <p className="text-gray-600 mt-1">Manage your pending opportunities</p>
        </div>
        <button className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
          <Plus className="w-5 h-5" />
          New Opportunity
        </button>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search opportunities..."
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

      {/* Pipeline List */}
      <TableArchive
        data={opportunities}
        columns={columns}
        itemsPerPage={10}
        onRowClick={(row) => console.log('Clicked:', row)}
        emptyMessage="No sales opportunities found"
      />
    </div>
  );
}
