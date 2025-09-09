import DashboardLayout from '@/components/DashboardLayout'

export default function ContactPage() {
  return (
    <DashboardLayout>
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold text-gray-900">Contact</h1>
        <p className="text-gray-600">Pour toute question, contactez-nous à contact@cfrm.org.</p>
      </div>
    </DashboardLayout>
  )
}
