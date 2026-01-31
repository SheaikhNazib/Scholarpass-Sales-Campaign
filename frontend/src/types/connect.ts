// Connect Module Types

export interface ConnectChannel {
  id: number;
  name: string;
  code: string;
  is_active: boolean;
  display_order: number;
  icon_class?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ConnectTemplate {
  id?: number;
  title: string;
  template_type: 'email' | 'sms' | 'whatsapp' | 'both';
  category?: string;
  public_or_private_template?: string;
  subject?: string;
  body_content: string;
  html_content?: string;
  tags?: string;
  merge_fields?: Record<string, any>;
  mail_merge_enabled?: boolean;
  published?: boolean;
  is_system_template?: boolean;
  usage_count?: number;
  last_used_at?: string;
  created_by_user_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface ConnectMessage {
  id?: number;
  message_type: 'email' | 'sms' | 'whatsapp' | 'chat';
  direction: 'inbound' | 'outbound';
  message_category?: string;
  sender_user_id?: number;
  sender_name?: string;
  sender_email?: string;
  to_recipients?: Array<Record<string, any>>;
  cc_recipients?: Array<Record<string, any>>;
  bcc_recipients?: Array<Record<string, any>>;
  subject?: string;
  body_text?: string;
  body_html?: string;
  attachments?: Array<Record<string, any>>;
  has_attachments?: boolean;
  template_id?: number;
  merge_data?: Record<string, any>;
  channel_id?: number;
  status?: string;
  is_scheduled?: boolean;
  scheduled_at?: string;
  sent_at?: string;
  delivered_at?: string;
  opened_at?: string;
  clicked_at?: string;
  bounced_at?: string;
  is_opened?: boolean;
  is_clicked?: boolean;
  open_count?: number;
  click_count?: number;
  is_ai_generated?: boolean;
  ai_prompt?: string;
  ai_model_used?: string;
  crm_contact_id?: number;
  crm_company_id?: number;
  lms_student_id?: number;
  lms_educator_id?: number;
  thread_id?: string;
  reply_to_message_id?: number;
  internal_notes?: string;
  follow_up_required?: boolean;
  message_archived?: boolean;
  archived_at_date?: string;
  created_by_user_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface ConnectCall {
  id?: number;
  call_sid: string;
  call_reference?: string;
  direction: 'inbound' | 'outbound';
  from_number: string;
  to_number: string;
  caller_name?: string;
  status: 'initiated' | 'ringing' | 'answered' | 'completed' | 'failed' | 'busy' | 'no-answer' | 'canceled';
  duration_seconds?: number;
  recording_url?: string;
  recording_duration?: number;
  started_at?: string;
  answered_at?: string;
  completed_at?: string;
  crm_contact_id?: number;
  crm_company_id?: number;
  call_notes?: string;
  created_by_user_id?: number;
  created_at?: string;
  updated_at?: string;
}
