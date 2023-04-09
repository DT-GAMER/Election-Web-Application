import os

class Config:
    def __init__(self, username, password, host, port, database):
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        self.CONNECTION_STRING = 'postgres://{username}:{password}@{host}:{port}/{database}'.format(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587

config = Config(
    username='electoralcollege-main-db-00e2a4d1aa8d4f008',
    password='AgaEqVczsdQYytD362kWxUvSd5JsWc',
    host='user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com',
    port='5432',
    database='electoralcollege-main-db-00e2a4d1aa8d4f008'
)

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
