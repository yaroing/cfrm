import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'

export default function QuickActions() {
  const { user } = useAuth()

  const actions = [
    {
      name: 'Nouveau ticket',
      description: 'Créer un nouveau ticket de feedback',
      href: '/tickets/new',
      icon: '➕',
      color: 'bg-blue-500 hover:bg-blue-600',
    },
    {
      name: 'Importer des données',
      description: 'Importer des tickets depuis un fichier',
      href: '/tickets/import',
      icon: '📥',
      color: 'bg-green-500 hover:bg-green-600',
    },
    {
      name: 'Générer un rapport',
      description: 'Créer un rapport personnalisé',
      href: '/reports/new',
      icon: '📊',
      color: 'bg-purple-500 hover:bg-purple-600',
    },
    {
      name: 'Gérer les canaux',
      description: 'Configurer les canaux de communication',
      href: '/channels',
      icon: '📱',
      color: 'bg-orange-500 hover:bg-orange-600',
    },
  ]

  // Filtrer les actions selon les permissions de l'utilisateur
  const filteredActions = actions.filter((action) => {
    if (action.name === 'Gérer les canaux' && !user?.role?.name?.includes('Admin')) {
      return false
    }
    return true
  })

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
          Actions rapides
        </h3>
        <div className="grid grid-cols-1 gap-3">
          {filteredActions.map((action) => (
            <Link
              key={action.name}
              href={action.href}
              className="relative group bg-white p-4 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
            >
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className={`w-8 h-8 ${action.color} rounded-md flex items-center justify-center text-white text-sm font-medium`}>
                    {action.icon}
                  </div>
                </div>
                <div className="ml-3 flex-1">
                  <h4 className="text-sm font-medium text-gray-900 group-hover:text-primary-600">
                    {action.name}
                  </h4>
                  <p className="text-xs text-gray-500 mt-1">
                    {action.description}
                  </p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
