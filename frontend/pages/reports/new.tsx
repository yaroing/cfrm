import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { apiService } from '../../services/api';
import DashboardLayout from '@/components/DashboardLayout';

interface Category {
  id: number;
  name: string;
}

interface Status {
  id: number;
  name: string;
}

interface Priority {
  id: number;
  name: string;
}

interface Channel {
  id: number;
  name: string;
}

interface ReportResponse {
  download_url?: string;
  message?: string;
}

interface ReportFilters {
  date_from: string;
  date_to: string;
  categories: number[];
  statuses: number[];
  priorities: number[];
  channels: number[];
  include_responses: boolean;
  include_logs: boolean;
}

export default function NewReport() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [statuses, setStatuses] = useState<Status[]>([]);
  const [priorities, setPriorities] = useState<Priority[]>([]);
  const [channels, setChannels] = useState<Channel[]>([]);
  const [reportUrl, setReportUrl] = useState<string | null>(null);

  const [filters, setFilters] = useState<ReportFilters>({
    date_from: '',
    date_to: '',
    categories: [],
    statuses: [],
    priorities: [],
    channels: [],
    include_responses: false,
    include_logs: false,
  });

  useEffect(() => {
    loadReferenceData();
    // Définir les dates par défaut (30 derniers jours)
    const today = new Date();
    const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);
    
    setFilters(prev => ({
      ...prev,
      date_from: thirtyDaysAgo.toISOString().split('T')[0],
      date_to: today.toISOString().split('T')[0],
    }));
  }, []);

  const loadReferenceData = async () => {
    try {
      setLoading(true);
      const [categoriesRes, statusesRes, prioritiesRes, channelsRes] = await Promise.all([
        apiService.get('/categories/'),
        apiService.get('/statuses/'),
        apiService.get('/priorities/'),
        apiService.get('/channels/'),
      ]);

      setCategories((categoriesRes as any).results || categoriesRes);
      setStatuses((statusesRes as any).results || statusesRes);
      setPriorities((prioritiesRes as any).results || prioritiesRes);
      setChannels((channelsRes as any).results || channelsRes);
    } catch (error) {
      console.error('Erreur lors du chargement des données de référence:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field: keyof ReportFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleArrayFilterChange = (field: 'categories' | 'statuses' | 'priorities' | 'channels', value: number) => {
    setFilters(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(id => id !== value)
        : [...prev[field], value],
    }));
  };

  const handleGenerateReport = async (format: 'pdf' | 'excel') => {
    try {
      setGenerating(true);
      setReportUrl(null);

      const response = await apiService.post('/reports/generate/', {
        ...filters,
        format,
      }) as ReportResponse;

      if (response.download_url) {
        setReportUrl(response.download_url);
        // Télécharger automatiquement le fichier
        window.open(response.download_url, '_blank');
      }
    } catch (error: any) {
      console.error('Erreur lors de la génération du rapport:', error);
      alert('Erreur lors de la génération du rapport: ' + (error.response?.data?.message || error.message));
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des données...</p>
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Nouveau rapport</h1>
          <button
            onClick={() => router.push('/dashboard')}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Filtres */}
              <div>
                <h2 className="text-lg font-medium text-gray-900 mb-6">Filtres du rapport</h2>
                
                <div className="space-y-6">
                  {/* Période */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Période</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="date_from" className="block text-sm text-gray-600">
                          Date de début
                        </label>
                        <input
                          type="date"
                          id="date_from"
                          value={filters.date_from}
                          onChange={(e) => handleFilterChange('date_from', e.target.value)}
                          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        />
                      </div>
                      <div>
                        <label htmlFor="date_to" className="block text-sm text-gray-600">
                          Date de fin
                        </label>
                        <input
                          type="date"
                          id="date_to"
                          value={filters.date_to}
                          onChange={(e) => handleFilterChange('date_to', e.target.value)}
                          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Catégories */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Catégories</h3>
                    <div className="space-y-2 max-h-32 overflow-y-auto">
                      {categories.map((category) => (
                        <label key={category.id} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={filters.categories.includes(category.id)}
                            onChange={() => handleArrayFilterChange('categories', category.id)}
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">{category.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Statuts */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Statuts</h3>
                    <div className="space-y-2 max-h-32 overflow-y-auto">
                      {statuses.map((status) => (
                        <label key={status.id} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={filters.statuses.includes(status.id)}
                            onChange={() => handleArrayFilterChange('statuses', status.id)}
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">{status.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Priorités */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Priorités</h3>
                    <div className="space-y-2 max-h-32 overflow-y-auto">
                      {priorities.map((priority) => (
                        <label key={priority.id} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={filters.priorities.includes(priority.id)}
                            onChange={() => handleArrayFilterChange('priorities', priority.id)}
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">{priority.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Canaux */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Canaux</h3>
                    <div className="space-y-2 max-h-32 overflow-y-auto">
                      {channels.map((channel) => (
                        <label key={channel.id} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={filters.channels.includes(channel.id)}
                            onChange={() => handleArrayFilterChange('channels', channel.id)}
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm text-gray-700">{channel.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Options supplémentaires */}
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-3">Options supplémentaires</h3>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.include_responses}
                          onChange={(e) => handleFilterChange('include_responses', e.target.checked)}
                          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">Inclure les réponses</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.include_logs}
                          onChange={(e) => handleFilterChange('include_logs', e.target.checked)}
                          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">Inclure les logs d'activité</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>

              {/* Aperçu et génération */}
              <div>
                <h2 className="text-lg font-medium text-gray-900 mb-6">Génération du rapport</h2>
                
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-sm font-medium text-gray-700 mb-4">Aperçu des filtres</h3>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p><strong>Période :</strong> {filters.date_from} - {filters.date_to}</p>
                    <p><strong>Catégories :</strong> {filters.categories.length === 0 ? 'Toutes' : filters.categories.length + ' sélectionnées'}</p>
                    <p><strong>Statuts :</strong> {filters.statuses.length === 0 ? 'Tous' : filters.statuses.length + ' sélectionnés'}</p>
                    <p><strong>Priorités :</strong> {filters.priorities.length === 0 ? 'Toutes' : filters.priorities.length + ' sélectionnées'}</p>
                    <p><strong>Canaux :</strong> {filters.channels.length === 0 ? 'Tous' : filters.channels.length + ' sélectionnés'}</p>
                    <p><strong>Réponses :</strong> {filters.include_responses ? 'Incluses' : 'Non incluses'}</p>
                    <p><strong>Logs :</strong> {filters.include_logs ? 'Inclus' : 'Non inclus'}</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <button
                    onClick={() => handleGenerateReport('pdf')}
                    disabled={generating}
                    className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {generating ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Génération...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Générer PDF
                      </>
                    )}
                  </button>

                  <button
                    onClick={() => handleGenerateReport('excel')}
                    disabled={generating}
                    className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {generating ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Génération...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Générer Excel
                      </>
                    )}
                  </button>
                </div>

                {reportUrl && (
                  <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-green-800">
                          Rapport généré avec succès
                        </h3>
                        <div className="mt-2 text-sm text-green-700">
                          <p>Le rapport a été généré et téléchargé automatiquement.</p>
                          <a
                            href={reportUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-medium underline hover:text-green-600"
                          >
                            Cliquer ici pour le télécharger à nouveau
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}