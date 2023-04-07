import os

class Config:
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        self.CONNECTION_STRING = 'postgres://electoralcollege-main-db-00e2a4d1aa8d4f008:AgaEqVczsdQYytD362kWxUvSd5JsWc@user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com:5432/electoralcollege-main-db-00e2a4d1aa8d4f008'.format(
            username=os.environ.get('electoralcollege-main-db-00e2a4d1aa8d4f008'),
            password=os.environ.get('AgaEqVczsdQYytD362kWxUvSd5JsWc'),
            host=os.environ.get('user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com'),
            port=os.environ.get('5432'),
            database=os.environ.get('electoralcollege-main-db-00e2a4d1aa8d4f008')
        )
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
