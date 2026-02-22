import { useState, useEffect } from "react";
import axios from "axios";
import { uploadPDFs, ingestDocs } from "../api/api";

export default function Upload() {
  const [library, setLibrary] = useState([]);
  const [backendStats, setBackendStats] = useState({ total_chunks: 0, library_size: 0 });
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);
  const [ingesting, setIngesting] = useState(false);

  // Retrieve current user for isolated requests
  const user = localStorage.getItem("user");

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  const fetchData = async () => {
    try {
      // Send user as query param to only get THEIR files
      const res = await axios.get(`https://pdf-ai-app-bm00.onrender.com/list-uploads?user=${user}`);
      setLibrary(res.data.files || []);
      setBackendStats(res.data.stats || { total_chunks: 0, library_size: 0 });
    } catch (err) {
      console.error("Connection error while fetching library", err);
    }
  };

  const dashboardStats = [
    { label: "Indexed Chunks", value: backendStats.total_chunks, icon: "fa-database", color: "text-blue-500" },
    { label: "Library Size", value: library.length, icon: "fa-book", color: "text-cyan-500" },
    { label: "User Access", value: user || "Guest", icon: "fa-user-shield", color: "text-sky-500" },
    { label: "Storage", value: "Private", icon: "fa-lock", color: "text-indigo-500" },
  ];

  const handleUpload = async () => {
    if (files.length === 0) return setStatus("⚠️ Select PDFs first.");
    setUploading(true);
    setStatus("⏳ Uploading to your secure vault...");
    try {
      // Ensure your api.js function is updated to accept 'user' or use axios directly here:
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));
      
      await axios.post(`https://pdf-ai-app-bm00.onrender.com/upload?user=${user}`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      setStatus("✅ Upload successful.");
      setFiles([]);
      fetchData();
    } catch (err) {
      setStatus("❌ Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleIngest = async () => {
    setIngesting(true);
    setStatus("🚀 Training AI on your private data...");
    try {
      // Pass user to ingestion so the vector DB handles isolation
      await axios.post(`https://pdf-ai-app-bm00.onrender.com/ingest?user=${user}`);
      setStatus("✨ Ingestion complete!");
      fetchData();
    } catch (err) {
      setStatus("❌ Ingestion failed.");
    } finally {
      setIngesting(false);
    }
  };

  return (
    <div className="space-y-10 animate-in fade-in duration-700">
      
      {/* ✨ DASHBOARD METRICS */}
      <section>
        <div className="flex items-center gap-3 mb-6">
          <span className="text-2xl animate-pulse">✨</span>
          <h2 className="text-xl font-bold tracking-tight text-slate-800 dark:text-white">Workspace Overview</h2>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {dashboardStats.map((s) => (
            <div key={s.label} className="p-6 rounded-2xl border transition-all shadow-sm bg-white border-slate-200 dark:bg-[#111827] dark:border-slate-800 group hover:border-blue-500/30">
              <div className="flex justify-between items-start mb-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center border transition-transform group-hover:scale-110 
                  bg-slate-50 border-slate-100 dark:bg-slate-900 dark:border-slate-800 ${s.color}`}>
                  <i className={`fas ${s.icon}`} />
                </div>
              </div>
              <div className="text-3xl font-bold tracking-tighter text-slate-900 dark:text-white mb-1">{s.value}</div>
              <div className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em]">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* WORKSPACE PANELS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* KNOWLEDGE ACQUISITION */}
        <div className="p-8 rounded-3xl border shadow-xl bg-white border-slate-200 dark:bg-[#111827] dark:border-slate-800 flex flex-col">
          <div className="flex items-center gap-3 mb-8">
            <i className="fas fa-cloud-arrow-up text-blue-500" />
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Private Knowledge Base</h3>
          </div>
          
          <div className="flex-1 border-2 border-dashed rounded-2xl p-14 flex flex-col items-center justify-center transition-all group cursor-pointer relative mb-6
            bg-slate-50 border-slate-200 hover:border-blue-400
            dark:bg-[#0a0f18]/40 dark:border-slate-800 dark:hover:border-blue-500/30">
            <input type="file" multiple accept=".pdf" className="absolute inset-0 opacity-0 cursor-pointer z-10" onChange={(e) => setFiles([...e.target.files])} />
            <div className="w-20 h-20 rounded-full flex items-center justify-center mb-4 transition-all bg-white dark:bg-slate-900 shadow-sm group-hover:shadow-md">
              <i className="fas fa-file-pdf text-3xl text-slate-300 dark:text-slate-700 group-hover:text-blue-500" />
            </div>
            <p className="font-medium text-slate-600 dark:text-slate-300 text-center">Drag & drop PDFs to your vault</p>
            <p className="text-[10px] mt-2 uppercase font-bold tracking-widest text-slate-400 dark:text-slate-600 text-center">Restricted to your account</p>
            
            {files.length > 0 && (
              <div className="mt-4 px-4 py-1.5 bg-blue-600 text-white text-[10px] font-bold rounded-full shadow-lg animate-bounce">
                {files.length} FILE(S) READY
              </div>
            )}
          </div>

          <div className="flex gap-3 mt-auto">
            <button onClick={handleUpload} disabled={uploading || ingesting} className="flex-1 py-4 rounded-xl font-bold transition-all disabled:opacity-50 flex items-center justify-center gap-2
              bg-slate-100 text-slate-700 hover:bg-slate-200
              dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700">
              <i className={`fas ${uploading ? 'fa-spinner fa-spin' : 'fa-upload'}`} />
              Upload
            </button>
            <button onClick={handleIngest} disabled={uploading || ingesting} className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-blue-600/20 disabled:opacity-50 flex items-center justify-center gap-2">
              <i className={`fas ${ingesting ? 'fa-circle-notch fa-spin' : 'fa-bolt'}`} />
              Process
            </button>
          </div>
          {status && <div className="mt-6 text-center text-[10px] font-bold text-blue-500 dark:text-blue-400 uppercase tracking-widest animate-pulse">{status}</div>}
        </div>

        {/* DOCUMENT LIBRARY */}
        <div className="p-8 rounded-3xl border shadow-xl bg-white border-slate-200 dark:bg-[#111827] dark:border-slate-800 flex flex-col">
          <div className="flex items-center gap-3 mb-6">
            <i className="fas fa-folder-tree text-blue-500" />
            <h3 className="text-lg font-semibold text-slate-800 dark:text-white">Secure Library</h3>
          </div>
          
          <div className="flex-1 space-y-3 max-h-[450px] overflow-y-auto custom-scrollbar pr-2">
            {library.length === 0 ? (
              <div className="py-20 text-center text-slate-300 dark:text-slate-700">
                <i className="fas fa-box-open text-4xl mb-4" />
                <p className="text-sm font-medium">No private files found</p>
              </div>
            ) : (
              library.map((doc, i) => (
                <div key={i} className="flex items-center justify-between p-4 border rounded-2xl transition-all group
                  bg-slate-50 border-slate-100 hover:border-blue-200
                  dark:bg-[#0a0f18]/60 dark:border-slate-800 dark:hover:border-blue-500/40">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center transition-colors bg-white border border-slate-200 text-slate-400 dark:bg-slate-900 dark:border-slate-800 dark:text-blue-400 group-hover:text-blue-500">
                      <i className="fas fa-file-pdf" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate max-w-[150px]">{doc.name}</p>
                      <p className="text-[10px] font-bold uppercase tracking-tighter text-slate-400 dark:text-slate-500">
                        {doc.size} <span className="mx-1 opacity-30">|</span> User Owned
                      </p>
                    </div>
                  </div>
                  <div className="w-6 h-6 rounded-full flex items-center justify-center bg-green-500/10 text-green-500">
                    <i className="fas fa-check text-[8px]" />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


