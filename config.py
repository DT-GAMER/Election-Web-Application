import os

class config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    CONNECTION_STRING = 'postgres://electapp-main-db-0fa618ed4ebf577c7:tucb65V2BzwXGwjEBv28ME3HqcAak2@user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com:5432/electapp-main-db-0fa618ed4ebf577c7'.format(
        USERNAME=os.environ.get('electapp-main-db-0fa618ed4ebf577c7'),
        PASSWORD=os.environ.get('tucb65V2BzwXGwjEBv28ME3HqcAak2'),
        DATABASE_HOST=os.environ.get('user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com'),
        DATABASE_PORT=os.environ.get('5432'),
        DATABASE_NAME=os.environ.get('electapp-main-db-0fa618ed4ebf577c7')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
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
