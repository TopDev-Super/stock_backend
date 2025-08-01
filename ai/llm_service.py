import logging
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from config import config

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.llm = None
        self.initialize_llm()
    
    def initialize_llm(self):
        """Initialize the LLM with OpenAI"""
        try:
            if not config.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found in environment variables")
            
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                api_key=config.OPENAI_API_KEY
            )
            logger.info("LLM service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}")
            raise
    
    def get_database_schema_prompt(self, table_info: Dict) -> str:
        """Generate a comprehensive database schema description for the LLM"""
        schema_prompt = """
You are an AI assistant that helps users query a stock market database. 
The database contains the following tables and their structure:

"""
        
        for table_name, columns in table_info.items():
            schema_prompt += f"\nTable: {table_name}\n"
            schema_prompt += "Columns:\n"
            for col in columns:
                schema_prompt += f"  - {col['field']} ({col['type']})"
                if col['null'] == 'NO':
                    schema_prompt += " [NOT NULL]"
                if col['key'] == 'PRI':
                    schema_prompt += " [PRIMARY KEY]"
                schema_prompt += "\n"
        
        schema_prompt += """
IMPORTANT: All the fields listed above are available in the database. Do NOT say fields don't exist.

Field interpretations for stock data:
- Nrnum: Stock identifier (like a symbol/ticker)
- Date: Trading date
- Price: Stock price
- UpsDowns: Trading volume/activity
- TheTrendD: Daily trend (1=uptrend, 2=downtrend, 0=sideways)
- TheTrendW: Weekly trend
- TheTrendM: Monthly trend
- MainSug: Main suggestion/indicator
- SubSug: Sub suggestion/indicator
- Index: Market index value
- Ma5StatusD: 5-day moving average status
- Rsi50StatusD: RSI 50 status
- FourSignals_D: Four signals indicator
- FinalGradeD: Final daily grade/rating

SQL Generation Rules:
1. Always use proper MySQL syntax
2. Use appropriate date functions (DATE(), YEAR(), MONTH(), etc.)
3. Handle NULL values with IS NULL or IS NOT NULL
4. Use proper JOIN syntax when combining tables
5. Always include LIMIT clauses (default: LIMIT 100)
6. Use proper aggregation functions (COUNT, SUM, AVG, MAX, MIN)
7. For boolean fields, use = 1 for TRUE, = 0 for FALSE
8. Use LIKE for text searches, = for exact matches
9. Use proper comparison operators (<, >, <=, >=, =, !=)
10. NEVER use placeholder text like [Enter value here] - use actual values
11. If filtering by specific stocks, use actual stock numbers from Nrnum field
12. Generate queries that can be executed immediately without modification
13. For trend analysis, use TheTrendD, TheTrendW, or TheTrendM fields
14. For volume analysis, use UpsDowns field
15. For price analysis, use Price field

CRITICAL: Generate ONLY valid, executable SQL. If you cannot create a valid query, return: SELECT 1 LIMIT 0;
"""
        
        return schema_prompt
    
    def generate_sql_query(self, user_question: str, table_info: Dict) -> Dict:
        """Generate SQL query from natural language question"""
        try:
            if not self.llm:
                raise ValueError("LLM not initialized")
            
            # Create the system prompt with database schema
            system_prompt = self.get_database_schema_prompt(table_info)
            
            # Create the user prompt with stronger instructions
            user_prompt = f"""
User Question: {user_question}

CRITICAL: Generate ONLY a valid MySQL SQL query that can be executed immediately.

Requirements:
- Return ONLY the SQL statement
- Start with SELECT, INSERT, UPDATE, or DELETE
- End with semicolon (;)
- NO placeholders like [Enter Stock Nrnum Here] or [specific value]
- NO explanations, no "I'm sorry", no additional text
- Use actual column names and values from the database
- If you need to filter by specific stocks, use actual stock numbers or names from the data
- If you cannot create a valid query, return: SELECT 1 LIMIT 0;

Example format:
SELECT column1, column2 FROM table_name WHERE condition LIMIT 100;

IMPORTANT: Never use placeholder text like [Enter value here] - use actual SQL syntax.
"""
            
            # Create messages for the LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            sql_query = response.content.strip()
            
            # Clean up the response to ensure it's only SQL
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()
            
            # Remove any explanatory text that might have been included
            if "I'm sorry" in sql_query or "I cannot" in sql_query or "does not contain" in sql_query:
                sql_query = "SELECT 1 LIMIT 0; -- No valid query could be generated"
            
            # Check for placeholder text and replace with valid SQL
            if "[Enter" in sql_query or "[specific" in sql_query or "[value" in sql_query:
                # Replace common placeholders with valid SQL
                sql_query = sql_query.replace("[Enter Stock Nrnum Here]", "1")  # Use first stock as example
                sql_query = sql_query.replace("[Enter specific value]", "1")
                sql_query = sql_query.replace("[value]", "1")
                sql_query = sql_query.replace("[Enter value here]", "1")
            
            # Ensure it ends with semicolon
            if not sql_query.endswith(";"):
                sql_query += ";"
            
            logger.info(f"Generated SQL query: {sql_query}")
            
            return {
                'status': 'success',
                'sql_query': sql_query,
                'original_question': user_question
            }
            
        except Exception as e:
            logger.error(f"Error generating SQL query: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'original_question': user_question
            }
    
    def explain_results(self, question: str, results: List[Dict], sql_query: str) -> str:
        """Generate a natural language explanation of the query results"""
        try:
            if not self.llm:
                raise ValueError("LLM not initialized")
            
            # Prepare the results summary
            result_count = len(results)
            sample_data = results[:3] if results else []
            
            explanation_prompt = f"""
Original Question: {question}
SQL Query Used: {sql_query}
Number of Results: {result_count}

Sample Results: {sample_data}

Please provide a natural language explanation of these results. 
Make it conversational and easy to understand for a non-technical user.
Include insights about what the data shows and any notable patterns.
"""
            
            messages = [
                SystemMessage(content="You are a helpful financial data analyst. Explain stock market data in clear, understandable terms."),
                HumanMessage(content=explanation_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Error explaining results: {e}")
            return f"Found {len(results)} results for your query. Please review the data for specific insights."
    
    def suggest_questions(self, table_info: Dict) -> List[str]:
        """Suggest example questions based on the database schema"""
        try:
            if not self.llm:
                raise ValueError("LLM not initialized")
            
            schema_prompt = self.get_database_schema_prompt(table_info)
            
            suggestion_prompt = f"""
{schema_prompt}

Based on this database schema, suggest 5-8 interesting and useful questions that users could ask about the stock data.
Focus on questions that would provide valuable insights for stock analysis.
Make the questions natural and conversational.

Return only the questions, one per line, no numbering or additional text.
"""
            
            messages = [
                SystemMessage(content="You are a financial data analyst. Suggest useful questions for stock market analysis."),
                HumanMessage(content=suggestion_prompt)
            ]
            
            response = self.llm.invoke(messages)
            suggestions = response.content.strip().split('\n')
            
            # Clean up suggestions
            suggestions = [s.strip() for s in suggestions if s.strip()]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating question suggestions: {e}")
            return [
                "Which stocks have a price above the moving average 50?",
                "Which stocks had the highest volume increase today?",
                "Show me stocks with positive price changes in the last week",
                "Which stocks have upcoming earnings announcements?",
                "Find stocks with consistent price increases over the last month"
            ]

# Global LLM service instance
llm_service = LLMService() 