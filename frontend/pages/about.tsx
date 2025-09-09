import DashboardLayout from '@/components/DashboardLayout'

export default function AboutPage() {
  return (
    <DashboardLayout>
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold text-gray-900">À propos</h1>
        <p className="text-gray-600">Informations sur la plateforme CFRM.</p>
      </div>
    </DashboardLayout>
  )
}
