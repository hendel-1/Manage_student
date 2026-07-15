"""
Entry point for the Flask REST API.

Run with:
    python main_web.py
"""
from src.frameworks.web.flask_app import create_app

if __name__ == "__main__":
    app = create_app()
    print("\n  Clean Architecture Student Attendance — REST API")
    print("  Running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
