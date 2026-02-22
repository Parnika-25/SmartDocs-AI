import { useEffect, useState } from "react";
import axios from "axios";

export default function Sidebar({ darkMode, setDarkMode, onWipe }) {
  const [isOpen, setIsOpen] = useState(true); // State to handle visibility
  const [health, setHealth] = useState({
    vector_db: "Checking...",
    openai: "Checking..."
  });

  // -------------------------------------------------
  // Real-time Health Monitoring
  // -------------------------------------------------
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await axios.get("https://pdf-ai-app-bm00.onrender.com/health");
        setHealth(res.data.components);
      } catch (err) {
        setHealth({ vector_db: "Offline", openai: "Disconnected" });
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      {/* 1. FLOATING TOGGLE BUTTON (Visible when sidebar is hidden) */}
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="fixed top-6 left-6 z-50 w-10 h-10 bg-blue-600 text-white rounded-xl shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
        >
          <i className="fas fa-bars" />
        </button>
      )}

      {/* 2. SIDEBAR COMPONENT */}
      <aside className={`fixed lg:relative h-screen p-6 flex flex-col border-r transition-all duration-500 z-40
        bg-white border-slate-200 
        dark:bg-[#0a0f18] dark:border-slate-800
        ${isOpen ? 'w-80 translate-x-0 opacity-100' : 'w-0 -translate-x-full opacity-0 overflow-hidden p-0 border-none'}`}>
        
        {/* BRANDING SECTION & COLLAPSE TRIGGER */}
        <div className="mb-10 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <i className="fas fa-file-shield text-white text-xl" />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">SmartDocs AI</h2>
              <p className="text-[10px] text-slate-500 uppercase font-bold tracking-[0.2em]">Enterprise Edition</p>
            </div>
          </div>
          
          {/* Collapse Button inside the Sidebar */}
          <button 
            onClick={() => setIsOpen(false)}
            className="text-slate-400 hover:text-blue-500 transition-colors p-2"
          >
            <i className="fas fa-chevron-left" />
          </button>
        </div>

        <div className="space-y-8 flex-1">
          {/* CONTROL CENTER */}
          <section>
            <h3 className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <i className="fas fa-sliders-h text-blue-500" /> Control Center
            </h3>
            
            <div className="space-y-3">
              <div 
                onClick={() => setDarkMode(!darkMode)}
                className="p-4 rounded-2xl flex justify-between items-center cursor-pointer border group transition-all
                  bg-slate-50 border-slate-100 hover:border-blue-400
                  dark:bg-[#111827] dark:border-slate-800/50 dark:hover:border-slate-700"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
                    darkMode ? 'bg-blue-500/10 text-blue-400' : 'bg-orange-500/10 text-orange-500'
                  }`}>
                    <i className={`fas ${darkMode ? 'fa-moon' : 'fa-sun'}`} />
                  </div>
                  <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {darkMode ? 'Dark Mode' : 'Light Mode'}
                  </span>
                </div>
                <div className={`w-10 h-5 rounded-full relative transition-all duration-300 ${darkMode ? 'bg-blue-600' : 'bg-slate-300'}`}>
                  <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all duration-300 ${darkMode ? 'right-1' : 'left-1'}`} />
                </div>
              </div>

              <button
                onClick={onWipe}
                className="w-full p-4 rounded-2xl text-xs font-bold uppercase tracking-widest transition-all flex items-center justify-center gap-3
                  bg-red-50 text-red-600 border border-red-100 hover:bg-red-100
                  dark:bg-red-500/5 dark:border-red-500/20 dark:text-red-500 dark:hover:bg-red-500/10"
              >
                <i className="fas fa-trash-alt" /> Wipe Session
              </button>
            </div>
          </section>

          {/* SYSTEM DIAGNOSTICS */}
          <section>
            <h3 className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <i className="fas fa-microchip text-blue-500" /> System Diagnostics
            </h3>
            <div className="p-5 rounded-2xl space-y-5 border bg-slate-50 border-slate-100 dark:bg-[#111827] dark:border-slate-800/50">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 text-slate-500 dark:text-slate-400">
                  <i className="fas fa-database text-xs" />
                  <span className="text-[11px] font-medium">Vector Database</span>
                </div>
                <span className={`text-[9px] px-2 py-0.5 rounded-md font-black uppercase tracking-tighter transition-all ${
                  health.vector_db === "Online" ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
                }`}>
                  {health.vector_db}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 text-slate-500 dark:text-slate-400">
                  <i className="fas fa-brain text-xs" />
                  <span className="text-[11px] font-medium">LLM Provider</span>
                </div>
                <span className={`text-[9px] px-2 py-0.5 rounded-md font-black uppercase tracking-tighter transition-all ${
                  health.openai === "Connected" ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
                }`}>
                  {health.openai}
                </span>
              </div>
            </div>
          </section>
        </div>

        {/* FOOTER */}
        <div className="pt-6 border-t border-slate-100 dark:border-slate-800 mt-auto">
          <div className="flex flex-col items-center gap-1">
            <p className="text-[9px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-[0.3em]">SmartDocs AI Enterprise</p>
            <p className="text-[8px] text-slate-400 dark:text-slate-700">&copy; 2026 · V1.0.4-STABLE</p>
          </div>
        </div>
      </aside>
    </>
  );
}
