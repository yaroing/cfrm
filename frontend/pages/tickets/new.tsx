import { useState, useEffect, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { apiService } from '../../services/api'
import DashboardLayout from '@/components/DashboardLayout'

type Option = { id: string | number; name: string }

export default function NewTicketPage() {
  const router = useRouter()

  // Core fields
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [isAnonymous, setIsAnonymous] = useState(false)

  // Foreign keys
  const [category, setCategory] = useState<string>('')
  const [priority, setPriority] = useState<string>('')
  const [channel, setChannel] = useState<string>('')

  // Optional identifiers / submitter info
  const [externalId, setExternalId] = useState('')
  const [submitterName, setSubmitterName] = useState('')
  const [submitterPhone, setSubmitterPhone] = useState('')
  const [submitterEmail, setSubmitterEmail] = useState('')
  const [submitterLocation, setSubmitterLocation] = useState('')

  // Geo
  const [latitude, setLatitude] = useState<string>('')
  const [longitude, setLongitude] = useState<string>('')

  // JSON fields
  const [tags, setTags] = useState<string>('') // comma-separated
  const [metadata, setMetadata] = useState<string>('') // JSON string

  // Attachments
  const [files, setFiles] = useState<FileList | null>(null)

  // Taxonomies
  const [categories, setCategories] = useState<Option[]>([])
  const [priorities, setPriorities] = useState<Option[]>([])
  const [channels, setChannels] = useState<Option[]>([])

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  useEffect(() => {
    const fetchMeta = async () => {
      try {
        const [cats, pris, chs] = await Promise.all([
          apiService.get<any>('/categories/'),
          apiService.get<any>('/priorities/'),
          apiService.get<any>('/channels/'),
        ])
        setCategories((cats?.results ?? cats ?? []).map((x: any) => ({ id: x.id, name: x.name })))
        setPriorities((pris?.results ?? pris ?? []).map((x: any) => ({ id: x.id, name: x.name })))
        setChannels((chs?.results ?? chs ?? []).map((x: any) => ({ id: x.id, name: x.name })))
      } catch (e) {
        // keep form usable, show minimal error
        setError('Impossible de charger les listes (catégories/priorités/canaux)')
      }
    }
    fetchMeta()
  }, [])

  const onFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFiles(e.target.files)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(null)
    try {
      const fd = new FormData()
      fd.append('title', title)
      fd.append('content', content)
      fd.append('is_anonymous', String(isAnonymous))
      fd.append('category', category)
      fd.append('priority', priority)
      fd.append('channel', channel)
      if (externalId) fd.append('external_id', externalId)
      if (submitterName) fd.append('submitter_name', submitterName)
      if (submitterPhone) fd.append('submitter_phone', submitterPhone)
      if (submitterEmail) fd.append('submitter_email', submitterEmail)
      if (submitterLocation) fd.append('submitter_location', submitterLocation)
      if (latitude) fd.append('latitude', latitude)
      if (longitude) fd.append('longitude', longitude)
      if (tags) fd.append('tags', JSON.stringify(tags.split(',').map(t => t.trim()).filter(Boolean)))
      if (metadata) fd.append('metadata', metadata)
      if (files) {
        Array.from(files).forEach((f) => fd.append('attachments', f))
      }

      await apiService.post('/tickets/', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setSuccess('Ticket créé avec succès')
      router.push('/tickets')
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.response?.data || 'Erreur lors de la création du ticket'
      setError(typeof detail === 'string' ? detail : JSON.stringify(detail))
    } finally {
      setLoading(false)
    }
  }

  return (
    <DashboardLayout>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Nouveau ticket</h1>
      </div>

      <div className="mt-6 max-w-3xl">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4 text-red-700 border border-red-200">{error}</div>
        )}
        {success && (
          <div className="mb-4 rounded-md bg-green-50 p-4 text-green-700 border border-green-200">{success}</div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6" encType="multipart/form-data">
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Titre</label>
              <input
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Contenu</label>
              <textarea
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                rows={5}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
              />
            </div>
            <div className="flex items-center">
              <input
                id="isAnonymous"
                type="checkbox"
                checked={isAnonymous}
                onChange={(e) => setIsAnonymous(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <label htmlFor="isAnonymous" className="ml-2 block text-sm text-gray-700">
                Feedback anonyme
              </label>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div>
              <label className="block text-sm font-medium text-gray-700">Catégorie</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                required
              >
                <option value="">Sélectionner</option>
                {categories.map((c) => (
                  <option key={String(c.id)} value={String(c.id)}>{c.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Priorité</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                required
              >
                <option value="">Sélectionner</option>
                {priorities.map((p) => (
                  <option key={String(p.id)} value={String(p.id)}>{p.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Canal</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={channel}
                onChange={(e) => setChannel(e.target.value)}
                required
              >
                <option value="">Sélectionner</option>
                {channels.map((ch) => (
                  <option key={String(ch.id)} value={String(ch.id)}>{ch.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">External ID</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={externalId} onChange={(e) => setExternalId(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Nom du plaignant</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={submitterName} onChange={(e) => setSubmitterName(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Téléphone</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={submitterPhone} onChange={(e) => setSubmitterPhone(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input type="email" className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={submitterEmail} onChange={(e) => setSubmitterEmail(e.target.value)} />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Localisation</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={submitterLocation} onChange={(e) => setSubmitterLocation(e.target.value)} />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">Latitude</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={latitude} onChange={(e) => setLatitude(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Longitude</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={longitude} onChange={(e) => setLongitude(e.target.value)} />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">Tags (séparés par des virgules)</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" value={tags} onChange={(e) => setTags(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Méta-données (JSON)</label>
              <input className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" placeholder='{"key":"value"}' value={metadata} onChange={(e) => setMetadata(e.target.value)} />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Pièces jointes</label>
            <input
              type="file"
              multiple
              onChange={onFileChange}
              className="mt-1 block w-full text-sm text-gray-700 file:mr-4 file:rounded-md file:border-0 file:bg-indigo-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-indigo-700"
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? 'Création…' : 'Créer'}
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  )
}
