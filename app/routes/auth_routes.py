from flask import request, jsonify
from app.routes import api_bp
from app.models import db, User
from flask_login import login_user, logout_user, current_user, login_required


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user (consider disabling in production)."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password:
            return jsonify({'error': 'username and password required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'username already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login with username and password (sets server session cookie)."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'username and password required'}), 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        login_user(user)
        return jsonify({'message': 'Logged in', 'user': {'id': user.id, 'username': user.username}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200


@api_bp.route('/auth/me', methods=['GET'])
def me():
    if current_user and current_user.is_authenticated:
        return jsonify({'user': {'id': current_user.id, 'username': current_user.username}}), 200
    return jsonify({'user': None}), 200
