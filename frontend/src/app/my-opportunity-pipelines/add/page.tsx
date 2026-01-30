'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Save } from 'lucide-react';
import { leadActions } from '@/actions/lead';
import { LeadCreate } from '@/actions/lead/types';
import { apiClient } from '@/lib/api-client';
import { API_PATH } from '../../../../constant/api-path';

interface Campaign {
  id: number;
  name: string;
}

export default function AddOpportunityPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [formData, setFormData] = useState<LeadCreate>({
    title: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    job_title: '',
    description: '',
    lead_score: undefined,
    expected_sales_amount: undefined,
    expected_closing_date: '',
    crm_sales_campaign_id: undefined,
    crm_sales_lead_status_id: undefined,
  });

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await apiClient.get<Campaign[]>(API_PATH.SALES.CAMPAIGNS.LIST);
        setCampaigns(response || []);
      } catch (error) {
        console.error('Failed to fetch campaigns:', error);
      }
    };
    fetchCampaigns();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? undefined : Number(value)) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title) {
      alert('Please enter a title');
      return;
    }

    try {
      setLoading(true);
      
      // Clean up the data - remove empty strings and convert to proper types
      const cleanedData: any = {
        title: formData.title,
      };
      
      // Only include fields with actual values (not empty strings)
      if (formData.first_name && formData.first_name.trim()) cleanedData.first_name = formData.first_name.trim();
      if (formData.last_name && formData.last_name.trim()) cleanedData.last_name = formData.last_name.trim();
      if (formData.email && formData.email.trim()) cleanedData.email = formData.email.trim();
      if (formData.phone && formData.phone.trim()) cleanedData.phone = formData.phone.trim();
      if (formData.job_title && formData.job_title.trim()) cleanedData.job_title = formData.job_title.trim();
      if (formData.description && formData.description.trim()) cleanedData.description = formData.description.trim();
      
      // Handle numeric fields - only include if they have a valid value
      if (formData.lead_score !== undefined && formData.lead_score !== null) {
        const score = Number(formData.lead_score);
        if (!isNaN(score)) cleanedData.lead_score = score;
      }
      if (formData.expected_sales_amount !== undefined && formData.expected_sales_amount !== null) {
        const amount = Number(formData.expected_sales_amount);
        if (!isNaN(amount)) cleanedData.expected_sales_amount = amount;
      }
      
      // Handle date
      if (formData.expected_closing_date && formData.expected_closing_date.trim()) {
        // Convert date to datetime format (append time)
        cleanedData.expected_closing_date = formData.expected_closing_date.trim() + 'T00:00:00';
      }
      
      // Handle foreign keys
      if (formData.crm_sales_campaign_id) {
        const campaignId = Number(formData.crm_sales_campaign_id);
        if (!isNaN(campaignId)) cleanedData.crm_sales_campaign_id = campaignId;
      }
      if (formData.crm_sales_lead_status_id) {
        const statusId = Number(formData.crm_sales_lead_status_id);
        if (!isNaN(statusId)) cleanedData.crm_sales_lead_status_id = statusId;
      }
      
      await leadActions.create(cleanedData);
      router.push('/my-opportunity-pipelines');
    } catch (error: any) {
      console.error('Failed to create lead:', error);
      const errorMessage = error?.response?.data?.detail 
        ? (typeof error.response.data.detail === 'string' 
          ? error.response.data.detail 
          : JSON.stringify(error.response.data.detail))
        : 'Failed to create opportunity. Please try again.';
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

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
        <h1 className="text-3xl font-bold text-gray-800">Add New Opportunity</h1>
        <p className="text-gray-600 mt-1">Create a new sales opportunity</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Title */}
          <div className="md:col-span-2">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter opportunity title"
            />
          </div>

          {/* First Name */}
          <div>
            <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-2">
              First Name
            </label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter first name"
            />
          </div>

          {/* Last Name */}
          <div>
            <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-2">
              Last Name
            </label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter last name"
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter email address"
            />
          </div>

          {/* Phone */}
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
              Phone
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter phone number"
            />
          </div>

          {/* Job Title */}
          <div>
            <label htmlFor="job_title" className="block text-sm font-medium text-gray-700 mb-2">
              Job Title
            </label>
            <input
              type="text"
              id="job_title"
              name="job_title"
              value={formData.job_title || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter job title"
            />
          </div>

          {/* Campaign */}
          <div>
            <label htmlFor="crm_sales_campaign_id" className="block text-sm font-medium text-gray-700 mb-2">
              Campaign
            </label>
            <select
              id="crm_sales_campaign_id"
              name="crm_sales_campaign_id"
              value={formData.crm_sales_campaign_id || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select a campaign</option>
              {campaigns.map(campaign => (
                <option key={campaign.id} value={campaign.id}>
                  {campaign.name}
                </option>
              ))}
            </select>
          </div>

          {/* Expected Sales Amount */}
          <div>
            <label htmlFor="expected_sales_amount" className="block text-sm font-medium text-gray-700 mb-2">
              Expected Sales Amount
            </label>
            <input
              type="number"
              id="expected_sales_amount"
              name="expected_sales_amount"
              value={formData.expected_sales_amount || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0.00"
              step="0.01"
              min="0"
            />
          </div>

          {/* Lead Score */}
          <div>
            <label htmlFor="lead_score" className="block text-sm font-medium text-gray-700 mb-2">
              Lead Score (0-100)
            </label>
            <input
              type="number"
              id="lead_score"
              name="lead_score"
              value={formData.lead_score || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="0"
              min="0"
              max="100"
            />
          </div>

          {/* Expected Closing Date */}
          <div>
            <label htmlFor="expected_closing_date" className="block text-sm font-medium text-gray-700 mb-2">
              Expected Closing Date
            </label>
            <input
              type="date"
              id="expected_closing_date"
              name="expected_closing_date"
              value={formData.expected_closing_date || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
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
              value={formData.description || ''}
              onChange={handleChange}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter opportunity description"
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end gap-4 mt-6 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={() => router.back()}
            className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-2 bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {loading ? 'Creating...' : 'Create Opportunity'}
          </button>
        </div>
      </form>
    </div>
  );
}
