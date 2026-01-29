import { apiClient } from '@/lib/api-client';
import { Lead, LeadCreate, LeadUpdate } from './types';
import { QueryParams } from '@/types/api';
import { API_PATH } from '../../../constant/api-path';

export const leadActions = {
  /**
   * Get all leads
   */
  async getAll(params?: QueryParams): Promise<Lead[]> {
    const queryParams = new URLSearchParams();
    
    if (params?.per_page) queryParams.append('limit', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    
    const url = `${API_PATH.SALES.LEADS.LIST}?${queryParams.toString()}`;
    return apiClient.get<Lead[]>(url);
  },

  /**
   * Get user's leads (owned by current user)
   * Note: Backend returns all leads, filtering should be done server-side if needed
   */
  async getMy(params?: QueryParams): Promise<Lead[]> {
    const queryParams = new URLSearchParams();
    
    if (params?.per_page) queryParams.append('limit', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    
    const url = API_PATH.SALES.LEADS.LIST + (queryParams.toString() ? `?${queryParams.toString()}` : '');
    return apiClient.get<Lead[]>(url);
  },

  /**
   * Get a single lead by ID
   */
  async getById(id: number): Promise<Lead> {
    return apiClient.get<Lead>(API_PATH.SALES.LEADS.GET_BY_ID(id.toString()));
  },

  /**
   * Create a new lead
   */
  async create(data: LeadCreate): Promise<Lead> {
    return apiClient.post<Lead>(API_PATH.SALES.LEADS.CREATE, data);
  },

  /**
   * Update an existing lead
   */
  async update(id: number, data: LeadUpdate): Promise<Lead> {
    return apiClient.put<Lead>(API_PATH.SALES.LEADS.UPDATE(id.toString()), data);
  },

  /**
   * Delete a lead
   */
  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(API_PATH.SALES.LEADS.DELETE(id.toString()));
  },

  /**
   * Get leads by campaign
   */
  async getByCampaign(campaignId: number, params?: QueryParams): Promise<Lead[]> {
    const queryParams = new URLSearchParams();
    
    if (params?.per_page) queryParams.append('limit', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    
    const url = `${API_PATH.SALES.LEADS.LIST_BY_CAMPAIGN(campaignId.toString())}?${queryParams.toString()}`;
    return apiClient.get<Lead[]>(url);
  },

  /**
   * Get leads by status
   */
  async getByStatus(statusId: number, params?: QueryParams): Promise<Lead[]> {
    const queryParams = new URLSearchParams();
    
    if (params?.per_page) queryParams.append('limit', params.per_page.toString());
    if (params?.search) queryParams.append('search', params.search);
    
    const url = `${API_PATH.SALES.LEADS.LIST_BY_STATUS(statusId.toString())}?${queryParams.toString()}`;
    return apiClient.get<Lead[]>(url);
  },
};
