'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { authActions } from '@/actions/auth/auth.actions';
import { User, LoginCredentials, RegisterData } from '@/types/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<User>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/register'];

  useEffect(() => {
    // Initialize auth state from localStorage
    const initAuth = () => {
      try {
        const storedUser = authActions.getStoredUser();
        const isAuth = authActions.isAuthenticated();

        if (isAuth && storedUser) {
          setUser(storedUser);
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  // Handle route protection
  useEffect(() => {
    if (!isLoading) {
      const isPublicRoute = publicRoutes.includes(pathname);
      
      if (!user && !isPublicRoute) {
        // Redirect to login if not authenticated and trying to access protected route
        router.push('/login');
      } else if (user && isPublicRoute) {
        // Redirect to dashboard if authenticated and trying to access login/register
        router.push('/my-campaigns');
      }
    }
  }, [user, isLoading, pathname, router]);

  const login = async (credentials: LoginCredentials): Promise<void> => {
    try {
      const response = await authActions.login(credentials);
      setUser(response.user);
      // Navigate to dashboard after successful login
      try {
        router.replace('/my-campaigns');
      } catch (err) {
        console.warn('Redirect after login failed:', err);
      }
    } catch (error: any) {
      console.error('Login error:', error);
      const resp = error?.response?.data;
      const message = typeof resp === 'string' ? resp : resp?.detail || resp?.message || error.message || 'Login failed';
      throw new Error(message);
    }
  };

  const register = async (data: RegisterData): Promise<User> => {
    try {
      const newUser = await authActions.register(data);
      return newUser;
    } catch (error: any) {
      console.error('Registration error:', error);
      const resp = error?.response?.data;
      const message = typeof resp === 'string' ? resp : resp?.detail || resp?.message || error.message || 'Registration failed';
      throw new Error(message);
    }
  };

  const logout = () => {
    authActions.logout();
    setUser(null);
    router.push('/login');
  };

  const refreshUser = async () => {
    try {
      if (user) {
        const updatedUser = await authActions.getUser(user.id);
        setUser(updatedUser);
        if (typeof window !== 'undefined') {
          localStorage.setItem('user', JSON.stringify(updatedUser));
        }
      }
    } catch (error) {
      console.error('Error refreshing user:', error);
      // If refresh fails, user might be invalid, logout
      logout();
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
