import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import DashboardLayout from '@/components/DashboardLayout';

interface Ticket {
  id: string;
  title: string;
  status_name: string;
  category_name: string;
  priority_name: string;
  channel_name: string;
  created_at: string;
  updated_at: string;
}

interface DashboardStats {
  status_stats: Array<{ status__name: string; count: number }>;
  category_stats: Array<{ category__name: string; count: number }>;
  channel_stats: Array<{ channel__name: string; count: number }>;
  overdue_count: number;
  weekly_tickets: number;
  avg_response_time: number | null;
}

export default function AnalyticsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    loadData();
  }, [timeRange]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [ticketsRes, statsRes] = await Promise.all([
        apiService.get('/tickets/'),
        apiService.get('/tickets/dashboard_stats/')
      ]);
      
      setTickets((ticketsRes as any).results || ticketsRes);
      setStats(statsRes as DashboardStats);
    } catch (error: any) {
      setError('Erreur lors du chargement des données');
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: string } = {
      'Ouvert': 'bg-blue-500',
      'En cours': 'bg-yellow-500',
      'Fermé': 'bg-green-500',
      'Escaladé': 'bg-red-500',
      'Annulé': 'bg-gray-500',
    };
    return colors[status] || 'bg-gray-400';
  };

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      'Critique': 'bg-red-500',
      'Élevée': 'bg-orange-500',
      'Moyenne': 'bg-yellow-500',
      'Faible': 'bg-green-500',
      'Information': 'bg-blue-500',
    };
    return colors[priority] || 'bg-gray-400';
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Erreur</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <div className="flex space-x-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="7d">7 derniers jours</option>
              <option value="30d">30 derniers jours</option>
              <option value="90d">90 derniers jours</option>
              <option value="1y">1 an</option>
            </select>
          </div>
        </div>

        {/* Métriques principales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Tickets ouverts</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {stats?.status_stats.find(s => s.status__name === 'Ouvert')?.count || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Tickets fermés</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {stats?.status_stats.find(s => s.status__name === 'Fermé')?.count || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Tickets en retard</dt>
                    <dd className="text-lg font-medium text-gray-900">{stats?.overdue_count || 0}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Cette semaine</dt>
                    <dd className="text-lg font-medium text-gray-900">{stats?.weekly_tickets || 0}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Graphique des statuts */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets par statut</h3>
            <div className="space-y-3">
              {stats?.status_stats.map((status) => (
                <div key={status.status__name} className="flex items-center">
                  <div className="flex-shrink-0 w-4 h-4">
                    <div className={`w-4 h-4 rounded-full ${getStatusColor(status.status__name)}`}></div>
                  </div>
                  <div className="ml-3 flex-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-900">{status.status__name}</span>
                      <span className="text-gray-500">{status.count}</span>
                    </div>
                    <div className="mt-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getStatusColor(status.status__name)}`}
                        style={{ width: `${(status.count / Math.max(...(stats?.status_stats.map(s => s.count) || [1]))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Graphique des catégories */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets par catégorie</h3>
            <div className="space-y-3">
              {stats?.category_stats.map((category) => (
                <div key={category.category__name} className="flex items-center">
                  <div className="flex-shrink-0 w-4 h-4">
                    <div className="w-4 h-4 rounded-full bg-indigo-500"></div>
                  </div>
                  <div className="ml-3 flex-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-900">{category.category__name}</span>
                      <span className="text-gray-500">{category.count}</span>
                    </div>
                    <div className="mt-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full bg-indigo-500"
                        style={{ width: `${(category.count / Math.max(...(stats?.category_stats.map(c => c.count) || [1]))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Graphique des canaux */}
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Tickets par canal</h3>
            <div className="space-y-3">
              {stats?.channel_stats.map((channel) => (
                <div key={channel.channel__name} className="flex items-center">
                  <div className="flex-shrink-0 w-4 h-4">
                    <div className="w-4 h-4 rounded-full bg-green-500"></div>
                  </div>
                  <div className="ml-3 flex-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-900">{channel.channel__name}</span>
                      <span className="text-gray-500">{channel.count}</span>
                    </div>
                    <div className="mt-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full bg-green-500"
                        style={{ width: `${(channel.count / Math.max(...(stats?.channel_stats.map(c => c.count) || [1]))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tickets récents */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Tickets récents</h3>
              <a href="/tickets" className="text-sm text-indigo-600 hover:text-indigo-500">Voir tout</a>
            </div>
            <div className="space-y-3">
              {tickets.slice(0, 5).map((ticket) => (
                <div key={ticket.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{ticket.title}</p>
                    <p className="text-sm text-gray-500">#{ticket.id.slice(0, 8)}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(ticket.status_name)} text-white`}>
                      {ticket.status_name}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date(ticket.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Graphique de tendance temporelle */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Tendance des tickets</h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <p className="mt-2 text-sm text-gray-500">Graphique de tendance à venir...</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}