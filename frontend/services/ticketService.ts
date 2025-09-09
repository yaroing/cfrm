import { apiService } from './api'

export interface Ticket {
  id: string
  title: string
  content: string
  is_anonymous: boolean
  category: {
    id: string
    name: string
  }
  priority: {
    id: string
    name: string
    level: number
  }
  status: {
    id: string
    name: string
  }
  channel: {
    id: string
    name: string
    type: string
  }
  external_id: string
  submitter_name: string
  submitter_phone: string
  submitter_email: string
  submitter_location: string
  assigned_to: {
    id: string
    username: string
    full_name: string
  } | null
  created_by: {
    id: string
    username: string
    full_name: string
  } | null
  created_at: string
  updated_at: string
  closed_at: string | null
  sla_deadline: string | null
  escalated_at: string | null
  escalated_to: string
  is_psea: boolean
  psea_contact: string
  psea_escalated: boolean
  attachments: any[]
  latitude: number | null
  longitude: number | null
  tags: string[]
  metadata: Record<string, any>
  is_overdue: boolean
  days_since_creation: number
  responses: Response[]
  logs: TicketLog[]
  feedback: Feedback | null
}

export interface Response {
  id: string
  content: string
  author: {
    id: string
    username: string
    full_name: string
  } | null
  channel: {
    id: string
    name: string
  }
  is_internal: boolean
  sent_at: string | null
  created_at: string
  delivery_status: string
  external_message_id: string
}

export interface TicketLog {
  id: string
  action: string
  action_display: string
  user: {
    id: string
    username: string
    full_name: string
  } | null
  description: string
  old_value: string
  new_value: string
  created_at: string
  ip_address: string
}

export interface Feedback {
  id: string
  satisfaction_rating: number
  response_time_rating: number
  quality_rating: number
  comments: string
  would_recommend: boolean | null
  created_at: string
}

export interface TicketFilters {
  category?: string
  priority?: string
  status?: string
  channel?: string
  assigned_to?: number
  is_anonymous?: boolean
  is_psea?: boolean
  is_overdue?: boolean
  created_after?: string
  created_before?: string
  updated_after?: string
  updated_before?: string
  search?: string
  has_location?: boolean
}

export interface TicketStats {
  status_stats: Array<{ status__name: string; count: number }>
  category_stats: Array<{ category__name: string; count: number }>
  channel_stats: Array<{ channel__name: string; count: number }>
  overdue_count: number
  weekly_tickets: number
  avg_response_time: number | null
}

export const ticketService = {
  async getTickets(filters?: TicketFilters, page = 1, pageSize = 20): Promise<{
    results: Ticket[]
    count: number
    next: string | null
    previous: string | null
  }> {
    const params = new URLSearchParams()
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, value.toString())
        }
      })
    }
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())

    return apiService.get(`/tickets/?${params.toString()}`)
  },

  async getTicket(id: string): Promise<Ticket> {
    return apiService.get(`/tickets/${id}/`)
  },

  async createTicket(data: Partial<Ticket>): Promise<Ticket> {
    return apiService.post('/tickets/', data)
  },

  async updateTicket(id: string, data: Partial<Ticket>): Promise<Ticket> {
    return apiService.patch(`/tickets/${id}/`, data)
  },

  async deleteTicket(id: string): Promise<void> {
    return apiService.delete(`/tickets/${id}/`)
  },

  async assignTicket(id: string, assignedTo: number): Promise<void> {
    return apiService.post(`/tickets/${id}/assign/`, { assigned_to: assignedTo })
  },

  async closeTicket(id: string): Promise<void> {
    return apiService.post(`/tickets/${id}/close/`)
  },

  async reopenTicket(id: string): Promise<void> {
    return apiService.post(`/tickets/${id}/reopen/`)
  },

  async escalateTicket(id: string, escalatedTo: string): Promise<void> {
    return apiService.post(`/tickets/${id}/escalate/`, { escalated_to: escalatedTo })
  },

  async getTicketStats(id: string): Promise<{
    days_since_creation: number
    is_overdue: boolean
    responses_count: number
    logs_count: number
    has_feedback: boolean
    feedback?: Feedback
  }> {
    return apiService.get(`/tickets/${id}/stats/`)
  },

  async getDashboardStats(): Promise<TicketStats> {
    return apiService.get('/tickets/dashboard_stats/')
  },

  async createResponse(ticketId: string, data: {
    content: string
    is_internal?: boolean
    channel: number
  }): Promise<Response> {
    return apiService.post('/responses/', {
      ticket: ticketId,
      ...data,
    })
  },

  async getResponses(ticketId: string): Promise<Response[]> {
    return apiService.get(`/responses/?ticket=${ticketId}`)
  },

  async createFeedback(ticketId: string, data: {
    satisfaction_rating: number
    response_time_rating: number
    quality_rating: number
    comments?: string
    would_recommend?: boolean
  }): Promise<Feedback> {
    return apiService.post('/feedback/', {
      ticket: ticketId,
      ...data,
    })
  },

  async getCategories(): Promise<Array<{ id: string; name: string; description: string; is_sensitive: boolean }>> {
    return apiService.get('/categories/')
  },

  async getPriorities(): Promise<Array<{ id: string; name: string; level: number; sla_hours: number }>> {
    return apiService.get('/priorities/')
  },

  async getStatuses(): Promise<Array<{ id: string; name: string; description: string; is_final: boolean }>> {
    return apiService.get('/statuses/')
  },

  async getChannels(): Promise<Array<{ id: string; name: string; type: string; is_active: boolean }>> {
    return apiService.get('/channels/')
  },
}
