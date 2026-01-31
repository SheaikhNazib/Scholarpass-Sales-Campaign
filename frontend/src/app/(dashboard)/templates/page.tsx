'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Plus, Mail, MessageSquare, FileText, Loader2, FilterX } from 'lucide-react';
import { connectActions } from '@/actions/connect';
import { ConnectTemplate } from '@/types/connect';

export default function Templates() {
  const [searchTerm, setSearchTerm] = useState('');
  const [templates, setTemplates] = useState<ConnectTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterOpen, setFilterOpen] = useState(false);
  const [newTemplateOpen, setNewTemplateOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<string>('email');

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await connectActions.getTemplatesByType(selectedType, false);
      setTemplates(data || []);
    } catch (err: any) {
      let errorMsg = 'Failed to fetch templates';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setError(errorMsg);
      console.error('Error fetching templates:', err);
      setTemplates([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTemplates();
  }, [selectedType]);

  // Apply search filter
  const filteredTemplates = templates.filter(template => {
    if (searchTerm && !template.title.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    return true;
  });

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'email': return <Mail className="w-5 h-5" />;
      case 'sms': return <MessageSquare className="w-5 h-5" />;
      case 'whatsapp': return <MessageSquare className="w-5 h-5" />;
      default: return <FileText className="w-5 h-5" />;
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Message Templates</h1>
          <p className="text-gray-600 mt-2">Create and manage reusable email and SMS templates</p>
        </div>
        <button 
          onClick={() => setNewTemplateOpen(true)}
          className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
        >
          <Plus className="w-5 h-5" />
          New Template
        </button>
      </div>

      {/* Type Tabs */}
      <div className="flex gap-2 mb-6">
        {['email', 'sms', 'whatsapp', 'both'].map((type) => (
          <button
            key={type}
            onClick={() => setSelectedType(type)}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
              selectedType === type
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-blue-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Search templates..."
              className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 text-gray-900 placeholder-gray-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <Loader2 className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mb-4" />
          <p className="text-gray-600 font-medium">Loading templates...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6">
          <p className="text-red-900 font-semibold mb-2">Error: {error}</p>
          <button onClick={fetchTemplates} className="text-red-700 hover:text-red-800 underline font-medium">
            Try again
          </button>
        </div>
      )}

      {/* Templates Grid */}
      {!loading && !error && (
        <>
          <div className="mb-4 text-sm text-gray-600 font-medium">
            Showing {filteredTemplates.length} of {templates.length} template{templates.length !== 1 ? 's' : ''}
          </div>

          {filteredTemplates.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTemplates.map((template) => (
                <div
                  key={template.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200 cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                        {getTypeIcon(template.template_type)}
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 line-clamp-1">{template.title}</h3>
                        <p className="text-xs text-gray-500 capitalize">{template.template_type}</p>
                      </div>
                    </div>
                    {template.published && (
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                        Published
                      </span>
                    )}
                  </div>
                  
                  {template.subject && (
                    <p className="text-sm text-gray-700 font-medium mb-2 line-clamp-1">
                      {template.subject}
                    </p>
                  )}
                  
                  <p className="text-sm text-gray-600 line-clamp-3 mb-4">
                    {template.body_content}
                  </p>
                  
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Used {template.usage_count || 0} times</span>
                    {template.category && (
                      <span className="px-2 py-1 bg-gray-100 rounded">{template.category}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
              <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No templates found</h3>
              <p className="text-gray-600 mb-4">Create your first {selectedType} template to get started</p>
              <button 
                onClick={() => setNewTemplateOpen(true)}
                className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                <Plus className="w-4 h-4" />
                Create Template
              </button>
            </div>
          )}
        </>
      )}

      {/* New Template Modal */}
      {newTemplateOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between rounded-t-2xl">
              <h2 className="text-2xl font-bold text-gray-900">New Template</h2>
              <button
                onClick={() => setNewTemplateOpen(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              <form className="space-y-5">
                {/* Template Type */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Template Type</label>
                    <select className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900">
                      <option value="email">Email</option>
                      <option value="sms">SMS</option>
                      <option value="whatsapp">WhatsApp</option>
                      <option value="both">Both (Email & SMS)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Category</label>
                    <select className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900">
                      <option value="general">General</option>
                      <option value="marketing">Marketing</option>
                      <option value="transactional">Transactional</option>
                      <option value="notification">Notification</option>
                    </select>
                  </div>
                </div>

                {/* Template Title */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Template Title</label>
                  <input
                    type="text"
                    placeholder="e.g., Welcome Email, Order Confirmation"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500"
                  />
                </div>

                {/* Subject (for email) */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Subject Line (Email only)</label>
                  <input
                    type="text"
                    placeholder="Enter email subject"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500"
                  />
                </div>

                {/* Template Content */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Template Content</label>
                  <textarea
                    rows={10}
                    placeholder="Type your template here... You can use variables like {{name}}, {{company}}, etc."
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900 placeholder-gray-500 resize-none font-mono text-sm"
                  />
                  <p className="text-xs text-gray-500 mt-2">Tip: Use double curly braces for variables, e.g., Hello {`{{name}}`}</p>
                </div>

                {/* Published Status */}
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    id="published"
                    className="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <label htmlFor="published" className="text-sm font-medium text-gray-700">
                    Publish template (make it available for use)
                  </label>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setNewTemplateOpen(false)}
                    className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-200 font-medium"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium"
                  >
                    <Plus className="w-5 h-5" />
                    Create Template
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
