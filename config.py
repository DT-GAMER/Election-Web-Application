import os

class Config:
    def __init__(self, username='default_username', password='default_password', host='default_host', port=None, database='default_database'):
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        if port is None:
            self.CONNECTION_STRING = 'postgres://{username}:{password}@{host}/{database}'.format(
                username=username,
                password=password,
                host=host,
                database=database
            )
        else:
            self.CONNECTION_STRING = 'postgres://{username}:{password}@{host}:{port}/{database}'.format(
                username=username,
                password=password,
                host=host,
                port=port,
                database=database
            )
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587

config = Config()
config.username = 'electoralcollege-main-db-00e2a4d1aa8d4f008'
config.password = 'AgaEqVczsdQYytD362kWxUvSd5JsWc'
config.host = 'user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com'
config.port = None  # Set port to None to use default port
config.database = 'electoralcollege-main-db-00e2a4d1aa8d4f008'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
