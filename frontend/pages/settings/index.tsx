import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import DashboardLayout from '@/components/DashboardLayout';

interface Settings {
  site_name: string;
  site_description: string;
  contact_email: string;
  contact_phone: string;
  timezone: string;
  language: string;
  maintenance_mode: boolean;
  allow_registration: boolean;
  require_email_verification: boolean;
  max_file_size: number;
  allowed_file_types: string[];
  smtp_host: string;
  smtp_port: number;
  smtp_username: string;
  smtp_password: string;
  twilio_account_sid: string;
  twilio_auth_token: string;
  whatsapp_access_token: string;
  encryption_key: string;
  session_timeout: number;
  max_login_attempts: number;
  password_min_length: number;
  password_require_special: boolean;
  audit_log_retention_days: number;
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings>({
    site_name: 'CFRM Feedback communautaire',
    site_description: 'Plateforme de feedback communautaire',
    contact_email: 'contact@cfrm.org',
    contact_phone: '+33 1 23 45 67 89',
    timezone: 'Europe/Paris',
    language: 'fr',
    maintenance_mode: false,
    allow_registration: true,
    require_email_verification: true,
    max_file_size: 10485760, // 10MB
    allowed_file_types: ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'],
    smtp_host: '',
    smtp_port: 587,
    smtp_username: '',
    smtp_password: '',
    twilio_account_sid: '',
    twilio_auth_token: '',
    whatsapp_access_token: '',
    encryption_key: '',
    session_timeout: 3600, // 1 hour
    max_login_attempts: 5,
    password_min_length: 8,
    password_require_special: true,
    audit_log_retention_days: 365,
  });
  
  const [activeTab, setActiveTab] = useState('general');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const tabs = [
    { id: 'general', name: 'Général', icon: '⚙️' },
    { id: 'security', name: 'Sécurité', icon: '🔒' },
    { id: 'email', name: 'Email', icon: '📧' },
    { id: 'sms', name: 'SMS/WhatsApp', icon: '📱' },
    { id: 'files', name: 'Fichiers', icon: '📁' },
    { id: 'audit', name: 'Audit', icon: '📊' },
  ];

  const handleSave = async () => {
    try {
      setSaving(true);
      // Ici, vous feriez un appel API pour sauvegarder les paramètres
      // await apiService.patch('/settings/', settings);
      
      setMessage({ type: 'success', text: 'Paramètres sauvegardés avec succès' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Erreur lors de la sauvegarde' });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (key: keyof Settings, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Nom du site</label>
        <input
          type="text"
          value={settings.site_name}
          onChange={(e) => handleChange('site_name', e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">Description du site</label>
        <textarea
          value={settings.site_description}
          onChange={(e) => handleChange('site_description', e.target.value)}
          rows={3}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Email de contact</label>
          <input
            type="email"
            value={settings.contact_email}
            onChange={(e) => handleChange('contact_email', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Téléphone de contact</label>
          <input
            type="tel"
            value={settings.contact_phone}
            onChange={(e) => handleChange('contact_phone', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Fuseau horaire</label>
          <select
            value={settings.timezone}
            onChange={(e) => handleChange('timezone', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="Europe/Paris">Europe/Paris</option>
            <option value="UTC">UTC</option>
            <option value="America/New_York">America/New_York</option>
            <option value="Asia/Tokyo">Asia/Tokyo</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Langue</label>
          <select
            value={settings.language}
            onChange={(e) => handleChange('language', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="fr">Français</option>
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="ar">العربية</option>
          </select>
        </div>
      </div>
      
      <div className="space-y-4">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={settings.maintenance_mode}
            onChange={(e) => handleChange('maintenance_mode', e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label className="ml-2 block text-sm text-gray-900">Mode maintenance</label>
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={settings.allow_registration}
            onChange={(e) => handleChange('allow_registration', e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label className="ml-2 block text-sm text-gray-900">Autoriser l'inscription</label>
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={settings.require_email_verification}
            onChange={(e) => handleChange('require_email_verification', e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label className="ml-2 block text-sm text-gray-900">Vérification email requise</label>
        </div>
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Clé de chiffrement</label>
        <input
          type="password"
          value={settings.encryption_key}
          onChange={(e) => handleChange('encryption_key', e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="Clé AES-256"
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Délai d'expiration de session (secondes)</label>
          <input
            type="number"
            value={settings.session_timeout}
            onChange={(e) => handleChange('session_timeout', parseInt(e.target.value))}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Tentatives de connexion max</label>
          <input
            type="number"
            value={settings.max_login_attempts}
            onChange={(e) => handleChange('max_login_attempts', parseInt(e.target.value))}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Longueur minimale du mot de passe</label>
          <input
            type="number"
            value={settings.password_min_length}
            onChange={(e) => handleChange('password_min_length', parseInt(e.target.value))}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={settings.password_require_special}
            onChange={(e) => handleChange('password_require_special', e.target.checked)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label className="ml-2 block text-sm text-gray-900">Caractères spéciaux requis</label>
        </div>
      </div>
    </div>
  );

  const renderEmailSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Serveur SMTP</label>
          <input
            type="text"
            value={settings.smtp_host}
            onChange={(e) => handleChange('smtp_host', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="smtp.gmail.com"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Port SMTP</label>
          <input
            type="number"
            value={settings.smtp_port}
            onChange={(e) => handleChange('smtp_port', parseInt(e.target.value))}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Nom d'utilisateur SMTP</label>
          <input
            type="text"
            value={settings.smtp_username}
            onChange={(e) => handleChange('smtp_username', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Mot de passe SMTP</label>
          <input
            type="password"
            value={settings.smtp_password}
            onChange={(e) => handleChange('smtp_password', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
    </div>
  );

  const renderSMSSettings = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700">Twilio Account SID</label>
          <input
            type="text"
            value={settings.twilio_account_sid}
            onChange={(e) => handleChange('twilio_account_sid', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Twilio Auth Token</label>
          <input
            type="password"
            value={settings.twilio_auth_token}
            onChange={(e) => handleChange('twilio_auth_token', e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">WhatsApp Access Token</label>
        <input
          type="password"
          value={settings.whatsapp_access_token}
          onChange={(e) => handleChange('whatsapp_access_token', e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>
    </div>
  );

  const renderFileSettings = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Taille maximale des fichiers (octets)</label>
        <input
          type="number"
          value={settings.max_file_size}
          onChange={(e) => handleChange('max_file_size', parseInt(e.target.value))}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
        <p className="mt-1 text-sm text-gray-500">Actuellement: {(settings.max_file_size / 1024 / 1024).toFixed(1)} MB</p>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">Types de fichiers autorisés</label>
        <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-2">
          {settings.allowed_file_types.map((type, index) => (
            <div key={index} className="flex items-center">
              <input
                type="checkbox"
                checked={true}
                onChange={(e) => {
                  if (!e.target.checked) {
                    handleChange('allowed_file_types', settings.allowed_file_types.filter((_, i) => i !== index));
                  }
                }}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-900">.{type}</label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderAuditSettings = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Rétention des logs d'audit (jours)</label>
        <input
          type="number"
          value={settings.audit_log_retention_days}
          onChange={(e) => handleChange('audit_log_retention_days', parseInt(e.target.value))}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
        <p className="mt-1 text-sm text-gray-500">Les logs seront supprimés après cette période</p>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general': return renderGeneralSettings();
      case 'security': return renderSecuritySettings();
      case 'email': return renderEmailSettings();
      case 'sms': return renderSMSSettings();
      case 'files': return renderFileSettings();
      case 'audit': return renderAuditSettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Paramètres</h1>
          <button
            onClick={handleSave}
            disabled={saving}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {saving ? 'Sauvegarde...' : 'Sauvegarder'}
          </button>
        </div>

        {message && (
          <div className={`rounded-md p-4 ${
            message.type === 'success' 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex">
              <div className="flex-shrink-0">
                {message.type === 'success' ? (
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="ml-3">
                <p className={`text-sm font-medium ${
                  message.type === 'success' ? 'text-green-800' : 'text-red-800'
                }`}>
                  {message.text}
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white shadow rounded-lg">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6" aria-label="Tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`${
                    activeTab === tab.id
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>
          
          <div className="p-6">
            {renderTabContent()}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}