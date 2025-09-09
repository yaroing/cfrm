import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'

export default function CTA() {
  const { user } = useAuth()

  return (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          <span className="block">Prêt à améliorer votre feedback communautaire ?</span>
          <span className="block text-primary-600">Commencez dès aujourd'hui.</span>
        </h2>
        <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div className="inline-flex rounded-md shadow">
            {user ? (
              <Link
                href="/dashboard"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Accéder au tableau de bord
              </Link>
            ) : (
              <Link
                href="/login"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Se connecter
              </Link>
            )}
          </div>
          <div className="ml-3 inline-flex rounded-md shadow">
            <Link
              href="/contact"
              className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50"
            >
              Nous contacter
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
