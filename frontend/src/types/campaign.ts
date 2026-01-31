export interface Campaign {
  id: number;
  name: string;
  description?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  duration?: string;
  projected_revenue?: number;
  revenue_earned?: number;
  projected_sales?: number;
  number_of_sales?: number;
  campaign_budget?: number;
  spent_amount?: number;
  status_open_closed?: boolean;
  primary_manager_user_id?: number;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

export interface CampaignCreate {
  name: string;
  description?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  duration?: string;
  projected_revenue?: number;
  projected_sales?: number;
  campaign_budget?: number;
  status_open_closed?: boolean;
  primary_manager_user_id?: number;
}

export interface CampaignUpdate {
  name?: string;
  description?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  duration?: string;
  projected_revenue?: number;
  revenue_earned?: number;
  projected_sales?: number;
  number_of_sales?: number;
  campaign_budget?: number;
  spent_amount?: number;
  status_open_closed?: boolean;
  primary_manager_user_id?: number;
}

export type CampaignStatus = 
  | 'Planning'
  | 'Active'
  | 'Paused'
  | 'Completed'
  | 'Cancelled';

export type CampaignType = 
  | 'Email'
  | 'Social Media'
  | 'Multi-Channel'
  | 'Event'
  | 'Webinar'
  | 'Direct Mail';
