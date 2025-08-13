from flask import request, jsonify, g
import jwt
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_TOKEN, algorithms=['HS256'])
            g.user_id = data['user_id'] # Store user_id in Flask's global context
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

        return f(*args, **kwargs)
    return decorated
