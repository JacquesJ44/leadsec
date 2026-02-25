from flask import Blueprint

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')

def register_routes(app):
    """Register all routes with the app"""
    from . import jobcard_routes, auth_routes
    app.register_blueprint(api_bp)
