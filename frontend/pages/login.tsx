import { useState } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import Layout from '@/components/Layout'
import LoginForm from '@/components/LoginForm'
import toast from 'react-hot-toast'

export default function Login() {
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const router = useRouter()

  const handleLogin = async (credentials: { username: string; password: string }) => {
    setLoading(true)
    try {
      await login(credentials)
      toast.success('Connexion réussie')
      router.push('/dashboard')
    } catch (error: any) {
      toast.error(error.message || 'Erreur de connexion')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Connexion à votre compte
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Plateforme de feedback communautaire
            </p>
          </div>
          <LoginForm onSubmit={handleLogin} loading={loading} />
        </div>
      </div>
    </Layout>
  )
}
