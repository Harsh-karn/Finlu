import { Sidebar } from '@/components/shared/Sidebar'
import { Header } from '@/components/shared/Header'
import { DeviceRegistrar } from '@/components/DeviceRegistrar'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-[#0f0f0f] text-gray-100 font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <DeviceRegistrar />
          {children}
        </main>
      </div>
    </div>
  )
}
