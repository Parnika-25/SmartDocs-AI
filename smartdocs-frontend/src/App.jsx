import { useEffect, useState, useRef } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import SessionControls from "./components/SessionControls";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import History from "./components/History";
import Analytics from "./components/Analytics";
import Profile from "./components/Profile";
import PdfViewer from "./components/PdfViewer";
import AuthPage from "./auth/AuthPage";

/* ============================================================
   1. PUBLIC LANDING PAGE (Marketing / Pre-Auth)
   ============================================================ */
function PublicLanding({ onGetStarted }) {
  const [activeSection, setActiveSection] = useState('home');

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setActiveSection(id);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#030712] selection:bg-blue-500/30 overflow-y-auto">
      {/* Top Navigation */}
      <nav className="sticky top-0 z-50 w-full bg-white/80 dark:bg-[#030712]/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <i className="fas fa-brain text-white" />
            </div>
            <span className="font-black text-2xl tracking-tighter dark:text-white">SmartDocs AI</span>
          </div>
          
          <div className="hidden md:flex items-center gap-8">
            {['Features', 'About', 'Contact'].map((item) => (
              <button
                key={item}
                onClick={() => scrollToSection(item.toLowerCase())}
                className="text-xs font-bold uppercase tracking-widest text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                {item}
              </button>
            ))}
          </div>

          <button 
            onClick={onGetStarted}
            className="text-xs font-black uppercase tracking-widest px-6 py-3 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/20"
          >
            Sign In
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="min-h-screen flex flex-col items-center justify-center text-center px-6 py-20">
        <div className="max-w-6xl space-y-10 animate-in fade-in slide-in-from-bottom-12 duration-1000">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/5 rounded-full border border-blue-500/10 backdrop-blur-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            <span className="text-[10px] font-black uppercase tracking-[0.2em] text-blue-600 dark:text-blue-400">Enterprise RAG Intelligence</span>
          </div>

          <h1 className="text-6xl md:text-8xl font-black tracking-tight text-slate-900 dark:text-white leading-[0.95]">
            Your Data. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400">Perfectly Cited.</span>
          </h1>

          <p className="text-xl md:text-2xl text-slate-500 dark:text-slate-400 max-w-3xl mx-auto font-medium leading-relaxed">
            The ultimate document intelligence platform. Ingest technical manuals, legal papers, 
            or research PDFs and chat with an AI that never hallucinates.
          </p>

          <div className="flex flex-col sm:flex-row gap-6 pt-6 justify-center">
            <button 
              onClick={onGetStarted}
              className="px-12 py-6 bg-blue-600 text-white rounded-2xl font-black uppercase tracking-widest hover:bg-blue-700 hover:scale-105 active:scale-95 transition-all shadow-[0_20px_50px_rgba(37,99,235,0.3)]"
            >
              Get Started For Free
            </button>
            <button 
              onClick={() => scrollToSection('features')}
              className="px-12 py-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl font-black uppercase tracking-widest hover:bg-slate-50 dark:hover:bg-slate-800 transition-all dark:text-white"
            >
              Explore Features
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full pt-16 opacity-60">
            {['Neural Search', 'PDF Inspector', 'Multi-User', 'Data Privacy'].map((f, i) => (
              <div key={i} className="flex items-center justify-center gap-2 text-[11px] font-bold uppercase tracking-widest dark:text-slate-400">
                <i className="fas fa-check-circle text-blue-500" /> {f}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 px-6 bg-white dark:bg-[#0a0f18]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black tracking-tight dark:text-white mb-6">
              Powerful <span className="text-blue-600">Features</span>
            </h2>
            <p className="text-xl text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">
              Everything you need to transform documents into intelligent, searchable knowledge bases
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: 'fa-brain', title: 'AI-Powered Search', desc: 'Neural semantic search finds exactly what you need, even with natural language queries', color: 'blue' },
              { icon: 'fa-file-pdf', title: 'PDF Intelligence', desc: 'Advanced PDF parsing with text extraction, table detection, and image analysis', color: 'red' },
              { icon: 'fa-quote-right', title: 'Source Citations', desc: 'Every answer includes precise citations with page numbers and highlighted excerpts', color: 'green' },
              { icon: 'fa-users', title: 'Multi-User Sessions', desc: 'Collaborate with your team with isolated user sessions and shared knowledge bases', color: 'purple' },
              { icon: 'fa-chart-line', title: 'Analytics Dashboard', desc: 'Track usage patterns, popular queries, and system performance metrics', color: 'yellow' },
              { icon: 'fa-shield-alt', title: 'Enterprise Security', desc: 'Your data stays private with local vector storage and encrypted sessions', color: 'indigo' }
            ].map((feature, idx) => (
              <div key={idx} className="p-8 bg-slate-50 dark:bg-[#111827] rounded-[2rem] border border-slate-200 dark:border-slate-800 hover:border-blue-500/50 transition-all group">
                <div className={`w-16 h-16 rounded-2xl bg-${feature.color}-500/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <i className={`fas ${feature.icon} text-3xl text-${feature.color}-500`} />
                </div>
                <h3 className="text-2xl font-black mb-4 dark:text-white">{feature.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-32 px-6 bg-white dark:bg-[#0a0f18]">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-5xl md:text-6xl font-black tracking-tight dark:text-white mb-6">
                About <span className="text-blue-600">SmartDocs AI</span>
              </h2>
              <p className="text-lg text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
                SmartDocs AI was built to solve the problem of information overload in document-heavy industries. 
                Our advanced RAG (Retrieval-Augmented Generation) technology ensures that every answer is grounded 
                in your actual documents, with precise citations.
              </p>
              <p className="text-lg text-slate-600 dark:text-slate-400 leading-relaxed mb-8">
                Whether you're in legal, healthcare, research, or any field dealing with complex documentation, 
                SmartDocs AI transforms how you interact with information.
              </p>
              <div className="grid grid-cols-3 gap-6">
                {[
                  { number: '10K+', label: 'Documents Processed' },
                  { number: '500+', label: 'Active Users' },
                  { number: '99.9%', label: 'Uptime' }
                ].map((stat, idx) => (
                  <div key={idx} className="text-center">
                    <div className="text-3xl font-black text-blue-600 mb-2">{stat.number}</div>
                    <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="aspect-square rounded-[3rem] overflow-hidden border-2 border-blue-500/20 shadow-2xl shadow-blue-500/20 bg-gradient-to-br from-blue-950 via-slate-900 to-indigo-950 flex items-center justify-center">
                <img 
                  src="/network-ai.jpg" 
                  alt="AI Network Visualization" 
                  className="w-full h-full object-cover"
                />
                {/* Fallback icon if image doesn't load */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <i className="fas fa-network-wired text-9xl text-blue-500 opacity-10" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-32 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-black tracking-tight dark:text-white mb-6">
              Get In <span className="text-blue-600">Touch</span>
            </h2>
            <p className="text-xl text-slate-500 dark:text-slate-400">
              Have questions? We'd love to hear from you.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Contact Info */}
            <div className="space-y-8">
              {[
                { icon: 'fa-envelope', title: 'Email', value: 'support@smartdocs.ai', link: 'mailto:support@smartdocs.ai' },
                { icon: 'fa-phone', title: 'Phone', value: '+1 (555) 123-4567', link: 'tel:+15551234567' },
                { icon: 'fa-map-marker-alt', title: 'Address', value: '123 AI Street, Tech Valley, CA 94000', link: null },
                { icon: 'fa-clock', title: 'Business Hours', value: 'Mon-Fri: 9AM - 6PM PST', link: null }
              ].map((contact, idx) => (
                <div key={idx} className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center flex-shrink-0">
                    <i className={`fas ${contact.icon} text-blue-500`} />
                  </div>
                  <div>
                    <h4 className="font-black text-sm uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-1">{contact.title}</h4>
                    {contact.link ? (
                      <a href={contact.link} className="text-lg font-bold dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                        {contact.value}
                      </a>
                    ) : (
                      <p className="text-lg font-bold dark:text-white">{contact.value}</p>
                    )}
                  </div>
                </div>
              ))}

              {/* Social Links */}
              <div className="pt-8">
                <h4 className="font-black text-sm uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-4">Follow Us</h4>
                <div className="flex gap-4">
                  {['fa-twitter', 'fa-linkedin', 'fa-github', 'fa-youtube'].map((social, idx) => (
                    <button key={idx} className="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-blue-600 dark:hover:bg-blue-600 text-slate-600 dark:text-slate-400 hover:text-white transition-all flex items-center justify-center">
                      <i className={`fab ${social}`} />
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <form className="space-y-6">
              <div>
                <input 
                  type="text" 
                  placeholder="Your Name" 
                  className="w-full px-6 py-4 rounded-2xl bg-white dark:bg-[#0a0f18] border border-slate-200 dark:border-slate-800 focus:border-blue-500 focus:outline-none dark:text-white transition-colors"
                />
              </div>
              <div>
                <input 
                  type="email" 
                  placeholder="Your Email" 
                  className="w-full px-6 py-4 rounded-2xl bg-white dark:bg-[#0a0f18] border border-slate-200 dark:border-slate-800 focus:border-blue-500 focus:outline-none dark:text-white transition-colors"
                />
              </div>
              <div>
                <textarea 
                  rows="5" 
                  placeholder="Your Message" 
                  className="w-full px-6 py-4 rounded-2xl bg-white dark:bg-[#0a0f18] border border-slate-200 dark:border-slate-800 focus:border-blue-500 focus:outline-none dark:text-white transition-colors resize-none"
                />
              </div>
              <button 
                type="submit"
                className="w-full py-4 bg-blue-600 text-white rounded-2xl font-black uppercase tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/20"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0a0f18]">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                  <i className="fas fa-brain text-white" />
                </div>
                <span className="font-black text-xl tracking-tighter dark:text-white">SmartDocs AI</span>
              </div>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Transforming documents into intelligent knowledge bases.
              </p>
            </div>
            
            {[
              { title: 'Product', links: ['Features', 'Security', 'Roadmap', 'API'] },
              { title: 'Company', links: ['About', 'Blog', 'Careers', 'Press'] },
              { title: 'Legal', links: ['Privacy', 'Terms', 'Cookies', 'Licenses'] }
            ].map((col, idx) => (
              <div key={idx}>
                <h4 className="font-black text-sm uppercase tracking-widest text-slate-900 dark:text-white mb-4">{col.title}</h4>
                <ul className="space-y-2">
                  {col.links.map((link, i) => (
                    <li key={i}>
                      <button className="text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                        {link}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          
          <div className="pt-8 border-t border-slate-200 dark:border-slate-800 text-center">
            <p className="text-sm text-slate-500 dark:text-slate-400">
              © 2026 SmartDocs AI. All rights reserved. Built with ❤️ for document intelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

/* ============================================================
   2. INTERNAL USER DASHBOARD (Home Page After Login)
   ============================================================ */
function WelcomeDashboard({ username, onStartChat, onUpload, onOpenHistory }) {
  return (
    <div className="h-full flex flex-col items-center justify-center text-center space-y-12 animate-in fade-in zoom-in duration-700">
      <div className="relative group">
        <div className="w-32 h-32 bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-[3rem] flex items-center justify-center shadow-2xl shadow-blue-500/20 group-hover:rotate-6 transition-transform duration-500">
          <i className="fas fa-rocket text-5xl text-white" />
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-4xl md:text-5xl font-black tracking-tight dark:text-white">
          Systems Online, <span className="text-blue-600">{username}</span>
        </h2>
        <p className="text-slate-500 dark:text-slate-400 font-medium text-lg">
          Select a module to begin your document analysis.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
        {[
          { label: "New Ingestion", icon: "fa-upload", desc: "Upload and vectorize PDFs", action: onUpload, color: "text-blue-500" },
          { label: "AI Chat", icon: "fa-comment-dots", desc: "Query your knowledge base", action: onStartChat, color: "text-indigo-500" },
          { label: "Session History", icon: "fa-history", desc: "Access previous insights", action: onOpenHistory, color: "text-slate-500" }
        ].map((card, idx) => (
          <button 
            key={idx}
            onClick={card.action}
            className="p-8 bg-white dark:bg-[#0a0f18] border border-slate-200 dark:border-slate-800 rounded-[2.5rem] hover:border-blue-500/50 transition-all text-left group shadow-sm hover:shadow-xl dark:shadow-none"
          >
            <i className={`fas ${card.icon} text-2xl ${card.color} mb-6 block`} />
            <h3 className="font-black text-xl mb-2 dark:text-white">{card.label}</h3>
            <p className="text-sm text-slate-500 font-medium leading-relaxed">{card.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

/* ============================================================
   3. MAIN APPLICATION ORCHESTRATOR
   ============================================================ */
export default function App() {
  const [user, setUser] = useState(localStorage.getItem("user"));
  const [showAuth, setShowAuth] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [messages, setMessages] = useState([]);
  const [activeTab, setActiveTab] = useState("welcome");
  const [pdf, setPdf] = useState(null);
  const [page, setPage] = useState(1);
  const [showPdf, setShowPdf] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Dark Mode Sync
  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  // Global Event Listener for Citations (Clicking a citation opens the PDF)
  useEffect(() => {
    const handler = (e) => {
      setPdf(e.detail.file);
      setPage(e.detail.page);
      setShowPdf(true);
    };
    window.addEventListener("open-pdf", handler);
    return () => window.removeEventListener("open-pdf", handler);
  }, []);

  const handleAuthSuccess = (username) => {
    localStorage.setItem("user", username);
    setUser(username);
    setShowAuth(false);
    setActiveTab("welcome");
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
    setShowAuth(false);
    setActiveTab("welcome");
    setMessages([]);
  };

  const tabs = [
    { id: "welcome", icon: "fa-home", label: "Dashboard" },
    { id: "ingestion", icon: "fa-upload", label: "Ingestion" },
    { id: "chat", icon: "fa-comment-dots", label: "Chat" },
    { id: "history", icon: "fa-history", label: "History" },
    { id: "analytics", icon: "fa-chart-pie", label: "Analytics" },
    { id: "profile", icon: "fa-user-circle", label: "Profile" }
  ];

  /* --- AUTHENTICATION FLOW RENDERING --- */
  if (!user) {
    return showAuth ? (
      <AuthPage onAuthSuccess={handleAuthSuccess} onBack={() => setShowAuth(false)} />
    ) : (
      <PublicLanding onGetStarted={() => setShowAuth(true)} />
    );
  }

  /* --- APP SHELL RENDERING (POST-AUTH) --- */
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 dark:bg-[#030712] text-slate-900 dark:text-slate-200 font-sans">
      
      {/* Side Navigation */}
      <Sidebar
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onWipe={() => setMessages([])}
      />

      <div className="flex-1 flex flex-col overflow-hidden relative">
        
        {/* Top bar with User Profile/Logout */}
        <Header onLogout={logout} onOpenProfile={() => setActiveTab("profile")} />

        <div className="flex flex-1 overflow-hidden">
          {/* Main Workspace Area */}
          <div className={`flex flex-col transition-all duration-500 ${showPdf ? "w-[55%]" : "w-full"}`}>

            {/* Tab Switched Header */}
            <div className="px-8 py-4 bg-white/50 dark:bg-[#0a0f18]/50 border-b border-slate-200 dark:border-slate-800/50 flex items-center gap-4">
              <div
                className={`flex bg-slate-100 dark:bg-[#111827] p-1 rounded-2xl transition-all duration-500 ${
                  !isSidebarOpen ? "w-full mx-4" : "w-auto"
                }`}
              >
                {tabs.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setActiveTab(t.id)}
                    className={`rounded-xl font-bold uppercase tracking-widest transition-all duration-300 flex items-center justify-center gap-3
                      ${activeTab === t.id ? "bg-blue-600 text-white shadow-lg" : "text-slate-500 hover:text-blue-500"}
                      ${!isSidebarOpen ? "flex-1 py-4 text-[11px]" : "px-6 py-2.5 text-[10px]"}`}
                  >
                    <i className={`fas ${t.icon}`} />
                    <span className={!isSidebarOpen ? "inline" : "hidden xl:inline"}>{t.label}</span>
                  </button>
                ))}
              </div>

              {/* Chat-specific controls */}
              {activeTab === "chat" && (
                <div className="ml-auto">
                  <SessionControls messages={messages} onSaved={() => setActiveTab("history")} />
                </div>
              )}
            </div>

            {/* Component Router */}
            <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
              {activeTab === "welcome" && (
                <WelcomeDashboard 
                  username={user}
                  onStartChat={() => setActiveTab("chat")}
                  onUpload={() => setActiveTab("ingestion")}
                  onOpenHistory={() => setActiveTab("history")}
                />
              )}
              {activeTab === "ingestion" && <Upload />}
              {activeTab === "chat" && <Chat messages={messages} setMessages={setMessages} />}
              {activeTab === "history" && (
                <History onLoad={(m) => { setMessages(m); setActiveTab("chat"); }} />
              )}
              {activeTab === "analytics" && <Analytics />}
              {activeTab === "profile" && (
                <Profile user={user} onUpdate={handleAuthSuccess} />
              )}
            </div>
          </div>

          {/* Contextual PDF Inspector Sidecar */}
          {showPdf && (
            <div className="w-[45%] border-l border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0a0f18] p-6 flex flex-col animate-in slide-in-from-right duration-500">
              <div className="flex justify-between items-center mb-6">
                 <h4 className="text-xs font-black uppercase tracking-[0.2em] text-blue-500">Source Verification</h4>
                 <button
                   onClick={() => setShowPdf(false)}
                   className="text-red-500 text-[10px] font-bold uppercase bg-red-500/10 px-4 py-2 rounded-xl hover:bg-red-500/20 transition-all"
                 >
                   Dismiss
                 </button>
              </div>
              <div className="flex-1 rounded-[2rem] overflow-hidden border border-slate-200 dark:border-slate-800 shadow-2xl">
                <PdfViewer file={pdf} page={page} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
