"""
    app.py
    Main entry point to run the Flask application using the app package.
"""

from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
