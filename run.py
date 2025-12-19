#!/usr/bin/env python
"""
Annotation Daily HQ - Launcher Script

Run this script to start the application:
    python run.py

Or use uvicorn directly:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import uvicorn

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Annotation Daily HQ")
    print("=" * 50)
    print("\n  Starting server...")
    print("  Open your browser to: http://localhost:8000")
    print("\n  - Annotator Portal: http://localhost:8000/log")
    print("  - Team Dashboard:   http://localhost:8000/dashboard")
    print("\n  Press Ctrl+C to stop the server\n")
    print("=" * 50 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

