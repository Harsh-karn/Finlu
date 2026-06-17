import { StatsCards } from "@/components/dashboard/StatsCards"
import { SpendingChart } from "@/components/dashboard/SpendingChart"

export default function DashboardPage() {
  // Mock data for initial render
  const stats = {
    income: 85000,
    expense: 42500,
    savings: 42500,
    savingsRate: 50.0
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-white">Dashboard</h2>
        <p className="text-gray-400 mt-1">Welcome back. Here's what's happening with your finances.</p>
      </div>
      
      <StatsCards {...stats} />
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <SpendingChart />
        {/* Placeholder for Donut chart and Recent txs */}
        <div className="col-span-4 lg:col-span-1 space-y-4">
            <div className="bg-[#1e1e2e] border border-[#2a2a4e] rounded-xl p-6 h-full flex items-center justify-center text-gray-500">
                Category Donut Chart (WIP)
            </div>
        </div>
      </div>
    </div>
  )
}
