import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowDownRight, ArrowUpRight, PiggyBank, Target } from "lucide-react"

interface StatsCardsProps {
  income: number;
  expense: number;
  savings: number;
  savingsRate: number;
}

export function StatsCards({ income, expense, savings, savingsRate }: StatsCardsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-gray-400">Total Income</CardTitle>
          <ArrowDownRight className="h-4 w-4 text-emerald-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">₹{income.toLocaleString()}</div>
          <p className="text-xs text-gray-500 mt-1">+2% from last month</p>
        </CardContent>
      </Card>
      
      <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-gray-400">Total Expense</CardTitle>
          <ArrowUpRight className="h-4 w-4 text-red-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">₹{expense.toLocaleString()}</div>
          <p className="text-xs text-gray-500 mt-1">-5% from last month</p>
        </CardContent>
      </Card>
      
      <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-gray-400">Net Savings</CardTitle>
          <PiggyBank className="h-4 w-4 text-indigo-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">₹{savings.toLocaleString()}</div>
          <p className="text-xs text-gray-500 mt-1">+12% from last month</p>
        </CardContent>
      </Card>
      
      <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-gray-400">Savings Rate</CardTitle>
          <Target className="h-4 w-4 text-indigo-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{savingsRate.toFixed(1)}%</div>
          <p className="text-xs text-gray-500 mt-1">Target: 20%</p>
        </CardContent>
      </Card>
    </div>
  )
}
