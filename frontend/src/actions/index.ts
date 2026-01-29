// Re-export all actions from a single entry point
export { opportunityActions } from './opportunity';
export { campaignActions } from './campaign';
export { authActions } from './auth';

// Re-export types
export type { OpportunityPipeline, OpportunityPipelineCreate, OpportunityPipelineUpdate } from '@/types/opportunity';
export type { Campaign, CampaignCreate, CampaignUpdate } from '@/types/campaign';
export type { User, LoginCredentials, LoginResponse, RegisterData } from '@/types/auth';
export type { ApiResponse, PaginatedResponse, ApiError, QueryParams } from '@/types/api';
