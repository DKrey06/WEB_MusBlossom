import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///musblossom.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-here'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    CORS_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:8080']
    
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    
class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',') if os.environ.get('CORS_ORIGINS') else []

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}