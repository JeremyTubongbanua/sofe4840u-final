import os
from datetime import timedelta

class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-change-this-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or None  # Should be set in production
    PASSWORD_RESET_EXPIRATION = timedelta(hours=1)
    JWT_EXPIRATION = timedelta(hours=1)
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCKOUT_DURATION = timedelta(minutes=15)
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Pagination settings
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 20
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100/hour"
    RATELIMIT_STORAGE_URL = "memory://"


class DevelopmentConfig(Config):
    DEBUG = True
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    

class ProductionConfig(Config):
    # Production settings should be set through environment variables
    
    def __init__(self):
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable is not set")
        
        if not os.environ.get('ENCRYPTION_KEY'):
            raise ValueError("ENCRYPTION_KEY environment variable is not set")


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
