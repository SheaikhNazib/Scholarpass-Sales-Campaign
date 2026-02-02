'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus, Loader2, Trash2 } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { campaignActions, Campaign } from '@/actions/campaign';
import { useRouter } from 'next/navigation';

interface CampaignFilters {
  search: string;
  status: string;
  primary_manager_user_id: string;
}

export default function MyCampaigns() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [filters, setFilters] = useState<CampaignFilters>({
    search: '',
    status: '',
    primary_manager_user_id: '',
  });

  // Fetch campaigns from API
  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const filterParams: any = {};
      
      // Add search filter
      if (filters.search || searchTerm) {
        filterParams.search = filters.search || searchTerm;
      }
      
      // Add status filter
      if (filters.status === 'active') {
        filterParams.status = true;
      } else if (filters.status === 'closed') {
        filterParams.status = false;
      }
      
      // Add owner filter
      if (filters.primary_manager_user_id) {
        filterParams.primary_manager_user_id = parseInt(filters.primary_manager_user_id);
      }
      
      const data = await campaignActions.getAll(100, 0, filterParams);
      setCampaigns(data);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch campaigns on mount only
  useEffect(() => {
    fetchCampaigns();
  }, []);

  const handleFilterChange = (key: keyof CampaignFilters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    setFilters(prev => ({ ...prev, search: searchTerm }));
    fetchCampaigns();
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setFilters({
      search: '',
      status: '',
      primary_manager_user_id: '',
    });
    // Fetch with cleared filters
    setTimeout(() => fetchCampaigns(), 0);
  };

  const handleDeleteClick = (row: Campaign) => {
    setSelectedCampaign(row);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedCampaign) return;
    
    try {
      setDeleting(true);
      await campaignActions.delete(selectedCampaign.id);
      
      // Refresh the list after successful deletion
      await fetchCampaigns();
      setShowDeleteModal(false);
      setSelectedCampaign(null);
    } catch (error) {
      console.error('Failed to delete campaign:', error);
      alert('Failed to delete the campaign. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setSelectedCampaign(null);
  };

  const columns: Column<Campaign>[] = [
    { 
      key: 'name', 
      title: 'Campaign Name',
      render: (value) => value || 'Untitled Campaign'
    },
    { 
      key: 'status_open_closed', 
      title: 'Status',
      render: (value) => (
        <span className={`px-2 py-1 rounded text-xs font-medium ${
          value ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
        }`}>
          {value ? 'Active' : 'Closed'}
        </span>
      )
    },
    { 
      key: 'location', 
      title: 'Location',
      render: (value) => value || 'N/A'
    },
    { 
      key: 'start_date', 
      title: 'Start Date',
      render: (value) => value ? new Date(value as string).toLocaleDateString() : 'N/A'
    },
    { 
      key: 'end_date',
      title: 'End Date',
      render: (value) => value ? new Date(value as string).toLocaleDateString() : 'N/A'
    },
    { 
      key: 'campaign_budget', 
      title: 'Budget', 
      render: (value) => value ? `$${(value as number).toLocaleString()}` : 'N/A'
    },
    { 
      key: 'projected_sales', 
      title: 'Projected Sales',
      render: (value) => value || 0
    },
    { 
      key: 'number_of_sales', 
      title: 'Actual Sales',
      render: (value) => value || 0
    },
  ];

  const hasActiveFilters = filters.status || filters.primary_manager_user_id;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Campaigns</h1>
          <p className="text-gray-600 mt-1">Manage your sales campaigns</p>
        </div>
        <button 
          onClick={() => router.push('/campaigns/create')}
          className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
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
            placeholder="Search campaigns by name or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleApplyFilters()}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
          />
        </div>
        <button
          onClick={() => setFilterOpen(!filterOpen)}
          className={`inline-flex items-center gap-2 px-4 py-2 border rounded-lg transition-colors ${
            hasActiveFilters
              ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
              : 'border-gray-300 hover:bg-gray-50'
          }`}
        >
          <Filter size={20} />
          Filter
          {hasActiveFilters && (
            <span className="ml-1 px-2 py-0.5 bg-indigo-600 text-white text-xs rounded-full">
              {[filters.status, filters.primary_manager_user_id].filter(Boolean).length}
            </span>
          )}
        </button>
      </div>

      {/* Filter Panel */}
      {filterOpen && (
        <div className="bg-white border border-gray-300 rounded-lg shadow-sm">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Advanced Filters</h3>
              {hasActiveFilters && (
                <button
                  onClick={handleClearFilters}
                  className="text-xs text-red-600 hover:text-red-700 font-medium"
                >
                  Clear all
                </button>
              )}
            </div>
          </div>
          <div className="p-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select 
                  value={filters.status}
                  onChange={(e) => handleFilterChange('status', e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                >
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Owner ID
                </label>
                <input
                  type="number"
                  value={filters.primary_manager_user_id}
                  onChange={(e) => handleFilterChange('primary_manager_user_id', e.target.value)}
                  placeholder="Enter user ID"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                />
              </div>
            </div>
            <div className="flex items-center gap-2 mt-4 pt-3 border-t border-gray-200">
              <button
                onClick={handleApplyFilters}
                className="flex-1 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Apply Filters
              </button>
              <button
                onClick={() => setFilterOpen(false)}
                className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading ? (
        <div className="flex items-center justify-center py-12 bg-white rounded-lg border border-gray-200">
          <Loader2 className="animate-spin text-indigo-600" size={32} />
        </div>
      ) : (
        <>
          {/* Results Count */}
          <div className="text-sm text-gray-600">
            Showing {campaigns.length} campaign{campaigns.length !== 1 ? 's' : ''}
          </div>

          {/* Table */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            {campaigns.length > 0 ? (
              <TableArchive
                data={campaigns}
                columns={columns}
                onRowClick={(row) => router.push(`/my-campaigns/${row.id}`)}
                onView={(row) => router.push(`/my-campaigns/${row.id}`)}
                onEdit={(row) => router.push(`/my-campaigns/${row.id}/edit`)}
                onDelete={handleDeleteClick}
              />
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500">No campaigns found</p>
                <p className="text-sm text-gray-400 mt-1">
                  Try adjusting your filters or create a new campaign
                </p>
              </div>
            )}
          </div>
        </>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedCampaign && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                  <Trash2 className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Delete Campaign</h3>
                  <p className="text-sm text-gray-500">This action cannot be undone</p>
                </div>
              </div>
              <p className="text-gray-700 mb-6">
                Are you sure you want to delete <span className="font-semibold">"{selectedCampaign.name}"</span>? 
                This will permanently remove this campaign and all associated data.
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
                  {deleting ? 'Deleting...' : 'Delete Campaign'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
