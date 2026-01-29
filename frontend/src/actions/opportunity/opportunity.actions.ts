import { apiClient } from '@/lib/api-client';
import { 
  OpportunityPipeline, 
  OpportunityPipelineCreate, 
  OpportunityPipelineUpdate 
} from '@/types/opportunity';
import { PaginatedResponse, QueryParams } from '@/types/api';

const BASE_PATH = '/api/opportunities';

export const opportunityActions = {
  /**
   * Get all opportunity pipelines
   */
  async getAll(params?: QueryParams): Promise<PaginatedResponse<OpportunityPipeline>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.sort_order) queryParams.append('sort_order', params.sort_order);
    
    const url = `${BASE_PATH}?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<OpportunityPipeline>>(url);
  },

  /**
   * Get user's opportunity pipelines
   */
  async getMy(params?: QueryParams): Promise<PaginatedResponse<OpportunityPipeline>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.sort_order) queryParams.append('sort_order', params.sort_order);
    
    const url = `${BASE_PATH}/my?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<OpportunityPipeline>>(url);
  },

  /**
   * Get a single opportunity pipeline by ID
   */
  async getById(id: number): Promise<OpportunityPipeline> {
    return apiClient.get<OpportunityPipeline>(`${BASE_PATH}/${id}`);
  },

  /**
   * Create a new opportunity pipeline
   */
  async create(data: OpportunityPipelineCreate): Promise<OpportunityPipeline> {
    return apiClient.post<OpportunityPipeline>(BASE_PATH, data);
  },

  /**
   * Update an existing opportunity pipeline
   */
  async update(id: number, data: OpportunityPipelineUpdate): Promise<OpportunityPipeline> {
    return apiClient.put<OpportunityPipeline>(`${BASE_PATH}/${id}`, data);
  },

  /**
   * Delete an opportunity pipeline
   */
  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${BASE_PATH}/${id}`);
  },

  /**
   * Update opportunity stage
   */
  async updateStage(id: number, stage: string): Promise<OpportunityPipeline> {
    return apiClient.patch<OpportunityPipeline>(`${BASE_PATH}/${id}/stage`, { stage });
  },

  /**
   * Get opportunities by stage
   */
  async getByStage(stage: string, params?: QueryParams): Promise<PaginatedResponse<OpportunityPipeline>> {
    const queryParams = new URLSearchParams();
    queryParams.append('stage', stage);
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    
    const url = `${BASE_PATH}?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<OpportunityPipeline>>(url);
  },
};
