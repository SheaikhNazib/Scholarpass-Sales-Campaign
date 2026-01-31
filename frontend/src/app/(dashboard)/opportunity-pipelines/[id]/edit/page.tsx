'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ArrowLeft, Save } from 'lucide-react';
import { leadActions } from '@/actions/lead';
import { Lead, LeadUpdate } from '@/actions/lead/types';
import { apiClient } from '@/lib/api-client';
import { API_PATH } from '@constant/api-path';

interface Campaign {
  id: number;
  name: string;
}

export default function EditOpportunityPage() {
  const router = useRouter();
  const params = useParams();
  const leadId = params.id as string;
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [formData, setFormData] = useState<LeadUpdate>({
    title: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    job_title: '',
    description: '',
    lead_score: 0,
    expected_sales_amount: 0,
    expected_closing_date: '',
    crm_sales_campaign_id: undefined,
    crm_sales_lead_status_id: undefined,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [leadResponse, campaignsResponse] = await Promise.all([
          leadActions.getById(Number(leadId)),
          apiClient.get<Campaign[]>(API_PATH.SALES.CAMPAIGNS.LIST)
        ]);
        
        setCampaigns(campaignsResponse || []);
        
        // Populate form with existing lead data
        setFormData({
          title: leadResponse.title,
          first_name: leadResponse.first_name || '',
          last_name: leadResponse.last_name || '',
          email: leadResponse.email || '',
          phone: leadResponse.phone || '',
          job_title: leadResponse.job_title || '',
          description: leadResponse.description || '',
          lead_score: leadResponse.lead_score || 0,
          expected_sales_amount: leadResponse.expected_sales_amount || 0,
          expected_closing_date: leadResponse.expected_closing_date 
            ? leadResponse.expected_closing_date.split('T')[0] 
            : '',
          crm_sales_campaign_id: leadResponse.crm_sales_campaign_id,
          crm_sales_lead_status_id: leadResponse.crm_sales_lead_status_id,
        });
      } catch (error) {
        console.error('Failed to fetch data:', error);
        alert('Failed to load opportunity details');
        router.push('/opportunity-pipelines');
      } finally {
        setLoading(false);
      }
    };

    if (leadId) {
      fetchData();
    }
  }, [leadId, router]);

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
      setSaving(true);
      
      // Clean up the data - remove empty strings and convert to proper types
      const cleanedData: any = {
        title: formData.title,
      };
      
      // Only include fields with actual values
      if (formData.first_name) cleanedData.first_name = formData.first_name;
      if (formData.last_name) cleanedData.last_name = formData.last_name;
      if (formData.email) cleanedData.email = formData.email;
      if (formData.phone) cleanedData.phone = formData.phone;
      if (formData.job_title) cleanedData.job_title = formData.job_title;
      if (formData.description) cleanedData.description = formData.description;
      if (formData.lead_score !== undefined && formData.lead_score !== null) cleanedData.lead_score = Number(formData.lead_score);
      if (formData.expected_sales_amount !== undefined && formData.expected_sales_amount !== null) cleanedData.expected_sales_amount = Number(formData.expected_sales_amount);
      if (formData.expected_closing_date) cleanedData.expected_closing_date = formData.expected_closing_date + 'T00:00:00';
      if (formData.crm_sales_campaign_id) cleanedData.crm_sales_campaign_id = Number(formData.crm_sales_campaign_id);
      if (formData.crm_sales_lead_status_id) cleanedData.crm_sales_lead_status_id = Number(formData.crm_sales_lead_status_id);
      
      await leadActions.update(Number(leadId), cleanedData);
      router.push(`/opportunity-pipelines/${leadId}`);
    } catch (error) {
      console.error('Failed to update lead:', error);
      alert('Failed to update opportunity. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading opportunity...</p>
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
        <h1 className="text-3xl font-bold text-gray-800">Edit Opportunity</h1>
        <p className="text-gray-600 mt-1">Update sales opportunity details</p>
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
            disabled={saving}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save className="w-5 h-5" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
}
