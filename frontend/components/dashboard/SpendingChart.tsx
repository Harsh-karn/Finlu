"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

const data = [
  { name: "Jan", income: 50000, expense: 35000 },
  { name: "Feb", income: 52000, expense: 32000 },
  { name: "Mar", income: 50000, expense: 41000 },
  { name: "Apr", income: 55000, expense: 33000 },
  { name: "May", income: 50000, expense: 48000 },
  { name: "Jun", income: 60000, expense: 38000 },
]

export function SpendingChart() {
  return (
    <Card className="bg-[#1e1e2e] border-[#2a2a4e] text-white col-span-4 lg:col-span-3">
      <CardHeader>
        <CardTitle>Cash Flow Overview</CardTitle>
      </CardHeader>
      <CardContent className="pl-2">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₹${value}`} />
            <Tooltip 
              cursor={{fill: '#2a2a4e'}} 
              contentStyle={{backgroundColor: '#1a1a2e', border: '1px solid #2a2a4e', borderRadius: '8px'}}
            />
            <Bar dataKey="income" fill="#22c55e" radius={[4, 4, 0, 0]} />
            <Bar dataKey="expense" fill="#ef4444" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
