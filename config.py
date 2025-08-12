import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # MongoDB Atlas Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://institute_dating_user:Sanichara54@dating.ccwswqz.mongodb.net/institute_dating?retryWrites=true&w=majority&appName=Dating'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Security Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Pagination
    USERS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 50

class DevelopmentConfig(Config):
    DEBUG = True
    # Use MongoDB Atlas for development
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://institute_dating_user:Sanichara54@dating.ccwswqz.mongodb.net/institute_dating?retryWrites=true&w=majority&appName=Dating'

class ProductionConfig(Config):
    DEBUG = False
    # Production MongoDB Atlas connection
    MONGO_URI = os.environ.get('MONGO_URI')
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    # Test MongoDB Atlas connection
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://institute_dating_user:Sanichara54@dating.ccwswqz.mongodb.net/institute_dating_test?retryWrites=true&w=majority&appName=Dating'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
