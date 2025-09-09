const features = [
  {
    name: 'Collecte multicanal',
    description: 'SMS, WhatsApp, Web, Email et téléphone pour toucher toutes les communautés.',
    icon: '📱',
  },
  {
    name: 'Sécurité renforcée',
    description: 'Chiffrement AES-256, authentification JWT et rôles granulaires.',
    icon: '🔒',
  },
  {
    name: 'Conformité normative',
    description: 'Respect des standards CHS, IASC, UNHCR et IFRC.',
    icon: '✅',
  },
  {
    name: 'PSEA intégré',
    description: 'Circuits sécurisés pour la protection contre l\'exploitation et les abus sexuels.',
    icon: '🛡️',
  },
  {
    name: 'Analytics avancés',
    description: 'Tableaux de bord, rapports et métriques en temps réel.',
    icon: '📊',
  },
  {
    name: 'Interopérabilité',
    description: 'API RESTful et intégrations avec les outils existants.',
    icon: '🔗',
  },
]

export default function Features() {
  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-primary-600 font-semibold tracking-wide uppercase">Fonctionnalités</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Une plateforme complète pour le feedback communautaire
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Conçue spécifiquement pour le secteur humanitaire avec les meilleures pratiques de sécurité et de conformité.
          </p>
        </div>

        <div className="mt-10">
          <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10 lg:grid-cols-3">
            {features.map((feature) => (
              <div key={feature.name} className="relative">
                <dt>
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white text-2xl">
                    {feature.icon}
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900">{feature.name}</p>
                </dt>
                <dd className="mt-2 ml-16 text-base text-gray-500">{feature.description}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  )
}
