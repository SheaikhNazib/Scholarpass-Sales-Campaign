export interface Lead {
  id: number;
  title: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  job_title?: string;
  description?: string;
  lead_score?: number;
  referral_code?: string;
  referred_by_email?: string;
  referred_by_phone?: string;
  lead_generation_link?: string;
  expected_sales_amount?: number;
  expected_closing_date?: string;
  created_date?: string;
  zone_id?: number;
  crm_sales_campaign_id?: number;
  crm_contact_id?: number;
  crm_company_id?: number;
  shop_product_id?: number;
  lms_course_id?: number;
  crm_sales_lead_source_channel_id?: number;
  crm_sales_lead_status_id?: number;
  lead_owner_user_id?: number;
  currency_id?: number;
  user_id?: number;
  is_app_user?: boolean;
  created_at?: string;
  updated_at?: string;
  
  // Related data that might be populated
  company_name?: string;
  contact_name?: string;
  status_name?: string;
  source_channel_name?: string;
  owner_name?: string;
}

export interface LeadCreate {
  title: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  job_title?: string;
  description?: string;
  lead_score?: number;
  referral_code?: string;
  referred_by_email?: string;
  referred_by_phone?: string;
  lead_generation_link?: string;
  expected_sales_amount?: number;
  expected_closing_date?: string;
  crm_sales_campaign_id?: number;
  crm_contact_id?: number;
  crm_company_id?: number;
  shop_product_id?: number;
  lms_course_id?: number;
  crm_sales_lead_source_channel_id?: number;
  crm_sales_lead_status_id?: number;
  lead_owner_user_id?: number;
  currency_id?: number;
  is_app_user?: boolean;
}

export interface LeadUpdate {
  title?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  job_title?: string;
  description?: string;
  lead_score?: number;
  referral_code?: string;
  referred_by_email?: string;
  referred_by_phone?: string;
  lead_generation_link?: string;
  expected_sales_amount?: number;
  expected_closing_date?: string;
  crm_sales_campaign_id?: number;
  crm_contact_id?: number;
  crm_company_id?: number;
  shop_product_id?: number;
  lms_course_id?: number;
  crm_sales_lead_source_channel_id?: number;
  crm_sales_lead_status_id?: number;
  lead_owner_user_id?: number;
  currency_id?: number;
  is_app_user?: boolean;
}

export interface LeadStatus {
  id: number;
  name: string;
  sequence_number?: number;
  created_at?: string;
  updated_at?: string;
}

export interface LeadSourceChannel {
  id: number;
  name: string;
  lead_source_link?: string;
  created_at?: string;
  updated_at?: string;
}
