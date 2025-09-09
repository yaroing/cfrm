import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { apiService } from '../services/api';
import TicketResponses from './TicketResponses';
import TicketLogs from './TicketLogs';

interface Ticket {
  id: string;
  title: string;
  content: string;
  is_anonymous: boolean;
  category_name: string;
  priority_name: string;
  status_name: string;
  channel_name: string;
  submitter_name: string;
  submitter_phone: string;
  submitter_email: string;
  submitter_location: string;
  assigned_to: string | null;
  created_at: string;
  updated_at: string;
  closed_at: string | null;
  sla_deadline: string | null;
  is_psea: boolean;
  psea_escalated: boolean;
  tags: string[];
  attachments: any[];
  latitude: number | null;
  longitude: number | null;
  // Champs pour l'édition
  category: string;
  priority: string;
  status: string;
}

interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

interface Category {
  id: string;
  name: string;
  description: string;
  is_sensitive: boolean;
}

interface Priority {
  id: string;
  name: string;
  level: number;
  color: string;
  sla_hours: number;
}

interface Status {
  id: string;
  name: string;
  description: string;
  is_final: boolean;
  color: string;
}

const TicketDetail: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [priorities, setPriorities] = useState<Priority[]>([]);
  const [statuses, setStatuses] = useState<Status[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // État du formulaire d'édition
  const [formData, setFormData] = useState({
    category: '',
    priority: '',
    status: '',
    assigned_to: '',
    is_psea: false,
    tags: [] as string[],
  });

  useEffect(() => {
    if (id) {
      loadTicketData();
    }
  }, [id]);

  const loadTicketData = async () => {
    try {
      setLoading(true);
      
      // Charger le ticket et les données de référence en parallèle
      const [ticketResponse, usersResponse, categoriesResponse, prioritiesResponse, statusesResponse] = await Promise.all([
        apiService.get(`/tickets/${id}/`),
        apiService.get('/users/'),
        apiService.get('/categories/'),
        apiService.get('/priorities/'),
        apiService.get('/statuses/'),
      ]);

      setTicket(ticketResponse as Ticket);
      setUsers(((usersResponse as any).results || usersResponse) as User[]);
      setCategories(((categoriesResponse as any).results || categoriesResponse) as Category[]);
      setPriorities(((prioritiesResponse as any).results || prioritiesResponse) as Priority[]);
      setStatuses(((statusesResponse as any).results || statusesResponse) as Status[]);

      // Initialiser le formulaire avec les données du ticket
      if (ticketResponse) {
        const ticket = ticketResponse as Ticket;
        setFormData({
          category: ticket.category || '',
          priority: ticket.priority || '',
          status: ticket.status || '',
          assigned_to: ticket.assigned_to || '',
          is_psea: ticket.is_psea || false,
          tags: ticket.tags || [],
        });
      }
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await apiService.patch(`/tickets/${id}/`, formData);
      await loadTicketData(); // Recharger les données
      setEditing(false);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditing(false);
    // Restaurer les données originales
    if (ticket) {
      setFormData({
        category: ticket.category || '',
        priority: ticket.priority || '',
        status: ticket.status || '',
        assigned_to: ticket.assigned_to || '',
        is_psea: ticket.is_psea || false,
        tags: ticket.tags || [],
      });
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('fr-FR');
  };

  const getPriorityColor = (priorityName: string) => {
    const priority = priorities.find(p => p.name === priorityName);
    return priority?.color || '#000000';
  };

  const getStatusColor = (statusName: string) => {
    const status = statuses.find(s => s.name === statusName);
    return status?.color || '#000000';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!ticket) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h1 className="text-xl font-semibold text-red-800 mb-2">Ticket non trouvé</h1>
          <p className="text-red-600">Le ticket demandé n'existe pas ou n'est pas accessible.</p>
          <button
            onClick={() => router.push('/tickets')}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Retour à la liste
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête du ticket */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Ticket #{ticket.id}</h2>
            <p className="text-gray-600 mt-2">{ticket.title}</p>
          </div>
          <div className="flex space-x-3">
            {!editing ? (
              <button
                onClick={() => setEditing(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Modifier
              </button>
            ) : (
              <div className="flex space-x-2">
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
                >
                  {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                </button>
                <button
                  onClick={handleCancel}
                  className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                >
                  Annuler
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Contenu principal */}
        <div className="lg:col-span-2 space-y-6">
          {/* Informations du ticket */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Informations du ticket</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Titre</label>
                <p className="mt-1 text-gray-900">{ticket.title}</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Contenu</label>
                <div className="mt-1 p-4 bg-gray-50 rounded border">
                  <p className="text-gray-900 whitespace-pre-wrap">{ticket.content}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Canal</label>
                <p className="mt-1 text-gray-900">{ticket.channel_name}</p>
              </div>

              {ticket.is_anonymous ? (
                <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                  <p className="text-yellow-800 font-medium">⚠️ Ticket anonyme</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {ticket.submitter_name && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Nom du plaignant</label>
                      <p className="mt-1 text-gray-900">{ticket.submitter_name}</p>
                    </div>
                  )}
                  {ticket.submitter_phone && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Téléphone</label>
                      <p className="mt-1 text-gray-900">{ticket.submitter_phone}</p>
                    </div>
                  )}
                  {ticket.submitter_email && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Email</label>
                      <p className="mt-1 text-gray-900">{ticket.submitter_email}</p>
                    </div>
                  )}
                  {ticket.submitter_location && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Localisation</label>
                      <p className="mt-1 text-gray-900">{ticket.submitter_location}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Pièces jointes */}
          {ticket.attachments && ticket.attachments.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Pièces jointes</h2>
              <div className="space-y-2">
                {ticket.attachments.map((attachment, index) => (
                  <div key={index} className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
                    <span className="text-gray-600">📎</span>
                    <span className="text-gray-900">{attachment.name || `Fichier ${index + 1}`}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tags */}
          {ticket.tags && ticket.tags.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Tags</h2>
              <div className="flex flex-wrap gap-2">
                {ticket.tags.map((tag, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Panneau latéral */}
        <div className="space-y-6">
          {/* Statut et priorité */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Classification</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Catégorie</label>
                {editing ? (
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Sélectionner une catégorie</option>
                    {categories.map(cat => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name} {cat.is_sensitive && '(Sensible)'}
                      </option>
                    ))}
                  </select>
                ) : (
                  <p className="mt-1 text-gray-900">{ticket.category_name}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Priorité</label>
                {editing ? (
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({...formData, priority: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Sélectionner une priorité</option>
                    {priorities.map(priority => (
                      <option key={priority.id} value={priority.id}>
                        {priority.name} (Niveau {priority.level})
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="mt-1 flex items-center space-x-2">
                    <span 
                      className="inline-block w-3 h-3 rounded-full"
                      style={{ backgroundColor: getPriorityColor(ticket.priority_name) }}
                    ></span>
                    <span className="text-gray-900">{ticket.priority_name}</span>
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Statut</label>
                {editing ? (
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Sélectionner un statut</option>
                    {statuses.map(status => (
                      <option key={status.id} value={status.id}>
                        {status.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="mt-1 flex items-center space-x-2">
                    <span 
                      className="inline-block w-3 h-3 rounded-full"
                      style={{ backgroundColor: getStatusColor(ticket.status_name) }}
                    ></span>
                    <span className="text-gray-900">{ticket.status_name}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Assignation */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Assignation</h2>
            
            <div>
              <label className="block text-sm font-medium text-gray-700">Assigné à</label>
              {editing ? (
                <select
                  value={formData.assigned_to}
                  onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                  className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Non assigné</option>
                  {users.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.first_name} {user.last_name} ({user.username})
                    </option>
                  ))}
                </select>
              ) : (
                <p className="mt-1 text-gray-900">
                  {ticket.assigned_to ? 
                    users.find(u => u.id === ticket.assigned_to)?.first_name + ' ' + 
                    users.find(u => u.id === ticket.assigned_to)?.last_name || 'Utilisateur inconnu'
                    : 'Non assigné'
                  }
                </p>
              )}
            </div>
          </div>

          {/* Informations PSEA */}
          {ticket.is_psea && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6">
              <h2 className="text-xl font-semibold text-red-800 mb-4">⚠️ Protocole PSEA</h2>
              <div className="space-y-2 text-red-700">
                <p className="font-medium">Ticket sensible - Protection contre l'exploitation et les abus sexuels</p>
                <p>Escaladé: {ticket.psea_escalated ? 'Oui' : 'Non'}</p>
                <p className="text-sm">Accès restreint aux personnes autorisées uniquement</p>
              </div>
            </div>
          )}

          {/* Métadonnées */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Métadonnées</h2>
            
            <div className="space-y-3 text-sm">
              <div>
                <span className="font-medium text-gray-700">Créé le:</span>
                <span className="ml-2 text-gray-900">{formatDate(ticket.created_at)}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Modifié le:</span>
                <span className="ml-2 text-gray-900">{formatDate(ticket.updated_at)}</span>
              </div>
              {ticket.closed_at && (
                <div>
                  <span className="font-medium text-gray-700">Fermé le:</span>
                  <span className="ml-2 text-gray-900">{formatDate(ticket.closed_at)}</span>
                </div>
              )}
              {ticket.sla_deadline && (
                <div>
                  <span className="font-medium text-gray-700">Échéance SLA:</span>
                  <span className="ml-2 text-gray-900">{formatDate(ticket.sla_deadline)}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Section des réponses */}
      <div>
        <TicketResponses ticketId={ticket.id} />
      </div>

      {/* Section de l'historique */}
      <div>
        <TicketLogs ticketId={ticket.id} />
      </div>
    </div>
  );
};

export default TicketDetail;
