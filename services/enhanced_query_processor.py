import logging
from typing import Dict, List, Optional, Any, Tuple
from services.semantic_mapping_service import semantic_mapping_service
from ai.llm_service import llm_service
from database.connection import db
from models.schemas import QueryResponse

logger = logging.getLogger(__name__)

class EnhancedQueryProcessor:
    """Enhanced query processor that combines semantic understanding with LLM"""
    
    def __init__(self):
        self.semantic_service = semantic_mapping_service
        self.llm_service = llm_service
    
    def process_question(self, question: str, table_info: Dict, limit: int = 100) -> QueryResponse:
        """Process a natural language question using enhanced understanding"""
        try:
            # Step 1: Classify the question type using semantic patterns
            question_type, context = self.semantic_service.classify_question_type(question)
            
            # Step 2: Try semantic-based approach first for known patterns
            if question_type != 'general':
                semantic_result = self._process_semantic_query(question, question_type, context)
                if semantic_result:
                    return semantic_result
            
            # Step 3: Fallback to LLM-based approach
            return self._process_llm_query(question, table_info, limit)
            
        except Exception as e:
            logger.error(f"Error in enhanced query processing: {e}")
            return QueryResponse(
                status="error",
                question=question,
                error_message=f"Failed to process query: {str(e)}"
            )
    
    def _process_semantic_query(self, question: str, question_type: str, context: Dict) -> Optional[QueryResponse]:
        """Process query using semantic understanding"""
        try:
            # Generate SQL using semantic patterns
            sql_query = self.semantic_service.generate_contextual_sql(question, question_type, context)
            
            if not sql_query:
                return None
            
            # Execute the query
            query_result = db.execute_query(sql_query)
            
            if query_result['status'] == 'error':
                logger.warning(f"Semantic query failed: {query_result['message']}")
                return None
            
            results = query_result['data']
            row_count = query_result['row_count']
            
            # Generate natural language response
            explanation = self.semantic_service.generate_natural_response(
                question, results, question_type
            )
            
            return QueryResponse(
                status="success",
                question=question,
                sql_query=sql_query,
                results=results,
                explanation=explanation,
                row_count=row_count,
                query_type=f"semantic_{question_type}"
            )
            
        except Exception as e:
            logger.error(f"Error in semantic query processing: {e}")
            return None
    
    def _process_llm_query(self, question: str, table_info: Dict, limit: int) -> QueryResponse:
        """Process query using LLM-based approach"""
        try:
            # Generate SQL using LLM
            llm_response = self.llm_service.generate_sql_query(question, table_info)
            
            if llm_response['status'] == 'error':
                return QueryResponse(
                    status="error",
                    question=question,
                    error_message=f"Failed to generate SQL query: {llm_response['message']}"
                )
            
            sql_query = llm_response['sql_query']
            
            # Add LIMIT clause if not present
            if 'LIMIT' not in sql_query.upper():
                sql_query += f" LIMIT {limit}"
            
            # Execute the query
            query_result = db.execute_query(sql_query)
            
            if query_result['status'] == 'error':
                return QueryResponse(
                    status="error",
                    question=question,
                    sql_query=sql_query,
                    error_message=f"Query execution failed: {query_result['message']}"
                )
            
            results = query_result['data']
            row_count = query_result['row_count']
            
            # Generate explanation using LLM
            explanation = self.llm_service.explain_results(question, results, sql_query)
            
            return QueryResponse(
                status="success",
                question=question,
                sql_query=sql_query,
                results=results,
                explanation=explanation,
                row_count=row_count,
                query_type="llm_generated"
            )
            
        except Exception as e:
            logger.error(f"Error in LLM query processing: {e}")
            return QueryResponse(
                status="error",
                question=question,
                error_message=f"Failed to process LLM query: {str(e)}"
            )
    
    def get_field_meaning(self, field_name: str) -> Optional[Dict]:
        """Get the semantic meaning of a database field"""
        field_def = self.semantic_service.get_field_definition(field_name)
        if field_def:
            return {
                'field_name': field_def.field_name,
                'type': field_def.field_type.value,
                'description': field_def.description,
                'possible_values': field_def.possible_values,
                'unit': field_def.unit,
                'table': field_def.table
            }
        return None
    
    def get_all_field_meanings(self) -> Dict[str, Dict]:
        """Get semantic meanings for all database fields"""
        meanings = {}
        for field_name, field_def in self.semantic_service.field_definitions.items():
            meanings[field_name] = {
                'field_name': field_def.field_name,
                'type': field_def.field_type.value,
                'description': field_def.description,
                'possible_values': field_def.possible_values,
                'unit': field_def.unit,
                'table': field_def.table
            }
        return meanings
    
    def suggest_questions(self) -> List[str]:
        """Suggest questions based on semantic understanding"""
        suggestions = [
            "What is the trend on symbol 230011 today?",
            "When was the last time symbol 230011 moved from uptrend to downtrend?",
            "Show me the trend history for symbol 230011 over the last 7 days",
            "What stocks have high volume today?",
            "Which stocks are in uptrend this week?",
            "Show me stocks with downtrend in the last month",
            "What is the current price of symbol 230011?",
            "Which stocks have the highest trading volume?",
            "Show me stock names and their current trends",
            "What stocks changed trend recently?"
        ]
        return suggestions

# Global instance
enhanced_query_processor = EnhancedQueryProcessor() 