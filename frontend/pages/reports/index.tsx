import DashboardLayout from '@/components/DashboardLayout'
import Link from 'next/link'

export default function ReportsPage() {
  return (
    <DashboardLayout>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Rapports</h1>
        <Link href="/reports/new" className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700">Nouveau rapport</Link>
      </div>
      <div className="mt-6 text-gray-600">Liste des rapports à venir…</div>
    </DashboardLayout>
  )
}
