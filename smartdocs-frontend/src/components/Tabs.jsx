import React from 'react';

export default function Tabs({ activeTab, setActiveTab, isSidebarOpen }) {
  const tabs = [
    { id: "ingestion", icon: "fa-upload", label: "Ingestion" },
    { id: "chat", icon: "fa-comment-dots", label: "Chat" },
    { id: "history", icon: "fa-history", label: "History" },
    { id: "analytics", icon: "fa-chart-pie", label: "Analytics" },
    { id: "profile", icon: "fa-user-circle", label: "Profile" }
  ];

  return (
    /* FIXED: Changed inline-flex to flex and added w-full when sidebar is closed */
    <div className={`flex bg-slate-100 dark:bg-[#111827] p-1 rounded-xl transition-all duration-500 ease-in-out ${
      !isSidebarOpen ? "w-full mx-4 shadow-xl border border-blue-500/20" : "w-auto"
    }`}>
      {tabs.map((t) => (
        <button
          key={t.id}
          onClick={() => setActiveTab(t.id)}
          /* FIXED: Added flex-1 and justify-center to ensure labels/icons take up equal space */
          className={`rounded-lg font-bold uppercase tracking-widest transition-all duration-300 flex items-center justify-center gap-3
            ${activeTab === t.id ? "bg-blue-600 text-white shadow-lg" : "text-slate-500 hover:text-blue-500 hover:bg-blue-500/5"}
            ${!isSidebarOpen ? "flex-1 py-4 text-[12px]" : "px-5 py-2 text-[10px]"}`}
        >
          <i className={`fas ${t.icon} ${!isSidebarOpen ? "text-sm" : "text-xs"}`} />
          <span className={!isSidebarOpen ? "inline" : "hidden lg:inline"}>{t.label}</span>
        </button>
      ))}
    </div>
  );
}
