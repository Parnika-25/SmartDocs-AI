export default function Metrics() {
  const items = [
    { icon: "fa-database", label: "Indexed Chunks", value: 479 },
    { icon: "fa-folder", label: "Library Size", value: 3 },
    { icon: "fa-comments", label: "Total Queries", value: 47 },
    { icon: "fa-clock", label: "Avg Latency", value: "—" },
  ];

  return (
    <div className="grid grid-cols-4 gap-6">
      {items.map((m) => (
        <div key={m.label} className="card">
          <i className={`fas ${m.icon} text-accent mb-3`} />
          <div className="text-3xl font-bold">{m.value}</div>
          <div className="text-sm text-slate-400">{m.label}</div>
        </div>
      ))}
    </div>
  );
}