export interface OpportunityPipeline {
  id: number;
  title: string;
  stage: string;
  value: number;
  probability: number;
  owner: string;
  owner_id?: number;
  customer_name?: string;
  description?: string;
  expected_close_date?: string;
  last_activity: string;
  created_at?: string;
  updated_at?: string;
}

export interface OpportunityPipelineCreate {
  title: string;
  stage: string;
  value: number;
  probability: number;
  customer_name?: string;
  description?: string;
  expected_close_date?: string;
}

export interface OpportunityPipelineUpdate {
  title?: string;
  stage?: string;
  value?: number;
  probability?: number;
  customer_name?: string;
  description?: string;
  expected_close_date?: string;
}

export type OpportunityStage = 
  | 'Lead'
  | 'Qualification'
  | 'Proposal'
  | 'Negotiation'
  | 'Closed Won'
  | 'Closed Lost';
