import logging
from typing import Dict, List, Optional
from database.connection import db
from ai.llm_service import llm_service
from services.enhanced_query_processor import enhanced_query_processor
from models.schemas import QueryResponse, QuestionSuggestionResponse

logger = logging.getLogger(__name__)

class StockAIService:
    def __init__(self):
        self.table_info = None
        self._load_table_info()
    
    def _load_table_info(self):
        """Load database table information"""
        try:
            db_status = db.test_connection()
            if db_status['status'] == 'connected':
                self.table_info = db_status['tables']
                logger.info(f"Loaded table info for {len(self.table_info)} tables")
            else:
                logger.error(f"Failed to load table info: {db_status.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"Error loading table info: {e}")
    
    def process_question(self, question: str, limit: int = 100) -> QueryResponse:
        """Process a natural language question and return results"""
        try:
            # Check if we have table info
            if not self.table_info:
                self._load_table_info()
                if not self.table_info:
                    return QueryResponse(
                        status="error",
                        question=question,
                        error_message="Database connection not available"
                    )
            
            # Use enhanced query processor with semantic understanding
            result = enhanced_query_processor.process_question(question, self.table_info, limit)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return QueryResponse(
                status="error",
                question=question,
                error_message=f"Unexpected error: {str(e)}"
            )
    
    def get_question_suggestions(self) -> QuestionSuggestionResponse:
        """Get suggested questions based on semantic understanding"""
        try:
            suggestions = enhanced_query_processor.suggest_questions()
            
            return QuestionSuggestionResponse(
                status="success",
                suggestions=suggestions
            )
            
        except Exception as e:
            logger.error(f"Error getting question suggestions: {e}")
            return QuestionSuggestionResponse(
                status="error",
                suggestions=[],
                error_message=f"Failed to generate suggestions: {str(e)}"
            )
    
    def get_database_status(self) -> Dict:
        """Get current database status and table information"""
        try:
            return db.test_connection()
        except Exception as e:
            logger.error(f"Error getting database status: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_llm_connection(self) -> bool:
        """Test if LLM service is available"""
        try:
            return llm_service.llm is not None
        except Exception as e:
            logger.error(f"Error testing LLM connection: {e}")
            return False
    
    def get_field_meanings(self) -> Dict[str, Dict]:
        """Get semantic meanings of all database fields"""
        try:
            return enhanced_query_processor.get_all_field_meanings()
        except Exception as e:
            logger.error(f"Error getting field meanings: {e}")
            return {}
    
    def get_field_meaning(self, field_name: str) -> Optional[Dict]:
        """Get semantic meaning of a specific database field"""
        try:
            return enhanced_query_processor.get_field_meaning(field_name)
        except Exception as e:
            logger.error(f"Error getting field meaning for {field_name}: {e}")
            return None

# Global service instance
stock_ai_service = StockAIService() 