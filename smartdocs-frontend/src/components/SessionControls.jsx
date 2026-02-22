import { createSession } from "../api/session";

export default function SessionControls({ messages, onSaved }) {
  const user = localStorage.getItem("user");

  if (!user) return null;

  const handleSave = async () => {
    if (!messages || messages.length === 0) {
      alert("Nothing to save yet. Start a chat first!");
      return;
    }

    try {
      // Logic assumes createSession sends a POST to your backend
      await createSession(user, messages);
      alert("✅ Session archived successfully");
      if (onSaved) onSaved();
    } catch (err) {
      alert("❌ Failed to save session. Check backend connection.");
      console.error(err);
    }
  };

  return (
    <div className="flex items-center gap-4">
      {/* Helper Text - Hidden on small screens to save space */}
      <span className="hidden md:flex items-center gap-2 text-[10px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-widest">
        <i className="fas fa-info-circle" />
        Manual Save Required
      </span>

      {/* Modern Save Button */}
      <button 
        onClick={handleSave}
        className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all
          bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 shadow-sm
          dark:bg-blue-600/10 dark:text-blue-400 dark:border-blue-500/20 dark:hover:bg-blue-600/20"
      >
        <i className="fas fa-save" />
        Save Session
      </button>
    </div>
  );
}
