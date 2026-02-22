import axios from "axios";

const API = axios.create({
  baseURL: "https://pdf-ai-app-bm00.onrender.com/",
});

/* -------------------------
   CREATE NEW SESSION
-------------------------- */
export const createSession = (user, history) =>
  API.post(`/session/create`, {
    user,
    history,
  });

/* -------------------------
   LIST ALL SESSIONS
-------------------------- */
export const listSessions = (user) =>
  API.get(`/session/${user}`);

/* -------------------------
   LOAD ONE SESSION
-------------------------- */
export const loadSession = (user, sessionId) =>
  API.get(`/session/${user}/${sessionId}`);

/* -------------------------
   DELETE SESSION
-------------------------- */
export const deleteSession = (user, sessionId) =>
  API.delete(`/session/${user}/${sessionId}`);

/* -------------------------
   ✅ RENAME SESSION (NEW)
-------------------------- */
export const renameSession = (user, sessionId, title) =>
  API.put(`/session/${user}/${sessionId}`, {
    title,
  });
