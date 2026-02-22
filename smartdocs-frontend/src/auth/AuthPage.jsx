import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

export default function AuthPage({ onAuthSuccess }) {
  const [isRegister, setIsRegister] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#030712] text-slate-200">
      
      {/* Glass Container */}
      <div
        className={`relative w-[900px] max-w-full min-h-[520px]
        bg-[#0a0f18]/70 backdrop-blur-xl
        border border-slate-800 rounded-[32px]
        shadow-[0_0_80px_rgba(59,130,246,0.12)]
        overflow-hidden transition-all duration-700`}
      >
        {/* LEFT: SIGN IN */}
        <div
          className={`absolute inset-y-0 left-0 w-1/2 p-10 flex items-center justify-center
          transition-all duration-700
          ${isRegister ? "translate-x-full opacity-0" : "opacity-100 z-20"}`}
        >
          <Login onLoginSuccess={onAuthSuccess} />
        </div>

        {/* RIGHT: SIGN UP */}
        <div
          className={`absolute inset-y-0 left-0 w-1/2 p-10 flex items-center justify-center
          transition-all duration-700
          ${isRegister ? "translate-x-full opacity-100 z-20" : "opacity-0 z-10"}`}
        >
          <Register onRegisterSuccess={onAuthSuccess} />
        </div>

        {/* TOGGLE PANEL */}
        <div
          className={`absolute inset-y-0 right-0 w-1/2
          bg-gradient-to-br from-[#0b1220] to-[#050914]
          border-l border-slate-800
          transition-all duration-700
          ${isRegister ? "-translate-x-full" : ""}`}
        >
          <div className="h-full flex flex-col items-center justify-center px-12 text-center">
            
            {!isRegister ? (
              <>
                <h1 className="text-2xl font-black tracking-tight text-white">
                  SmartDocs AI
                </h1>
                <p className="text-xs uppercase tracking-widest text-blue-400 mt-1">
                  Enterprise Edition
                </p>

                <p className="text-slate-400 text-sm mt-6 leading-relaxed">
                  New here? Create a secure private knowledge workspace and unlock
                  enterprise-grade document intelligence.
                </p>

                <button
                  onClick={() => setIsRegister(true)}
                  className="mt-8 px-8 py-3 rounded-xl
                  border border-blue-500/40
                  text-blue-400 font-bold text-sm uppercase tracking-widest
                  hover:bg-blue-500/10 transition"
                >
                  Create Account
                </button>
              </>
            ) : (
              <>
                <h1 className="text-2xl font-black tracking-tight text-white">
                  Welcome Back
                </h1>

                <p className="text-slate-400 text-sm mt-6 leading-relaxed">
                  Sign in to access your private documents, analytics,
                  and secure AI workspace.
                </p>

                <button
                  onClick={() => setIsRegister(false)}
                  className="mt-8 px-8 py-3 rounded-xl
                  border border-slate-600
                  text-slate-300 font-bold text-sm uppercase tracking-widest
                  hover:bg-white/5 transition"
                >
                  Sign In
                </button>
              </>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}
