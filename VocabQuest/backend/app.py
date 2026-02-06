import socket
import json
import os
import logging
from flask import Flask
from flask_cors import CORS
from extensions import limiter

# Blueprints
from blueprints.vocab_routes import vocab_bp
from blueprints.math_routes import math_bp
from blueprints.comprehension_routes import comprehension_bp
from blueprints.mock_routes import mock_bp
from blueprints.core_routes import core_bp

from seeder import seed_database

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
env_frontend = os.environ.get("FRONTEND_URL")
if env_frontend:
    allowed_origins.append(env_frontend)

CORS(app, resources={r"/*": {"origins": allowed_origins}})

# Initialize Limiter
limiter.init_app(app)

# Register Blueprints
app.register_blueprint(vocab_bp)
app.register_blueprint(math_bp)
app.register_blueprint(comprehension_bp)
app.register_blueprint(mock_bp)
app.register_blueprint(core_bp)

@app.cli.command("seed-db")
def seed_db_command():
    """Seeds the database with initial data."""
    seed_database()
    print("Database seeded successfully.")

def find_available_port(start_port, max_port=5100):
    """Finds the first available port in the range."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('0.0.0.0', port)) != 0:
                return port
    return start_port

if __name__ == '__main__':
    port = find_available_port(5000)
    app.run(host='0.0.0.0', port=port)
