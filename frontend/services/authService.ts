import { apiService } from './api'

export interface LoginCredentials {
  username: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
  user: {
    id: string
    username: string
    email: string
    first_name: string
    last_name: string
    full_name: string
    organization: {
      id: string
      name: string
    }
    role: {
      id: string
      name: string
    }
    is_active: boolean
    is_verified: boolean
  }
}

export interface User {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  organization: {
    id: string
    name: string
  }
  role: {
    id: string
    name: string
  }
  is_active: boolean
  is_verified: boolean
  last_login: string
  last_activity: string
  created_at: string
}

export interface PasswordChangeData {
  old_password: string
  new_password: string
  new_password_confirm: string
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    return apiService.post('/auth/login/', credentials)
  },

  async logout(): Promise<void> {
    return apiService.post('/auth/logout/')
  },

  async getCurrentUser(): Promise<User> {
    return apiService.get('/auth/me/')
  },

  async refreshToken(): Promise<{ access: string }> {
    const refresh = localStorage.getItem('refresh')
    if (!refresh) {
      throw new Error('No refresh token available')
    }
    return apiService.post('/auth/token/refresh/', { refresh })
  },

  async changePassword(data: PasswordChangeData): Promise<void> {
    return apiService.post('/users/users/change_password/', data)
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    return apiService.patch('/users/users/me/', data)
  },
}
