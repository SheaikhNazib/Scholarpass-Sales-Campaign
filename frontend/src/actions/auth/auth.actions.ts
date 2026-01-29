import { apiClient } from '@/lib/api-client';
import { LoginCredentials, LoginResponse, RegisterData, User } from '@/types/auth';

const BASE_PATH = '/api/auth';

export const authActions = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const response = await apiClient.post<LoginResponse>(`${BASE_PATH}/login`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Store token
    if (response.access_token) {
      apiClient.setToken(response.access_token);
    }
    
    return response;
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<User> {
    return apiClient.post<User>(`${BASE_PATH}/register`, data);
  },

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>(`${BASE_PATH}/me`);
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    // Clear token from storage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    // Optionally call backend logout endpoint
    // return apiClient.post<void>(`${BASE_PATH}/logout`);
  },

  /**
   * Refresh token
   */
  async refreshToken(): Promise<LoginResponse> {
    return apiClient.post<LoginResponse>(`${BASE_PATH}/refresh`);
  },

  /**
   * Change password
   */
  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    return apiClient.post<void>(`${BASE_PATH}/change-password`, {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<void> {
    return apiClient.post<void>(`${BASE_PATH}/password-reset/request`, { email });
  },

  /**
   * Reset password with token
   */
  async resetPassword(token: string, newPassword: string): Promise<void> {
    return apiClient.post<void>(`${BASE_PATH}/password-reset/confirm`, {
      token,
      new_password: newPassword,
    });
  },
};
