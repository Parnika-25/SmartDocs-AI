# # import json
# # import os
# # import time
# # from datetime import datetime
# # from utils.error_handler import logger

# # class SessionManager:
# #     def __init__(self, storage_dir="sessions"):
# #         self.storage_dir = storage_dir
# #         os.makedirs(storage_dir, exist_ok=True)

# #     def create_session(self):
# #         """Initializes a new session with a unique ID."""
# #         return f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# #     def save_session_state(self, session_id, data):
# #         """Persists conversation data to a local JSON file."""
# #         file_path = os.path.join(self.storage_dir, f"{session_id}.json")
# #         try:
# #             with open(file_path, "w") as f:
# #                 json.dump(data, f, default=str, indent=4)
# #             return True
# #         except Exception as e:
# #             logger.error(f"Failed to save session {session_id}: {e}")
# #             return False

# #     def load_session_state(self, session_id):
# #         """Restores a previous session from JSON."""
# #         file_path = os.path.join(self.storage_dir, f"{session_id}.json")
# #         if os.path.exists(file_path):
# #             with open(file_path, "r") as f:
# #                 return json.load(f)
# #         return None


# import json
# import os
# from datetime import datetime
# from utils.error_handler import logger


# class SessionManager:
#     def __init__(self, storage_dir="sessions"):
#         self.storage_dir = storage_dir
#         os.makedirs(storage_dir, exist_ok=True)

#     # ----------------------------
#     # INTERNAL HELPERS
#     # ----------------------------

#     def _user_dir(self, user: str):
#         path = os.path.join(self.storage_dir, user)
#         os.makedirs(path, exist_ok=True)
#         return path

#     def _session_path(self, user: str, session_id: str):
#         return os.path.join(self._user_dir(user), f"{session_id}.json")

#     # ----------------------------
#     # CREATE SESSION
#     # ----------------------------

#     def create_session(self, user: str, title: str = None):
#         session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
#         data = {
#             "session_id": session_id,
#             "user": user,
#             "title": title or f"Session {datetime.now().strftime('%d %b %H:%M')}",
#             "created_at": datetime.utcnow().isoformat(),
#             "history": []
#         }
#         self.save_session_state(user, session_id, data)
#         return session_id

#     # ----------------------------
#     # SAVE / LOAD
#     # ----------------------------

#     def save_session_state(self, user: str, session_id: str, data: dict):
#         file_path = self._session_path(user, session_id)
#         try:
#             with open(file_path, "w", encoding="utf-8") as f:
#                 json.dump(data, f, indent=2)
#             return True
#         except Exception as e:
#             logger.error(f"Failed to save session {session_id}: {e}")
#             return False

#     def load_session_state(self, user: str, session_id: str):
#         file_path = self._session_path(user, session_id)
#         if not os.path.exists(file_path):
#             return None

#         with open(file_path, encoding="utf-8") as f:
#             return json.load(f)

#     # ----------------------------
#     # APPEND CHAT (🔥 THIS FIXES YOUR UI)
#     # ----------------------------

#     def append_to_session(
#         self,
#         user: str,
#         session_id: str,
#         question: str,
#         answer: str,
#         citations: list
#     ):
#         session = self.load_session_state(user, session_id)

#         if not session:
#             raise FileNotFoundError("Session not found")

#         session.setdefault("history", [])

#         session["history"].append({
#             "question": question,
#             "answer": answer,
#             "citations": citations or [],
#             "timestamp": datetime.utcnow().isoformat()
#         })

#         self.save_session_state(user, session_id, session)

#     # ----------------------------
#     # UPDATE TITLE (OPTIONAL)
#     # ----------------------------

#     def update_title(self, user: str, session_id: str, title: str):
#         session = self.load_session_state(user, session_id)
#         if not session:
#             raise FileNotFoundError("Session not found")

#         session["title"] = title.strip() or session.get("title", "Untitled Session")
#         self.save_session_state(user, session_id, session)


import json
import os
from datetime import datetime
from utils.error_handler import logger


class SessionManager:
    def __init__(self, storage_dir="sessions"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    # ----------------------------
    # INTERNAL HELPERS
    # ----------------------------

    def _user_dir(self, user: str):
        path = os.path.join(self.storage_dir, user)
        os.makedirs(path, exist_ok=True)
        return path

    def _session_path(self, user: str, session_id: str):
        return os.path.join(self._user_dir(user), f"{session_id}.json")

    # ----------------------------
    # CREATE SESSION
    # ----------------------------

    def create_session(self, user: str):
        session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        data = {
            "session_id": session_id,
            "user": user,
            "title": "New Chat",  # 🔥 placeholder only
            "created_at": datetime.utcnow().isoformat(),
            "history": []
        }
        self.save_session_state(user, session_id, data)
        return session_id

    # ----------------------------
    # SAVE / LOAD
    # ----------------------------

    def save_session_state(self, user: str, session_id: str, data: dict):
        try:
            with open(self._session_path(user, session_id), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {e}")
            return False

    def load_session_state(self, user: str, session_id: str):
        path = self._session_path(user, session_id)
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------
    # APPEND CHAT (🔥 CHATGPT-LIKE FIX)
    # ----------------------------

    def append_to_session(
        self,
        user: str,
        session_id: str,
        question: str,
        answer: str,
        citations: list
    ):
        session = self.load_session_state(user, session_id)
        if not session:
            raise FileNotFoundError("Session not found")

        history = session.setdefault("history", [])

        # 🔥 FIRST QUESTION → SET TITLE
        if len(history) == 0:
            session["title"] = question.strip()[:60]

        history.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.utcnow().isoformat()
        })

        history.append({
            "role": "assistant",
            "content": answer,
            "citations": citations or [],
            "timestamp": datetime.utcnow().isoformat()
        })

        self.save_session_state(user, session_id, session)

    # ----------------------------
    # MANUAL TITLE UPDATE (OPTIONAL)
    # ----------------------------

    def update_title(self, user: str, session_id: str, title: str):
        session = self.load_session_state(user, session_id)
        if not session:
            raise FileNotFoundError("Session not found")

        session["title"] = title.strip() or session.get("title", "New Chat")
        self.save_session_state(user, session_id, session)
