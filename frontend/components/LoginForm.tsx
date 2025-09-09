import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline'

interface LoginFormProps {
  onSubmit: (credentials: { username: string; password: string }) => void
  loading: boolean
}

interface FormData {
  username: string
  password: string
  remember: boolean
}

export default function LoginForm({ onSubmit, loading }: LoginFormProps) {
  const [showPassword, setShowPassword] = useState(false)
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>()

  const handleFormSubmit = (data: FormData) => {
    onSubmit({
      username: data.username,
      password: data.password,
    })
  }

  return (
    <form className="mt-8 space-y-6" onSubmit={handleSubmit(handleFormSubmit)}>
      <div className="space-y-4">
        <div>
          <label htmlFor="username" className="form-label">
            Nom d'utilisateur ou email
          </label>
          <input
            {...register('username', { required: 'Le nom d\'utilisateur est requis' })}
            type="text"
            autoComplete="username"
            className={`form-input ${errors.username ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
            placeholder="Entrez votre nom d'utilisateur ou email"
          />
          {errors.username && (
            <p className="form-error">{errors.username.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="password" className="form-label">
            Mot de passe
          </label>
          <div className="relative">
            <input
              {...register('password', { required: 'Le mot de passe est requis' })}
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              className={`form-input pr-10 ${errors.password ? 'border-danger-300 focus:border-danger-500 focus:ring-danger-500' : ''}`}
              placeholder="Entrez votre mot de passe"
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-3 flex items-center"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeSlashIcon className="h-5 w-5 text-gray-400" />
              ) : (
                <EyeIcon className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
          {errors.password && (
            <p className="form-error">{errors.password.message}</p>
          )}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              {...register('remember')}
              id="remember"
              type="checkbox"
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="remember" className="ml-2 block text-sm text-gray-700">
              Se souvenir de moi
            </label>
          </div>

          <div className="text-sm">
            <a href="/forgot-password" className="font-medium text-primary-600 hover:text-primary-500">
              Mot de passe oublié ?
            </a>
          </div>
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="flex items-center">
              <div className="loading-spinner mr-2"></div>
              Connexion...
            </div>
          ) : (
            'Se connecter'
          )}
        </button>
      </div>

      <div className="text-center">
        <p className="text-sm text-gray-600">
          Pas encore de compte ?{' '}
          <a href="/register" className="font-medium text-primary-600 hover:text-primary-500">
            Créer un compte
          </a>
        </p>
      </div>
    </form>
  )
}
