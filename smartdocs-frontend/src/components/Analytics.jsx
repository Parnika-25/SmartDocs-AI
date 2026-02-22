import { useEffect, useState } from "react";
import axios from "axios";
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function Analytics() {
  const [data, setData] = useState(null);
  const user = localStorage.getItem("user");

  useEffect(() => {
    axios.get(`https://pdf-ai-app-bm00.onrender.com/analytics-data?user=${user}`)
      .then(res => setData(res.data));
  }, [user]);

  if (!data) return <div className="p-10 text-slate-500 animate-pulse font-bold">LOADING METRICS...</div>;

  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      <header>
        <h1 className="text-3xl font-black text-white uppercase tracking-tighter">System Insights</h1>
        <p className="text-slate-400 text-sm mt-1">Real-time performance metrics for {user}</p>
      </header>

      {/* 3 Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {data.stats.map((s, idx) => (
          <div key={idx} className="bg-[#0f172a] border border-slate-800 p-8 rounded-[2.5rem] hover:border-blue-500/40 transition-all group shadow-xl">
            {/* The Icon Container */}
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 bg-slate-900 border border-slate-800 group-hover:bg-blue-500/10 transition-colors`}>
              {/* Force 'fas' prefix for Font Awesome 6 support */}
              <i className={`fas ${s.icon} ${s.color} text-2xl`} />
            </div>
            
            <div className="text-4xl font-black text-white tracking-tight">{s.value}</div>
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-[0.2em] mt-2">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Chart Section */}
      <div className="bg-[#0f172a] border border-slate-800 p-10 rounded-[3rem]">
        <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-10">Activity Trend (Last 7 Days)</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data.trend}>
              <defs>
                <linearGradient id="colorQueries" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
              <XAxis 
                dataKey="day" 
                axisLine={false} 
                tickLine={false} 
                tick={{fill: '#64748b', fontSize: 12, fontWeight: 'bold'}} 
              />
              <Tooltip 
                contentStyle={{backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '16px', fontWeight: 'bold'}}
                itemStyle={{color: '#3b82f6'}}
              />
              <Area 
                type="monotone" 
                dataKey="queries" 
                stroke="#3b82f6" 
                strokeWidth={4} 
                fillOpacity={1} 
                fill="url(#colorQueries)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
