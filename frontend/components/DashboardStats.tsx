import { useEffect, useState } from 'react'
import { ticketService, TicketStats } from '@/services/ticketService'

export default function DashboardStats() {
  const [stats, setStats] = useState<TicketStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await ticketService.getDashboardStats()
        setStats(data)
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      <div className="h-6 bg-gray-200 rounded animate-pulse mt-1"></div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              Erreur de chargement
            </h3>
            <div className="mt-2 text-sm text-red-700">
              Impossible de charger les statistiques du tableau de bord.
            </div>
          </div>
        </div>
      </div>
    )
  }

  const statCards = [
    {
      name: 'Tickets ouverts',
      value: stats.status_stats.find(s => s.status__name === 'Ouvert')?.count || 0,
      icon: '🎫',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'Tickets fermés',
      value: stats.status_stats.find(s => s.status__name === 'Fermé')?.count || 0,
      icon: '✅',
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      name: 'Tickets en retard',
      value: stats.overdue_count,
      icon: '⚠️',
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      name: 'Cette semaine',
      value: stats.weekly_tickets,
      icon: '📅',
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ]

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      {statCards.map((card) => (
        <div key={card.name} className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className={`w-8 h-8 ${card.bgColor} rounded-md flex items-center justify-center`}>
                  <span className="text-lg">{card.icon}</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {card.name}
                  </dt>
                  <dd className={`text-lg font-medium ${card.color}`}>
                    {card.value.toLocaleString()}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
