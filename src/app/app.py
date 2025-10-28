
print(__file__)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if True:
    from flask_login import LoginManager
    
if True:
    from flask_session import Session

# from pymongo import MongoClient

if False:
    import redis

import config as config

#from app.tool import dbg # for print
import app.tool as tool

try:
    mysqldb = SQLAlchemy()
except:
    tool.print_exception_info()
    
# try:
#     mongodb = MongoClient(config.MONGODB_ADDRESS)
# except:
#     tool.print_exception_info()

if True:
    try:
        session = Session()
    except:
        tool.print_exception_info()
    
def create_new_db_connection():
    print("create_new_db_connection")
    global mysqldb
    mysqldb.session.remove()
    mysqldb.session = mysqldb.create_scoped_session(options = {'autocommit':False})

if True:
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    #login_manager.login_view = 'site.need_to_login'

def create_app(config_name):
    print("create_app")
    app = Flask(__name__, static_folder = "resource")
    app.config.from_object(config.config_list[config_name])
    config.config_list[config_name].init_app(app)

    #mysqldb.init_app(app)
    
    if True:
        login_manager.init_app(app)
    
    print(app.config)
    
    if False:
        session.init_app(app)
    
    from app.site.site import site_blueprint
    from flask import redirect

    app.register_blueprint(site_blueprint, url_prefix = '/site')

    @app.route('/')
    def index():
        return redirect('/site/')

    print('create_app() ok')
    return app
