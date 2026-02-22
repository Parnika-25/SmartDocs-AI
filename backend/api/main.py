# import os
# import json
# import shutil
# from typing import List, Optional
# from datetime import datetime, timedelta
# from collections import Counter

# from fastapi import FastAPI, UploadFile, File, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from passlib.context import CryptContext

# # ================= INTERNAL IMPORTS =================
# from backend.batch_processor import BatchProcessor
# from backend.search_engine import SearchEngine
# from backend.qa_engine import QAEngine
# from backend.vector_db import VectorDatabase
# from backend.session_manager import SessionManager
# from backend.api.schemas import QueryRequest, QueryResponse, HealthResponse
# from backend.api.session import router as session_router
# from utils.error_handler import validate_pdf, validate_query

# # ================= APP SETUP =================
# app = FastAPI(
#     title="SmartDocs AI API",
#     version="1.0",
#     description="Enterprise RAG Backend"
# )

# # ================= DIRECTORIES (CREATE FIRST) =================
# UPLOAD_DIR = "uploads"
# SESSIONS_DIR = "sessions"
# USER_DB_FILE = "users_db.json"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(SESSIONS_DIR, exist_ok=True)

# # ================= STATIC FILES =================
# app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# # ================= CORS (RENDER + LOCAL SAFE) =================
# FRONTEND_URL = os.getenv("FRONTEND_URL")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         FRONTEND_URL,
#         "http://localhost:5173"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ================= ROUTERS =================
# app.include_router(session_router)

# # ================= LOAD USERS =================
# if os.path.exists(USER_DB_FILE):
#     try:
#         with open(USER_DB_FILE, "r") as f:
#             users_db = json.load(f)
#     except json.JSONDecodeError:
#         users_db = {}
# else:
#     users_db = {}

# def save_users():
#     with open(USER_DB_FILE, "w") as f:
#         json.dump(users_db, f, indent=2)

# # ================= ENGINES =================
# search_engine = SearchEngine()
# qa_engine = QAEngine()
# session_manager = SessionManager()

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     bcrypt__ident="2b",
#     deprecated="auto"
# )

# # ================= SCHEMAS =================
# class AuthSchema(BaseModel):
#     username: str
#     password: str

# class ProfileUpdateSchema(BaseModel):
#     current_username: str
#     new_username: Optional[str] = None
#     new_password: Optional[str] = None

# def safe_password(password: str) -> str:
#     return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

# # ================= AUTH ROUTES =================
# @app.post("/register")
# def register(user: AuthSchema):
#     if not user.username or not user.password:
#         raise HTTPException(400, "Username and password required")

#     if user.username in users_db:
#         raise HTTPException(400, "User already exists")

#     users_db[user.username] = pwd_context.hash(safe_password(user.password))
#     save_users()
#     return {"message": "Registration successful", "username": user.username}

# @app.post("/login")
# def login(user: AuthSchema):
#     hashed = users_db.get(user.username)
#     if not hashed or not pwd_context.verify(safe_password(user.password), hashed):
#         raise HTTPException(401, "Invalid username or password")

#     return {"message": "Login successful", "username": user.username}

# # ================= FILE UPLOAD =================
# @app.post("/upload")
# async def upload(
#     files: List[UploadFile] = File(...),
#     user: str = Query(...)
# ):
#     if not user:
#         raise HTTPException(400, "User required")

#     user_dir = os.path.join(UPLOAD_DIR, user)
#     os.makedirs(user_dir, exist_ok=True)

#     uploaded = []
#     for file in files:
#         validate_pdf(file)
#         path = os.path.join(user_dir, file.filename)
#         with open(path, "wb") as f:
#             shutil.copyfileobj(file.file, f)
#         uploaded.append(file.filename)

#     return {"uploaded": uploaded}

# # ================= INGEST =================
# @app.post("/ingest")
# def ingest(user: str = Query(...)):
#     user_upload_dir = os.path.join(UPLOAD_DIR, user)

#     if not os.path.exists(user_upload_dir):
#         raise HTTPException(400, "No PDFs uploaded for this user")

#     pdfs = [
#         os.path.join(user_upload_dir, f)
#         for f in os.listdir(user_upload_dir)
#         if f.lower().endswith(".pdf")
#     ]

#     if not pdfs:
#         raise HTTPException(400, "No PDFs to ingest")

#     BatchProcessor(user=user, max_workers=3).process_files_parallel(pdfs)

#     return {"status": "ingested", "user": user, "files": len(pdfs)}

# # ================= HEALTH =================
# @app.get("/health", response_model=HealthResponse)
# def health():
#     try:
#         VectorDatabase().get_collection_stats()
#         db_status = "Online"
#     except:
#         db_status = "Offline"

#     return {
#         "status": "ok",
#         "components": {
#             "vector_db": db_status,
#             "openai": "Connected" if os.getenv("OPENAI_API_KEY") else "Missing"
#         }
#     }

# # ================= PROFILE UPDATE =================
# @app.post("/update-profile")
# def update_profile(data: ProfileUpdateSchema):
#     if data.current_username not in users_db:
#         raise HTTPException(404, "User not found")

#     current_key = data.current_username

#     if data.new_username and data.new_username != current_key:
#         if data.new_username in users_db:
#             raise HTTPException(400, "Username already taken")
#         users_db[data.new_username] = users_db.pop(current_key)
#         current_key = data.new_username

#     if data.new_password:
#         users_db[current_key] = pwd_context.hash(safe_password(data.new_password))

#     save_users()
#     return {"message": "Profile updated", "username": current_key}

# # ================= LIST UPLOADS =================
# @app.get("/list-uploads")
# async def list_uploads(user: str):
#     user_dir = os.path.join(UPLOAD_DIR, user)

#     if not os.path.exists(user_dir):
#         return {"files": [], "stats": {"library_size": 0, "total_chunks": 0}}

#     files = []
#     for filename in os.listdir(user_dir):
#         if filename.lower().endswith(".pdf"):
#             size_mb = round(os.path.getsize(os.path.join(user_dir, filename)) / (1024 * 1024), 2)
#             files.append({"name": filename, "size": f"{size_mb} MB", "status": "Ready"})

#     return {
#         "files": files,
#         "stats": {"library_size": len(files), "total_chunks": 0}
#     }

# # ================= ANALYTICS =================
# @app.get("/analytics-data")
# async def analytics(user: str):
#     user_path = os.path.join(SESSIONS_DIR, user)
#     total_queries = 0
#     query_dates = []
#     doc_usage = Counter()

#     if os.path.exists(user_path):
#         for file in os.listdir(user_path):
#             if not file.endswith(".json"):
#                 continue
#             with open(os.path.join(user_path, file), encoding="utf-8") as f:
#                 data = json.load(f)
#                 history = data.get("history", [])
#                 user_msgs = [m for m in history if m.get("role") == "user"]
#                 total_queries += len(user_msgs)

#                 date_str = data.get("created_at", "").split("T")[0]
#                 if date_str:
#                     query_dates.extend([date_str] * len(user_msgs))

#                 for m in history:
#                     for c in m.get("citations", []):
#                         doc_usage[c.get("source_file", "Unknown")] += 1

#     days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
#     trend = []
#     for i in range(6, -1, -1):
#         target_date = datetime.now() - timedelta(days=i)
#         key = target_date.strftime("%Y-%m-%d")
#         trend.append({
#             "day": days[int(target_date.strftime("%w"))],
#             "queries": query_dates.count(key)
#         })

#     return {
#         "stats": [
#             {"label": "Total Queries", "value": str(total_queries)},
#             {"label": "Avg/Day", "value": f"{round(total_queries/7, 1)}"},
#             {"label": "Documents", "value": str(len(os.listdir(UPLOAD_DIR)))}
#         ],
#         "trend": trend,
#         "top_docs": [{"name": n[:15], "queries": c} for n, c in doc_usage.most_common(3)]
#     }

# # ================= QUERY =================
# @app.post("/query", response_model=QueryResponse)
# def query(req: QueryRequest):
#     validate_query(req.query)

#     chunks = search_engine.search_similar_chunks(req.query, k=8)
#     result = qa_engine.generate_answer(req.query, chunks)

#     session_id = req.session_id or session_manager.create_session(req.user)

#     session_manager.append_to_session(
#         user=req.user,
#         session_id=session_id,
#         question=req.query,
#         answer=result["answer"],
#         citations=result.get("citations", [])
#     )

#     session = session_manager.load_session_state(req.user, session_id)
#     if session and len(session.get("history", [])) == 1:
#         session_manager.update_title(req.user, session_id, req.query[:60])

#     return {
#         "answer": result["answer"],
#         "citations": result.get("citations", []),
#         "session_id": session_id
#     }
import os
import json
import shutil
from typing import List, Optional
from datetime import datetime, timedelta
from collections import Counter

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.context import CryptContext

# ================= INTERNAL IMPORTS =================
from backend.batch_processor import BatchProcessor
from backend.search_engine import SearchEngine
from backend.qa_engine import QAEngine
from backend.vector_db import VectorDatabase
from backend.session_manager import SessionManager
from backend.api.schemas import QueryRequest, QueryResponse
from backend.api.session import router as session_router
from utils.error_handler import validate_pdf, validate_query

# ================= APP SETUP =================
app = FastAPI(
    title="SmartDocs AI API",
    version="1.0",
    description="Enterprise RAG Backend"
)

# ================= DIRECTORIES =================
UPLOAD_DIR = "uploads"
SESSIONS_DIR = "sessions"
PROFILE_PICS_DIR = "profile_pics"
USER_DB_FILE = "users_db.json"

for d in [UPLOAD_DIR, SESSIONS_DIR, PROFILE_PICS_DIR]:
    os.makedirs(d, exist_ok=True)

# ================= STATIC FILES =================
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/profile_pics", StaticFiles(directory=PROFILE_PICS_DIR), name="profile_pics")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pdf-ai-app-1.onrender.com",
        "http://localhost:5173",
        os.getenv("FRONTEND_URL", "")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= ROUTERS =================
app.include_router(session_router)

# ================= LOAD USERS =================
if os.path.exists(USER_DB_FILE):
    try:
        with open(USER_DB_FILE, "r") as f:
            users_db = json.load(f)
    except json.JSONDecodeError:
        users_db = {}
else:
    users_db = {}

def save_users():
    with open(USER_DB_FILE, "w") as f:
        json.dump(users_db, f, indent=2)

# ================= ENGINES =================
#search_engine = SearchEngine()
qa_engine = QAEngine()
session_manager = SessionManager()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",
    deprecated="auto"
)

# ================= SCHEMAS =================
class AuthSchema(BaseModel):
    username: str
    password: str

class ProfileUpdateSchema(BaseModel):
    current_username: str
    new_username: Optional[str] = None
    new_password: Optional[str] = None

def safe_password(password: str) -> str:
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

# ================= AUTH =================
@app.post("/register")
def register(user: AuthSchema):
    if user.username in users_db:
        raise HTTPException(400, "User already exists")

    users_db[user.username] = {
        "password": pwd_context.hash(safe_password(user.password)),
        "profile_pic": None
    }
    save_users()
    return {"username": user.username}

@app.post("/login")
def login(user: AuthSchema):
    u = users_db.get(user.username)

    # backward compatibility
    if isinstance(u, str):
        if not pwd_context.verify(safe_password(user.password), u):
            raise HTTPException(401, "Invalid credentials")
        users_db[user.username] = {"password": u, "profile_pic": None}
        save_users()

    elif isinstance(u, dict):
        if not pwd_context.verify(safe_password(user.password), u["password"]):
            raise HTTPException(401, "Invalid credentials")
    else:
        raise HTTPException(401, "Invalid credentials")

    return {
        "username": user.username,
        "profile_pic": users_db[user.username]["profile_pic"]
    }

# ================= PROFILE PIC =================
@app.post("/upload-profile-pic")
async def upload_profile_pic(
    user: str = Query(...),
    file: UploadFile = File(...)
):
    if user not in users_db:
        raise HTTPException(404, "User not found")

    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only images allowed")

    ext = file.filename.split(".")[-1]
    filename = f"{user}.{ext}"
    path = os.path.join(PROFILE_PICS_DIR, filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    users_db[user]["profile_pic"] = f"/profile_pics/{filename}"
    save_users()
    return {"profile_pic": users_db[user]["profile_pic"]}

# ================= PROFILE UPDATE =================
@app.post("/update-profile")
def update_profile(data: ProfileUpdateSchema):
    if data.current_username not in users_db:
        raise HTTPException(404, "User not found")

    user = data.current_username

    if data.new_username and data.new_username != user:
        if data.new_username in users_db:
            raise HTTPException(400, "Username already exists")
        users_db[data.new_username] = users_db.pop(user)
        user = data.new_username

    if data.new_password:
        users_db[user]["password"] = pwd_context.hash(safe_password(data.new_password))

    save_users()
    return {"username": user}

# ================= FILE UPLOAD =================
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...), user: str = Query(...)):
    user_dir = os.path.join(UPLOAD_DIR, user)
    os.makedirs(user_dir, exist_ok=True)

    uploaded = []
    for file in files:
        validate_pdf(file)
        path = os.path.join(user_dir, file.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        uploaded.append(file.filename)

    return {"uploaded": uploaded}

# ================= LIST UPLOADS (RESTORED) =================
@app.get("/list-uploads")
def list_uploads(user: str):
    user_dir = os.path.join(UPLOAD_DIR, user)

    if not os.path.exists(user_dir):
        return {
            "files": [],
            "stats": {"library_size": 0, "total_chunks": 0}
        }

    files = []
    for f in os.listdir(user_dir):
        if f.lower().endswith(".pdf"):
            size = round(os.path.getsize(os.path.join(user_dir, f)) / (1024 * 1024), 2)
            files.append({"name": f, "size": f"{size} MB", "status": "Ready"})

    return {
        "files": files,
        "stats": {
            "library_size": len(files),
            "total_chunks": 0
        }
    }

# ================= INGEST =================
@app.post("/ingest")
def ingest(user: str = Query(...)):
    user_dir = os.path.join(UPLOAD_DIR, user)
    if not os.path.exists(user_dir):
        raise HTTPException(400, "No PDFs uploaded")

    pdfs = [os.path.join(user_dir, f) for f in os.listdir(user_dir) if f.endswith(".pdf")]
    if not pdfs:
        raise HTTPException(400, "No PDFs to ingest")

    BatchProcessor(user=user, max_workers=3).process_files_parallel(pdfs)
    return {"status": "ingested", "files": len(pdfs)}

## ================= ANALYTICS =================
@app.get("/analytics-data")
def analytics(user: str):
    user_path = os.path.join(SESSIONS_DIR, user)
    total = 0
    dates = []
    docs_usage = Counter()

    if os.path.exists(user_path):
        for f in os.listdir(user_path):
            if not f.endswith(".json"):
                continue
            try:
                with open(os.path.join(user_path, f), "r", encoding="utf-8") as file:
                    data = json.load(file)
            except:
                continue

            history = data.get("history", [])
            msgs = [m for m in history if m.get("role") == "user"]
            total += len(msgs)

            created = data.get("created_at")
            if created:
                # Store dates to calculate trend
                dates.extend([created.split("T")[0]] * len(msgs))

            # Count which documents are being cited
            for m in history:
                for c in m.get("citations", []):
                    docs_usage[c.get("source_file", "Unknown")] += 1

    # Generate 7-day trend labels (Sun, Mon, etc.)
    days_map = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    trend = []
    for i in range(6, -1, -1):
        target_date = datetime.now() - timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")
        day_label = days_map[int(target_date.strftime("%w"))]
        trend.append({
            "day": day_label, 
            "queries": dates.count(date_str)
        })

    uploads = os.path.join(UPLOAD_DIR, user)
    doc_count = len([f for f in os.listdir(uploads) if f.endswith(".pdf")]) if os.path.exists(uploads) else 0

    return {
        "stats": [
            {
                "label": "Total Queries", 
                "value": str(total), 
                "icon": "fa-chart-line", 
                "color": "text-blue-500"
            },
            {
                "label": "Avg/Day", 
                "value": str(round(total / 7, 1)), 
                "icon": "fa-calendar-day", 
                "color": "text-cyan-500"
            },
            {
                "label": "Documents", 
                "value": str(doc_count), 
                "icon": "fa-file-alt", 
                "color": "text-sky-500"
            }
        ],
        "trend": trend,
        "top_docs": [{"name": k[:15], "queries": v} for k, v in docs_usage.most_common(3)]
    }
# ================= QUERY (RESTORED) =================
@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    validate_query(req.query)

    search_engine = SearchEngine(user=req.user)

    chunks = search_engine.search_similar_chunks(
        query=req.query,
        k=8
    )

    result = qa_engine.generate_answer(req.query, chunks)

    sid = req.session_id or session_manager.create_session(req.user)

    session_manager.append_to_session(
        user=req.user,
        session_id=sid,
        question=req.query,
        answer=result["answer"],
        citations=result.get("citations", [])
    )

    return {
        "answer": result["answer"],
        "citations": result.get("citations", []),
        "session_id": sid
    }

# ================= HEALTH =================
@app.get("/health")
def health():
    try:
        VectorDatabase().get_collection_stats()
        db = "Online"
    except:
        db = "Offline"

    return {
        "status": "ok",
        "components": {
            "vector_db": db,
            "openai": "Connected" if os.getenv("OPENAI_API_KEY") else "Missing"
        }
    }
