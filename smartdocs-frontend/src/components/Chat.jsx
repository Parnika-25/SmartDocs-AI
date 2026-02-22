import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../api/api";

export default function Chat({ messages, setMessages }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const suggestions = [
    { label: "Summarize Documents", icon: "fa-list-ul", prompt: "Can you provide a high-level summary of the uploaded documents?" },
    { label: "Extract Action Items", icon: "fa-tasks", prompt: "What are the key action items or next steps mentioned?" },
    { label: "Find Key Dates", icon: "fa-calendar-alt", prompt: "List all important dates and deadlines found in the files." },
    { label: "Technical Specs", icon: "fa-microchip", prompt: "Summarize the technical specifications or requirements." }
  ];

  const ask = async (customPrompt) => {
    const textToSearch = customPrompt || query;
    if (!textToSearch.trim() || loading) return;

    // 🔥 Use 'content' to stay consistent with backend
    const userMsg = { role: "user", content: textToSearch };
    setMessages((prev) => [...prev, userMsg]);
    setQuery("");
    setLoading(true);

    try {
      const res = await askQuestion(textToSearch);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.data.answer,
          citations: res.data.citations || [],
        },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
      <div className="flex-1 overflow-y-auto space-y-6 pr-4 custom-scrollbar">
        
        {/* ✨ EMPTY STATE */}
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center py-10 animate-in fade-in zoom-in duration-1000">
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-3xl animate-pulse" />
              <div className="relative w-24 h-24 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-blue-500/50 border border-white/10 group transition-transform duration-500 hover:scale-110">
                <i className="fas fa-robot text-4xl text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]" />
              </div>
            </div>

            <h2 className="text-2xl font-bold tracking-tight text-slate-800 dark:text-white text-center">
              SmartDocs AI Ready
            </h2>
            <p className="text-slate-500 dark:text-slate-400 text-sm mt-2 max-w-xs text-center leading-relaxed mb-10">
              I've indexed your knowledge base. Select a suggestion below or type your own question.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl px-4">
              {suggestions.map((s) => (
                <button
                  key={s.label}
                  onClick={() => ask(s.prompt)}
                  className="flex items-center gap-4 p-4 rounded-2xl border transition-all text-left group bg-white border-slate-200 hover:border-blue-400 hover:shadow-md dark:bg-[#111827] dark:border-slate-800"
                >
                  <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-600/10 flex items-center justify-center text-blue-500 group-hover:scale-110 transition">
                    <i className={`fas ${s.icon}`} />
                  </div>
                  <span className="text-xs font-bold text-slate-600 dark:text-slate-300 uppercase tracking-widest leading-tight">
                    {s.label}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* MESSAGES RENDERING */}
        {messages.map((m, i) => {
          // 🔥 Fix: Fallback to .text if .content is missing (and vice-versa)
          const messageContent = m.content || m.text || "";

          return (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"} animate-in slide-in-from-bottom-2`}>
              <div className={`max-w-[85%] p-4 rounded-2xl shadow-sm ${
                m.role === "user" 
                ? "bg-blue-600 text-white rounded-tr-none shadow-blue-500/20" 
                : "bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-none"
              }`}>
                {/* 🔥 Use the standardized content variable */}
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{messageContent}</p>
                
                {m.citations?.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/50 flex flex-wrap gap-2">
                    {m.citations.map((c, j) => (
                      <button
                        key={j}
                        onClick={() => window.dispatchEvent(new CustomEvent("open-pdf", {
                          detail: { file: c.source_file, page: c.page_number }
                        }))}
                        className="flex items-center gap-2 text-[10px] font-bold uppercase bg-slate-50 dark:bg-slate-800/50 hover:bg-slate-100 px-3 py-1.5 rounded-lg text-blue-600 border border-slate-200 dark:border-slate-700 transition-all"
                      >
                        <i className="fas fa-file-pdf" />
                        {c.source_file} <span className="opacity-30">|</span> P.{c.page_number}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 p-4 rounded-2xl rounded-tl-none">
              <div className="flex gap-1.5">
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:-.3s]" />
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:-.15s]" />
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" />
              </div>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      <div className="mt-6 relative">
        <input
          className="w-full py-4 pl-6 pr-16 text-sm rounded-2xl border transition-all shadow-sm bg-white border-slate-200 text-slate-800 focus:border-blue-500 focus:outline-none dark:bg-[#111827] dark:border-slate-800 dark:text-slate-200"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask()}
        />
        <button 
          onClick={() => ask()}
          disabled={loading || !query.trim()}
          className="absolute right-3 top-2.5 w-11 h-11 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-xl flex items-center justify-center text-white transition-all shadow-lg active:scale-95"
        >
          {loading ? <i className="fas fa-circle-notch fa-spin" /> : <i className="fas fa-paper-plane" />}
        </button>
      </div>
    </div>
  );
}
