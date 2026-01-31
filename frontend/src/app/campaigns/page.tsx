'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus, X } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { campaignActions } from '@/actions/campaign';
import { Campaign, CampaignCreate } from '@/types/campaign';

export default function Campaigns() {
  const [searchTerm, setSearchTerm] = useState('');
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const [formData, setFormData] = useState<CampaignCreate>({
    name: '',
    description: '',
    location: '',
    start_date: '',
    end_date: '',
    campaign_budget: 0,
    projected_revenue: 0,
    projected_sales: 0,
    status_open_closed: true,
  });

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await campaignActions.getAll(100);
      setCampaigns(data || []);
    } catch (err: any) {
      let errorMsg = 'Failed to fetch campaigns';
      if (err.response?.data?.detail) {
        // Handle both string and array/object error formats from FastAPI
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setError(errorMsg);
      console.error('Error fetching campaigns:', err);
      // Set empty array on error so UI doesn't break
      setCampaigns([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setCreating(true);
      await campaignActions.create(formData);
      setShowCreateModal(false);
      // Reset form
      setFormData({
        name: '',
        description: '',
        location: '',
        start_date: '',
        end_date: '',
        campaign_budget: 0,
        projected_revenue: 0,
        projected_sales: 0,
        status_open_closed: true,
      });
      // Refresh campaigns list
      await fetchCampaigns();
    } catch (err: any) {
      let errorMsg = 'Failed to create campaign';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      alert(`Error: ${errorMsg}`);
      console.error('Error creating campaign:', err);
    } finally {
      setCreating(false);
    }
  };

  const filteredCampaigns = campaigns.filter(campaign =>
    campaign.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<Campaign>[] = [
    {
      key: 'name',
      title: 'Campaign Name',
      sortable: true,
      render: (value) => (
        <div className="text-sm font-medium text-gray-900">{value as string}</div>
      )
    },
    {
      key: 'status_open_closed',
      title: 'Status',
      sortable: true,
      render: (value) => (
        <span className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full ${
          value === true
            ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-2 border-green-200' 
            : 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-700 border-2 border-gray-300'
        }`}>
          {value === true ? 'Open' : 'Closed'}
        </span>
      )
    },
    {
      key: 'location',
      title: 'Location',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value || '-'}</span>
      )
    },
    {
      key: 'start_date',
      title: 'Duration',
      sortable: false,
      render: (value, row) => (
        <span className="text-sm text-gray-500">
          {row.start_date ? new Date(row.start_date).toLocaleDateString() : '-'} - {row.end_date ? new Date(row.end_date).toLocaleDateString() : '-'}
        </span>
      )
    },
    {
      key: 'campaign_budget',
      title: 'Budget',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value ? `$${(value as number).toLocaleString()}` : '-'}</span>
      )
    },
    {
      key: 'projected_revenue',
      title: 'Projected Revenue',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value ? `$${(value as number).toLocaleString()}` : '-'}</span>
      )
    },
    {
      key: 'number_of_sales',
      title: 'Sales',
      sortable: true,
      render: (value) => (
        <span className="text-sm text-gray-900">{value || 0}</span>
      )
    }
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Campaign List</h1>
          <p className="text-gray-600 mt-2">View and manage all campaigns in the system</p>
        </div>
        <button 
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
        >
          <Plus className="w-5 h-5" />
          New Campaign
        </button>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-blue-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Search campaigns by name..."
              className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          {/* Filter button commented out - not implemented yet
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Filter className="w-5 h-5" />
            Filter
          </button>
          */}
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mb-4"></div>
          <p className="text-gray-600 font-medium">Loading campaigns...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="flex-1">
              <p className="text-red-900 font-semibold mb-2">Error: {error}</p>
              <button 
                onClick={fetchCampaigns}
                className="text-red-700 hover:text-red-800 underline font-medium"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Campaign List */}
      {!loading && !error && filteredCampaigns.length > 0 && (
        <TableArchive
          data={filteredCampaigns}
          columns={columns}
          itemsPerPage={10}
          onRowClick={(row) => console.log('Clicked:', row)}
          emptyMessage="No campaigns found"
        />
      )}

      {/* Empty State - No campaigns */}
      {!loading && !error && campaigns.length === 0 && (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-sm border-2 border-blue-100 p-16 text-center">
          <div className="max-w-md mx-auto">
            <div className="mb-6">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-4">
                <svg className="h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">No campaigns yet</h3>
            <p className="text-gray-600 mb-8 text-lg">Get started by creating your first campaign</p>
            <button 
              onClick={() => setShowCreateModal(true)}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-8 py-4 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-lg hover:shadow-xl font-semibold"
            >
              <Plus className="w-5 h-5" />
              Create Your First Campaign
            </button>
          </div>
        </div>
      )}

      {/* No results from search */}
      {!loading && !error && campaigns.length > 0 && filteredCampaigns.length === 0 && (
        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl shadow-sm border-2 border-gray-200 p-16 text-center">
          <div className="max-w-md mx-auto">
            <div className="mb-6">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-200 rounded-full mb-4">
                <Search className="h-10 w-10 text-gray-600" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">No campaigns found</h3>
            <p className="text-gray-600 mb-6 text-lg">No campaigns match &quot;{searchTerm}&quot;</p>
            <button 
              onClick={() => setSearchTerm('')}
              className="text-blue-600 hover:text-blue-700 underline font-semibold text-lg"
            >
              Clear search
            </button>
          </div>
        </div>
      )}

      {/* Create Campaign Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-gray-200">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-gray-900">Create New Campaign</h2>
              <button onClick={() => setShowCreateModal(false)} className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg p-2 transition-colors">
                <X className="w-6 h-6" />
              </button>
            </div>
            <form onSubmit={handleCreateCampaign}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Campaign Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                    placeholder="Enter campaign name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                    rows={3}
                    placeholder="Enter campaign description"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                    placeholder="Enter location"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Start Date</label>
                    <input
                      type="date"
                      value={formData.start_date}
                      onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">End Date</label>
                    <input
                      type="date"
                      value={formData.end_date}
                      onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Budget</label>
                    <input
                      type="number"
                      value={formData.campaign_budget}
                      onChange={(e) => setFormData({ ...formData, campaign_budget: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                      placeholder="0"
                      min="0"
                      step="0.01"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Projected Revenue</label>
                    <input
                      type="number"
                      value={formData.projected_revenue}
                      onChange={(e) => setFormData({ ...formData, projected_revenue: parseFloat(e.target.value) || 0 })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                      placeholder="0"
                      min="0"
                      step="0.01"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Projected Sales</label>
                    <input
                      type="number"
                      value={formData.projected_sales}
                      onChange={(e) => setFormData({ ...formData, projected_sales: parseInt(e.target.value) || 0 })}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
                      placeholder="0"
                      min="0"
                    />
                  </div>
                </div>
                <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-4">
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.status_open_closed}
                      onChange={(e) => setFormData({ ...formData, status_open_closed: e.target.checked })}
                      className="mr-3 w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm font-semibold text-gray-900">Campaign is Open/Active</span>
                  </label>
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-8 pt-6 border-t border-gray-200">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 font-medium"
                  disabled={creating}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 disabled:from-blue-300 disabled:to-blue-300 shadow-md hover:shadow-lg font-semibold"
                  disabled={creating}
                >
                  {creating ? 'Creating...' : 'Create Campaign'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
