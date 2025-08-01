from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Dict, Any

from models.schemas import (
    QueryRequest, QueryResponse, QuestionSuggestionResponse,
    DatabaseStatusResponse, HealthCheckResponse, ErrorResponse
)
from services.stock_ai_service import stock_ai_service
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Stock AI Analysis System",
    description="AI-powered stock market data analysis system with natural language querying and semantic understanding",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Stock AI Analysis System...")
    try:
        # Test database connection
        db_status = stock_ai_service.get_database_status()
        if db_status['status'] == 'connected':
            logger.info("Database connection established")
        else:
            logger.warning(f"Database connection issue: {db_status.get('message', 'Unknown error')}")
        
        # Test LLM connection
        if stock_ai_service.test_llm_connection():
            logger.info("LLM service initialized")
        else:
            logger.warning("LLM service not available")
            
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Stock AI Analysis System...")
    try:
        from database.connection import db
        db.close()
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Stock AI Analysis System with Semantic Understanding",
        "version": "1.0.0",
        "status": "running",
        "features": "Natural language querying, Semantic field understanding, Trend analysis, Stock data analysis"
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        db_status = stock_ai_service.get_database_status()
        llm_available = stock_ai_service.test_llm_connection()
        
        return HealthCheckResponse(
            status="healthy" if db_status['status'] == 'connected' and llm_available else "degraded",
            database_connected=db_status['status'] == 'connected',
            llm_available=llm_available,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            database_connected=False,
            llm_available=False,
            timestamp=datetime.now()
        )

@app.get("/database/status", response_model=DatabaseStatusResponse)
async def get_database_status():
    """Get database status and schema information"""
    try:
        status = stock_ai_service.get_database_status()
        return DatabaseStatusResponse(
            status=status['status'],
            database=status.get('database', ''),
            tables=status.get('tables', {}),
            message=status.get('message', '')
        )
    except Exception as e:
        logger.error(f"Database status error: {e}")
        return DatabaseStatusResponse(
            status="error",
            database="",
            tables={},
            message=str(e)
        )

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process natural language query and return results"""
    try:
        logger.info(f"Processing question: {request.question}")
        
        # Process the question using enhanced semantic understanding
        result = stock_ai_service.process_question(request.question, request.limit)
        
        return result
        
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        return QueryResponse(
            status="error",
            question=request.question,
            error_message=f"Failed to process query: {str(e)}"
        )

@app.get("/suggestions", response_model=QuestionSuggestionResponse)
async def get_question_suggestions():
    """Get suggested questions based on semantic understanding"""
    try:
        result = stock_ai_service.get_question_suggestions()
        return result
    except Exception as e:
        logger.error(f"Suggestions error: {e}")
        return QuestionSuggestionResponse(
            status="error",
            suggestions=[],
            error_message=f"Failed to get suggestions: {str(e)}"
        )

@app.get("/fields/meanings")
async def get_field_meanings():
    """Get semantic meanings of all database fields"""
    try:
        meanings = stock_ai_service.get_field_meanings()
        return {
            "status": "success",
            "field_meanings": meanings,
            "total_fields": len(meanings),
            "message": "Semantic meanings of database fields"
        }
    except Exception as e:
        logger.error(f"Field meanings error: {e}")
        return {
            "status": "error",
            "field_meanings": {},
            "error_message": f"Failed to get field meanings: {str(e)}"
        }

@app.get("/fields/{field_name}/meaning")
async def get_field_meaning(field_name: str):
    """Get semantic meaning of a specific database field"""
    try:
        meaning = stock_ai_service.get_field_meaning(field_name)
        if meaning:
            return {
                "status": "success",
                "field_name": field_name,
                "meaning": meaning
            }
        else:
            return {
                "status": "error",
                "field_name": field_name,
                "error_message": f"Field '{field_name}' not found or has no semantic meaning defined"
            }
    except Exception as e:
        logger.error(f"Field meaning error for {field_name}: {e}")
        return {
            "status": "error",
            "field_name": field_name,
            "error_message": f"Failed to get field meaning: {str(e)}"
        }

@app.get("/examples")
async def get_example_questions():
    """Get example questions for users"""
    examples = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011 over the last 7 days",
        "What stocks have high volume?",
        "Show me stocks with uptrend in the last week",
        "What is the average price for stock 230011?",
        "Which stocks have the highest price today?",
        "Show me stocks with downtrend in the last month",
        "What is the current trend for stock 230011?",
        "When did stock 230011 change from long to short position?"
    ]
    
    return {
        "examples": examples,
        "message": "These are example questions you can ask. The system uses semantic understanding to interpret database fields and provide accurate answers.",
        "features": [
            "Semantic field understanding",
            "Trend analysis (uptrend/downtrend/sideways)",
            "Stock symbol recognition",
            "Natural language responses",
            "Multi-table queries"
        ]
    }

@app.get("/semantic/trend-values")
async def get_trend_value_meanings():
    """Get the meaning of trend values"""
    return {
        "status": "success",
        "trend_values": {
            "0": "sideways (no clear trend)",
            "1": "uptrend (long position)",
            "2": "downtrend (short position)"
        },
        "description": "These are the semantic meanings of trend values in the TheTrendD, TheTrendW, and TheTrendM fields"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": "internal_error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG,
        log_level="info"
    ) 