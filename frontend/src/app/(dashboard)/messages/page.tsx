'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus, Mail, MessageSquare, Phone, Send, Loader2, FilterX } from 'lucide-react';
import { connectActions } from '@/actions/connect';
import { ConnectMessage } from '@/types/connect';

interface MessageFilters {
  search: string;
  messageType: string;
  direction: string;
  status: string;
}

export default function Messages() {
  const [searchTerm, setSearchTerm] = useState('');
  const [messages, setMessages] = useState<ConnectMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterOpen, setFilterOpen] = useState(false);
  const [newMessageOpen, setNewMessageOpen] = useState(false);
  const [filters, setFilters] = useState<MessageFilters>({
    search: '',
    messageType: '',
    direction: '',
    status: '',
  });

  const fetchMessages = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await connectActions.getAllMessages(100);
      setMessages(data || []);
    } catch (err: any) {
      let errorMsg = 'Failed to fetch messages';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setError(errorMsg);
      console.error('Error fetching messages:', err);
      setMessages([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleFilterChange = (key: keyof MessageFilters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    setFilters(prev => ({ ...prev, search: searchTerm }));
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setFilters({
      search: '',
      messageType: '',
      direction: '',
      status: '',
    });
  };

  const hasActiveFilters = filters.messageType || filters.direction || filters.status;

  // Apply filters
  const filteredMessages = messages.filter(message => {
    // Search filter
    if (filters.search && message.subject && 
        !message.subject.toLowerCase().includes(filters.search.toLowerCase()) &&
        !message.sender_name?.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    
    // Message type filter
    if (filters.messageType && message.message_type !== filters.messageType) {
      return false;
    }
    
    // Direction filter
    if (filters.direction && message.direction !== filters.direction) {
      return false;
    }
    
    // Status filter
    if (filters.status && message.status !== filters.status) {
      return false;
    }
    
    return true;
  });

  const getMessageIcon = (type: string) => {
    switch (type) {
      case 'email': return <Mail className="w-4 h-4" />;
      case 'sms': return <MessageSquare className="w-4 h-4" />;
      case 'whatsapp': return <MessageSquare className="w-4 h-4" />;
      case 'chat': return <MessageSquare className="w-4 h-4" />;
      default: return <Mail className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'sent': return 'bg-blue-100 text-blue-800';
      case 'delivered': return 'bg-green-100 text-green-800';
      case 'opened': return 'bg-purple-100 text-purple-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Messages</h1>
          <p className="text-gray-600 mt-2">Manage your email, SMS, and other communications</p>
        </div>
        <button 
          onClick={() => setNewMessageOpen(true)}
          className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
        >
          <Send className="w-5 h-5" />
          New Message
        </button>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-blue-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Search messages by subject or sender..."
              className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleApplyFilters()}
            />
          </div>
          <button 
            onClick={() => setFilterOpen(!filterOpen)}
            className={`flex items-center gap-2 px-6 py-3 rounded-xl transition-all duration-200 font-medium shadow-sm ${
              hasActiveFilters
                ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white hover:from-blue-700 hover:to-blue-600 shadow-md'
                : 'border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400'
            }`}
          >
            <Filter className="w-5 h-5" />
            Filter
            {hasActiveFilters && (
              <span className="ml-1 px-2 py-0.5 bg-white text-blue-600 text-xs rounded-full font-bold">
                {[filters.messageType, filters.direction, filters.status].filter(Boolean).length}
              </span>
            )}
          </button>
        </div>

        {/* Filter Panel */}
        {filterOpen && (
          <div className="mt-4 border-t-2 border-gray-200 pt-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-base font-bold text-gray-900">Filters</h3>
              {hasActiveFilters && (
                <button
                  onClick={handleClearFilters}
                  className="flex items-center gap-1 text-xs text-red-600 hover:text-red-700 font-semibold hover:bg-red-50 px-2 py-1 rounded transition-colors"
                >
                  <FilterX className="w-3 h-3" />
                  Clear all
                </button>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-x-4 gap-y-3">
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Message Type
                </label>
                <select
                  value={filters.messageType}
                  onChange={(e) => handleFilterChange('messageType', e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white text-gray-900"
                >
                  <option value="">All Types</option>
                  <option value="email">Email</option>
                  <option value="sms">SMS</option>
                  <option value="whatsapp">WhatsApp</option>
                  <option value="chat">Chat</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Direction
                </label>
                <select
                  value={filters.direction}
                  onChange={(e) => handleFilterChange('direction', e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white text-gray-900"
                >
                  <option value="">All Directions</option>
                  <option value="inbound">Inbound</option>
                  <option value="outbound">Outbound</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={filters.status}
                  onChange={(e) => handleFilterChange('status', e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white text-gray-900"
                >
                  <option value="">All Status</option>
                  <option value="draft">Draft</option>
                  <option value="sent">Sent</option>
                  <option value="delivered">Delivered</option>
                  <option value="opened">Opened</option>
                  <option value="failed">Failed</option>
                </select>
              </div>
            </div>
            <div className="flex items-center gap-2 mt-4 pt-3 border-t border-gray-200">
              <button
                onClick={handleApplyFilters}
                className="flex-1 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-blue-500 text-white text-sm font-semibold rounded-lg hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-sm hover:shadow"
              >
                Apply Filters
              </button>
              <button
                onClick={() => setFilterOpen(false)}
                className="px-4 py-2.5 border-2 border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <Loader2 className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mb-4" />
          <p className="text-gray-600 font-medium">Loading messages...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6">
          <p className="text-red-900 font-semibold mb-2">Error: {error}</p>
          <button onClick={fetchMessages} className="text-red-700 hover:text-red-800 underline font-medium">
            Try again
          </button>
        </div>
      )}

      {/* Messages List */}
      {!loading && !error && (
        <>
          <div className="mb-4 text-sm text-gray-600 font-medium">
            Showing {filteredMessages.length} of {messages.length} message{messages.length !== 1 ? 's' : ''}
          </div>

          {filteredMessages.length > 0 ? (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="divide-y divide-gray-200">
                {filteredMessages.map((message) => (
                  <div key={message.id} className="p-4 hover:bg-gray-50 cursor-pointer transition-colors">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0 mt-1">
                        {getMessageIcon(message.message_type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <h3 className="text-sm font-semibold text-gray-900 truncate">
                                {message.subject || 'No Subject'}
                              </h3>
                              <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${getStatusColor(message.status || 'draft')}`}>
                                {message.status || 'draft'}
                              </span>
                            </div>
                            <p className="text-xs text-gray-600 mb-1">
                              {message.direction === 'outbound' ? 'To' : 'From'}: {message.sender_name || message.sender_email || 'Unknown'}
                            </p>
                            {message.body_text && (
                              <p className="text-sm text-gray-700 truncate">{message.body_text.substring(0, 100)}...</p>
                            )}
                          </div>
                          <div className="text-right flex-shrink-0">
                            <div className="text-xs text-gray-500">
                              {message.created_at ? new Date(message.created_at).toLocaleDateString() : ''}
                            </div>
                            <div className="text-xs text-gray-400 capitalize">
                              {message.message_type}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <Mail className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No messages found</h3>
              <p className="text-gray-600">Try adjusting your filters or create a new message</p>
            </div>
          )}
        </>
      )}

      {/* New Message Modal */}
      {newMessageOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl">
              <h2 className="text-2xl font-bold text-gray-900">New Message</h2>
              <button
                onClick={() => setNewMessageOpen(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              <form className="space-y-5">
                {/* Message Type */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Message Type</label>
                  <select className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900">
                    <option value="email">Email</option>
                    <option value="sms">SMS</option>
                    <option value="whatsapp">WhatsApp</option>
                  </select>
                </div>

                {/* Recipient */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Recipient</label>
                  <input
                    type="text"
                    placeholder="Enter email or phone number"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500"
                  />
                </div>

                {/* Subject */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
                  <input
                    type="text"
                    placeholder="Enter subject"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500"
                  />
                </div>

                {/* Message Body */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Message</label>
                  <textarea
                    rows={8}
                    placeholder="Type your message here..."
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 resize-none"
                  />
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setNewMessageOpen(false)}
                    className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-200 font-medium"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
                  >
                    <Send className="w-5 h-5" />
                    Send Message
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
