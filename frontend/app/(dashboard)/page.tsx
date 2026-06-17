"use client";

import { useEffect, useState } from "react";
import { StatsCards } from "@/components/dashboard/StatsCards"
import { SpendingChart } from "@/components/dashboard/SpendingChart"
import api from "@/lib/api"

export default function DashboardPage() {
  const [stats, setStats] = useState({
    income: 0,
    expense: 0,
    savings: 0,
    savingsRate: 0.0
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const res = await api.get(`/analytics/summary?date=${yyyy}-${mm}`);
        if (res.data) {
          setStats({
            income: res.data.total_income || 0,
            expense: res.data.total_expense || 0,
            savings: res.data.net_savings || 0,
            savingsRate: res.data.savings_rate || 0.0
          });
        }
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-white">Dashboard</h2>
        <p className="text-gray-400 mt-1">Live from your Android Device.</p>
      </div>
      
      {loading ? (
         <div className="text-gray-500 animate-pulse text-lg py-4">Syncing live financial data...</div>
      ) : (
         <StatsCards {...stats} />
      )}
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <SpendingChart />
        <div className="col-span-4 lg:col-span-1 space-y-4">
            <div className="bg-[#1e1e2e] border border-[#2a2a4e] rounded-xl p-6 h-full flex flex-col justify-start text-gray-500">
                <h3 className="text-xl font-semibold text-white mb-4">Live SMS Activity</h3>
                <p className="text-sm">Waiting for incoming SMS transactions. Spend something to see this update!</p>
            </div>
        </div>
      </div>
    </div>
  )
}
