import socket
from flask import Flask
from flask_cors import CORS
from extensions import limiter
from seeder import init_db

# Blueprints
from blueprints.vocab_routes import vocab_bp
from blueprints.math_routes import math_bp
from blueprints.comprehension_routes import comprehension_bp
from blueprints.mock_routes import mock_bp
from blueprints.core_routes import core_bp

app = Flask(__name__)
CORS(app)

# Initialize Limiter
limiter.init_app(app)

# Register Blueprints
app.register_blueprint(vocab_bp)
app.register_blueprint(math_bp)
app.register_blueprint(comprehension_bp)
app.register_blueprint(mock_bp)
app.register_blueprint(core_bp)

def find_available_port(start_port, max_port=5100):
    """Finds the first available port in the range."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('0.0.0.0', port)) != 0:
                return port
    return start_port

if __name__ == '__main__':
    # Initialize Data
    with app.app_context():
        init_db()

    port = find_available_port(5000)
    app.run(host='0.0.0.0', port=port)
