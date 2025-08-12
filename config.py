import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'institute-dating-secret-key-2025'
    
    # MongoDB Atlas Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://institute_dating_user:Sanichara54@dating.ccwswqz.mongodb.net/institute_dating?retryWrites=true&w=majority&appName=Dating'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Security Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application Configuration
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    UPLOAD_FOLDER = 'uploads'
    
    # Pagination
    USERS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 50
    
    # Email Configurations for different purposes
    # OTP and Account Verification Emails
    OTP_MAIL_SERVER = 'smtp.gmail.com'
    OTP_MAIL_PORT = 587
    OTP_MAIL_USE_TLS = True
    OTP_MAIL_USERNAME = 'surajkumarch110@gmail.com'  # Primary OTP email
    OTP_MAIL_PASSWORD = 'tkna qlfx bouq olwm'
    OTP_MAIL_DEFAULT_SENDER = 'surajkumarch110@gmail.com'
    
    # Notification and General Message Emails
    NOTIFICATION_MAIL_SERVER = 'smtp.gmail.com'
    NOTIFICATION_MAIL_PORT = 587
    NOTIFICATION_MAIL_USE_TLS = True
    NOTIFICATION_MAIL_USERNAME = 'mindcodex5@gmail.com'  # New email for notifications
    NOTIFICATION_MAIL_PASSWORD = 'bppw pjcr rltd mcyq'  # App password for Dating
    NOTIFICATION_MAIL_DEFAULT_SENDER = 'mindcodex5@gmail.com'
    
    # Welcome and Confirmation Emails
    WELCOME_MAIL_SERVER = 'smtp.gmail.com'
    WELCOME_MAIL_PORT = 587
    WELCOME_MAIL_USE_TLS = True
    WELCOME_MAIL_USERNAME = 'mindcodex5@gmail.com'  # Same email for welcome messages
    WELCOME_MAIL_PASSWORD = 'bppw pjcr rltd mcyq'  # App password for Dating
    WELCOME_MAIL_DEFAULT_SENDER = 'mindcodex5@gmail.com'

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
