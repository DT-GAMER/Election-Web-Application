import os

class config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:k0r0.day@localhost:5432/electiondb'.format(
        DB_USER=os.environ.get('postgres'),
        DB_PASSWORD=os.environ.get('k0r0.day'),
        DB_HOST=os.environ.get('localhost'),
        DB_PORT=os.environ.get('5432'),
        DB_NAME=os.environ.get('electiondb')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class smpt:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
