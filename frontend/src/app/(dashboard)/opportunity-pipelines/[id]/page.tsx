'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ArrowLeft, Edit, Trash2, Mail, Phone, Calendar, DollarSign, TrendingUp, Briefcase } from 'lucide-react';
import { leadActions } from '@/actions/lead';
import { Lead } from '@/actions/lead/types';

export default function ViewOpportunityPage() {
  const router = useRouter();
  const params = useParams();
  const leadId = params.id as string;
  
  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchLead = async () => {
      try {
        setLoading(true);
        const response = await leadActions.getById(Number(leadId));
        setLead(response);
      } catch (error) {
        console.error('Failed to fetch lead:', error);
        alert('Failed to load opportunity details');
        router.push('/opportunity-pipelines');
      } finally {
        setLoading(false);
      }
    };

    if (leadId) {
      fetchLead();
    }
  }, [leadId, router]);

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this opportunity?')) {
      return;
    }

    try {
      setDeleting(true);
      await leadActions.delete(Number(leadId));
      router.push('/opportunity-pipelines');
    } catch (error) {
      console.error('Failed to delete lead:', error);
      alert('Failed to delete opportunity. Please try again.');
    } finally {
      setDeleting(false);
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

  if (!lead) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <p className="text-gray-600">Opportunity not found</p>
          <button
            onClick={() => router.push('/opportunity-pipelines')}
            className="mt-4 text-primary-600 hover:text-primary-700"
          >
            Go back to list
          </button>
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
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">{lead.title}</h1>
            <p className="text-gray-600 mt-1">Opportunity Details</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => router.push(`/opportunity-pipelines/${leadId}/edit`)}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Edit className="w-4 h-4" />
              Edit
            </button>
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Trash2 className="w-4 h-4" />
              {deleting ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Contact Information */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Contact Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Name</label>
                <p className="text-gray-900 mt-1">
                  {lead.first_name || lead.last_name
                    ? `${lead.first_name || ''} ${lead.last_name || ''}`.trim()
                    : 'Not provided'}
                </p>
              </div>
              
              {lead.email && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <div className="flex items-center gap-2 mt-1">
                    <Mail className="w-4 h-4 text-gray-400" />
                    <a href={`mailto:${lead.email}`} className="text-primary-600 hover:underline">
                      {lead.email}
                    </a>
                  </div>
                </div>
              )}
              
              {lead.phone && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Phone</label>
                  <div className="flex items-center gap-2 mt-1">
                    <Phone className="w-4 h-4 text-gray-400" />
                    <a href={`tel:${lead.phone}`} className="text-primary-600 hover:underline">
                      {lead.phone}
                    </a>
                  </div>
                </div>
              )}
              
              {lead.job_title && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Job Title</label>
                  <div className="flex items-center gap-2 mt-1">
                    <Briefcase className="w-4 h-4 text-gray-400" />
                    <p className="text-gray-900">{lead.job_title}</p>
                  </div>
                </div>
              )}

              {lead.company_name && (
                <div className="md:col-span-2">
                  <label className="text-sm font-medium text-gray-500">Company</label>
                  <p className="text-gray-900 mt-1">{lead.company_name}</p>
                </div>
              )}
            </div>
          </div>

          {/* Description */}
          {lead.description && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Description</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{lead.description}</p>
            </div>
          )}

          {/* Additional Information */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Additional Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {lead.referral_code && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Referral Code</label>
                  <p className="text-gray-900 mt-1">{lead.referral_code}</p>
                </div>
              )}
              
              {lead.referred_by_email && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Referred By (Email)</label>
                  <p className="text-gray-900 mt-1">{lead.referred_by_email}</p>
                </div>
              )}
              
              {lead.referred_by_phone && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Referred By (Phone)</label>
                  <p className="text-gray-900 mt-1">{lead.referred_by_phone}</p>
                </div>
              )}
              
              {lead.lead_generation_link && (
                <div className="md:col-span-2">
                  <label className="text-sm font-medium text-gray-500">Lead Generation Link</label>
                  <a 
                    href={lead.lead_generation_link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary-600 hover:underline mt-1 block truncate"
                  >
                    {lead.lead_generation_link}
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Status Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Status</h3>
            <span className="px-3 py-1.5 inline-flex text-sm font-semibold rounded-full bg-blue-100 text-blue-800">
              {lead.status_name || 'New'}
            </span>
          </div>

          {/* Sales Metrics */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Sales Metrics</h3>
            <div className="space-y-4">
              {/* Expected Sales Amount */}
              <div>
                <div className="flex items-center gap-2 text-sm font-medium text-gray-500 mb-1">
                  <DollarSign className="w-4 h-4" />
                  Expected Value
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  {lead.expected_sales_amount 
                    ? `$${lead.expected_sales_amount.toLocaleString()}` 
                    : 'N/A'}
                </p>
              </div>

              {/* Lead Score */}
              <div>
                <div className="flex items-center gap-2 text-sm font-medium text-gray-500 mb-2">
                  <TrendingUp className="w-4 h-4" />
                  Lead Score
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        (lead.lead_score || 0) >= 70 ? 'bg-green-500' : 
                        (lead.lead_score || 0) >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${lead.lead_score || 0}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 w-8">
                    {lead.lead_score || 0}
                  </span>
                </div>
              </div>

              {/* Expected Closing Date */}
              {lead.expected_closing_date && (
                <div>
                  <div className="flex items-center gap-2 text-sm font-medium text-gray-500 mb-1">
                    <Calendar className="w-4 h-4" />
                    Expected Close
                  </div>
                  <p className="text-gray-900">
                    {new Date(lead.expected_closing_date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Timestamps */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Timeline</h3>
            <div className="space-y-3">
              {lead.created_at && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Created</label>
                  <p className="text-gray-900 text-sm mt-1">
                    {new Date(lead.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
              )}
              
              {lead.updated_at && (
                <div>
                  <label className="text-sm font-medium text-gray-500">Last Updated</label>
                  <p className="text-gray-900 text-sm mt-1">
                    {new Date(lead.updated_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
