import { apiClient } from '@/lib/api-client';
import { API_PATH } from '@/../constant/api-path';
import { ConnectMessage, ConnectTemplate } from '@/types/connect';

export const connectActions = {
  // Messages
  async getAllMessages(limit: number = 100): Promise<ConnectMessage[]> {
    const url = `${API_PATH.CONNECT.MESSAGES.LIST}?limit=${limit}`;
    return apiClient.get<ConnectMessage[]>(url);
  },

  async getMessageById(id: number): Promise<ConnectMessage> {
    return apiClient.get<ConnectMessage>(API_PATH.CONNECT.MESSAGES.GET_BY_ID(id.toString()));
  },

  async getMessagesByUser(userId: number, limit: number = 50): Promise<ConnectMessage[]> {
    const url = `${API_PATH.CONNECT.MESSAGES.LIST_BY_USER(userId.toString())}?limit=${limit}`;
    return apiClient.get<ConnectMessage[]>(url);
  },

  async getMessagesByContact(contactId: number, limit: number = 50): Promise<ConnectMessage[]> {
    const url = `${API_PATH.CONNECT.MESSAGES.LIST_BY_CONTACT(contactId.toString())}?limit=${limit}`;
    return apiClient.get<ConnectMessage[]>(url);
  },

  async getMessagesByCompany(companyId: number, limit: number = 50): Promise<ConnectMessage[]> {
    const url = `${API_PATH.CONNECT.MESSAGES.LIST_BY_COMPANY(companyId.toString())}?limit=${limit}`;
    return apiClient.get<ConnectMessage[]>(url);
  },

  async createMessage(data: ConnectMessage): Promise<{
    message: ConnectMessage;
    delivery: {
      success: boolean;
      demo_mode: boolean;
      error?: string;
      message_sid?: string;
    };
  }> {
    return apiClient.post(API_PATH.CONNECT.MESSAGES.CREATE, data);
  },

  async updateMessage(id: number, data: Partial<ConnectMessage>): Promise<ConnectMessage> {
    return apiClient.put<ConnectMessage>(API_PATH.CONNECT.MESSAGES.UPDATE(id.toString()), data);
  },

  async deleteMessage(id: number): Promise<void> {
    return apiClient.delete<void>(API_PATH.CONNECT.MESSAGES.DELETE(id.toString()));
  },

  // Templates
  async getAllTemplates(
    limit: number = 100,
    publishedOnly: boolean = true
  ): Promise<ConnectTemplate[]> {
    const url = `/api/connect/templates?limit=${limit}&published_only=${publishedOnly}`;
    return apiClient.get<ConnectTemplate[]>(url);
  },

  async getTemplatesByType(
    templateType: string,
    publishedOnly: boolean = true
  ): Promise<ConnectTemplate[]> {
    const url = `${API_PATH.CONNECT.TEMPLATES.LIST_BY_TYPE(templateType)}?published_only=${publishedOnly}`;
    return apiClient.get<ConnectTemplate[]>(url);
  },

  async getTemplatesByCategory(category: string): Promise<ConnectTemplate[]> {
    return apiClient.get<ConnectTemplate[]>(API_PATH.CONNECT.TEMPLATES.LIST_BY_CATEGORY(category));
  },

  async getTemplateById(id: number): Promise<ConnectTemplate> {
    return apiClient.get<ConnectTemplate>(API_PATH.CONNECT.TEMPLATES.GET_BY_ID(id.toString()));
  },

  async createTemplate(data: ConnectTemplate): Promise<ConnectTemplate> {
    return apiClient.post<ConnectTemplate>(API_PATH.CONNECT.TEMPLATES.CREATE, data);
  },

  async updateTemplate(id: number, data: Partial<ConnectTemplate>): Promise<ConnectTemplate> {
    return apiClient.put<ConnectTemplate>(API_PATH.CONNECT.TEMPLATES.UPDATE(id.toString()), data);
  },

  async deleteTemplate(id: number): Promise<void> {
    return apiClient.delete<void>(API_PATH.CONNECT.TEMPLATES.DELETE(id.toString()));
  },
};
