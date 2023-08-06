from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatResponse(BaseModel):
    response: str = Field(...)
    context_referenced: Optional[List[Dict[str, Any]]] = Field(default=None)
    response_code: int = Field(...)


class UploadResponse(BaseModel):
    response: str = Field(...)
    response_code: int = Field(...)
