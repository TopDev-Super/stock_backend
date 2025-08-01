#!/usr/bin/env python3
"""
Test LLM-based query processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.stock_ai_service import stock_ai_service

def test_llm_queries():
    """Test the LLM-based query processing"""
    
    print("=== LLM-Based Query Processing Test ===\n")
    
    # Test questions that should be handled by LLM
    test_questions = [
        "What is the current trend for stock 230011?",
        "When was the last time stock 230011 changed from uptrend to downtrend?",
        "Show me the trend history for stock 230011 over the last 7 days",
        "How is stock 230011 trending today?",
        "What stocks have high volume?",
        "Show me stocks with uptrend in the last week",
        "Show me stock names and their current trends",
        "Which stocks have the highest price and what are their names?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"Question {i}: {question}")
        try:
            result = stock_ai_service.process_question(question)
            if result.status == "success":
                print(f"   ✓ Success: {result.sql_query[:100]}...")
                print(f"   ✓ Results: {result.row_count} rows")
                print(f"   ✓ Explanation: {result.explanation[:100]}...")
            else:
                print(f"   ✗ Error: {result.error_message}")
        except Exception as e:
            print(f"   ✗ Exception: {e}")
        print()

def test_multi_table_queries():
    """Test queries that specifically use multiple tables"""
    
    print("=== Multi-Table Query Test ===\n")
    
    multi_table_questions = [
        "Show me stock names and their current prices",
        "Which stocks have uptrend and what are their names?",
        "Show me the names of stocks with high volume",
        "List stock names with their trend information",
        "What are the names of stocks that changed trend recently?"
    ]
    
    for i, question in enumerate(multi_table_questions, 1):
        print(f"Multi-table Question {i}: {question}")
        try:
            result = stock_ai_service.process_question(question)
            if result.status == "success":
                print(f"   ✓ SQL: {result.sql_query}")
                print(f"   ✓ Results: {result.row_count} rows")
                # Check if the query uses JOIN
                if "JOIN" in result.sql_query.upper():
                    print(f"   ✓ Uses JOIN (multi-table query)")
                else:
                    print(f"   ⚠ Single table query")
            else:
                print(f"   ✗ Error: {result.error_message}")
        except Exception as e:
            print(f"   ✗ Exception: {e}")
        print()

def test_database_status():
    """Test database connection and schema"""
    
    print("=== Database Status Test ===\n")
    
    try:
        status = stock_ai_service.get_database_status()
        if status['status'] == 'connected':
            print(f"   ✓ Database connected")
            print(f"   ✓ Tables: {list(status['tables'].keys())}")
            for table_name, columns in status['tables'].items():
                print(f"   ✓ {table_name}: {len(columns)} columns")
        else:
            print(f"   ✗ Database error: {status.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    print()

def test_llm_connection():
    """Test LLM service connection"""
    
    print("=== LLM Connection Test ===\n")
    
    try:
        is_connected = stock_ai_service.test_llm_connection()
        if is_connected:
            print("   ✓ LLM service connected")
        else:
            print("   ✗ LLM service not available")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    print()

if __name__ == "__main__":
    try:
        test_database_status()
        test_llm_connection()
        test_llm_queries()
        test_multi_table_queries()
        print("\n=== Test completed ===")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc() 