import { useEffect, useState } from 'react'
import Link from 'next/link'
import { apiService } from '../../services/api'
import DashboardLayout from '@/components/DashboardLayout'

interface Ticket {
  id: string
  title: string
  content: string
  status_name?: string
  category_name?: string
  priority_name?: string
  channel_name?: string
  created_at?: string
  updated_at?: string
  is_anonymous?: boolean
  submitter_name?: string
  submitter_email?: string
  submitter_phone?: string
}

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        console.log('Chargement des tickets...')
        const data = await apiService.get<any>('/tickets/')
        console.log('Données reçues:', data)
        // DRF pagination returns { results: [...] } by default
        const items: Ticket[] = Array.isArray(data) ? data : (data?.results ?? [])
        console.log('Tickets extraits:', items)
        setTickets(items)
      } catch (e: any) {
        console.error('Erreur lors du chargement:', e)
        setError(e?.response?.data?.detail || 'Erreur lors du chargement des tickets')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <DashboardLayout>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Tickets</h1>
        <Link
          href="/tickets/new"
          className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Nouveau ticket
        </Link>
      </div>

      <div className="mt-6">
        {loading && (
          <div className="text-gray-500">Chargement…</div>
        )}
        {error && (
          <div className="rounded-md bg-red-50 p-4 text-red-700 border border-red-200">{error}</div>
        )}
        {!loading && !error && (
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <ul role="list" className="divide-y divide-gray-200">
              {tickets.map((t) => (
                <li key={t.id} className="px-6 py-4 hover:bg-gray-50">
                  <Link href={`/tickets/${t.id}`} className="block">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          <p className="text-sm font-medium text-gray-900 hover:text-blue-600">{t.title}</p>
                          <span className="inline-flex items-center rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-800">
                            {t.category_name || '—'}
                          </span>
                          <span className="inline-flex items-center rounded-full bg-yellow-100 px-2 py-0.5 text-xs font-medium text-yellow-800">
                            {t.priority_name || '—'}
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-gray-500 line-clamp-2">{t.content}</p>
                        <div className="mt-2 flex items-center space-x-4 text-xs text-gray-400">
                          <span>Canal: {t.channel_name || '—'}</span>
                          <span>Créé: {t.created_at ? new Date(t.created_at).toLocaleDateString('fr-FR') : '—'}</span>
                          {t.submitter_name && <span>Par: {t.submitter_name}</span>}
                        </div>
                      </div>
                      <div className="ml-4 flex items-center space-x-2">
                        <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800">
                          {t.status_name || '—'}
                        </span>
                        <span className="text-gray-400">→</span>
                      </div>
                    </div>
                  </Link>
                </li>
              ))}
              {tickets.length === 0 && (
                <li className="px-6 py-8 text-center text-gray-500">Aucun ticket</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
