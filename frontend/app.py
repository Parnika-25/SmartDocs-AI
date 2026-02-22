import streamlit as st
import os
import time
import base64
import json
import shutil
import pandas as pd
from datetime import datetime

# Performance & Backend Logic
from backend.batch_processor import BatchProcessor
from backend.search_engine import SearchEngine
from backend.qa_engine import QAEngine
from backend.vector_db import VectorDatabase
from backend.ingestion_pipeline import DocumentIngestion
from backend.session_manager import SessionManager

# Task 15: Error Handling & Validation
from utils.error_handler import (
    validate_pdf, validate_query, ValidationError, 
    EmbeddingError, DatabaseError, APIError, logger
)

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="SmartDocs AI | Enterprise Edition",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================
# PERSISTENCE & USER AUTH LOGIC
# =================================================
USER_DB_PATH = "users_db.json"
sm = SessionManager()

def load_users():
    if not os.path.exists(USER_DB_PATH):
        default_db = {"admin": "admin"}
        with open(USER_DB_PATH, "w") as f: json.dump(default_db, f)
        return default_db
    with open(USER_DB_PATH, "r") as f: return json.load(f)

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(USER_DB_PATH, "w") as f: json.dump(users, f)

# =================================================
# TASK 15: SYSTEM HEALTH LOGIC
# =================================================
def check_system_health():
    """Health check endpoint verifying DB, API, and Disk space."""
    health = {}
    try:
        db_check = VectorDatabase()
        db_check.get_collection_stats()
        health["Vector Database"] = "✅ Online"
    except (DatabaseError, Exception):
        health["Vector Database"] = "❌ Offline"

    total, used, free = shutil.disk_usage("/")
    health["Disk Space"] = f"💾 {free // (2**30)}GB Free"
    
    if os.getenv("OPENAI_API_KEY"):
        health["API Connectivity"] = "🌐 Connected"
    else:
        health["API Connectivity"] = "⚠️ Key Missing"
    return health

# =================================================
# SESSION STATE INITIALIZATION
# =================================================
if "auth_status" not in st.session_state: st.session_state.auth_status = "landing"
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "bookmarks" not in st.session_state: st.session_state.bookmarks = []
if "query_cache" not in st.session_state: st.session_state.query_cache = []
if "response_times" not in st.session_state: st.session_state.response_times = []
if "selected_pdf" not in st.session_state: st.session_state.selected_pdf = None
if "selected_page" not in st.session_state: st.session_state.selected_page = 1
if "interaction_count" not in st.session_state: st.session_state.interaction_count = 0

# =================================================
# THEME ENGINE
# =================================================
def apply_theme():
    is_dark = st.session_state.get("dark_mode", True)
    bg, text, card, border, accent = ("#0f172a", "#f1f5f9", "#1e293b", "#334155", "#0ea5e9") if is_dark else ("#fcfcfc", "#1e293b", "#ffffff", "#cbd5e1", "#0284c7")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg}; color: {text}; }}
        .stMarkdown p, .stMarkdown li, label {{ color: {text} !important; }}
        section[data-testid="stSidebar"] {{ background-color: {card}; border-right: 1px solid {border}; }}
        section[data-testid="stSidebar"] * {{ color: {text} !important; }}

        div[data-testid="stMetric"] {{
            background: {card}; border: 1px solid {border};
            padding: 25px !important; border-radius: 15px;
            position: relative;
        }}
        div[data-testid="stMetric"]::before {{
            font-size: 1.2rem; position: absolute; top: 15px; left: 15px;
            background: rgba(14, 165, 233, 0.1); padding: 5px 10px; border-radius: 8px;
        }}
        div[data-testid="stMetric"]:nth-of-type(1)::before {{ content: "📊"; }} 
        div[data-testid="stMetric"]:nth-of-type(2)::before {{ content: "📚"; }}
        div[data-testid="stMetric"]:nth-of-type(3)::before {{ content: "💬"; }}
        div[data-testid="stMetric"]:nth-of-type(4)::before {{ content: "⏱️"; }}

        .stButton > button {{
            background: linear-gradient(135deg, {accent}, #0284c7);
            color: white !important; border: none; border-radius: 8px;
            font-weight: 600; width: 100%; transition: 0.3s;
        }}
        [data-testid="stMetricValue"] {{ color: {accent} !important; font-weight: 800 !important; }}
    </style>
    """, unsafe_allow_html=True)

# =================================================
# MAIN DASHBOARD
# =================================================
def show_main_dashboard():
    # Auto-save logic
    if st.session_state.interaction_count > 0 and st.session_state.interaction_count % 5 == 0:
        sm.save_session_state(st.session_state.logged_in_user, {
            "chat_history": st.session_state.chat_history,
            "bookmarks": st.session_state.bookmarks
        })

    with st.sidebar:
        st.markdown(f"### Hello, {st.session_state.logged_in_user}!")
        st.toggle("Dark Mode", key="dark_mode", value=True)
        apply_theme()
        
        st.subheader("⚙️ Session Controls")
        col_s1, col_s2 = st.columns(2)
        if col_s1.button("💾 Save"):
            sm.save_session_state(st.session_state.logged_in_user, {
                "chat_history": st.session_state.chat_history, 
                "bookmarks": st.session_state.bookmarks
            })
            st.toast("Session Saved")
        
        if col_s2.button("🗑️ Wipe"): 
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("---")
        st.subheader("🛠️ System Health")
        with st.expander("Diagnostics", expanded=False):
            health = check_system_health()
            for k, v in health.items(): st.write(f"**{k}:** {v}")

        st.markdown("---")
        st.subheader("📄 Document Inspector")
        if st.session_state.selected_pdf:
            path = os.path.join("uploads", st.session_state.selected_pdf)
            if os.path.exists(path):
                # Lazy loading
                encoded = base64.b64encode(open(path, "rb").read()).decode()
                st.markdown(f'<iframe src="data:application/pdf;base64,{encoded}#page={st.session_state.selected_page}" width="100%" height="450"></iframe>', unsafe_allow_html=True)

        if st.button("🚪 Logout"): 
            st.session_state.auth_status = "landing"
            st.rerun()

    # Metrics
    st.markdown("## ✨ Dashboard")
    db = VectorDatabase()
    stats = db.get_collection_stats()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Indexed Chunks", stats.get("total_documents", 0))
    m2.metric("Library Size", len(os.listdir("uploads")) if os.path.exists("uploads") else 0)
    m3.metric("Queries", len(st.session_state.chat_history))
    m4.metric("Avg Latency", f"{sum(st.session_state.response_times)/len(st.session_state.response_times) if st.session_state.response_times else 0:.2f}s")

    tab1, tab2, tab3 = st.tabs(["📤 Ingestion", "💬 Chat", "🕒 History Log"])

    with tab1:
        st.subheader("Knowledge Acquisition")
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🚀 Process Knowledge"):
            os.makedirs("uploads", exist_ok=True)
            valid_paths = []
            for f in files:
                try: 
                    validate_pdf(f)
                    p = os.path.join("uploads", f.name)
                    with open(p, "wb") as out: out.write(f.getbuffer())
                    valid_paths.append(p)
                except ValidationError as e: st.error(str(e))
            if valid_paths:
                prog = st.progress(0); BatchProcessor(max_workers=3).process_files_parallel(valid_paths, lambda v: prog.progress(v))
                st.success("Indexing Complete.")

    with tab2:
        engine, qa = SearchEngine(), QAEngine()
        for i, chat in enumerate(st.session_state.chat_history):
            st.chat_message("user").write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
                
                # Citations
                if chat.get("citations"):
                    cols = st.columns(len(chat["citations"]) + 1)
                    for j, cite in enumerate(chat["citations"]):
                        if cols[j].button(f"📄 Pg {cite['page_number']}", key=f"c_{i}_{j}"):
                            st.session_state.selected_pdf, st.session_state.selected_page = cite["source_file"], cite["page_number"]; st.rerun()
                
                # Bookmarks
                if st.button("🔖 Bookmark", key=f"bk_{i}"):
                    if chat not in st.session_state.bookmarks: st.session_state.bookmarks.append(chat); st.toast("Saved!")

                # RESTORED: Document Relevance
                if chat.get("relevance_df") is not None:
                    with st.expander("📊 Document Relevance Analytics"):
                        st.bar_chart(chat["relevance_df"].set_index("Document"), color="#0ea5e9")

        query = st.chat_input("Ask a question about your documents...")
        if query:
            try:
                validate_query(query)
                start_t = time.time()
                st.session_state.interaction_count += 1
                
                cached = next((c for c in st.session_state.query_cache if c["q"] == query), None)
                if cached: result = cached["r"]
                else:
                    try: chunks = engine.search_similar_chunks(query, k=8)
                    except (EmbeddingError, DatabaseError): chunks = engine.keyword_search(query, k=8)
                    result = qa.generate_answer(query, chunks, st.session_state.chat_history)
                    st.session_state.query_cache.append({"q": query, "r": result})

                # Relevance Calculation
                all_files = os.listdir("uploads") if os.listdir("uploads") else []
                relevance = {doc: 0.0 for doc in all_files}
                for c in chunks:
                    if c["source_file"] in relevance: relevance[c["source_file"]] = max(relevance[c["source_file"]], c.get("relevance_score", 0))
                df = pd.DataFrame(list(relevance.items()), columns=["Document", "Relevance Score"])
                if not df.empty and df["Relevance Score"].max() > 0: df["Relevance Score"] /= df["Relevance Score"].max()

                st.session_state.response_times.append(time.time() - start_t)
                st.session_state.chat_history.append({"question": query, "answer": result["answer"], "citations": result.get("citations", []), "relevance_df": df, "timestamp": datetime.now().strftime("%H:%M:%S")})
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")

    with tab3:
        st.subheader("🕒 History & Export")
        if st.session_state.chat_history:
            st.download_button("📥 Export History (JSON)", json.dumps(st.session_state.chat_history, default=str, indent=2), "history.json", use_container_width=True)
            for h in reversed(st.session_state.chat_history):
                with st.expander(f"🕒 {h['timestamp']} | {h['question'][:50]}..."):
                    st.write(f"**Q:** {h['question']}\n**A:** {h['answer']}")
                    if h.get("relevance_df") is not None: st.bar_chart(h["relevance_df"].set_index("Document"), color="#0ea5e9")

# --- Routing ---
def show_landing_page():
    apply_theme()
    st.markdown("<div style='text-align: center; padding: 100px 0;'><h1>✨ SmartDocs AI</h1><p>Enterprise Intelligence.</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2); b1 = c1.button("🔐 Login"); b2 = c2.button("📝 Register")
    if b1: st.session_state.auth_status = "login"; st.rerun()
    if b2: st.session_state.auth_status = "register"; st.rerun()

def show_login_page():
    apply_theme(); users = load_users()
    st.markdown("<h2 style='text-align: center;'>🔐 Login</h2>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        user = st.text_input("Username"); pw = st.text_input("Password", type="password")
        if st.button("Sign In"):
            if user in users and users[user] == pw:
                st.session_state.auth_status = "authenticated"; st.session_state.logged_in_user = user
                loaded = sm.load_session_state(user)
                if loaded: st.session_state.chat_history = loaded.get("chat_history", [])
                st.rerun()
            else: st.error("Invalid credentials.")
        if st.button("Back"): st.session_state.auth_status = "landing"; st.rerun()

def show_register_page():
    apply_theme(); users = load_users()
    st.markdown("<h2 style='text-align: center;'>📝 Register</h2>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        new_u = st.text_input("Username"); new_p = st.text_input("Password", type="password"); conf = st.text_input("Confirm", type="password")
        if st.button("Create Account"):
            if new_p == conf and new_u not in users and new_u:
                save_user(new_u, new_p); st.success("Account created!"); st.session_state.auth_status = "login"; st.rerun()
            else: st.error("Failed.")
        if st.button("Back"): st.session_state.auth_status = "landing"; st.rerun()

if st.session_state.auth_status == "landing": show_landing_page()
elif st.session_state.auth_status == "login": show_login_page()
elif st.session_state.auth_status == "register": show_register_page()
else: show_main_dashboard()