import { apiClient } from '@/lib/api-client';
import { 
  Campaign, 
  CampaignCreate, 
  CampaignUpdate 
} from '@/types/campaign';
import { PaginatedResponse, QueryParams } from '@/types/api';

const BASE_PATH = '/api/campaigns';

export const campaignActions = {
  /**
   * Get all campaigns
   */
  async getAll(params?: QueryParams): Promise<PaginatedResponse<Campaign>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.sort_order) queryParams.append('sort_order', params.sort_order);
    
    const url = `${BASE_PATH}?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<Campaign>>(url);
  },

  /**
   * Get user's campaigns
   */
  async getMy(params?: QueryParams): Promise<PaginatedResponse<Campaign>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    if (params?.sort_order) queryParams.append('sort_order', params.sort_order);
    
    const url = `${BASE_PATH}/my?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<Campaign>>(url);
  },

  /**
   * Get a single campaign by ID
   */
  async getById(id: number): Promise<Campaign> {
    return apiClient.get<Campaign>(`${BASE_PATH}/${id}`);
  },

  /**
   * Create a new campaign
   */
  async create(data: CampaignCreate): Promise<Campaign> {
    return apiClient.post<Campaign>(BASE_PATH, data);
  },

  /**
   * Update an existing campaign
   */
  async update(id: number, data: CampaignUpdate): Promise<Campaign> {
    return apiClient.put<Campaign>(`${BASE_PATH}/${id}`, data);
  },

  /**
   * Delete a campaign
   */
  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${BASE_PATH}/${id}`);
  },

  /**
   * Update campaign status
   */
  async updateStatus(id: number, status: string): Promise<Campaign> {
    return apiClient.patch<Campaign>(`${BASE_PATH}/${id}/status`, { status });
  },

  /**
   * Get campaigns by status
   */
  async getByStatus(status: string, params?: QueryParams): Promise<PaginatedResponse<Campaign>> {
    const queryParams = new URLSearchParams();
    queryParams.append('status', status);
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    
    const url = `${BASE_PATH}?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<Campaign>>(url);
  },

  /**
   * Get campaign analytics
   */
  async getAnalytics(id: number): Promise<any> {
    return apiClient.get<any>(`${BASE_PATH}/${id}/analytics`);
  },

  /**
   * Get campaign leads
   */
  async getLeads(id: number, params?: QueryParams): Promise<PaginatedResponse<any>> {
    const queryParams = new URLSearchParams();
    
    if (params?.page) queryParams.append('page', params.page.toString());
    if (params?.per_page) queryParams.append('per_page', params.per_page.toString());
    
    const url = `${BASE_PATH}/${id}/leads?${queryParams.toString()}`;
    return apiClient.get<PaginatedResponse<any>>(url);
  },
};
