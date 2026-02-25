from flask import Flask
from flask_cors import CORS
from config import config
from app.models import db
from app.routes import register_routes
from flask_login import LoginManager
import os

def create_app(config_name=None):
    """Application factory"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    # Initialize Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'api.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None
    
    # Enable CORS and allow cookies for session-based auth
    CORS(app, resources={
        r"/api/*": {
            "origins": os.getenv('FRONTEND_URL', 'http://localhost:5173'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "credentials": True
        }
    }, supports_credentials=True)
    
    # Register routes
    register_routes(app)
    
    # Note: Database tables are created via Alembic migrations, not db.create_all()
    # db.create_all() is disabled to avoid conflicts with Alembic
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
