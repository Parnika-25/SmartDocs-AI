import { useEffect, useState, useRef } from "react";
import { listSessions, loadSession } from "../api/session";
import { exportSessionToPDF } from "../utils/exportPdf";

export default function History({ onLoad }) {
  const user = localStorage.getItem("user");
  const [sessions, setSessions] = useState([]);
  const [search, setSearch] = useState("");
  const [activeSession, setActiveSession] = useState(null);
  const [isExporting, setIsExporting] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (user) fetchSessions();
  }, [user]);

  useEffect(() => {
    if (activeSession) {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [activeSession]);

  const fetchSessions = async () => {
    try {
      const res = await listSessions(user);
      setSessions(res.data.sessions || res.data || []);
    } catch (err) {
      console.error("Failed to fetch sessions", err);
      setSessions([]);
    }
  };

  const selectSession = async (sessionId) => {
    try {
      const res = await loadSession(user, sessionId);
      setActiveSession(res.data);
    } catch (err) {
      console.error("Load Error:", err);
    }
  };

  const handleExport = async (sessionId) => {
    try {
      setIsExporting(true);
      const res = await loadSession(user, sessionId);
      if (res.data?.history) {
        exportSessionToPDF(res.data);
      }
    } catch (err) {
      console.error("Export Error:", err);
    } finally {
      setIsExporting(false);
    }
  };

  const filtered = sessions.filter((s) =>
    (s.title || "").toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex h-[calc(100vh-180px)] gap-6 animate-in fade-in duration-500">
      
      {/* --- LEFT SIDEBAR: Session List --- */}
      <div className="w-1/3 flex flex-col border-r border-slate-200 dark:border-slate-800 pr-4">
        <div className="relative mb-4">
          <i className="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs" />
          <input
            className="w-full py-2.5 pl-9 pr-4 text-xs rounded-xl border bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 focus:outline-none focus:border-blue-500 transition-all"
            placeholder="Search questions..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="flex-1 overflow-y-auto space-y-2 custom-scrollbar">
          {filtered.length === 0 ? (
            <div className="text-center py-10 opacity-50">
               <i className="fas fa-history text-2xl mb-2" />
               <p className="text-[10px] font-bold uppercase">No history found</p>
            </div>
          ) : (
            filtered.map((s) => (
              <div
                key={s.session_id}
                onClick={() => selectSession(s.session_id)}
                className={`p-4 rounded-2xl cursor-pointer transition-all border ${
                  activeSession?.session_id === s.session_id
                    ? "bg-blue-600/10 border-blue-500/40"
                    : "border-transparent hover:bg-slate-100 dark:hover:bg-slate-800/50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${activeSession?.session_id === s.session_id ? 'bg-blue-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'}`}>
                    <i className="fas fa-comment-dots text-xs" />
                  </div>
                  <div className="overflow-hidden">
                    <p className="text-sm font-bold truncate text-slate-700 dark:text-slate-200">
                      {s.title || "Untitled Conversation"}
                    </p>
                    <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">
                      {new Date(s.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* --- RIGHT PANEL: Elaborated View --- */}
      <div className="flex-1 flex flex-col bg-white dark:bg-[#0b1120] rounded-3xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-2xl">
        {activeSession ? (
          <>
            <div className="p-5 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center bg-slate-50/50 dark:bg-slate-900/50">
              <div className="flex flex-col">
                <h3 className="font-bold text-slate-800 dark:text-white text-base truncate">
                  {activeSession.title}
                </h3>
                <span className="text-[10px] text-blue-500 font-bold uppercase tracking-widest">Active Insight Mode</span>
              </div>
              <div className="flex gap-2">
                <button 
                  onClick={() => onLoad(activeSession.history)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/20 flex items-center gap-2"
                >
                  <i className="fas fa-reply-all" /> Continue Chat
                </button>
                <button 
                  onClick={() => handleExport(activeSession.session_id)}
                  disabled={isExporting}
                  className="p-2 text-slate-500 hover:text-blue-500 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all"
                >
                  <i className={`fas ${isExporting ? 'fa-spinner fa-spin' : 'fa-file-pdf'}`} />
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar">
              {activeSession.history.map((chat, idx) => {
                const isUser = chat.role === "user";
                return (
                  <div key={idx} className="flex gap-4 items-start animate-in fade-in slide-in-from-bottom-2 duration-500">
                    {/* Icon */}
                    <div className={`w-10 h-10 rounded-2xl flex-shrink-0 flex items-center justify-center border ${
                      isUser 
                        ? "bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700" 
                        : "bg-gradient-to-br from-blue-600 to-indigo-700 shadow-xl shadow-blue-500/20"
                    }`}>
                      <i className={`fas ${isUser ? "fa-user text-slate-500" : "fa-robot text-white"}`} />
                    </div>

                    {/* Content */}
                    <div className="flex-1 space-y-2">
                      <p className={`text-[11px] font-black uppercase ${isUser ? "text-slate-400" : "text-blue-500"}`}>
                        {isUser ? "User Query" : "SmartDocs AI Response"}
                      </p>
                      
                      <div className={`text-sm leading-relaxed whitespace-pre-wrap font-medium ${
                        isUser 
                          ? "text-slate-800 dark:text-slate-100 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl border border-slate-100 dark:border-slate-800"
                          : "text-slate-600 dark:text-slate-300"
                      }`}>
                        {chat.content}
                      </div>

                      {/* Citations (Only AI) */}
                      {!isUser && chat.citations && chat.citations.length > 0 && (
                        <div className="flex flex-wrap gap-2 pt-2">
                          {chat.citations.map((c, i) => (
                            <div key={i} className="flex items-center gap-2 text-[10px] bg-blue-500/10 text-blue-600 dark:text-blue-400 px-3 py-1.5 rounded-full border border-blue-500/20">
                              <i className="fas fa-quote-left text-[8px]" />
                              <span>{c.source_file} • Page {c.page_number}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
              <div ref={chatEndRef} />
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-10 opacity-40">
            <div className="w-24 h-24 bg-slate-100 dark:bg-slate-900 rounded-3xl flex items-center justify-center mb-6">
              <i className="fas fa-comment-dots text-4xl text-slate-400" />
            </div>
            <h3 className="text-sm font-black uppercase tracking-widest text-slate-500">History Explorer</h3>
            <p className="text-xs font-medium mt-2">Select a session on the left to elaborate the full context.</p>
          </div>
        )}
      </div>
    </div>
  );
}
