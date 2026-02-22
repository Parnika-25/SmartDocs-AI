import { useEffect, useState } from "react";
import axios from "axios";

export default function Profile({ user, onUpdate }) {
  const [username, setUsername] = useState(user);
  const [password, setPassword] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(
    localStorage.getItem("profile_pic")
      ? `https://pdf-ai-app-bm00.onrender.com${localStorage.getItem("profile_pic")}`
      : null
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setUsername(user);
  }, [user]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const uploadProfilePic = async (currentUser) => {
    if (!image) return;
    const formData = new FormData();
    formData.append("file", image);

    const res = await axios.post(
      `https://pdf-ai-app-bm00.onrender.com/upload-profile-pic?user=${currentUser}`,
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    localStorage.setItem("profile_pic", res.data.profile_pic);
    window.dispatchEvent(new Event("profile-pic-updated"));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post("https://pdf-ai-app-bm00.onrender.com/update-profile", {
        current_username: user,
        new_username: username !== user ? username : null,
        new_password: password || null
      });

      const updatedUser = res.data.username;
      await uploadProfilePic(updatedUser);
      localStorage.setItem("user", updatedUser);
      onUpdate(updatedUser);

      alert("Profile updated successfully");
      setPassword("");
    } catch (err) {
      alert(err.response?.data?.detail || "Profile update failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-[2.5rem] p-10 shadow-xl">
        
        <header className="mb-10 text-center md:text-left">
          <h2 className="text-2xl font-black text-slate-900 dark:text-white uppercase tracking-tight">
            Account Settings
          </h2>
          <p className="text-slate-500 text-sm mt-1">
            Manage your profile and security
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-8">

          {/* Profile Picture Section */}
          <div className="flex flex-col md:flex-row items-center gap-6 pb-6 border-b border-slate-100 dark:border-slate-800/50">
            <div className="relative group">
              <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-blue-500/20 p-1 bg-white dark:bg-slate-900">
                {preview ? (
                  <img src={preview} alt="Profile" className="w-full h-full rounded-full object-cover" />
                ) : (
                  <div className="w-full h-full rounded-full flex items-center justify-center bg-gradient-to-tr from-blue-600 to-cyan-400 text-white font-bold text-xl uppercase">
                    {user.substring(0, 2)}
                  </div>
                )}
              </div>
              <label className="absolute bottom-0 right-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center cursor-pointer text-white shadow-lg hover:bg-blue-500 transition-colors border-2 border-white dark:border-slate-900">
                <i className="fas fa-camera text-[10px]" />
                <input type="file" accept="image/*" className="hidden" onChange={handleImageChange} />
              </label>
            </div>
            <div className="text-center md:text-left">
              <h4 className="text-sm font-bold text-slate-900 dark:text-white">Profile Photo</h4>
              <p className="text-xs text-slate-500 mt-1">JPG or PNG. Max size 2MB</p>
            </div>
          </div>

          {/* Username and Password - SIDE BY SIDE */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">
                Username
              </label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#030712] border border-slate-200 dark:border-slate-800 rounded-2xl py-4 px-6 text-sm mt-1.5 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/5 outline-none transition"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">
                New Password
              </label>
              <input
                type="password"
                placeholder="Keep empty to stay same"
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-50 dark:bg-[#030712] border border-slate-200 dark:border-slate-800 rounded-2xl py-4 px-6 text-sm mt-1.5 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/5 outline-none transition"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="w-full md:w-auto bg-blue-600 hover:bg-blue-500 text-white px-10 py-4 rounded-2xl font-bold text-sm shadow-lg shadow-blue-500/20 transition-all active:scale-95 disabled:opacity-60 flex items-center justify-center"
            >
              {loading ? (
                <i className="fas fa-circle-notch fa-spin mr-3" />
              ) : (
                <i className="fas fa-save mr-3" />
              )}
              Save Profile Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
