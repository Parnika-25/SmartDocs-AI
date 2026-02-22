from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import json, os

router = APIRouter()
BASE_DIR = "sessions"
os.makedirs(BASE_DIR, exist_ok=True)

# ----------------------------
# MODELS
# ----------------------------

class SessionSaveRequest(BaseModel):
    user: str
    history: List[Dict]

class RenameSessionRequest(BaseModel):
    title: str

# ----------------------------
# HELPERS
# ----------------------------

def user_dir(user: str):
    path = os.path.join(BASE_DIR, user)
    os.makedirs(path, exist_ok=True)
    return path

def session_path(user: str, session_id: str):
    return os.path.join(user_dir(user), f"{session_id}.json")

# ----------------------------
# CREATE NEW SESSION
# ----------------------------

@router.post("/session/create")
def create_session(payload: SessionSaveRequest):
    session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    path = session_path(payload.user, session_id)

    data = {
        "session_id": session_id,
        "user": payload.user,
        "title": f"Session {datetime.now().strftime('%d %b %H:%M')}",
        "created_at": datetime.utcnow().isoformat(),
        "history": payload.history
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return {"session_id": session_id}

# ----------------------------
# LIST USER SESSIONS
# ----------------------------

@router.get("/session/{user}")
def list_sessions(user: str):
    path = user_dir(user)
    sessions = []

    for file in sorted(os.listdir(path), reverse=True):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(path, file), encoding="utf-8") as f:
            data = json.load(f)

            sessions.append({
                "session_id": data["session_id"],
                "title": data.get("title", "Untitled Session"),
                "created_at": data["created_at"]
            })

    return {"sessions": sessions}

# ----------------------------
# LOAD ONE SESSION
# ----------------------------

@router.get("/session/{user}/{session_id}")
def load_session(user: str, session_id: str):
    path = session_path(user, session_id)
    if not os.path.exists(path):
        raise HTTPException(404, "Session not found")

    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# ✅ RENAME SESSION (PUT)
# ----------------------------

@router.put("/session/{user}/{session_id}")
def rename_session(user: str, session_id: str, payload: RenameSessionRequest):
    path = session_path(user, session_id)

    if not os.path.exists(path):
        raise HTTPException(404, "Session not found")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    data["title"] = payload.title.strip() or data.get("title", "Untitled Session")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return {"status": "renamed", "title": data["title"]}

# ----------------------------
# DELETE SESSION
# ----------------------------

@router.delete("/session/{user}/{session_id}")
def delete_session(user: str, session_id: str):
    path = session_path(user, session_id)
    if os.path.exists(path):
        os.remove(path)
    return {"status": "deleted"}