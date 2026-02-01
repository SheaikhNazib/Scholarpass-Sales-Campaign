'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ArrowLeft, Edit, Trash2, Calendar, DollarSign, TrendingUp, MapPin, Users } from 'lucide-react';
import { campaignActions } from '@/actions/campaign';
import { Campaign } from '@/types/campaign';

export default function ViewCampaignPage() {
  const router = useRouter();
  const params = useParams();
  const campaignId = params.id as string;
  
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    const fetchCampaign = async () => {
      try {
        setLoading(true);
        const campaignResponse = await campaignActions.getById(Number(campaignId));
        setCampaign(campaignResponse);
      } catch (error) {
        console.error('Failed to fetch campaign:', error);
        alert('Failed to load campaign details');
        router.push('/campaigns');
      } finally {
        setLoading(false);
      }
    };

    if (campaignId) {
      fetchCampaign();
    }
  }, [campaignId, router]);

  const handleDelete = async () => {
    try {
      setDeleting(true);
      await campaignActions.delete(Number(campaignId));
      router.push('/campaigns');
    } catch (error) {
      console.error('Failed to delete campaign:', error);
      alert('Failed to delete campaign. Please try again.');
    } finally {
      setDeleting(false);
      setShowDeleteModal(false);
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

  if (!campaign) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <p className="text-gray-600">Campaign not found</p>
          <button
            onClick={() => router.push('/campaigns')}
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
            <h1 className="text-3xl font-bold text-gray-800">{campaign.name}</h1>
            <p className="text-gray-600 mt-1">Campaign Details</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => router.push(`/campaigns/${campaignId}/edit`)}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Edit className="w-4 h-4" />
              Edit
            </button>
            <button
              onClick={() => setShowDeleteModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          </div>
        </div>
      </div>

      {/* Campaign Information */}
      <div className="bg-white rounded-lg shadow-md border border-gray-200">
        {/* Status Badge */}
        <div className="p-6 border-b border-gray-200">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            campaign.status_open_closed 
              ? 'bg-green-100 text-green-800' 
              : 'bg-gray-100 text-gray-800'
          }`}>
            {campaign.status_open_closed ? 'Active' : 'Closed'}
          </span>
        </div>

        {/* Campaign Details Grid */}
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Description */}
          <div className="md:col-span-2">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Description</h3>
            <p className="text-gray-900">{campaign.description || 'No description provided'}</p>
          </div>

          {/* Location */}
          {campaign.location && (
            <div className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-gray-400 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Location</h3>
                <p className="text-gray-900 mt-1">{campaign.location}</p>
              </div>
            </div>
          )}

          {/* Duration */}
          {campaign.duration && (
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Duration</h3>
                <p className="text-gray-900 mt-1">{campaign.duration}</p>
              </div>
            </div>
          )}

          {/* Start Date */}
          {campaign.start_date && (
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">Start Date</h3>
                <p className="text-gray-900 mt-1">{new Date(campaign.start_date).toLocaleDateString()}</p>
              </div>
            </div>
          )}

          {/* End Date */}
          {campaign.end_date && (
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-gray-500">End Date</h3>
                <p className="text-gray-900 mt-1">{new Date(campaign.end_date).toLocaleDateString()}</p>
              </div>
            </div>
          )}

          {/* Budget & Spend */}
          <div className="flex items-start gap-3">
            <DollarSign className="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-gray-500">Budget</h3>
              <p className="text-gray-900 mt-1">
                ${campaign.campaign_budget?.toLocaleString() || '0'}
              </p>
              {campaign.spent_amount != null && (
                <p className="text-sm text-gray-600 mt-1">
                  Spent: ${campaign.spent_amount.toLocaleString()}
                </p>
              )}
            </div>
          </div>

          {/* Revenue */}
          <div className="flex items-start gap-3">
            <TrendingUp className="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-gray-500">Revenue</h3>
              <p className="text-gray-900 mt-1">
                Projected: ${campaign.projected_revenue?.toLocaleString() || '0'}
              </p>
              {campaign.revenue_earned != null && (
                <p className="text-sm text-gray-600 mt-1">
                  Earned: ${campaign.revenue_earned.toLocaleString()}
                </p>
              )}
            </div>
          </div>

          {/* Sales */}
          <div className="flex items-start gap-3">
            <Users className="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-gray-500">Sales</h3>
              <p className="text-gray-900 mt-1">
                Projected: {campaign.projected_sales || 0}
              </p>
              {campaign.number_of_sales != null && (
                <p className="text-sm text-gray-600 mt-1">
                  Actual: {campaign.number_of_sales}
                </p>
              )}
            </div>
          </div>

          {/* Timestamps */}
          <div className="md:col-span-2 pt-4 border-t border-gray-200">
            <div className="flex gap-8 text-sm text-gray-500">
              {campaign.created_at && (
                <div>
                  <span className="font-medium">Created:</span>{' '}
                  {new Date(campaign.created_at).toLocaleString()}
                </div>
              )}
              {campaign.updated_at && (
                <div>
                  <span className="font-medium">Updated:</span>{' '}
                  {new Date(campaign.updated_at).toLocaleString()}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
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
                Are you sure you want to delete <span className="font-semibold">"{campaign.name}"</span>? 
                This will permanently remove this campaign and all associated data.
              </p>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowDeleteModal(false)}
                  disabled={deleting}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium text-gray-700"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDelete}
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
