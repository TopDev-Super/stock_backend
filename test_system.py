#!/usr/bin/env python3
"""
Test script for Stock AI Analysis System
"""

import asyncio
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_config():
    """Test configuration loading"""
    try:
        from config import config
        logger.info("✓ Configuration loaded successfully")
        logger.info(f"  Database: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
        logger.info(f"  OpenAI API Key: {'✓ Set' if config.OPENAI_API_KEY else '✗ Missing'}")
        logger.info(f"  App Host: {config.APP_HOST}:{config.APP_PORT}")
        return True
    except Exception as e:
        logger.error(f"✗ Configuration error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database.connection import db
        status = db.test_connection()
        
        if status['status'] == 'connected':
            logger.info("✓ Database connection successful")
            logger.info(f"  Database: {status['database']}")
            logger.info(f"  Tables: {list(status['tables'].keys())}")
            return True
        else:
            logger.error(f"✗ Database connection failed: {status.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        logger.error(f"✗ Database connection error: {e}")
        return False

def test_llm_service():
    """Test LLM service"""
    try:
        from ai.llm_service import llm_service
        if llm_service.llm is not None:
            logger.info("✓ LLM service initialized successfully")
            return True
        else:
            logger.error("✗ LLM service not initialized")
            return False
    except Exception as e:
        logger.error(f"✗ LLM service error: {e}")
        return False

def test_stock_ai_service():
    """Test stock AI service"""
    try:
        from services.stock_ai_service import stock_ai_service
        
        # Test database status
        db_status = stock_ai_service.get_database_status()
        if db_status['status'] == 'connected':
            logger.info("✓ Stock AI service database connection OK")
        else:
            logger.warning(f"⚠ Stock AI service database issue: {db_status.get('message', 'Unknown')}")
        
        # Test LLM connection
        if stock_ai_service.test_llm_connection():
            logger.info("✓ Stock AI service LLM connection OK")
        else:
            logger.warning("⚠ Stock AI service LLM connection issue")
        
        return True
    except Exception as e:
        logger.error(f"✗ Stock AI service error: {e}")
        return False

def test_api_imports():
    """Test API imports"""
    try:
        from api.main import app
        logger.info("✓ API imports successful")
        return True
    except Exception as e:
        logger.error(f"✗ API import error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("Stock AI Analysis System - System Test")
    logger.info("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Database Connection", test_database_connection),
        ("LLM Service", test_llm_service),
        ("Stock AI Service", test_stock_ai_service),
        ("API Imports", test_api_imports),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nTesting {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Results Summary")
    logger.info("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! System is ready to run.")
        logger.info("\nTo start the server, run:")
        logger.info("  python run.py")
        logger.info("\nOr visit the API documentation at:")
        logger.info("  http://localhost:8000/docs")
    else:
        logger.error("❌ Some tests failed. Please check the configuration and dependencies.")
        logger.info("\nCommon issues:")
        logger.info("  1. Check your .env file configuration")
        logger.info("  2. Ensure MySQL server is running")
        logger.info("  3. Verify OpenAI API key is set")
        logger.info("  4. Install all dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 