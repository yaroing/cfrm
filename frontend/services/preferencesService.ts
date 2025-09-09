import { apiService } from './api'

export interface UserPreferences {
  id?: string
  notifications_email?: boolean
  notifications_push?: boolean
  language?: string
  timezone?: string
}

export const preferencesService = {
  async getMyPreferences(): Promise<UserPreferences> {
    return apiService.get('/users/preferences/my_preferences/')
  },
  async updateMyPreferences(data: Partial<UserPreferences>): Promise<UserPreferences> {
    return apiService.post('/users/preferences/update_preferences/', data)
  },
}
