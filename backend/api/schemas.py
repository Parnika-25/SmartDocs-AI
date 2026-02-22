from pydantic import BaseModel
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    query: str
    user:str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    citations: List[Dict]

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, str]