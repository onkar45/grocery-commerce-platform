#!/usr/bin/env python3
"""Test database connection"""

try:
    from app.db.session import engine
    print("Testing database connection...")
    
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Database connection successful!")
        print("Test query result:", result.fetchone())
        
except Exception as e:
    print(f"Database connection failed: {e}")
    print(f"Error type: {type(e).__name__}")