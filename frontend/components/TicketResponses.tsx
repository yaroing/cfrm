import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface Response {
  id: string;
  content: string;
  author: string | null;
  author_name: string | null;
  is_internal: boolean;
  created_at: string;
  sent_at: string | null;
  delivery_status: string;
}

interface TicketResponsesProps {
  ticketId: string;
}

const TicketResponses: React.FC<TicketResponsesProps> = ({ ticketId }) => {
  const [responses, setResponses] = useState<Response[]>([]);
  const [loading, setLoading] = useState(true);
  const [newResponse, setNewResponse] = useState('');
  const [isInternal, setIsInternal] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadResponses();
  }, [ticketId]);

  const loadResponses = async () => {
    try {
      setLoading(true);
      const data = await apiService.get(`/responses/?ticket=${ticketId}`);
      setResponses(Array.isArray(data) ? data : (data as any).results || []);
    } catch (error) {
      console.error('Erreur lors du chargement des réponses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newResponse.trim()) return;

    try {
      setSaving(true);
      await apiService.post('/responses/', {
        ticket: ticketId,
        content: newResponse,
        is_internal: isInternal,
      });
      
      setNewResponse('');
      setIsInternal(false);
      await loadResponses();
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la réponse:', error);
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('fr-FR');
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Réponses</h2>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Réponses</h2>
      
      {/* Liste des réponses */}
      <div className="space-y-4 mb-6">
        {responses.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Aucune réponse pour ce ticket</p>
        ) : (
          responses.map((response) => (
            <div
              key={response.id}
              className={`p-4 rounded-lg border ${
                response.is_internal
                  ? 'bg-yellow-50 border-yellow-200'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-gray-900">
                    {response.author_name || 'Système'}
                  </span>
                  {response.is_internal && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                      Interne
                    </span>
                  )}
                </div>
                <span className="text-sm text-gray-500">
                  {formatDate(response.created_at)}
                </span>
              </div>
              
              <div className="text-gray-700 whitespace-pre-wrap">
                {response.content}
              </div>
              
              {response.sent_at && (
                <div className="mt-2 text-xs text-gray-500">
                  Envoyé le: {formatDate(response.sent_at)}
                  {response.delivery_status && (
                    <span className="ml-2">Status: {response.delivery_status}</span>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Formulaire d'ajout de réponse */}
      <form onSubmit={handleSubmit} className="border-t pt-4">
        <h3 className="text-lg font-medium mb-3">Ajouter une réponse</h3>
        
        <div className="mb-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={isInternal}
              onChange={(e) => setIsInternal(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            />
            <span className="ml-2 text-sm text-gray-700">
              Note interne (non visible par le plaignant)
            </span>
          </label>
        </div>

        <div className="mb-4">
          <textarea
            value={newResponse}
            onChange={(e) => setNewResponse(e.target.value)}
            placeholder="Tapez votre réponse..."
            rows={4}
            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving || !newResponse.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {saving ? 'Envoi...' : 'Envoyer la réponse'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TicketResponses;
