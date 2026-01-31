import { apiClient } from '@/lib/api-client';
import { API_PATH } from '@/../constant/api-path';
import { 
  Campaign, 
  CampaignCreate, 
  CampaignUpdate 
} from '@/types/campaign';

export const campaignActions = {
  /**
   * Get all campaigns
   */
  async getAll(limit: number = 100): Promise<Campaign[]> {
    const url = `${API_PATH.SALES.CAMPAIGNS.LIST}?limit=${limit}`;
    return apiClient.get<Campaign[]>(url);
  },

  /**
   * Get active campaigns only
   */
  async getActive(limit: number = 100): Promise<Campaign[]> {
    const url = `${API_PATH.SALES.CAMPAIGNS.LIST_ACTIVE}?limit=${limit}`;
    return apiClient.get<Campaign[]>(url);
  },

  /**
   * Get a single campaign by ID
   */
  async getById(id: number): Promise<Campaign> {
    return apiClient.get<Campaign>(API_PATH.SALES.CAMPAIGNS.GET_BY_ID(id.toString()));
  },

  /**
   * Create a new campaign
   */
  async create(data: CampaignCreate): Promise<Campaign> {
    // Format dates to ISO datetime strings for backend
    const formattedData = {
      ...data,
      start_date: data.start_date ? `${data.start_date}T00:00:00` : undefined,
      end_date: data.end_date ? `${data.end_date}T23:59:59` : undefined,
    };
    return apiClient.post<Campaign>(API_PATH.SALES.CAMPAIGNS.CREATE, formattedData);
  },

  /**
   * Update an existing campaign
   */
  async update(id: number, data: CampaignUpdate): Promise<Campaign> {
    return apiClient.put<Campaign>(API_PATH.SALES.CAMPAIGNS.UPDATE(id.toString()), data);
  },

  /**
   * Delete a campaign
   */
  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(API_PATH.SALES.CAMPAIGNS.DELETE(id.toString()));
  },
};
