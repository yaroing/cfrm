import React from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import DashboardLayout from '@/components/DashboardLayout';
import TicketDetail from '../../components/TicketDetail';

const TicketDetailPage: React.FC = () => {
  const router = useRouter();

  return (
    <>
      <Head>
        <title>Détail du ticket - CFRM</title>
        <meta name="description" content="Détail et gestion du ticket de feedback" />
      </Head>
      <DashboardLayout>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Détail du ticket</h1>
            <button
              onClick={() => router.push('/tickets')}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <TicketDetail />
        </div>
      </DashboardLayout>
    </>
  );
};

export default TicketDetailPage;

