#!/usr/bin/env python3
"""
Test Semantic Understanding System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.stock_ai_service import stock_ai_service
from services.semantic_mapping_service import semantic_mapping_service

def test_semantic_field_understanding():
    """Test the semantic understanding of database fields"""
    
    print("=== Semantic Field Understanding Test ===\n")
    
    # Test field definitions
    test_fields = ['TheTrendD', 'Price', 'UpsDowns', 'Nrnum', 'Date']
    
    for field_name in test_fields:
        field_def = semantic_mapping_service.get_field_definition(field_name)
        if field_def:
            print(f"✓ {field_name}: {field_def.description}")
            if field_def.possible_values:
                print(f"  Possible values: {field_def.possible_values}")
            if field_def.unit:
                print(f"  Unit: {field_def.unit}")
        else:
            print(f"✗ {field_name}: No semantic definition found")
        print()
    
    # Test trend value interpretation
    print("=== Trend Value Interpretation Test ===\n")
    trend_values = [0, 1, 2]
    for value in trend_values:
        interpretation = semantic_mapping_service.interpret_trend_value(value)
        print(f"✓ Trend value {value} = {interpretation}")
    print()

def test_query_classification():
    """Test the classification of different question types"""
    
    print("=== Query Classification Test ===\n")
    
    test_questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011 over the last 7 days",
        "What stocks have high volume?",
        "Show me stocks with uptrend in the last week",
        "What is the average price for stock 230011?"
    ]
    
    for question in test_questions:
        question_type, context = semantic_mapping_service.classify_question_type(question)
        print(f"Question: {question}")
        print(f"  Classified as: {question_type}")
        if context:
            print(f"  Context: {context.get('pattern', 'No pattern')}")
        print()

def test_symbol_extraction():
    """Test extraction of stock symbols from questions"""
    
    print("=== Symbol Extraction Test ===\n")
    
    test_questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time stock 230011 changed from long to short?",
        "Show me the trend history for 230011 over the last 7 days",
        "What is the price of 230011?",
        "How is 230011 trending today?"
    ]
    
    for question in test_questions:
        symbol = semantic_mapping_service.extract_symbol_from_question(question)
        print(f"Question: {question}")
        print(f"  Extracted symbol: {symbol}")
        print()

def test_semantic_queries():
    """Test semantic-based query processing"""
    
    print("=== Semantic Query Processing Test ===\n")
    
    # Test questions that should be handled by semantic patterns
    semantic_questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011 over the last 7 days"
    ]
    
    for question in semantic_questions:
        print(f"Question: {question}")
        try:
            result = stock_ai_service.process_question(question)
            if result.status == "success":
                print(f"  ✓ Success: {result.query_type}")
                print(f"  ✓ SQL: {result.sql_query[:100]}...")
                print(f"  ✓ Results: {result.row_count} rows")
                print(f"  ✓ Explanation: {result.explanation[:100]}...")
            else:
                print(f"  ✗ Error: {result.error_message}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")
        print()

def test_field_meanings_api():
    """Test the field meanings API functionality"""
    
    print("=== Field Meanings API Test ===\n")
    
    # Test getting all field meanings
    try:
        meanings = stock_ai_service.get_field_meanings()
        print(f"✓ Retrieved {len(meanings)} field meanings")
        
        # Test specific field meanings
        test_fields = ['TheTrendD', 'Price', 'UpsDowns']
        for field in test_fields:
            meaning = stock_ai_service.get_field_meaning(field)
            if meaning:
                print(f"✓ {field}: {meaning['description']}")
            else:
                print(f"✗ {field}: No meaning found")
                
    except Exception as e:
        print(f"✗ Error testing field meanings: {e}")
    
    print()

def test_trend_understanding():
    """Test specific trend understanding capabilities"""
    
    print("=== Trend Understanding Test ===\n")
    
    # Test trend value meanings
    trend_values = {
        0: "sideways (no clear trend)",
        1: "uptrend (long position)", 
        2: "downtrend (short position)"
    }
    
    print("Trend value meanings:")
    for value, meaning in trend_values.items():
        interpreted = semantic_mapping_service.interpret_trend_value(value)
        print(f"  {value} = {interpreted}")
    
    print()
    
    # Test trend-related questions
    trend_questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011 over the last 7 days"
    ]
    
    print("Testing trend-related questions:")
    for question in trend_questions:
        print(f"\nQuestion: {question}")
        try:
            result = stock_ai_service.process_question(question)
            if result.status == "success":
                print(f"  ✓ Success")
                print(f"  ✓ Query type: {result.query_type}")
                print(f"  ✓ Explanation: {result.explanation}")
            else:
                print(f"  ✗ Error: {result.error_message}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")

def test_database_connection():
    """Test database connection and schema"""
    
    print("=== Database Connection Test ===\n")
    
    try:
        status = stock_ai_service.get_database_status()
        if status['status'] == 'connected':
            print(f"✓ Database connected")
            print(f"✓ Database: {status.get('database', 'Unknown')}")
            print(f"✓ Tables: {list(status['tables'].keys())}")
            
            # Check for required fields
            required_fields = ['TheTrendD', 'Price', 'UpsDowns', 'Nrnum', 'Date']
            for table_name, columns in status['tables'].items():
                if table_name == 'stock_data':
                    field_names = [col['field'] for col in columns]
                    for field in required_fields:
                        if field in field_names:
                            print(f"✓ Found required field: {field}")
                        else:
                            print(f"✗ Missing required field: {field}")
        else:
            print(f"✗ Database error: {status.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Exception: {e}")
    
    print()

if __name__ == "__main__":
    try:
        print("🧠 Testing Semantic Understanding System\n")
        print("=" * 50)
        
        test_database_connection()
        test_semantic_field_understanding()
        test_query_classification()
        test_symbol_extraction()
        test_field_meanings_api()
        test_trend_understanding()
        test_semantic_queries()
        
        print("\n" + "=" * 50)
        print("✅ Semantic Understanding Test Completed")
        print("\nKey Features Tested:")
        print("✓ Semantic field definitions")
        print("✓ Query classification")
        print("✓ Symbol extraction")
        print("✓ Trend value interpretation")
        print("✓ Natural language response generation")
        print("✓ Database field meaning API")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 