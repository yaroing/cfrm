import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ticketService, Ticket } from '@/services/ticketService'

export default function RecentTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const data = await ticketService.getTickets({}, 1, 5)
        setTickets(data.results)
      } catch (error) {
        console.error('Erreur lors du chargement des tickets récents:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTickets()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Ouvert':
        return 'bg-blue-100 text-blue-800'
      case 'En cours':
        return 'bg-yellow-100 text-yellow-800'
      case 'Fermé':
        return 'bg-green-100 text-green-800'
      case 'Escaladé':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critique':
        return 'text-red-600'
      case 'Élevée':
        return 'text-orange-600'
      case 'Moyenne':
        return 'text-yellow-600'
      case 'Faible':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Tickets récents
          </h3>
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Tickets récents
          </h3>
          <Link
            href="/tickets"
            className="text-sm font-medium text-primary-600 hover:text-primary-500"
          >
            Voir tout
          </Link>
        </div>
        
        {tickets.length === 0 ? (
          <div className="text-center py-4">
            <p className="text-sm text-gray-500">Aucun ticket récent</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tickets.map((ticket) => (
              <div key={ticket.id} className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <Link
                      href={`/tickets/${ticket.id}`}
                      className="text-sm font-medium text-gray-900 hover:text-primary-600 truncate block"
                    >
                      {ticket.title}
                    </Link>
                    <p className="text-xs text-gray-500 mt-1">
                      #{ticket.id.slice(0, 8)} • {ticket.category.name}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2 ml-2">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(ticket.status.name)}`}>
                      {ticket.status.name}
                    </span>
                    <span className={`text-xs font-medium ${getPriorityColor(ticket.priority.name)}`}>
                      {ticket.priority.name}
                    </span>
                  </div>
                </div>
                <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
                  <span>{ticket.channel.name}</span>
                  <span>{new Date(ticket.created_at).toLocaleDateString('fr-FR')}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
