from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    # Use environment variables for database connection
    DB_USER = os.getenv('DATABASE_USER', 'user')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
    DB_HOST = os.getenv('DATABASE_HOST', 'host')
    DB_PORT = 3306
    DB_NAME = "accounting_book"

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)