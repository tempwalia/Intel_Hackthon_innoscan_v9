"""
InnoScan Flask Application
Modular Flask app with routes and services separated into logical modules
"""

import sys
import os
import signal

# Add parent directories to path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from frontend.config import SECRET_KEY, DEBUG, HOST, PORT
from frontend.services.user_service import init_default_managers, init_default_employees
from frontend.routes.pages import register_page_routes
from frontend.routes.auth import register_auth_routes
from frontend.routes.submit import register_submit_routes
from frontend.routes.exceptions import register_exception_routes


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = SECRET_KEY
    app.config['SESSION_PERMANENT'] = True
    
    # Initialize default data files
    init_default_managers()
    init_default_employees()
    
    # Register all routes
    register_page_routes(app)
    register_auth_routes(app)
    register_submit_routes(app)
    register_exception_routes(app)
    
    # Error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404
    
    return app


# Graceful shutdown handler
def shutdown_handler(signum, frame):
    print("\n\n🛑 Shutting down gracefully...")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


if __name__ == '__main__':
    try:
        print("🚀 Starting Flask server on http://localhost:5001")
        print("Press Ctrl+C to stop the server gracefully\n")
        
        app = create_app()
        app.run(
            debug=DEBUG,
            port=PORT,
            host=HOST,
            use_reloader=False,
            threaded=True
        )
    
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Server error: {e}")
        sys.exit(1)
