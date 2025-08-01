#!/usr/bin/env python3
"""
Check database schema
"""

from database.connection import db

def check_schema():
    """Check database schema"""
    print("=== Database Schema Check ===\n")
    
    result = db.test_connection()
    print(f"Connection status: {result['status']}")
    
    if result['status'] == 'connected':
        print(f"Database: {result['database']}")
        print(f"Tables: {list(result['tables'].keys())}")
        
        print("\n=== Table Details ===")
        for table_name, columns in result['tables'].items():
            print(f"\nTable: {table_name}")
            print("Columns:")
            for col in columns:
                print(f"  - {col['field']} ({col['type']})")
                if col['null'] == 'NO':
                    print("    [NOT NULL]")
                if col['key'] == 'PRI':
                    print("    [PRIMARY KEY]")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    check_schema() 