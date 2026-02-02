'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Mail, Phone, MessageSquare, Calendar, User, Building, FileText, Trash2, Edit, Loader2 } from 'lucide-react';
import { connectActions } from '@/actions/connect';
import { ConnectMessage } from '@/types/connect';

export default function ViewMessagePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [message, setMessage] = useState<ConnectMessage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchMessage = async () => {
      try {
        setLoading(true);
        const data = await connectActions.getMessageById(parseInt(id));
        setMessage(data);
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

  const handleDelete = async () => {
    try {
      setDeleting(true);
      await connectActions.deleteMessage(parseInt(id));
      router.push('/messages');
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || 'Failed to delete message');
      setDeleting(false);
    }
  };

  const getMessageTypeIcon = (type: string) => {
    switch (type) {
      case 'email': return <Mail className="w-5 h-5 text-blue-600" />;
      case 'sms': return <MessageSquare className="w-5 h-5 text-green-600" />;
      case 'whatsapp': return <Phone className="w-5 h-5 text-green-600" />;
      default: return <Mail className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const styles: Record<string, string> = {
      draft: 'bg-gray-100 text-gray-800',
      sent: 'bg-blue-100 text-blue-800',
      delivered: 'bg-green-100 text-green-800',
      opened: 'bg-purple-100 text-purple-800',
      failed: 'bg-red-100 text-red-800',
    };
    return styles[status] || styles.draft;
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
            onClick={() => router.push('/messages')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span className="font-medium">Back to Messages</span>
          </button>
          <div className="flex gap-3">
            <button
              onClick={() => router.push(`/messages/${id}/edit`)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
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

        {/* Message Details Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {/* Header Section */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-5 border-b border-gray-200">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  {getMessageTypeIcon(message.message_type)}
                  <h1 className="text-2xl font-bold text-gray-900">
                    {message.subject || 'No Subject'}
                  </h1>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusBadge(message.status || 'draft')}`}>
                    {message.status || 'draft'}
                  </span>
                  <span className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full capitalize">
                    {message.direction || 'outbound'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Content Section */}
          <div className="p-6 space-y-6">
            {/* Recipients */}
            <div>
              <h3 className="text-sm font-semibold text-gray-500 mb-3">Recipients</h3>
              <div className="space-y-2">
                {message.to_recipients && message.to_recipients.length > 0 ? (
                  message.to_recipients.map((recipient, idx) => (
                    <div key={idx} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <User className="w-4 h-4 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {recipient.name || 'Unknown'}
                        </p>
                        <p className="text-xs text-gray-600">
                          {recipient.email || recipient.phone || 'No contact info'}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">No recipients</p>
                )}
              </div>
            </div>

            {/* Sender */}
            {message.direction === 'inbound' && (
              <div>
                <h3 className="text-sm font-semibold text-gray-500 mb-3">Sender</h3>
                <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  <User className="w-4 h-4 text-gray-400" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {message.sender_name || 'Unknown'}
                    </p>
                    <p className="text-xs text-gray-600">
                      {message.sender_email || 'No contact info'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Message Body */}
            <div>
              <h3 className="text-sm font-semibold text-gray-500 mb-3">Message Content</h3>
              <div className="p-4 bg-gray-50 rounded-lg">
                {message.body_html ? (
                  <div 
                    className="prose max-w-none text-gray-900"
                    dangerouslySetInnerHTML={{ __html: message.body_html }}
                  />
                ) : (
                  <p className="text-sm text-gray-900 whitespace-pre-wrap">
                    {message.body_text || 'No content'}
                  </p>
                )}
              </div>
            </div>

            {/* Message Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-200">
              {/* Message Type */}
              <div className="flex items-start gap-3">
                <FileText className="w-5 h-5 text-gray-400 mt-0.5" />
                <div>
                  <h3 className="text-sm font-medium text-gray-500">Message Type</h3>
                  <p className="text-gray-900 mt-1 capitalize">{message.message_type}</p>
                </div>
              </div>

              {/* Channel */}
              {message.channel_id && (
                <div className="flex items-start gap-3">
                  <Building className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Channel ID</h3>
                    <p className="text-gray-900 mt-1">{message.channel_id}</p>
                  </div>
                </div>
              )}

              {/* Sent At */}
              {message.sent_at && (
                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Sent At</h3>
                    <p className="text-gray-900 mt-1">
                      {new Date(message.sent_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              )}

              {/* Delivered At */}
              {message.delivered_at && (
                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div>
                    <h3 className="text-sm font-medium text-gray-500">Delivered At</h3>
                    <p className="text-gray-900 mt-1">
                      {new Date(message.delivered_at).toLocaleString()}
                    </p>
                  </div>
                </div>
              )}

              {/* Timestamps */}
              <div className="md:col-span-2 pt-4 border-t border-gray-200">
                <div className="flex gap-8 text-sm text-gray-500">
                  {message.created_at && (
                    <div>
                      <span className="font-medium">Created:</span>{' '}
                      {new Date(message.created_at).toLocaleString()}
                    </div>
                  )}
                  {message.updated_at && (
                    <div>
                      <span className="font-medium">Updated:</span>{' '}
                      {new Date(message.updated_at).toLocaleString()}
                    </div>
                  )}
                </div>
              </div>
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
                  <h3 className="text-lg font-semibold text-gray-900">Delete Message</h3>
                  <p className="text-sm text-gray-600">This action cannot be undone</p>
                </div>
              </div>
              <p className="text-gray-700 mb-6">
                Are you sure you want to delete this message?
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowDeleteModal(false)}
                  disabled={deleting}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {deleting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Deleting...
                    </>
                  ) : (
                    'Delete Message'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
