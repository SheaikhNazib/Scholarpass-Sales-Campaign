'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Filter, Plus, Mail, MessageSquare, Phone, Send, Loader2, FilterX, Eye, Edit, Trash2 } from 'lucide-react';
import { connectActions } from '@/actions/connect';
import { ConnectMessage } from '@/types/connect';

interface MessageFilters {
  search: string;
  messageType: string;
  direction: string;
  status: string;
}

interface CountryCode {
  code: string;
  name: string;
  flag: string;
}

interface NewMessageForm {
  messageType: 'email' | 'sms' | 'whatsapp';
  countryCode: string;
  recipient: string;
  subject: string;
  message: string;
}

export default function Messages() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState('');
  const [messages, setMessages] = useState<ConnectMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterOpen, setFilterOpen] = useState(false);
  const [newMessageOpen, setNewMessageOpen] = useState(false);
  const [sending, setSending] = useState(false);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [countryCodeSearch, setCountryCodeSearch] = useState('');
  const [showCountryDropdown, setShowCountryDropdown] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState<ConnectMessage | null>(null);
  const [deleting, setDeleting] = useState(false);
  const countryDropdownRef = useRef<HTMLDivElement>(null);
  const [filters, setFilters] = useState<MessageFilters>({
    search: '',
    messageType: '',
    direction: '',
    status: '',
  });
  const [newMessageForm, setNewMessageForm] = useState<NewMessageForm>({
    messageType: 'email',
    countryCode: '+1',
    recipient: '',
    subject: '',
    message: '',
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

  // Close country dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (countryDropdownRef.current && !countryDropdownRef.current.contains(event.target as Node)) {
        setShowCountryDropdown(false);
        setCountryCodeSearch('');
      }
    };

    if (showCountryDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showCountryDropdown]);

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

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    // Validate recipient
    if (!newMessageForm.recipient.trim()) {
      errors.recipient = 'Recipient is required';
    } else if (newMessageForm.messageType === 'email') {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(newMessageForm.recipient)) {
        errors.recipient = 'Invalid email address';
      }
    } else {
      // Validate phone number for SMS/WhatsApp
      const phoneRegex = /^\d{10,15}$/;
      if (!phoneRegex.test(newMessageForm.recipient.replace(/[\s-]/g, ''))) {
        errors.recipient = 'Invalid phone number (10-15 digits)';
      }
    }

    // Validate subject for email
    if (newMessageForm.messageType === 'email' && !newMessageForm.subject.trim()) {
      errors.subject = 'Subject is required for email';
    }

    // Validate message
    if (!newMessageForm.message.trim()) {
      errors.message = 'Message content is required';
    } else if (newMessageForm.messageType === 'sms' && newMessageForm.message.length > 160) {
      errors.message = 'SMS message must be 160 characters or less';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setSending(true);
    setFormErrors({});
    setSuccessMessage(null);

    try {
      const messageData: Partial<ConnectMessage> = {
        message_type: newMessageForm.messageType,
        direction: 'outbound',
        status: 'draft', // Will be updated by backend based on delivery
        body_text: newMessageForm.message,
      };

      // Add recipient based on type
      if (newMessageForm.messageType === 'email') {
        messageData.subject = newMessageForm.subject;
        messageData.to_recipients = [{ email: newMessageForm.recipient, name: newMessageForm.recipient.split('@')[0] }];
        messageData.sender_email = 'noreply@scholarpass.com';
        messageData.sender_name = 'ScholarPass Team';
      } else {
        // SMS/WhatsApp
        const fullPhone = newMessageForm.countryCode + newMessageForm.recipient.replace(/[\s-]/g, '');
        const countryInfo = countryCodes.find(c => c.code === newMessageForm.countryCode);
        messageData.subject = `${newMessageForm.messageType.toUpperCase()} to ${countryInfo?.flag || ''} ${fullPhone}`;
        messageData.to_recipients = [{ 
          phone: fullPhone,
          name: `${countryInfo?.flag || ''} ${fullPhone}`.trim()
        }];
        messageData.sender_name = `${countryInfo?.name || 'Phone'}: ${fullPhone}`;
      }

      const response = await connectActions.createMessage(messageData as ConnectMessage);
      
      // Show delivery status
      if (response.delivery.demo_mode) {
        setSuccessMessage(
          `📝 Message saved to database (Demo Mode)\n\n` +
          `⚠️ Not actually delivered - ${response.delivery.error || 'API not configured'}\n\n` +
          `To enable real delivery, see WHATSAPP_SETUP_GUIDE.md`
        );
      } else if (response.delivery.success) {
        setSuccessMessage(
          `✅ Message delivered successfully!\n` +
          (response.delivery.message_sid ? `Tracking ID: ${response.delivery.message_sid}` : '')
        );
      } else {
        setSuccessMessage(
          `❌ Message saved but delivery failed\n` +
          `Error: ${response.delivery.error || 'Unknown error'}`
        );
      }
      
      // Reset form
      setNewMessageForm({
        messageType: 'email',
        countryCode: '+1',
        recipient: '',
        subject: '',
        message: '',
      });

      // Refresh messages list
      await fetchMessages();
      
      // Don't close modal automatically - let user read the delivery status
      // They can close it manually by clicking Cancel or the X button
    } catch (err: any) {
      let errorMsg = 'Failed to send message';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string'
          ? err.response.data.detail
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setFormErrors({ submit: errorMsg });
    } finally {
      setSending(false);
    }
  };

  const handleCloseNewMessage = () => {
    setNewMessageOpen(false);
    setNewMessageForm({
      messageType: 'email',
      countryCode: '+1',
      recipient: '',
      subject: '',
      message: '',
    });
    setFormErrors({});
    setSuccessMessage(null);
  };

  const handleFormChange = (field: keyof NewMessageForm, value: string) => {
    setNewMessageForm(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    if (formErrors[field]) {
      setFormErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleDeleteClick = (message: ConnectMessage) => {
    setSelectedMessage(message);
    setShowDeleteModal(true);
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setSelectedMessage(null);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedMessage) return;
    
    try {
      setDeleting(true);
      await connectActions.deleteMessage(selectedMessage.id!);
      setMessages(messages.filter(m => m.id !== selectedMessage.id));
      setShowDeleteModal(false);
      setSelectedMessage(null);
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || 'Failed to delete message');
    } finally {
      setDeleting(false);
    }
  };

  const countryCodes = [
    { code: '+1', name: 'United States', flag: '🇺🇸' },
    { code: '+1', name: 'Canada', flag: '🇨🇦' },
    { code: '+7', name: 'Russia', flag: '🇷🇺' },
    { code: '+20', name: 'Egypt', flag: '🇪🇬' },
    { code: '+27', name: 'South Africa', flag: '🇿🇦' },
    { code: '+30', name: 'Greece', flag: '🇬🇷' },
    { code: '+31', name: 'Netherlands', flag: '🇳🇱' },
    { code: '+32', name: 'Belgium', flag: '🇧🇪' },
    { code: '+33', name: 'France', flag: '🇫🇷' },
    { code: '+34', name: 'Spain', flag: '🇪🇸' },
    { code: '+36', name: 'Hungary', flag: '🇭🇺' },
    { code: '+39', name: 'Italy', flag: '🇮🇹' },
    { code: '+40', name: 'Romania', flag: '🇷🇴' },
    { code: '+41', name: 'Switzerland', flag: '🇨🇭' },
    { code: '+43', name: 'Austria', flag: '🇦🇹' },
    { code: '+44', name: 'United Kingdom', flag: '🇬🇧' },
    { code: '+45', name: 'Denmark', flag: '🇩🇰' },
    { code: '+46', name: 'Sweden', flag: '🇸🇪' },
    { code: '+47', name: 'Norway', flag: '🇳🇴' },
    { code: '+48', name: 'Poland', flag: '🇵🇱' },
    { code: '+49', name: 'Germany', flag: '🇩🇪' },
    { code: '+51', name: 'Peru', flag: '🇵🇪' },
    { code: '+52', name: 'Mexico', flag: '🇲🇽' },
    { code: '+53', name: 'Cuba', flag: '🇨🇺' },
    { code: '+54', name: 'Argentina', flag: '🇦🇷' },
    { code: '+55', name: 'Brazil', flag: '🇧🇷' },
    { code: '+56', name: 'Chile', flag: '🇨🇱' },
    { code: '+57', name: 'Colombia', flag: '🇨🇴' },
    { code: '+58', name: 'Venezuela', flag: '🇻🇪' },
    { code: '+60', name: 'Malaysia', flag: '🇲🇾' },
    { code: '+61', name: 'Australia', flag: '🇦🇺' },
    { code: '+62', name: 'Indonesia', flag: '🇮🇩' },
    { code: '+63', name: 'Philippines', flag: '🇵🇭' },
    { code: '+64', name: 'New Zealand', flag: '🇳🇿' },
    { code: '+65', name: 'Singapore', flag: '🇸🇬' },
    { code: '+66', name: 'Thailand', flag: '🇹🇭' },
    { code: '+81', name: 'Japan', flag: '🇯🇵' },
    { code: '+82', name: 'South Korea', flag: '🇰🇷' },
    { code: '+84', name: 'Vietnam', flag: '🇻🇳' },
    { code: '+86', name: 'China', flag: '🇨🇳' },
    { code: '+90', name: 'Turkey', flag: '🇹🇷' },
    { code: '+91', name: 'India', flag: '🇮🇳' },
    { code: '+92', name: 'Pakistan', flag: '🇵🇰' },
    { code: '+93', name: 'Afghanistan', flag: '🇦🇫' },
    { code: '+94', name: 'Sri Lanka', flag: '🇱🇰' },
    { code: '+95', name: 'Myanmar', flag: '🇲🇲' },
    { code: '+98', name: 'Iran', flag: '🇮🇷' },
    { code: '+211', name: 'South Sudan', flag: '🇸🇸' },
    { code: '+212', name: 'Morocco', flag: '🇲🇦' },
    { code: '+213', name: 'Algeria', flag: '🇩🇿' },
    { code: '+216', name: 'Tunisia', flag: '🇹🇳' },
    { code: '+218', name: 'Libya', flag: '🇱🇾' },
    { code: '+220', name: 'Gambia', flag: '🇬🇲' },
    { code: '+221', name: 'Senegal', flag: '🇸🇳' },
    { code: '+222', name: 'Mauritania', flag: '🇲🇷' },
    { code: '+223', name: 'Mali', flag: '🇲🇱' },
    { code: '+224', name: 'Guinea', flag: '🇬🇳' },
    { code: '+225', name: 'Ivory Coast', flag: '🇨🇮' },
    { code: '+226', name: 'Burkina Faso', flag: '🇧🇫' },
    { code: '+227', name: 'Niger', flag: '🇳🇪' },
    { code: '+228', name: 'Togo', flag: '🇹🇬' },
    { code: '+229', name: 'Benin', flag: '🇧🇯' },
    { code: '+230', name: 'Mauritius', flag: '🇲🇺' },
    { code: '+231', name: 'Liberia', flag: '🇱🇷' },
    { code: '+232', name: 'Sierra Leone', flag: '🇸🇱' },
    { code: '+233', name: 'Ghana', flag: '🇬🇭' },
    { code: '+234', name: 'Nigeria', flag: '🇳🇬' },
    { code: '+235', name: 'Chad', flag: '🇹🇩' },
    { code: '+236', name: 'Central African Republic', flag: '🇨🇫' },
    { code: '+237', name: 'Cameroon', flag: '🇨🇲' },
    { code: '+238', name: 'Cape Verde', flag: '🇨🇻' },
    { code: '+239', name: 'São Tomé and Príncipe', flag: '🇸🇹' },
    { code: '+240', name: 'Equatorial Guinea', flag: '🇬🇶' },
    { code: '+241', name: 'Gabon', flag: '🇬🇦' },
    { code: '+242', name: 'Republic of the Congo', flag: '🇨🇬' },
    { code: '+243', name: 'DR Congo', flag: '🇨🇩' },
    { code: '+244', name: 'Angola', flag: '🇦🇴' },
    { code: '+245', name: 'Guinea-Bissau', flag: '🇬🇼' },
    { code: '+246', name: 'British Indian Ocean Territory', flag: '🇮🇴' },
    { code: '+248', name: 'Seychelles', flag: '🇸🇨' },
    { code: '+249', name: 'Sudan', flag: '🇸🇩' },
    { code: '+250', name: 'Rwanda', flag: '🇷🇼' },
    { code: '+251', name: 'Ethiopia', flag: '🇪🇹' },
    { code: '+252', name: 'Somalia', flag: '🇸🇴' },
    { code: '+253', name: 'Djibouti', flag: '🇩🇯' },
    { code: '+254', name: 'Kenya', flag: '🇰🇪' },
    { code: '+255', name: 'Tanzania', flag: '🇹🇿' },
    { code: '+256', name: 'Uganda', flag: '🇺🇬' },
    { code: '+257', name: 'Burundi', flag: '🇧🇮' },
    { code: '+258', name: 'Mozambique', flag: '🇲🇿' },
    { code: '+260', name: 'Zambia', flag: '🇿🇲' },
    { code: '+261', name: 'Madagascar', flag: '🇲🇬' },
    { code: '+262', name: 'Réunion', flag: '🇷🇪' },
    { code: '+263', name: 'Zimbabwe', flag: '🇿🇼' },
    { code: '+264', name: 'Namibia', flag: '🇳🇦' },
    { code: '+265', name: 'Malawi', flag: '🇲🇼' },
    { code: '+266', name: 'Lesotho', flag: '🇱🇸' },
    { code: '+267', name: 'Botswana', flag: '🇧🇼' },
    { code: '+268', name: 'Eswatini', flag: '🇸🇿' },
    { code: '+269', name: 'Comoros', flag: '🇰🇲' },
    { code: '+290', name: 'Saint Helena', flag: '🇸🇭' },
    { code: '+291', name: 'Eritrea', flag: '🇪🇷' },
    { code: '+297', name: 'Aruba', flag: '🇦🇼' },
    { code: '+298', name: 'Faroe Islands', flag: '🇫🇴' },
    { code: '+299', name: 'Greenland', flag: '🇬🇱' },
    { code: '+350', name: 'Gibraltar', flag: '🇬🇮' },
    { code: '+351', name: 'Portugal', flag: '🇵🇹' },
    { code: '+352', name: 'Luxembourg', flag: '🇱🇺' },
    { code: '+353', name: 'Ireland', flag: '🇮🇪' },
    { code: '+354', name: 'Iceland', flag: '🇮🇸' },
    { code: '+355', name: 'Albania', flag: '🇦🇱' },
    { code: '+356', name: 'Malta', flag: '🇲🇹' },
    { code: '+357', name: 'Cyprus', flag: '🇨🇾' },
    { code: '+358', name: 'Finland', flag: '🇫🇮' },
    { code: '+359', name: 'Bulgaria', flag: '🇧🇬' },
    { code: '+370', name: 'Lithuania', flag: '🇱🇹' },
    { code: '+371', name: 'Latvia', flag: '🇱🇻' },
    { code: '+372', name: 'Estonia', flag: '🇪🇪' },
    { code: '+373', name: 'Moldova', flag: '🇲🇩' },
    { code: '+374', name: 'Armenia', flag: '🇦🇲' },
    { code: '+375', name: 'Belarus', flag: '🇧🇾' },
    { code: '+376', name: 'Andorra', flag: '🇦🇩' },
    { code: '+377', name: 'Monaco', flag: '🇲🇨' },
    { code: '+378', name: 'San Marino', flag: '🇸🇲' },
    { code: '+380', name: 'Ukraine', flag: '🇺🇦' },
    { code: '+381', name: 'Serbia', flag: '🇷🇸' },
    { code: '+382', name: 'Montenegro', flag: '🇲🇪' },
    { code: '+383', name: 'Kosovo', flag: '🇽🇰' },
    { code: '+385', name: 'Croatia', flag: '🇭🇷' },
    { code: '+386', name: 'Slovenia', flag: '🇸🇮' },
    { code: '+387', name: 'Bosnia and Herzegovina', flag: '🇧🇦' },
    { code: '+389', name: 'North Macedonia', flag: '🇲🇰' },
    { code: '+420', name: 'Czech Republic', flag: '🇨🇿' },
    { code: '+421', name: 'Slovakia', flag: '🇸🇰' },
    { code: '+423', name: 'Liechtenstein', flag: '🇱🇮' },
    { code: '+500', name: 'Falkland Islands', flag: '🇫🇰' },
    { code: '+501', name: 'Belize', flag: '🇧🇿' },
    { code: '+502', name: 'Guatemala', flag: '🇬🇹' },
    { code: '+503', name: 'El Salvador', flag: '🇸🇻' },
    { code: '+504', name: 'Honduras', flag: '🇭🇳' },
    { code: '+505', name: 'Nicaragua', flag: '🇳🇮' },
    { code: '+506', name: 'Costa Rica', flag: '🇨🇷' },
    { code: '+507', name: 'Panama', flag: '🇵🇦' },
    { code: '+508', name: 'Saint Pierre and Miquelon', flag: '🇵🇲' },
    { code: '+509', name: 'Haiti', flag: '🇭🇹' },
    { code: '+590', name: 'Guadeloupe', flag: '🇬🇵' },
    { code: '+591', name: 'Bolivia', flag: '🇧🇴' },
    { code: '+592', name: 'Guyana', flag: '🇬🇾' },
    { code: '+593', name: 'Ecuador', flag: '🇪🇨' },
    { code: '+594', name: 'French Guiana', flag: '🇬🇫' },
    { code: '+595', name: 'Paraguay', flag: '🇵🇾' },
    { code: '+596', name: 'Martinique', flag: '🇲🇶' },
    { code: '+597', name: 'Suriname', flag: '🇸🇷' },
    { code: '+598', name: 'Uruguay', flag: '🇺🇾' },
    { code: '+599', name: 'Curaçao', flag: '🇨🇼' },
    { code: '+670', name: 'East Timor', flag: '🇹🇱' },
    { code: '+672', name: 'Antarctica', flag: '🇦🇶' },
    { code: '+673', name: 'Brunei', flag: '🇧🇳' },
    { code: '+674', name: 'Nauru', flag: '🇳🇷' },
    { code: '+675', name: 'Papua New Guinea', flag: '🇵🇬' },
    { code: '+676', name: 'Tonga', flag: '🇹🇴' },
    { code: '+677', name: 'Solomon Islands', flag: '🇸🇧' },
    { code: '+678', name: 'Vanuatu', flag: '🇻🇺' },
    { code: '+679', name: 'Fiji', flag: '🇫🇯' },
    { code: '+680', name: 'Palau', flag: '🇵🇼' },
    { code: '+681', name: 'Wallis and Futuna', flag: '🇼🇫' },
    { code: '+682', name: 'Cook Islands', flag: '🇨🇰' },
    { code: '+683', name: 'Niue', flag: '🇳🇺' },
    { code: '+685', name: 'Samoa', flag: '🇼🇸' },
    { code: '+686', name: 'Kiribati', flag: '🇰🇮' },
    { code: '+687', name: 'New Caledonia', flag: '🇳🇨' },
    { code: '+688', name: 'Tuvalu', flag: '🇹🇻' },
    { code: '+689', name: 'French Polynesia', flag: '🇵🇫' },
    { code: '+690', name: 'Tokelau', flag: '🇹🇰' },
    { code: '+691', name: 'Micronesia', flag: '🇫🇲' },
    { code: '+692', name: 'Marshall Islands', flag: '🇲🇭' },
    { code: '+850', name: 'North Korea', flag: '🇰🇵' },
    { code: '+852', name: 'Hong Kong', flag: '🇭🇰' },
    { code: '+853', name: 'Macau', flag: '🇲🇴' },
    { code: '+855', name: 'Cambodia', flag: '🇰🇭' },
    { code: '+856', name: 'Laos', flag: '🇱🇦' },
    { code: '+880', name: 'Bangladesh', flag: '🇧🇩' },
    { code: '+886', name: 'Taiwan', flag: '🇹🇼' },
    { code: '+960', name: 'Maldives', flag: '🇲🇻' },
    { code: '+961', name: 'Lebanon', flag: '🇱🇧' },
    { code: '+962', name: 'Jordan', flag: '🇯🇴' },
    { code: '+963', name: 'Syria', flag: '🇸🇾' },
    { code: '+964', name: 'Iraq', flag: '🇮🇶' },
    { code: '+965', name: 'Kuwait', flag: '🇰🇼' },
    { code: '+966', name: 'Saudi Arabia', flag: '🇸🇦' },
    { code: '+967', name: 'Yemen', flag: '🇾🇪' },
    { code: '+968', name: 'Oman', flag: '🇴🇲' },
    { code: '+970', name: 'Palestine', flag: '🇵🇸' },
    { code: '+971', name: 'United Arab Emirates', flag: '🇦🇪' },
    { code: '+972', name: 'Israel', flag: '🇮🇱' },
    { code: '+973', name: 'Bahrain', flag: '🇧🇭' },
    { code: '+974', name: 'Qatar', flag: '🇶🇦' },
    { code: '+975', name: 'Bhutan', flag: '🇧🇹' },
    { code: '+976', name: 'Mongolia', flag: '🇲🇳' },
    { code: '+977', name: 'Nepal', flag: '🇳🇵' },
    { code: '+992', name: 'Tajikistan', flag: '🇹🇯' },
    { code: '+993', name: 'Turkmenistan', flag: '🇹🇲' },
    { code: '+994', name: 'Azerbaijan', flag: '🇦🇿' },
    { code: '+995', name: 'Georgia', flag: '🇬🇪' },
    { code: '+996', name: 'Kyrgyzstan', flag: '🇰🇬' },
    { code: '+998', name: 'Uzbekistan', flag: '🇺🇿' },
  ];

  const selectedCountry = countryCodes.find(c => c.code === newMessageForm.countryCode) || countryCodes[0];

  const filteredCountryCodes = countryCodes.filter(country =>
    country.name.toLowerCase().includes(countryCodeSearch.toLowerCase()) ||
    country.code.includes(countryCodeSearch)
  );

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
      {/* API Configuration Warning */}
      <div className="mb-6 bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-xl p-5 shadow-sm">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 mt-0.5">
            <svg className="w-6 h-6 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-amber-900 font-bold text-lg mb-2">📱 Demo Mode - Messages Not Actually Sent</h3>
            <p className="text-amber-800 text-sm mb-3">
              Messages are saved to the database but <strong>NOT sent through WhatsApp/SMS/Email</strong>. 
              To enable actual message delivery, you need to configure messaging APIs.
            </p>
            <div className="flex flex-wrap gap-2">
              <a 
                href="/backend/WHATSAPP_SETUP_GUIDE.md"
                target="_blank"
                className="inline-flex items-center gap-2 bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
                Setup Guide
              </a>
              <span className="inline-flex items-center gap-2 bg-white border-2 border-amber-300 text-amber-900 px-4 py-2 rounded-lg text-sm font-medium">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                </svg>
                Required: Twilio, SendGrid, or Meta API
              </span>
            </div>
          </div>
        </div>
      </div>
      {/* Integration Notice */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-xl p-5 mb-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 mt-1">
            <svg className="w-6 h-6 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-bold text-amber-900 mb-2">⚠️ API Integration Required</h3>
            <p className="text-amber-800 mb-3 leading-relaxed">
              This is a <strong>demo messaging interface</strong>. Messages are stored in the database but not actually sent. 
              To send real messages, you need to integrate with messaging APIs:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
              <div className="bg-white bg-opacity-60 rounded-lg p-3 border border-amber-200">
                <div className="font-bold text-amber-900 mb-1">📧 Email</div>
                <div className="text-amber-700">SendGrid, AWS SES, Mailgun</div>
              </div>
              <div className="bg-white bg-opacity-60 rounded-lg p-3 border border-amber-200">
                <div className="font-bold text-amber-900 mb-1">💬 SMS</div>
                <div className="text-amber-700">Twilio, Vonage, AWS SNS</div>
              </div>
              <div className="bg-white bg-opacity-60 rounded-lg p-3 border border-amber-200">
                <div className="font-bold text-amber-900 mb-1">📱 WhatsApp</div>
                <div className="text-amber-700">Twilio WhatsApp API, 360Dialog</div>
              </div>
            </div>
            <p className="text-amber-700 text-sm mt-3">
              💡 <strong>Current Status:</strong> Messages show as "sent" in the UI for demonstration purposes only.
            </p>
          </div>
        </div>
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
                  <div key={message.id} className="p-4 hover:bg-gray-50 transition-colors">
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
                              {message.direction === 'outbound' 
                                ? `To: ${message.to_recipients?.[0]?.name || message.to_recipients?.[0]?.email || message.to_recipients?.[0]?.phone || 'Unknown'}`
                                : `From: ${message.sender_name || message.sender_email || 'Unknown'}`
                              }
                            </p>
                            {message.body_text && (
                              <p className="text-sm text-gray-700 truncate">{message.body_text.substring(0, 100)}...</p>
                            )}
                          </div>
                          <div className="flex items-start gap-3">
                            <div className="text-right flex-shrink-0">
                              <div className="text-xs text-gray-500">
                                {message.created_at ? new Date(message.created_at).toLocaleDateString() : ''}
                              </div>
                              <div className="text-xs text-gray-400 capitalize">
                                {message.message_type}
                              </div>
                            </div>
                            <div className="flex gap-1">
                              <button
                                onClick={() => router.push(`/messages/${message.id}`)}
                                className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                title="View"
                              >
                                <Eye className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => router.push(`/messages/${message.id}/edit`)}
                                className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                                title="Edit"
                              >
                                <Edit className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteClick(message)}
                                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                title="Delete"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
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
                onClick={handleCloseNewMessage}
                type="button"
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              {successMessage && (
                <div className={`mb-4 p-4 border-2 rounded-xl ${
                  successMessage.includes('✅') ? 'bg-green-50 border-green-200' :
                  successMessage.includes('📝') ? 'bg-amber-50 border-amber-200' :
                  'bg-red-50 border-red-200'
                }`}>
                  <div className={`font-semibold flex items-start gap-2 ${
                    successMessage.includes('✅') ? 'text-green-800' :
                    successMessage.includes('📝') ? 'text-amber-800' :
                    'text-red-800'
                  }`}>
                    <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <div className="whitespace-pre-wrap">{successMessage}</div>
                  </div>
                </div>
              )}

              {formErrors.submit && (
                <div className="mb-4 p-4 bg-red-50 border-2 border-red-200 rounded-xl">
                  <p className="text-red-800 font-semibold">{formErrors.submit}</p>
                </div>
              )}

              <form onSubmit={handleSendMessage} className="space-y-5">
                {/* Message Type */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Message Type</label>
                  <select 
                    value={newMessageForm.messageType}
                    onChange={(e) => handleFormChange('messageType', e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 text-gray-900"
                  >
                    <option value="email">📧 Email</option>
                    <option value="sms">💬 SMS</option>
                    <option value="whatsapp">📱 WhatsApp</option>
                  </select>
                </div>

                {/* Recipient */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    {newMessageForm.messageType === 'email' ? 'Email Address' : 'Phone Number'}
                  </label>
                  
                  {newMessageForm.messageType === 'email' ? (
                    <input
                      type="email"
                      value={newMessageForm.recipient}
                      onChange={(e) => handleFormChange('recipient', e.target.value)}
                      placeholder="recipient@example.com"
                      className={`w-full px-4 py-3 border-2 ${formErrors.recipient ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-gray-50'} rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500 transition-all`}
                    />
                  ) : (
                    <div className="flex gap-2">
                      {/* Country Code Selector with Search */}
                      <div ref={countryDropdownRef} className="relative w-48">
                        <button
                          type="button"
                          onClick={() => setShowCountryDropdown(!showCountryDropdown)}
                          className="w-full px-3 py-3 border-2 border-gray-200 rounded-xl bg-gray-50 text-gray-900 hover:border-gray-300 transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center justify-between"
                        >
                          <span className="flex items-center gap-2">
                            <span className="text-xl">{selectedCountry.flag}</span>
                            <span className="font-medium">{selectedCountry.code}</span>
                          </span>
                          <svg className={`w-4 h-4 transition-transform ${showCountryDropdown ? 'rotate-180' : ''}`} fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                          </svg>
                        </button>
                        
                        {showCountryDropdown && (
                          <div className="absolute z-50 mt-2 w-80 bg-white border-2 border-gray-200 rounded-xl shadow-2xl">
                            <div className="p-3 border-b border-gray-200">
                              <input
                                type="text"
                                placeholder="Search country..."
                                value={countryCodeSearch}
                                onChange={(e) => setCountryCodeSearch(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                                autoFocus
                              />
                            </div>
                            <div className="max-h-64 overflow-y-auto">
                              {filteredCountryCodes.length > 0 ? (
                                filteredCountryCodes.map((country, idx) => (
                                  <button
                                    key={`${country.code}-${idx}`}
                                    type="button"
                                    onClick={() => {
                                      handleFormChange('countryCode', country.code);
                                      setShowCountryDropdown(false);
                                      setCountryCodeSearch('');
                                    }}
                                    className={`w-full px-4 py-2.5 text-left hover:bg-blue-50 transition-colors flex items-center gap-3 ${
                                      newMessageForm.countryCode === country.code ? 'bg-blue-100' : ''
                                    }`}
                                  >
                                    <span className="text-2xl">{country.flag}</span>
                                    <div className="flex-1 min-w-0">
                                      <div className="font-medium text-gray-900 truncate">{country.name}</div>
                                      <div className="text-sm text-gray-600">{country.code}</div>
                                    </div>
                                    {newMessageForm.countryCode === country.code && (
                                      <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                      </svg>
                                    )}
                                  </button>
                                ))
                              ) : (
                                <div className="px-4 py-8 text-center text-gray-500">
                                  No countries found
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                      <input
                        type="tel"
                        value={newMessageForm.recipient}
                        onChange={(e) => handleFormChange('recipient', e.target.value.replace(/[^\d]/g, ''))}
                        placeholder="1234567890"
                        className={`flex-1 px-4 py-3 border-2 ${formErrors.recipient ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-gray-50'} rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500 transition-all`}
                      />
                    </div>
                  )}
                  {formErrors.recipient && (
                    <p className="text-red-600 text-sm mt-1 font-medium">{formErrors.recipient}</p>
                  )}
                </div>

                {/* Subject (Email only) */}
                {newMessageForm.messageType === 'email' && (
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
                    <input
                      type="text"
                      value={newMessageForm.subject}
                      onChange={(e) => handleFormChange('subject', e.target.value)}
                      placeholder="Enter email subject"
                      className={`w-full px-4 py-3 border-2 ${formErrors.subject ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-gray-50'} rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500`}
                    />
                    {formErrors.subject && (
                      <p className="text-red-600 text-sm mt-1 font-medium">{formErrors.subject}</p>
                    )}
                  </div>
                )}

                {/* Message Body */}
                <div>
                  <label className="flex items-center justify-between text-sm font-semibold text-gray-700 mb-2">
                    <span>Message</span>
                    {newMessageForm.messageType === 'sms' && (
                      <span className={`text-xs ${newMessageForm.message.length > 160 ? 'text-red-600 font-bold' : 'text-gray-500'}`}>
                        {newMessageForm.message.length}/160
                      </span>
                    )}
                  </label>
                  <textarea
                    rows={8}
                    value={newMessageForm.message}
                    onChange={(e) => handleFormChange('message', e.target.value)}
                    placeholder="Type your message here..."
                    className={`w-full px-4 py-3 border-2 ${formErrors.message ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-gray-50'} rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500 resize-none`}
                  />
                  {formErrors.message && (
                    <p className="text-red-600 text-sm mt-1 font-medium">{formErrors.message}</p>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={handleCloseNewMessage}
                    disabled={sending}
                    className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={sending}
                    className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-blue-600 transition-all duration-200 shadow-md hover:shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {sending ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Sending...
                      </>
                    ) : (
                      <>
                        <Send className="w-5 h-5" />
                        Send Message
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedMessage && (
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
                Are you sure you want to delete the message <span className="font-semibold">"{selectedMessage.subject || 'No Subject'}"</span>?
              </p>
              <div className="flex gap-3">
                <button
                  onClick={handleDeleteCancel}
                  disabled={deleting}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDeleteConfirm}
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
