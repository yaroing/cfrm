import { useEffect, useState } from 'react'
import { ticketService, TicketStats } from '@/services/ticketService'

export default function Charts() {
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
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Statistiques
          </h3>
          <div className="space-y-4">
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
              <div className="h-32 bg-gray-200 rounded"></div>
            </div>
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
              <div className="h-32 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Statistiques
          </h3>
          <div className="text-center py-8">
            <p className="text-sm text-gray-500">Impossible de charger les statistiques</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Tickets par statut */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Tickets par statut
          </h3>
          <div className="space-y-3">
            {stats.status_stats.map((item) => {
              const total = stats.status_stats.reduce((sum, s) => sum + s.count, 0)
              const percentage = total > 0 ? (item.count / total) * 100 : 0
              
              return (
                <div key={item.status__name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-primary-500 mr-3"></div>
                    <span className="text-sm font-medium text-gray-700">
                      {item.status__name}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500 w-8 text-right">
                      {item.count}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Tickets par canal */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Tickets par canal
          </h3>
          <div className="space-y-3">
            {stats.channel_stats.map((item) => {
              const total = stats.channel_stats.reduce((sum, c) => sum + c.count, 0)
              const percentage = total > 0 ? (item.count / total) * 100 : 0
              
              return (
                <div key={item.channel__name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
                    <span className="text-sm font-medium text-gray-700">
                      {item.channel__name}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500 w-8 text-right">
                      {item.count}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Métriques de performance */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Métriques de performance
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">
                {stats.avg_response_time ? `${stats.avg_response_time.toFixed(1)}h` : 'N/A'}
              </div>
              <div className="text-sm text-gray-500">Temps de réponse moyen</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {stats.weekly_tickets}
              </div>
              <div className="text-sm text-gray-500">Tickets cette semaine</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
