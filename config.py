import os

class Config:
    class Smpt:
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
    
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        self.CONNECTION_STRING = 'postgres://{username}:{password}@{host}:{port}/{database}'.format(
            username=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            database=os.environ.get('DB_NAME')
        )
        self.SMTP = Config.Smpt()

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
