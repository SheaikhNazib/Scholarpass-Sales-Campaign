'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import { connectActions } from '@/actions/connect';
import { ConnectMessage } from '@/types/connect';

export default function EditMessagePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [message, setMessage] = useState<ConnectMessage | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    subject: '',
    body_text: '',
    body_html: '',
    message_type: 'email' as 'email' | 'sms' | 'whatsapp' | 'chat',
    status: 'draft',
    to_recipients: [] as any[],
  });

  useEffect(() => {
    const fetchMessage = async () => {
      try {
        setLoading(true);
        const data = await connectActions.getMessageById(parseInt(id));
        setMessage(data);
        setFormData({
          subject: data.subject || '',
          body_text: data.body_text || '',
          body_html: data.body_html || '',
          message_type: data.message_type || 'email',
          status: data.status || 'draft',
          to_recipients: data.to_recipients || [],
        });
      } catch (err: any) {
        setError(err.response?.data?.detail || err.message || 'Failed to fetch message');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchMessage();
    }
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setSaving(true);
      await connectActions.updateMessage(parseInt(id), formData);
      router.push(`/messages/${id}`);
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || 'Failed to update message');
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <Loader2 className="inline-block animate-spin h-12 w-12 text-blue-600 mb-4" />
            <p className="text-gray-600 font-medium">Loading message...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !message) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6">
            <p className="text-red-900 font-semibold mb-2">Error: {error || 'Message not found'}</p>
            <button 
              onClick={() => router.push('/messages')} 
              className="text-red-700 hover:text-red-800 underline font-medium"
            >
              Back to messages
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => router.push(`/messages/${id}`)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-medium">Back to Message</span>
          </button>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-5 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">Edit Message</h1>
            <p className="text-gray-600 mt-1">Update message details</p>
          </div>

          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            {/* Message Type */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Message Type
              </label>
              <select
                value={formData.message_type}
                onChange={(e) => setFormData({ ...formData, message_type: e.target.value as any })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="email">Email</option>
                <option value="sms">SMS</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="chat">Chat</option>
              </select>
            </div>

            {/* Status */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="draft">Draft</option>
                <option value="sent">Sent</option>
                <option value="delivered">Delivered</option>
                <option value="opened">Opened</option>
                <option value="failed">Failed</option>
              </select>
            </div>

            {/* Subject (for email) */}
            {formData.message_type === 'email' && (
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter email subject"
                  required={formData.message_type === 'email'}
                />
              </div>
            )}

            {/* Message Body */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Message Content
              </label>
              <textarea
                value={formData.body_text}
                onChange={(e) => setFormData({ ...formData, body_text: e.target.value })}
                rows={10}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                placeholder="Enter message content"
                required
              />
              {formData.message_type === 'sms' && (
                <p className={`text-xs mt-1 ${formData.body_text.length > 160 ? 'text-red-600 font-bold' : 'text-gray-500'}`}>
                  {formData.body_text.length}/160 characters
                </p>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4 border-t border-gray-200">
              <button
                type="button"
                onClick={() => router.push(`/messages/${id}`)}
                disabled={saving}
                className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving}
                className="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Save className="w-5 h-5" />
                    Save Changes
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
