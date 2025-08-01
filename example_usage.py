#!/usr/bin/env python3
"""
Example usage of the trend analysis system
"""

import requests
import json

# API base URL (adjust if your server runs on different port)
BASE_URL = "http://localhost:8000"

def test_natural_language_queries():
    """Test natural language queries"""
    
    print("=== Natural Language Query Examples ===\n")
    
    # Example questions
    questions = [
        "What is the trend on symbol 230011 today?",
        "When was the last time symbol 230011 moved from uptrend to downtrend?",
        "Show me the trend history for symbol 230011",
        "How is symbol 230011 trending?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"Question {i}: {question}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 'success':
                    print(f"✓ Answer: {result.get('explanation', 'No explanation')}")
                    if result.get('query_type') == 'trend_analysis':
                        print(f"  Trend analysis detected!")
                else:
                    print(f"✗ Error: {result.get('error_message', 'Unknown error')}")
            else:
                print(f"✗ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Request failed: {e}")
        
        print()

def test_direct_api_endpoints():
    """Test direct API endpoints"""
    
    print("=== Direct API Endpoint Examples ===\n")
    
    symbol = "230011"
    
    # Test current trend
    print(f"1. Getting current trend for {symbol}...")
    try:
        response = requests.post(f"{BASE_URL}/trend/current/{symbol}")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"✓ Current trend: {result['trend_description']} (value: {result['current_trend']})")
                print(f"✓ Date: {result['date']}")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    print()
    
    # Test trend changes
    print(f"2. Getting trend changes for {symbol}...")
    try:
        response = requests.post(f"{BASE_URL}/trend/changes/{symbol}")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"✓ Found {result['total_changes']} trend changes")
                if result['trend_changes']:
                    latest = result['trend_changes'][0]
                    print(f"✓ Latest change: {latest['date']} from {latest['from_trend_desc']} to {latest['to_trend_desc']}")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    print()
    
    # Test trend history
    print(f"3. Getting trend history for {symbol} (last 7 days)...")
    try:
        response = requests.post(f"{BASE_URL}/trend/history/{symbol}?days=7")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"✓ Found {result['total_days']} days of history")
                if result['history']:
                    print(f"✓ Latest entry: {result['history'][0]['date']} - {result['history'][0]['trend_description']}")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    print()
    
    # Test comprehensive analysis
    print(f"4. Getting comprehensive analysis for {symbol}...")
    try:
        response = requests.post(f"{BASE_URL}/trend/analysis/{symbol}")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                stats = result['statistics']
                print(f"✓ Analysis complete:")
                print(f"  - Current trend: {result['current_trend']['trend_description']}")
                print(f"  - Total trend changes: {stats['total_trend_changes']}")
                print(f"  - Days analyzed: {stats['days_analyzed']}")
                print(f"  - Trend distribution: {stats['trend_distribution']}")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

def test_specific_trend_changes():
    """Test specific trend change queries"""
    
    print("=== Specific Trend Change Examples ===\n")
    
    symbol = "230011"
    
    # Test uptrend to downtrend
    print(f"1. Finding when {symbol} moved from uptrend to downtrend...")
    try:
        response = requests.post(f"{BASE_URL}/trend/changes/{symbol}?from_trend=1&to_trend=2")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                if result['trend_changes']:
                    for change in result['trend_changes']:
                        print(f"✓ {change['date']}: {change['from_trend_desc']} → {change['to_trend_desc']}")
                else:
                    print("✓ No uptrend to downtrend changes found")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")
    
    print()
    
    # Test downtrend to uptrend
    print(f"2. Finding when {symbol} moved from downtrend to uptrend...")
    try:
        response = requests.post(f"{BASE_URL}/trend/changes/{symbol}?from_trend=2&to_trend=1")
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                if result['trend_changes']:
                    for change in result['trend_changes']:
                        print(f"✓ {change['date']}: {change['from_trend_desc']} → {change['to_trend_desc']}")
                else:
                    print("✓ No downtrend to uptrend changes found")
            else:
                print(f"✗ Error: {result['message']}")
        else:
            print(f"✗ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Request failed: {e}")

if __name__ == "__main__":
    print("Stock Trend Analysis System - Example Usage")
    print("=" * 50)
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Server is running!")
        else:
            print("✗ Server is not responding properly")
            exit(1)
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        print("Make sure the server is running on http://localhost:8000")
        exit(1)
    
    print()
    
    # Run examples
    test_natural_language_queries()
    test_direct_api_endpoints()
    test_specific_trend_changes()
    
    print("=== Example usage completed ===") 