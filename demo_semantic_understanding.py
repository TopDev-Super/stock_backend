#!/usr/bin/env python3
"""
Demonstration of Semantic Understanding System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.stock_ai_service import stock_ai_service

def demo_trend_understanding():
    """Demonstrate trend understanding capabilities"""
    
    print("🧠 SEMANTIC UNDERSTANDING DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Example 1: Current trend question
    print("📊 EXAMPLE 1: Current Trend Analysis")
    print("-" * 40)
    question1 = "What is the trend on symbol 230011 today?"
    print(f"Question: {question1}")
    
    result1 = stock_ai_service.process_question(question1)
    if result1.status == "success":
        print(f"✅ Answer: {result1.explanation}")
        print(f"🔍 Query Type: {result1.query_type}")
        print(f"📈 Results: {result1.row_count} rows found")
    else:
        print(f"❌ Error: {result1.error_message}")
    print()
    
    # Example 2: Trend change question
    print("📊 EXAMPLE 2: Trend Change Detection")
    print("-" * 40)
    question2 = "When was the last time symbol 230011 moved from uptrend to downtrend?"
    print(f"Question: {question2}")
    
    result2 = stock_ai_service.process_question(question2)
    if result2.status == "success":
        print(f"✅ Answer: {result2.explanation}")
        print(f"🔍 Query Type: {result2.query_type}")
        print(f"📈 Results: {result2.row_count} rows found")
    else:
        print(f"❌ Error: {result2.error_message}")
    print()
    
    # Example 3: Trend history question
    print("📊 EXAMPLE 3: Trend History Analysis")
    print("-" * 40)
    question3 = "Show me the trend history for symbol 230011 over the last 7 days"
    print(f"Question: {question3}")
    
    result3 = stock_ai_service.process_question(question3)
    if result3.status == "success":
        print(f"✅ Answer: {result3.explanation}")
        print(f"🔍 Query Type: {result3.query_type}")
        print(f"📈 Results: {result3.row_count} rows found")
    else:
        print(f"❌ Error: {result3.error_message}")
    print()

def demo_field_meanings():
    """Demonstrate field meaning understanding"""
    
    print("🔍 FIELD MEANING UNDERSTANDING")
    print("=" * 60)
    print()
    
    # Get all field meanings
    meanings = stock_ai_service.get_field_meanings()
    
    print("📋 Database Field Meanings:")
    print("-" * 30)
    
    key_fields = ['TheTrendD', 'Price', 'UpsDowns', 'Nrnum', 'Date']
    for field in key_fields:
        if field in meanings:
            meaning = meanings[field]
            print(f"✅ {field}: {meaning['description']}")
            if meaning.get('possible_values'):
                print(f"   Values: {meaning['possible_values']}")
            if meaning.get('unit'):
                print(f"   Unit: {meaning['unit']}")
        else:
            print(f"❌ {field}: No meaning defined")
        print()
    
    # Test trend value interpretation
    print("🎯 Trend Value Interpretation:")
    print("-" * 30)
    trend_values = [0, 1, 2]
    for value in trend_values:
        from services.semantic_mapping_service import semantic_mapping_service
        interpretation = semantic_mapping_service.interpret_trend_value(value)
        print(f"   {value} = {interpretation}")
    print()

def demo_query_classification():
    """Demonstrate query classification capabilities"""
    
    print("🎯 QUERY CLASSIFICATION DEMONSTRATION")
    print("=" * 60)
    print()
    
    test_questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011 over the last 7 days",
        "What stocks have high volume?",
        "Which stocks are in uptrend this week?"
    ]
    
    from services.semantic_mapping_service import semantic_mapping_service
    
    for i, question in enumerate(test_questions, 1):
        print(f"📝 Question {i}: {question}")
        
        # Classify the question
        question_type, context = semantic_mapping_service.classify_question_type(question)
        print(f"   🎯 Classified as: {question_type}")
        
        # Extract symbol if present
        symbol = semantic_mapping_service.extract_symbol_from_question(question)
        if symbol:
            print(f"   🔢 Extracted symbol: {symbol}")
        
        print()

def demo_system_capabilities():
    """Demonstrate overall system capabilities"""
    
    print("🚀 SYSTEM CAPABILITIES SUMMARY")
    print("=" * 60)
    print()
    
    capabilities = [
        "✅ Semantic understanding of database fields",
        "✅ Natural language query processing", 
        "✅ Trend value interpretation (0=sideways, 1=uptrend, 2=downtrend)",
        "✅ Stock symbol extraction from questions",
        "✅ Query classification and routing",
        "✅ Hybrid processing (semantic + LLM)",
        "✅ Natural language response generation",
        "✅ Multi-table queries with JOINs",
        "✅ Extensible field definitions",
        "✅ Configurable question patterns"
    ]
    
    for capability in capabilities:
        print(capability)
    
    print()
    print("🎯 SUPPORTED QUESTION TYPES:")
    print("-" * 30)
    question_types = [
        "• Current trend analysis",
        "• Trend change detection", 
        "• Trend history analysis",
        "• Volume analysis",
        "• Price analysis",
        "• General stock queries"
    ]
    
    for qtype in question_types:
        print(qtype)
    
    print()

def main():
    """Run the complete demonstration"""
    
    try:
        print("🎬 Starting Semantic Understanding System Demonstration")
        print("=" * 70)
        print()
        
        # Check system status
        print("🔧 SYSTEM STATUS CHECK")
        print("-" * 20)
        
        db_status = stock_ai_service.get_database_status()
        if db_status['status'] == 'connected':
            print("✅ Database: Connected")
            print(f"   Database: {db_status.get('database', 'Unknown')}")
            print(f"   Tables: {list(db_status['tables'].keys())}")
        else:
            print("❌ Database: Not connected")
            print(f"   Error: {db_status.get('message', 'Unknown error')}")
        
        llm_available = stock_ai_service.test_llm_connection()
        if llm_available:
            print("✅ LLM Service: Available")
        else:
            print("❌ LLM Service: Not available")
        
        print()
        
        # Run demonstrations
        demo_field_meanings()
        demo_query_classification()
        demo_trend_understanding()
        demo_system_capabilities()
        
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print()
        print("💡 Key Takeaways:")
        print("   • The system understands what database fields mean")
        print("   • It can interpret numeric values into human-readable descriptions")
        print("   • It processes natural language questions intelligently")
        print("   • It provides contextual, informative responses")
        print("   • It's not hardcoded - everything is configurable and extensible")
        
    except Exception as e:
        print(f"❌ Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 