from flask import Flask
from .database import get_db, close_connection, check_connection

def create_app():
    app = Flask(__name__)
    # ...existing code...
    
    if not check_connection():
        raise Exception("Failed to connect to the database.")
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_connection(exception)
    
    # ...existing code...
    return app
