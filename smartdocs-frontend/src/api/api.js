// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://localhost:8000", // FastAPI
// });

// // ---------- Upload PDFs ----------
// export const uploadPDFs = (files) => {
//   const formData = new FormData();
//   files.forEach(file => formData.append("files", file));

//   return API.post("/upload", formData, {
//     headers: { "Content-Type": "multipart/form-data" }
//   });
// };

// // ---------- Ingest ----------
// export const ingestDocs = () => API.post("/ingest");

// // ---------- Query ----------
// export const askQuestion = (query) =>
//   API.post("/query", { query });

// // ---------- Health ----------
// export const getHealth = () => API.get("/health");

// export default API;

import axios from "axios";

const API = axios.create({
  baseURL: "https://pdf-ai-app-bm00.onrender.com/", // FastAPI
});

// ---------- Upload PDFs ----------
export const uploadPDFs = (files) => {
  const formData = new FormData();
  files.forEach(file => formData.append("files", file));

  return API.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

// ---------- Ingest ----------
export const ingestDocs = () => API.post("/ingest");

// ---------- Query (✅ FIXED) ----------
export const askQuestion = (query, sessionId = null) => {
  const user = localStorage.getItem("user");

  return API.post("/query", {
    query: query,
    user: user,
    session_id: sessionId
  });
};

// ---------- Health ----------
export const getHealth = () => API.get("/health");

export default API;
