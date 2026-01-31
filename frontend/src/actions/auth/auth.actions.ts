import { apiClient } from '@/lib/api-client';
import { LoginCredentials, LoginResponse, RegisterData, User } from '@/types/auth';
import { Role } from '@/types/user';
import { API_PATH } from '../../../constant/api-path';

export const authActions = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(
      API_PATH.AUTH.LOGIN,
      credentials
    );
    
    // Store token
    if (response.access_token) {
      apiClient.setToken(response.access_token);
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.user));
      }
    }
    
    return response;
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>(API_PATH.AUTH.REGISTER, data);
    return response;
  },

  /**
   * Get user by ID
   */
  async getUser(userId: number): Promise<User> {
    return apiClient.get<User>(API_PATH.AUTH.GET_USER(userId.toString()));
  },

  /**
   * Get all available roles
   */
  async getAllRoles(): Promise<Role[]> {
    return apiClient.get<Role[]>(API_PATH.AUTH.GET_ALL_ROLES);
  },

  /**
   * Assign role to user
   */
  async assignRole(userId: number, roleId: number, assignedBy: number): Promise<void> {
    const url = API_PATH.AUTH.ASSIGN_ROLE(userId.toString(), roleId.toString());
    return apiClient.post<void>(url, { assigned_by: assignedBy });
  },

  /**
   * Remove role from user
   */
  async removeRole(userId: number, roleId: number): Promise<void> {
    const url = API_PATH.AUTH.REMOVE_ROLE(userId.toString(), roleId.toString());
    return apiClient.delete<void>(url);
  },

  /**
   * Logout user
   */
  logout(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }
  },

  /**
   * Get stored user from localStorage
   */
  getStoredUser(): User | null {
    if (typeof window !== 'undefined') {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          return JSON.parse(userStr);
        } catch {
          return null;
        }
      }
    }
    return null;
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      return !!localStorage.getItem('access_token');
    }
    return false;
  },
};

