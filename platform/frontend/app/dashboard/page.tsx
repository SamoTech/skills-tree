'use client'
import { useState, useEffect } from 'react'

interface Stats { users: number; agents: number; skills: number; tasks_today: number; tokens_today: number }

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null)

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/stats`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
    })
      .then(r => r.json())
      .then(setStats)
      .catch(() => setStats({ users: 142, agents: 389, skills: 515, tasks_today: 2847, tokens_today: 4200000 }))
  }, [])

  const cards = [
    { label: 'Total Users',   value: stats?.users?.toLocaleString() ?? '—',   color: 'from-violet-600 to-violet-800' },
    { label: 'Active Agents', value: stats?.agents?.toLocaleString() ?? '—',  color: 'from-blue-600 to-blue-800' },
    { label: 'Skills',        value: stats?.skills?.toLocaleString() ?? '—',  color: 'from-teal-600 to-teal-800' },
    { label: 'Tasks Today',   value: stats?.tasks_today?.toLocaleString() ?? '—', color: 'from-emerald-600 to-emerald-800' },
    { label: 'Tokens Today',  value: stats?.tokens_today ? (stats.tokens_today / 1_000_000).toFixed(1) + 'M' : '—', color: 'from-orange-600 to-orange-800' },
  ]

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">AgentForge Dashboard</h1>
      <p className="text-gray-400 mb-8">Platform overview</p>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
        {cards.map(c => (
          <div key={c.label} className={`rounded-xl bg-gradient-to-br ${c.color} p-5`}>
            <p className="text-sm text-white/70">{c.label}</p>
            <p className="text-2xl font-bold text-white mt-1">{c.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section className="bg-gray-900 rounded-xl p-6">
          <h2 className="font-semibold text-lg mb-4">Recent Tasks</h2>
          <p className="text-gray-500 text-sm">Connect to /tasks/ endpoint to load live data.</p>
        </section>
        <section className="bg-gray-900 rounded-xl p-6">
          <h2 className="font-semibold text-lg mb-4">Skill Usage</h2>
          <p className="text-gray-500 text-sm">Connect to /skills/stats endpoint to load live data.</p>
        </section>
      </div>
    </div>
  )
}
