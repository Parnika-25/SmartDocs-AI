import { useState } from "react";
import axios from "axios";

export default function Login({ onLoginSuccess }) {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post("https://pdf-ai-app-bm00.onrender.com/login", formData);
      // Notify parent immediately to swap views
      onLoginSuccess(res.data.username);
    } catch (err) {
      alert(err.response?.data?.detail || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-center">
      <img src="/logo.svg" className="w-16 h-16 mx-auto mb-4" alt="SmartDocs Logo" />
      <h1 className="text-xl font-black text-slate-900 dark:text-white uppercase mb-6 tracking-tight">SmartDocs AI</h1>
      
      <form onSubmit={handleLogin} className="space-y-4 text-left">
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Username</label>
          <input 
            required 
            className="w-full bg-slate-50 dark:bg-[#1f2937] border border-slate-200 dark:border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition mt-1" 
            placeholder="Enter username" 
            onChange={(e) => setFormData({...formData, username: e.target.value})} 
          />
        </div>
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Password</label>
          <input 
            required 
            type="password" 
            className="w-full bg-slate-50 dark:bg-[#1f2937] border border-slate-200 dark:border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition mt-1" 
            placeholder="••••••••" 
            onChange={(e) => setFormData({...formData, password: e.target.value})} 
          />
        </div>
        <button 
          type="submit" 
          disabled={loading} 
          className="w-full bg-blue-600 hover:bg-blue-500 text-white py-3.5 rounded-xl font-bold shadow-lg shadow-blue-500/20 transition-all active:scale-95 mt-2 disabled:opacity-50"
        >
          {loading ? <i className="fas fa-circle-notch fa-spin" /> : "Sign In"}
        </button>
      </form>
    </div>
  );
}
