'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { leadActions, Lead } from '@/actions/lead';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

export default function MyOpportunityPipelines() {
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Debounce search term
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm);
    }, 500);

    return () => clearTimeout(timer);
  }, [searchTerm]);

  // Fetch leads from API
  useEffect(() => {
    if (!isAuthenticated || !user) return;

    const fetchLeads = async () => {
      try {
        setLoading(true);
        const response = await leadActions.getMy({
          per_page: 100, // Get more items since backend doesn't support pagination
          search: debouncedSearch || undefined,
        });
        
        // Filter leads where user_id matches the current user's id
        const filteredByUser = (response || []).filter(
          (lead) => lead.user_id === user.id
        );
        
        setLeads(filteredByUser);
      } catch (error) {
        console.error('Failed to fetch leads:', error);
        setLeads([]);
      } finally {
        setLoading(false);
      }
    };

    fetchLeads();
  }, [debouncedSearch, isAuthenticated, user]);

  if (authLoading) {
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

  // Filter leads based on search term (client-side fallback)
  const filteredLeads = leads.filter((lead) => {
    if (!debouncedSearch) return true;
    
    const searchLower = debouncedSearch.toLowerCase();
    return (
      lead.title?.toLowerCase().includes(searchLower) ||
      lead.first_name?.toLowerCase().includes(searchLower) ||
      lead.last_name?.toLowerCase().includes(searchLower) ||
      lead.email?.toLowerCase().includes(searchLower) ||
      lead.company_name?.toLowerCase().includes(searchLower) ||
      lead.status_name?.toLowerCase().includes(searchLower)
    );
  });

  const handleDelete = async (row: Lead) => {
    if (confirm('Are you sure you want to delete this opportunity?')) {
      try {
        await leadActions.delete(row.id);
        
        // Refresh the list after successful deletion
        if (!user) return;
        
        const response = await leadActions.getMy({
          per_page: 100,
          search: debouncedSearch || undefined,
        });
        
        // Filter leads where user_id matches the current user's id
        const filteredByUser = (response || []).filter(
          (lead) => lead.user_id === user.id
        );
        
        setLeads(filteredByUser);
      } catch (error) {
        console.error('Failed to delete lead:', error);
        alert('Failed to delete the opportunity. Please try again.');
      }
    }
  };

  const columns: Column<Lead>[] = [
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
      key: 'first_name',
      title: 'Contact',
      sortable: true,
      render: (value, item) => (
        <div className="flex flex-col">
          <span className="text-sm text-gray-900">
            {item.first_name && item.last_name 
              ? `${item.first_name} ${item.last_name}` 
              : item.first_name || item.last_name || 'N/A'}
          </span>
          <span className="text-xs text-gray-500">{item.email || 'No email'}</span>
        </div>
      )
    },
    {
      key: 'company_name',
      title: 'Company',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value || 'N/A'}</span>
      )
    },
    {
      key: 'status_name',
      title: 'Status',
      sortable: true,
      render: (value) => (
        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
          {value || 'New'}
        </span>
      )
    },
    {
      key: 'expected_sales_amount',
      title: 'Exp. Value',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">
          {value ? `$${value.toLocaleString()}` : 'N/A'}
        </span>
      )
    },
    {
      key: 'lead_score',
      title: 'Score',
      sortable: true,
      render: (value) => {
        const score = value || 0;
        return (
          <div className="flex items-center gap-2">
            <div className="w-16 bg-gray-200 rounded-full h-1.5">
              <div 
                className={`h-1.5 rounded-full ${score >= 70 ? 'bg-green-500' : score >= 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
                style={{ width: `${score}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-600">{score}</span>
          </div>
        );
      }
    },
    {
      key: 'expected_closing_date',
      title: 'Closing Date',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-500">
          {value ? new Date(value).toLocaleDateString() : 'N/A'}
        </span>
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
        <button 
          onClick={() => window.location.href = '/my-opportunity-pipelines/add'}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
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
        </div>
      </div>

      {/* Pipeline List */}
      <TableArchive
        data={filteredLeads}
        columns={columns}
        itemsPerPage={10}
        loading={loading}
        onRowClick={(row) => window.location.href = `/my-opportunity-pipelines/${row.id}`}
        onView={(row) => window.location.href = `/my-opportunity-pipelines/${row.id}`}
        onEdit={(row) => window.location.href = `/my-opportunity-pipelines/${row.id}/edit`}
        onDelete={handleDelete}
        emptyMessage="No sales opportunities found"
      />
    </div>
  );
}
