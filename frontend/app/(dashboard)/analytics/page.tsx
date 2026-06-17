import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { SpendingChart } from "@/components/dashboard/SpendingChart"

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-white">Analytics</h2>
        <p className="text-gray-400 mt-1">Deep dive into your spending habits.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <SpendingChart />
        
        <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white col-span-4 lg:col-span-1">
          <CardHeader>
            <CardTitle>Top Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <span className="text-sm">Food</span>
                    <span className="font-bold">₹15,000</span>
                </div>
                <div className="flex justify-between items-center">
                    <span className="text-sm">Transport</span>
                    <span className="font-bold">₹8,000</span>
                </div>
                <div className="flex justify-between items-center">
                    <span className="text-sm">Utilities</span>
                    <span className="font-bold">₹5,000</span>
                </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
