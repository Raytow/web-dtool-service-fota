import os
basedir = os.path.abspath(os.path.dirname(__file__))


RESOURCE_DIR = '/web-dtool-service/src/app/resource/'

SITE_THIRDPARTY_DIR = '/web-dtool-service/src/app/third_party/'

SITE_DFOTA_DIR = '/web-dtool-service/src/app/resource/dfota/'
#SITE_DFOTA_URL = 'http://aaa.bbb.com/api/resource/dfota/'

TEMP_FILE_PATH = '/web-dtool-service/src/tmp/'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'g dtool rd to gues ols s?'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SESSION_COOKIE_NAME = "dtools session"
    
    # flask-session config
    SESSION_TYPE = 'sqlalchemy' #'null'#'sqlalchemy'
    SESSION_KEY_PREFIX = 'dtools_'
    SESSION_USE_SIGNER = True

    SESSION_SQLALCHEMY_TABLE = 'site_session'
    
    #SESSION_MONGODB = 
    #SESSION_MONGODB_DB = 'common_data'
    #SESSION_MONGODB_COLLECT = 'hz_tools_session'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://aaa:bbb@ccc:3306/dtools'
    SQLALCHEMY_BINDS = {
        'dtools':'mysql+mysqlconnector://aaa:bbb@ccc:3306/dtools'
    }
    SQLALCHEMY_POOL_SIZE = 256
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_MAX_OVERFLOW = 32


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql+mysqlconnector://gg:gg@localhost/gg'


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://aaa:bbb@ccc:3306/dtools'
    SQLALCHEMY_BINDS = {
        'dtools':'mysql+mysqlconnector://aaa:bbb@ccc:3306/dtools'
    }
    SQLALCHEMY_POOL_SIZE = 256
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_MAX_OVERFLOW = 32

config_list = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

