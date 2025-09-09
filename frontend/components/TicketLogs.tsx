import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface Log {
  id: string;
  action: string;
  action_display: string;
  description: string;
  old_value: string;
  new_value: string;
  user: string | null;
  user_name: string | null;
  created_at: string;
  ip_address: string | null;
}

interface TicketLogsProps {
  ticketId: string;
}

const TicketLogs: React.FC<TicketLogsProps> = ({ ticketId }) => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
  }, [ticketId]);

  const loadLogs = async () => {
    try {
      setLoading(true);
      const data = await apiService.get(`/logs/?ticket=${ticketId}&v=2`);
      setLogs(Array.isArray(data) ? data : (data as any).results || []);
    } catch (error) {
      console.error('Erreur lors du chargement des logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('fr-FR');
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'created':
        return '🆕';
      case 'updated':
        return '✏️';
      case 'assigned':
        return '👤';
      case 'status_changed':
        return '🔄';
      case 'priority_changed':
        return '⚡';
      case 'escalated':
        return '📈';
      case 'closed':
        return '🔒';
      case 'reopened':
        return '🔓';
      case 'response_added':
        return '💬';
      default:
        return '📝';
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'created':
        return 'bg-green-100 text-green-800';
      case 'updated':
        return 'bg-blue-100 text-blue-800';
      case 'assigned':
        return 'bg-purple-100 text-purple-800';
      case 'status_changed':
        return 'bg-yellow-100 text-yellow-800';
      case 'priority_changed':
        return 'bg-orange-100 text-orange-800';
      case 'escalated':
        return 'bg-red-100 text-red-800';
      case 'closed':
        return 'bg-gray-100 text-gray-800';
      case 'reopened':
        return 'bg-green-100 text-green-800';
      case 'response_added':
        return 'bg-indigo-100 text-indigo-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Historique</h2>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Historique des modifications</h2>
      
      {logs.length === 0 ? (
        <p className="text-gray-500 text-center py-4">Aucun historique disponible</p>
      ) : (
        <div className="space-y-4">
          {logs.map((log) => (
            <div key={log.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0">
                <span className="text-2xl">{getActionIcon(log.action)}</span>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getActionColor(log.action)}`}>
                    {log.action_display}
                  </span>
                  <span className="text-sm text-gray-500">
                    {formatDate(log.created_at)}
                  </span>
                </div>
                
                <p className="text-sm text-gray-900 mb-1">
                  {log.description}
                </p>
                
                {log.user_name && (
                  <p className="text-xs text-gray-600">
                    Par: {log.user_name}
                  </p>
                )}
                
                {(log.old_value || log.new_value) && (
                  <div className="mt-2 text-xs">
                    {log.old_value && (
                      <span className="text-red-600">
                        Ancien: {log.old_value}
                      </span>
                    )}
                    {log.old_value && log.new_value && (
                      <span className="mx-2">→</span>
                    )}
                    {log.new_value && (
                      <span className="text-green-600">
                        Nouveau: {log.new_value}
                      </span>
                    )}
                  </div>
                )}
                
                {log.ip_address && (
                  <p className="text-xs text-gray-400 mt-1">
                    IP: {log.ip_address}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TicketLogs;
