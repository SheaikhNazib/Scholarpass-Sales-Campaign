'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus, Trash2, Users, DollarSign, TrendingUp, Target } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { leadActions, Lead } from '@/actions/lead';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

export default function OpportunityPipelines() {
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [deleting, setDeleting] = useState(false);
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
    if (!isAuthenticated) return;

    const fetchLeads = async () => {
      try {
        setLoading(true);
        
        // Fetch all leads without filtering by user
        const response = await leadActions.getAll({
          per_page: 100,
          search: debouncedSearch || undefined,
        });
        
        setLeads(response || []);
      } catch (error) {
        console.error('Failed to fetch leads:', error);
        setLeads([]);
      } finally {
        setLoading(false);
      }
    };

    fetchLeads();
  }, [debouncedSearch, isAuthenticated]);

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

  // Calculate stats
  const totalLeads = filteredLeads.length;
  const totalValue = filteredLeads.reduce((sum, lead) => sum + (lead.expected_sales_amount || 0), 0);
  const avgScore = totalLeads > 0 ? filteredLeads.reduce((sum, lead) => sum + (lead.lead_score || 0), 0) / totalLeads : 0;
  const highPotential = filteredLeads.filter(lead => (lead.lead_score || 0) >= 75).length;
  const conversionRate = totalLeads > 0 ? (highPotential / totalLeads * 100).toFixed(1) : '0.0';

  const handleDeleteClick = (row: Lead) => {
    setSelectedLead(row);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedLead) return;
    
    try {
      setDeleting(true);
      await leadActions.delete(selectedLead.id);
      
      // Refresh the list after successful deletion
      const response = await leadActions.getAll({
        per_page: 100,
        search: debouncedSearch || undefined,
      });
      
      setLeads(response || []);
      setShowDeleteModal(false);
      setSelectedLead(null);
    } catch (error) {
      console.error('Failed to delete lead:', error);
      alert('Failed to delete the opportunity. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setSelectedLead(null);
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
          <h1 className="text-3xl font-bold text-gray-800">Opportunity Pipeline List</h1>
          <p className="text-gray-600 mt-1">View all opportunities in the system</p>
        </div>
        <button 
          onClick={() => window.location.href = '/opportunity-pipelines/add'}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          New Opportunity
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl shadow-sm border border-blue-200 p-6 hover:shadow-md transition-all duration-300 hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-500 rounded-lg">
              <Users className="w-6 h-6 text-white" />
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-blue-900">{totalLeads}</div>
            </div>
          </div>
          <div className="text-sm font-semibold text-blue-700 mb-1">Total Leads</div>
          <div className="text-xs text-blue-600">Active leads in pipeline</div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl shadow-sm border border-green-200 p-6 hover:shadow-md transition-all duration-300 hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-green-500 rounded-lg">
              <DollarSign className="w-6 h-6 text-white" />
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-green-900">${totalValue.toLocaleString()}</div>
            </div>
          </div>
          <div className="text-sm font-semibold text-green-700 mb-1">Total Value</div>
          <div className="text-xs text-green-600">Total pipeline value</div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl shadow-sm border border-purple-200 p-6 hover:shadow-md transition-all duration-300 hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-purple-500 rounded-lg">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-purple-900">{avgScore.toFixed(1)}</div>
            </div>
          </div>
          <div className="text-sm font-semibold text-purple-700 mb-1">Avg Lead Score</div>
          <div className="text-xs text-purple-600">Average lead quality score</div>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl shadow-sm border border-orange-200 p-6 hover:shadow-md transition-all duration-300 hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-orange-500 rounded-lg">
              <Target className="w-6 h-6 text-white" />
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-orange-900">{conversionRate}%</div>
            </div>
          </div>
          <div className="text-sm font-semibold text-orange-700 mb-1">Conversion Rate</div>
          <div className="text-xs text-orange-600">High potential leads (Score ≥ 75)</div>
        </div>
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
        onRowClick={(row) => window.location.href = `/opportunity-pipelines/${row.id}`}
        onView={(row) => window.location.href = `/opportunity-pipelines/${row.id}`}
        onEdit={(row) => window.location.href = `/opportunity-pipelines/${row.id}/edit`}
        onDelete={handleDeleteClick}
        emptyMessage="No opportunities found"
      />

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedLead && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                  <Trash2 className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Delete Opportunity</h3>
                  <p className="text-sm text-gray-500">This action cannot be undone</p>
                </div>
              </div>
              <p className="text-gray-700 mb-6">
                Are you sure you want to delete <span className="font-semibold">"{selectedLead.title}"</span>? 
                This will permanently remove this opportunity and all associated data.
              </p>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={handleDeleteCancel}
                  disabled={deleting}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteConfirm}
                  disabled={deleting}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  {deleting ? 'Deleting...' : 'Delete Opportunity'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
