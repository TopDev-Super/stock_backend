from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class DatabaseStatusResponse(BaseModel):
    status: str
    database: Optional[str] = None
    tables: Optional[Dict[str, List[Dict[str, Any]]]] = None
    message: Optional[str] = None

class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question about stock data")
    limit: Optional[int] = Field(100, description="Maximum number of results to return")

class QueryResponse(BaseModel):
    status: str
    question: str
    sql_query: Optional[str] = None
    results: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[str] = None
    row_count: Optional[int] = None
    error_message: Optional[str] = None
    query_type: Optional[str] = None

class QuestionSuggestionResponse(BaseModel):
    status: str
    suggestions: List[str]
    error_message: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    database_connected: bool
    llm_available: bool
    timestamp: datetime

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[str] = None 