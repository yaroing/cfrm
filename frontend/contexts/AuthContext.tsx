import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/router'
import { authService } from '@/services/authService'
import toast from 'react-hot-toast'

interface User {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  organization: {
    id: string
    name: string
  }
  role: {
    id: string
    name: string
  }
  is_active: boolean
  is_verified: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: { username: string; password: string }) => Promise<void>
  logout: () => Promise<void>
  updateUser: (userData: Partial<User>) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('token')
      if (token) {
        const userData = await authService.getCurrentUser()
        setUser(userData)
      }
    } catch (error) {
      localStorage.removeItem('token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: { username: string; password: string }) => {
    try {
      const response = await authService.login(credentials)
      localStorage.setItem('token', response.access)
      localStorage.setItem('refresh', response.refresh)
      setUser(response.user)
    } catch (error: any) {
      const data = error?.response?.data
      const backendMsg =
        data?.message ||
        (Array.isArray(data?.non_field_errors) && data.non_field_errors[0]) ||
        data?.detail ||
        'Erreur de connexion'
      throw new Error(backendMsg)
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    } finally {
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      setUser(null)
      router.push('/login')
    }
  }

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...userData })
    }
  }

  const value = {
    user,
    loading,
    login,
    logout,
    updateUser,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
