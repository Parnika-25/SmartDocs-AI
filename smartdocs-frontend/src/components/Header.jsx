import { useEffect, useRef, useState } from "react";

export default function Header({ onLogout, onOpenProfile }) {
  const user = localStorage.getItem("user");
  const [open, setOpen] = useState(false);
  const [profilePic, setProfilePic] = useState(
    localStorage.getItem("profile_pic")
  );

  const dropdownRef = useRef(null);

  // 🔁 Listen for profile picture changes (from Profile page)
  useEffect(() => {
    const syncProfilePic = () => {
      setProfilePic(localStorage.getItem("profile_pic"));
    };

    window.addEventListener("profile-pic-updated", syncProfilePic);
    return () =>
      window.removeEventListener("profile-pic-updated", syncProfilePic);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="px-8 py-4 flex items-center justify-between bg-[#0a0f18]/30 backdrop-blur-md border-b border-slate-800">
      
      {/* Left */}
      <span className="text-sm font-medium text-slate-300">
        Welcome, {user}
      </span>

      {/* Right */}
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setOpen(!open)}
          className="w-9 h-9 rounded-full overflow-hidden
                     flex items-center justify-center
                     bg-gradient-to-tr from-blue-600 to-cyan-400
                     hover:scale-105 transition"
        >
          {profilePic ? (
            <img
              src={`https://pdf-ai-app-bm00.onrender.com${profilePic}`}
              alt="profile"
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-xs font-bold text-white uppercase">
              {user ? user.substring(0, 2) : "AI"}
            </span>
          )}
        </button>

        {open && (
          <div
            className="absolute right-0 mt-3 w-48 bg-[#0f172a]
                       border border-slate-700 rounded-xl shadow-xl overflow-hidden
                       animate-in fade-in slide-in-from-top-2 duration-200"
          >
            <button
              onClick={() => {
                onOpenProfile();
                setOpen(false);
              }}
              className="w-full px-4 py-3 text-sm text-slate-300
                         hover:bg-white/5 transition flex items-center gap-3"
            >
              <i className="fas fa-user-cog text-slate-400" />
              Profile / Settings
            </button>

            <div className="h-px bg-slate-700" />

            <button
              onClick={onLogout}
              className="w-full px-4 py-3 text-sm text-red-400
                         hover:bg-red-500/10 transition flex items-center gap-3"
            >
              <i className="fas fa-sign-out-alt" />
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
