export interface Campaign {
  id: number;
  name: string;
  status: string;
  type: string;
  start_date: string;
  end_date: string;
  budget: number;
  leads: number;
  owner: string;
  owner_id?: number;
  description?: string;
  target_audience?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CampaignCreate {
  name: string;
  status: string;
  type: string;
  start_date: string;
  end_date: string;
  budget: number;
  description?: string;
  target_audience?: string;
}

export interface CampaignUpdate {
  name?: string;
  status?: string;
  type?: string;
  start_date?: string;
  end_date?: string;
  budget?: number;
  description?: string;
  target_audience?: string;
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
