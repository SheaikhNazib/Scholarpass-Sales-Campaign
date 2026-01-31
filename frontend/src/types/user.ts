export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name?: string;
  active_or_archive: boolean;
  email_confirmed: boolean;
  created_at: string;
}

export interface Role {
  id: number;
  name: string;
  description?: string;
  is_active: boolean;
  display_sequence?: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name?: string;
  primary_role_id?: number;
}
