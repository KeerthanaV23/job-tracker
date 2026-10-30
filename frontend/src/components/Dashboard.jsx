import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../api/client";

const COLORS = { wishlist: "#94a3b8", applied: "#3b82f6", interview: "#f59e0b", offer: "#10b981", rejected: "#f43f5e" };

const Stat = ({ label, value }) => (
  <div className="card">
    <p className="text-sm text-slate-500">{label}</p>
    <p className="mt-1 text-3xl font-semibold">{value}</p>
  </div>
);

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => { api.get("/analytics/summary/").then((r) => setData(r.data)); }, []);
  if (!data) return <p className="text-slate-500">Loading...</p>;

  const pie = Object.entries(data.by_status).filter(([, n]) => n > 0).map(([name, value]) => ({ name, value }));
  const weekly = data.weekly.map((w) => ({ week: w.week.slice(5), count: w.count }));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Total applications" value={data.total} />
        <Stat label="Interviews reached" value={data.funnel.interview} />
        <Stat label="Interview rate" value={`${data.funnel.interview_rate}%`} />
        <Stat label="Offers" value={data.funnel.offer} />
      </div>
      {data.total === 0 ? (
        <div className="card text-center text-slate-500">Add your first application to see charts here.</div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card">
            <h2 className="mb-3 font-medium">Applications per week</h2>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={weekly}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week" /><YAxis allowDecimals={false} /><Tooltip />
                <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="card">
            <h2 className="mb-3 font-medium">By status</h2>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={pie} dataKey="value" nameKey="name" outerRadius={90} label>
                  {pie.map((p) => <Cell key={p.name} fill={COLORS[p.name]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
