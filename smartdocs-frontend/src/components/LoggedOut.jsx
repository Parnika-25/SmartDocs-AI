import { Link } from "react-router-dom";

export default function LoggedOut() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#030712] p-6 text-center">
      {/* Decorative Blur */}
      <div className="absolute inset-0 bg-blue-600/5 blur-[120px] rounded-full" />

      <div className="relative max-w-sm w-full bg-[#0F172A] border border-slate-800 p-10 rounded-[2.5rem] shadow-2xl animate-in fade-in zoom-in duration-500">
        <div className="flex flex-col items-center">
          {/* Success Icon */}
          <div className="w-20 h-20 rounded-full bg-green-500/10 border border-green-500/20 flex items-center justify-center mb-6 shadow-lg shadow-green-500/5">
            <i className="fas fa-sign-out-alt text-3xl text-green-500" />
          </div>

          <h1 className="text-2xl font-black text-white tracking-tighter uppercase mb-2">
            Logged <span className="text-blue-500">Out</span>
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed mb-8">
            You have been safely signed out of your SmartDocs AI session.
          </p>

          <Link 
            to="/login"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-2xl shadow-lg shadow-blue-600/20 transition-all active:scale-95"
          >
            Sign Back In
          </Link>
        </div>
      </div>
    </div>
  );
}