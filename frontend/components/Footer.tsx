import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center">
              <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">C</span>
              </div>
              <div className="ml-3">
                <h3 className="text-lg font-bold text-gray-900">CFRM</h3>
                <p className="text-sm text-gray-500">Plateforme de feedback communautaire</p>
              </div>
            </div>
            <p className="mt-4 text-sm text-gray-600 max-w-md">
              Une plateforme multicanal sécurisée pour la collecte et la gestion 
              du feedback communautaire dans le secteur humanitaire.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">Plateforme</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="/about" className="text-sm text-gray-600 hover:text-primary-600">
                  À propos
                </Link>
              </li>
              <li>
                <Link href="/features" className="text-sm text-gray-600 hover:text-primary-600">
                  Fonctionnalités
                </Link>
              </li>
              <li>
                <Link href="/security" className="text-sm text-gray-600 hover:text-primary-600">
                  Sécurité
                </Link>
              </li>
              <li>
                <Link href="/api" className="text-sm text-gray-600 hover:text-primary-600">
                  API
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">Support</h4>
            <ul className="mt-4 space-y-2">
              <li>
                <Link href="/help" className="text-sm text-gray-600 hover:text-primary-600">
                  Centre d'aide
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-sm text-gray-600 hover:text-primary-600">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-sm text-gray-600 hover:text-primary-600">
                  Confidentialité
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-sm text-gray-600 hover:text-primary-600">
                  Conditions d'utilisation
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-500">
              © 2024 CFRM. Tous droits réservés.
            </p>
            <div className="mt-4 md:mt-0 flex space-x-6">
              <Link href="/privacy" className="text-sm text-gray-500 hover:text-gray-700">
                Politique de confidentialité
              </Link>
              <Link href="/terms" className="text-sm text-gray-500 hover:text-gray-700">
                Conditions d'utilisation
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
