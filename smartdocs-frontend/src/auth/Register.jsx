import { useState } from "react";
import axios from "axios";

export default function Register({ onRegisterSuccess }) {
  const [formData, setFormData] = useState({ username: "", password: "", confirmPassword: "" });
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) return alert("Passwords mismatch");
    
    setLoading(true);
    try {
      await axios.post("https://pdf-ai-app-bm00.onrender.com/register", {
        username: formData.username,
        password: formData.password
      });
      // Automatically log them in after registration
      onRegisterSuccess(formData.username);
    } catch (err) {
      alert(err.response?.data?.detail || "Registration failed. Username may exist.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-center">
      <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-500/20">
        <i className="fas fa-user-plus text-blue-500 text-xl" />
      </div>
      <h1 className="text-xl font-black text-slate-900 dark:text-white uppercase mb-6 tracking-tight">Create Account</h1>
      
      <form onSubmit={handleRegister} className="space-y-4 text-left">
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Choose Username</label>
          <input required className="w-full bg-slate-50 dark:bg-[#1f2937] border border-slate-200 dark:border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-900 dark:text-white mt-1" placeholder="Username" onChange={(e) => setFormData({...formData, username: e.target.value})} />
        </div>
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Password</label>
          <input required type="password" className="w-full bg-slate-50 dark:bg-[#1f2937] border border-slate-200 dark:border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-900 dark:text-white mt-1" placeholder="Password" onChange={(e) => setFormData({...formData, password: e.target.value})} />
        </div>
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Verify Password</label>
          <input required type="password" className="w-full bg-slate-50 dark:bg-[#1f2937] border border-slate-200 dark:border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-900 dark:text-white mt-1" placeholder="Repeat Password" onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})} />
        </div>
        <button 
          type="submit" 
          disabled={loading} 
          className="w-full bg-blue-600 hover:bg-blue-500 text-white py-3.5 rounded-xl font-bold shadow-lg transition-all active:scale-95 mt-2"
        >
          {loading ? "Creating Account..." : "Register Now"}
        </button>
      </form>
    </div>
  );
}
