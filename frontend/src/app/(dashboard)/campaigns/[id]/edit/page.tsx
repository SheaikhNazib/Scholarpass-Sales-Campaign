'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ArrowLeft, Save } from 'lucide-react';
import { campaignActions } from '@/actions/campaign';
import { Campaign, CampaignUpdate } from '@/types/campaign';

export default function EditCampaignPage() {
  const router = useRouter();
  const params = useParams();
  const campaignId = params.id as string;
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState<CampaignUpdate>({
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
    const fetchData = async () => {
      try {
        setLoading(true);
        const campaignResponse = await campaignActions.getById(Number(campaignId));
        
        setFormData({
          name: campaignResponse.name || '',
          description: campaignResponse.description || '',
          location: campaignResponse.location || '',
          duration: campaignResponse.duration || '',
          start_date: campaignResponse.start_date 
            ? new Date(campaignResponse.start_date).toISOString().split('T')[0] 
            : '',
          end_date: campaignResponse.end_date 
            ? new Date(campaignResponse.end_date).toISOString().split('T')[0] 
            : '',
          campaign_budget: campaignResponse.campaign_budget || 0,
          spent_amount: campaignResponse.spent_amount || 0,
          projected_revenue: campaignResponse.projected_revenue || 0,
          revenue_earned: campaignResponse.revenue_earned || 0,
          projected_sales: campaignResponse.projected_sales || 0,
          number_of_sales: campaignResponse.number_of_sales || 0,
          status_open_closed: campaignResponse.status_open_closed ?? true,
          primary_manager_user_id: campaignResponse.primary_manager_user_id,
        });
      } catch (error) {
        console.error('Failed to fetch campaign:', error);
        alert('Failed to load campaign details');
        router.push('/campaigns');
      } finally {
        setLoading(false);
      }
    };

    if (campaignId) {
      fetchData();
    }
  }, [campaignId, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (type === 'number') {
      setFormData(prev => ({ ...prev, [name]: value === '' ? 0 : parseFloat(value) }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name?.trim()) {
      alert('Campaign name is required');
      return;
    }

    try {
      setSaving(true);
      
      const updateData: CampaignUpdate = {
        ...formData,
        start_date: formData.start_date ? `${formData.start_date}T00:00:00` : undefined,
        end_date: formData.end_date ? `${formData.end_date}T23:59:59` : undefined,
      };

      await campaignActions.update(Number(campaignId), updateData);
      router.push(`/campaigns/${campaignId}`);
    } catch (error: any) {
      console.error('Failed to update campaign:', error);
      const errorMessage = error?.response?.data?.detail 
        ? (typeof error.response.data.detail === 'string' 
          ? error.response.data.detail 
          : JSON.stringify(error.response.data.detail))
        : 'Failed to update campaign. Please try again.';
      alert(errorMessage);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading campaign...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <button
          onClick={() => router.back()}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>
        <h1 className="text-3xl font-bold text-gray-800">Edit Campaign</h1>
        <p className="text-gray-600 mt-1">Update campaign details</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Campaign Name */}
          <div className="md:col-span-2">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Campaign Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter campaign name"
            />
          </div>

          {/* Description */}
          <div className="md:col-span-2">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter campaign description"
            />
          </div>

          {/* Location */}
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Location
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter location"
            />
          </div>

          {/* Duration */}
          <div>
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-2">
              Duration
            </label>
            <input
              type="text"
              id="duration"
              name="duration"
              value={formData.duration || ''}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="e.g., 3 months"
            />
          </div>

          {/* Start Date */}
          <div>
            <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
              Start Date
            </label>
            <input
              type="date"
              id="start_date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* End Date */}
          <div>
            <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
              End Date
            </label>
            <input
              type="date"
              id="end_date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Budget */}
          <div>
            <label htmlFor="campaign_budget" className="block text-sm font-medium text-gray-700 mb-2">
              Campaign Budget
            </label>
            <input
              type="number"
              id="campaign_budget"
              name="campaign_budget"
              value={formData.campaign_budget}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0.00"
            />
          </div>

          {/* Spent Amount */}
          <div>
            <label htmlFor="spent_amount" className="block text-sm font-medium text-gray-700 mb-2">
              Spent Amount
            </label>
            <input
              type="number"
              id="spent_amount"
              name="spent_amount"
              value={formData.spent_amount || 0}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0.00"
            />
          </div>

          {/* Projected Revenue */}
          <div>
            <label htmlFor="projected_revenue" className="block text-sm font-medium text-gray-700 mb-2">
              Projected Revenue
            </label>
            <input
              type="number"
              id="projected_revenue"
              name="projected_revenue"
              value={formData.projected_revenue}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0.00"
            />
          </div>

          {/* Revenue Earned */}
          <div>
            <label htmlFor="revenue_earned" className="block text-sm font-medium text-gray-700 mb-2">
              Revenue Earned
            </label>
            <input
              type="number"
              id="revenue_earned"
              name="revenue_earned"
              value={formData.revenue_earned || 0}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0.00"
            />
          </div>

          {/* Projected Sales */}
          <div>
            <label htmlFor="projected_sales" className="block text-sm font-medium text-gray-700 mb-2">
              Projected Sales
            </label>
            <input
              type="number"
              id="projected_sales"
              name="projected_sales"
              value={formData.projected_sales}
              onChange={handleChange}
              min="0"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0"
            />
          </div>

          {/* Number of Sales */}
          <div>
            <label htmlFor="number_of_sales" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Sales
            </label>
            <input
              type="number"
              id="number_of_sales"
              name="number_of_sales"
              value={formData.number_of_sales || 0}
              onChange={handleChange}
              min="0"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0"
            />
          </div>

          {/* Status */}
          <div className="md:col-span-2">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="status_open_closed"
                checked={formData.status_open_closed}
                onChange={handleChange}
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <span className="text-sm font-medium text-gray-700">Campaign is Active</span>
            </label>
          </div>
        </div>

        {/* Form Actions */}
        <div className="flex gap-3 justify-end mt-6 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={() => router.back()}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
}
