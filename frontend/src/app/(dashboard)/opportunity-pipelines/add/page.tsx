'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, Save } from 'lucide-react';
import { leadActions } from '@/actions/lead';
import { LeadCreate } from '@/actions/lead/types';
import { apiClient } from '@/lib/api-client';
import { API_PATH } from '@constant/api-path';
import { useAuth } from '@/hooks/useAuth';
import { AutocompleteSelect } from '@/components/common/autocomplete-select';

import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/style.css';

interface Campaign {
  id: number;
  name: string;
}

interface Company {
  id: number;
  name: string;
}

interface Contact {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
}

interface Product {
  id: number;
  name: string;
}

interface Currency {
  id: number;
  code: string;
  name: string;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export default function AddOpportunityPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [currencies, setCurrencies] = useState<Currency[]>([]);
  const [users, setUsers] = useState<User[]>([]);
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
    referral_code: '',
    referred_by_email: '',
    referred_by_phone: '',
    lead_generation_link: '',
    // zone_id: undefined, // Commented out: No backend endpoint available
    crm_contact_id: undefined,
    crm_company_id: undefined,
    shop_product_id: undefined,
    // lms_course_id: undefined, // Commented out: No backend endpoint available
    // crm_sales_lead_source_channel_id: undefined, // Commented out: No backend endpoint available
    lead_owner_user_id: undefined,
    currency_id: undefined,
    is_app_user: false,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [campaignsRes, companiesRes, contactsRes, productsRes, currenciesRes, usersRes] = await Promise.all([
          apiClient.get<Campaign[]>(API_PATH.SALES.CAMPAIGNS.LIST),
          apiClient.get<Company[]>(API_PATH.CRM.COMPANIES.LIST),
          apiClient.get<Contact[]>(API_PATH.CRM.CONTACTS.LIST),
          apiClient.get<Product[]>(API_PATH.SHOP.PRODUCTS.LIST),
          apiClient.get<Currency[]>(API_PATH.MASTER.CURRENCIES.LIST),
          apiClient.get<User[]>(API_PATH.AUTH.LIST_USERS),
        ]);
        setCampaigns(campaignsRes || []);
        setCompanies(companiesRes || []);
        setContacts(contactsRes || []);
        setProducts(productsRes || []);
        setCurrencies(currenciesRes || []);
        setUsers(usersRes || []);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    fetchData();
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

    if (!user) {
      alert('User not authenticated');
      return;
    }

    try {
      setLoading(true);
      
      // Clean up the data - remove empty strings and convert to proper types
      const cleanedData: any = {
        title: formData.title,
        // user_id is not set for general opportunity pipelines (remains null)
      };
      
      // Only include fields with actual values (not empty strings)
      if (formData.first_name && formData.first_name.trim()) cleanedData.first_name = formData.first_name.trim();
      if (formData.last_name && formData.last_name.trim()) cleanedData.last_name = formData.last_name.trim();
      if (formData.email && formData.email.trim()) cleanedData.email = formData.email.trim();
      if (formData.phone && formData.phone.trim()) cleanedData.phone = formData.phone.trim();
      if (formData.job_title && formData.job_title.trim()) cleanedData.job_title = formData.job_title.trim();
      if (formData.description && formData.description.trim()) cleanedData.description = formData.description.trim();
      if (formData.referral_code && formData.referral_code.trim()) cleanedData.referral_code = formData.referral_code.trim();
      if (formData.referred_by_email && formData.referred_by_email.trim()) cleanedData.referred_by_email = formData.referred_by_email.trim();
      if (formData.referred_by_phone && formData.referred_by_phone.trim()) cleanedData.referred_by_phone = formData.referred_by_phone.trim();
      if (formData.lead_generation_link && formData.lead_generation_link.trim()) cleanedData.lead_generation_link = formData.lead_generation_link.trim();
      
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
      // Commented out: No backend endpoint available
      // if (formData.zone_id) {
      //   const zoneId = Number(formData.zone_id);
      //   if (!isNaN(zoneId)) cleanedData.zone_id = zoneId;
      // }
      if (formData.crm_contact_id) {
        const contactId = Number(formData.crm_contact_id);
        if (!isNaN(contactId)) cleanedData.crm_contact_id = contactId;
      }
      if (formData.crm_company_id) {
        const companyId = Number(formData.crm_company_id);
        if (!isNaN(companyId)) cleanedData.crm_company_id = companyId;
      }
      if (formData.shop_product_id) {
        const productId = Number(formData.shop_product_id);
        if (!isNaN(productId)) cleanedData.shop_product_id = productId;
      }
      // Commented out: No backend endpoint available
      // if (formData.lms_course_id) {
      //   const courseId = Number(formData.lms_course_id);
      //   if (!isNaN(courseId)) cleanedData.lms_course_id = courseId;
      // }
      // Commented out: No backend endpoint available
      // if (formData.crm_sales_lead_source_channel_id) {
      //   const channelId = Number(formData.crm_sales_lead_source_channel_id);
      //   if (!isNaN(channelId)) cleanedData.crm_sales_lead_source_channel_id = channelId;
      // }
      if (formData.lead_owner_user_id) {
        const ownerId = Number(formData.lead_owner_user_id);
        if (!isNaN(ownerId)) cleanedData.lead_owner_user_id = ownerId;
      }
      if (formData.currency_id) {
        const currencyId = Number(formData.currency_id);
        if (!isNaN(currencyId)) cleanedData.currency_id = currencyId;
      }
      
      // Handle boolean
      cleanedData.is_app_user = formData.is_app_user || false;
      
      await leadActions.create(cleanedData);
      router.push('/opportunity-pipelines');
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
        {/* Basic Information Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Title */}
            <div className="md:col-span-2">
              <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2">
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
            <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
              Email <span className="text-red-500">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email || ''}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter email address"
            />
          </div>

          {/* Phone */}
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
              Phone
            </label>
            <PhoneInput
              country={'us'}
              value={formData.phone || ''}
              onChange={(value: string) => setFormData(prev => ({ ...prev, phone: value }))}
              inputClass="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              containerClass="w-full"
              buttonClass="border border-gray-300 rounded-l-lg"
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
          </div>
        </div>

        {/* Sales Details Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Sales Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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

          </div>
        </div>

        {/* Description Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Description</h2>
          <div className="grid grid-cols-1 gap-6">
          {/* Description */}
          <div>
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
        </div>

        {/* Referral Information Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Referral Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Referral Code */}
          <div>
            <label htmlFor="referral_code" className="block text-sm font-medium text-gray-700 mb-2">
              Referral Code
            </label>
            <input
              type="text"
              id="referral_code"
              name="referral_code"
              value={formData.referral_code || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter referral code"
            />
          </div>

          {/* Referred By Email */}
          <div>
            <label htmlFor="referred_by_email" className="block text-sm font-medium text-gray-700 mb-2">
              Referred By Email
            </label>
            <input
              type="email"
              id="referred_by_email"
              name="referred_by_email"
              value={formData.referred_by_email || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter referrer's email"
            />
          </div>

          {/* Referred By Phone */}
          <div>
            <label htmlFor="referred_by_phone" className="block text-sm font-medium text-gray-700 mb-2">
              Referred By Phone
            </label>
            <input
              type="tel"
              id="referred_by_phone"
              name="referred_by_phone"
              value={formData.referred_by_phone || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter referrer's phone"
            />
          </div>

          {/* Lead Generation Link */}
          <div>
            <label htmlFor="lead_generation_link" className="block text-sm font-medium text-gray-700 mb-2">
              Lead Generation Link
            </label>
            <input
              type="url"
              id="lead_generation_link"
              name="lead_generation_link"
              value={formData.lead_generation_link || ''}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Enter lead generation link"
            />
          </div>

          </div>
        </div>

        {/* Advanced Settings Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Advanced Settings</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* CRM Contact */}
          <div>
            <label htmlFor="crm_contact_id" className="block text-sm font-medium text-gray-700 mb-2">
              CRM Contact
            </label>
            <AutocompleteSelect
              id="crm_contact_id"
              name="crm_contact_id"
              value={formData.crm_contact_id}
              onChange={(value) => setFormData(prev => ({ ...prev, crm_contact_id: value }))}
              options={contacts.map(c => ({ id: c.id, label: `${c.first_name} ${c.last_name} (${c.email})` }))}
              placeholder="Select a contact"
            />
          </div>

          {/* CRM Company */}
          <div>
            <label htmlFor="crm_company_id" className="block text-sm font-medium text-gray-700 mb-2">
              CRM Company
            </label>
            <AutocompleteSelect
              id="crm_company_id"
              name="crm_company_id"
              value={formData.crm_company_id}
              onChange={(value) => setFormData(prev => ({ ...prev, crm_company_id: value }))}
              options={companies.map(c => ({ id: c.id, label: c.name }))}
              placeholder="Select a company"
            />
          </div>

          {/* Shop Product */}
          <div>
            <label htmlFor="shop_product_id" className="block text-sm font-medium text-gray-700 mb-2">
              Shop Product
            </label>
            <AutocompleteSelect
              id="shop_product_id"
              name="shop_product_id"
              value={formData.shop_product_id}
              onChange={(value) => setFormData(prev => ({ ...prev, shop_product_id: value }))}
              options={products.map(p => ({ id: p.id, label: p.name }))}
              placeholder="Select a product"
            />
          </div>

          {/* Lead Owner User */}
          <div>
            <label htmlFor="lead_owner_user_id" className="block text-sm font-medium text-gray-700 mb-2">
              Lead Owner
            </label>
            <AutocompleteSelect
              id="lead_owner_user_id"
              name="lead_owner_user_id"
              value={formData.lead_owner_user_id}
              onChange={(value) => setFormData(prev => ({ ...prev, lead_owner_user_id: value }))}
              options={users.map(u => ({ id: u.id, label: `${u.first_name} ${u.last_name} (${u.username})` }))}
              placeholder="Select a lead owner"
            />
          </div>

          {/* Currency */}
          <div>
            <label htmlFor="currency_id" className="block text-sm font-medium text-gray-700 mb-2">
              Currency
            </label>
            <AutocompleteSelect
              id="currency_id"
              name="currency_id"
              value={formData.currency_id}
              onChange={(value) => setFormData(prev => ({ ...prev, currency_id: value }))}
              options={currencies.map(c => ({ id: c.id, label: `${c.code} - ${c.name}` }))}
              placeholder="Select a currency"
            />
          </div>

          {/* Zone - Commented out: No backend endpoint available 
          <div>
            <label htmlFor="zone_id" className="block text-sm font-medium text-gray-700 mb-2">
              Zone
            </label>
            <AutocompleteSelect
              options={zones.map(z => ({ id: z.id, label: z.name }))}
              value={formData.zone_id || 0}
              onChange={(value) => setFormData({ ...formData, zone_id: value })}
              placeholder="Search zones..."
            />
          </div>
          */}

          {/* LMS Course - Commented out: No backend endpoint available
          <div>
            <label htmlFor="lms_course_id" className="block text-sm font-medium text-gray-700 mb-2">
              LMS Course
            </label>
            <AutocompleteSelect
              options={courses.map(c => ({ id: c.id, label: c.course_name }))}
              value={formData.lms_course_id || 0}
              onChange={(value) => setFormData({ ...formData, lms_course_id: value })}
              placeholder="Search courses..."
            />
          </div>
          */}

          {/* Lead Source Channel - Commented out: No backend endpoint available
          <div>
            <label htmlFor="crm_sales_lead_source_channel_id" className="block text-sm font-medium text-gray-700 mb-2">
              Lead Source Channel
            </label>
            <AutocompleteSelect
              options={leadSourceChannels.map(l => ({ id: l.id, label: l.name }))}
              value={formData.crm_sales_lead_source_channel_id || 0}
              onChange={(value) => setFormData({ ...formData, crm_sales_lead_source_channel_id: value })}
              placeholder="Search lead source channels..."
            />
          </div>
          */}

          {/* Is App User */}
          <div className="md:col-span-2">
            <div className="flex items-start">
              <div className="flex items-center h-5">
                <input
                  type="checkbox"
                  id="is_app_user"
                  name="is_app_user"
                  checked={formData.is_app_user || false}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_app_user: e.target.checked }))}
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
                />
              </div>
              <div className="ml-3">
                <label htmlFor="is_app_user" className="font-medium text-gray-700 cursor-pointer">
                  Is App User
                </label>
                <p className="text-sm text-gray-500">Check if this lead is also an app user</p>
              </div>
            </div>
          </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-between items-center gap-4 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            <span className="text-red-500">*</span> Required fields
          </p>
          <div className="flex gap-3">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 bg-primary-600 text-white px-6 py-2.5 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-sm"
            >
              <Save className="w-5 h-5" />
              {loading ? 'Creating...' : 'Create Opportunity'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
