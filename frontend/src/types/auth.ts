export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string | null;
  active_or_archive: boolean;
  email_confirmed: boolean;
  created_at: string;
  primary_role_id?: number;
  primary_role_name?: string | null;
  profile_picture_url?: string | null;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name?: string;
}
