from app import db, bcrypt
from app.models.user import User
from app.utils.validators import validate_email, validate_password
import datetime
import jwt
from flask import current_app

class AuthService:
    @staticmethod
    def register(data):
        # Validate input
        if not all(field in data for field in ['username', 'email', 'password']):
            return {'message': 'Missing required fields'}, 400

        if not validate_email(data['email']):
            return {'message': 'Invalid email format'}, 400

        is_valid_password, password_message = validate_password(data['password'])
        if not is_valid_password:
            return {'message': password_message}, 400

        if len(data['username']) < 3:
            return {'message': 'Username must be at least 3 characters long'}, 400

        # Check existing users
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 409
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already taken'}, 409

        # Create new user
        try:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(
                username=data['username'],
                email=data['email'].lower(),
                password=hashed_password
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'message': 'Registered successfully!',
                'user': new_user.to_dict
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Registration failed', 'error': str(e)}, 500

    @staticmethod
    def login(data):
        try:
            if not all(k in data for k in ['email', 'password']):
                return {'message': 'Missing email or password'}, 400
                
            user = User.query.filter_by(email=data['email'].lower()).first()
            if user and bcrypt.check_password_hash(user.password, data['password']):
                token = jwt.encode({
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                    'iat': datetime.datetime.utcnow()
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                
                return {
                    'message': 'Login successful',
                    'token': token,
                    'user': user.to_dict
                }, 200
                
            return {'message': 'Invalid email or password'}, 401
            
        except Exception as e:
            return {'message': 'Login failed', 'error': str(e)}, 500

    @staticmethod
    def logout():
        try:
            # In a more complex implementation, you might want to blacklist the token
            # For now, we'll just return a success message as the client should
            # remove the token from their storage
            return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            return {'message': 'Logout failed', 'error': str(e)}, 500 