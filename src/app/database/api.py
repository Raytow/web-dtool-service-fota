
print(__file__)

'''
from .. import mysqldb, login_manager

print('import model')
from . model import * # mysql
import config as config

from flask import request

from datetime import datetime, timedelta
import traceback
import random
import time
import json
import re

# sqlalchemy
from sqlalchemy import text, desc, func, and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


import app.tool as tool
from app.tool import dbg # for print
import app.error as error

class DatabaseError(Exception):
    def __init__(self, msg = "", error_no = 0):
        self.msg = msg
        self.error_no = error_no
        
    def __str__(self):
        return repr(self.msg)
        
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
    

def get_user(**kwargs):
    try:
        if 'user' in kwargs:
            return kwargs['user']
        elif "phone" in kwargs:
            return request.mysqldb_session.query(User).filter(User.phone == kwargs['phone']).one()
        elif "user_id" in kwargs:
            user = request.mysqldb_session.query(User).filter(User.id == kwargs['user_id']).one()
            return user
        elif "name" in kwargs:
            return request.mysqldb_session.query(User).filter(User.name == kwargs['name']).one()
        elif "email" in kwargs:
            return request.mysqldb_session.query(User).filter(User.email == kwargs['email']).one()
        else:
            return None
    except NoResultFound:
        return None
    except:
        tool.print_exception_info()
        raise DatabaseError()
        
@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id = user_id)
    
'''