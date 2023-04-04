import os

class Config:
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
    
class smpt:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

class ProductionConfig(config):
    iiCONNECTION_STRING = 'postgres://electapp-main-db-0fa618ed4ebf577c7:tucb65V2BzwXGwjEBv28ME3HqcAak2@user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com:5432/electapp-main-db-0fa618ed4ebf577c7'
    DEBUG = False

class StagingConfig(config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(config):
    TESTING = True
