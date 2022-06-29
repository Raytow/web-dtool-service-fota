print(__file__)

import json

'''
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from app import mysqldb as db

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, Float, String, Text, Table, Boolean, UniqueConstraint, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

import config as config

ROLE_USER = 0
ROLE_GOD = 1
ROLE_AGENT = 2
ROLE_FACTORY = 3

class User(UserMixin, db.Model):
    __bind_key__ = 'user'
    __tablename__ = 'user'
    __table_args__ = {'schema':config.USER_SCHEMA, 'extend_existing':True}
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True, index = True, nullable = False)
    phone = db.Column(db.String(24), unique = True, nullable = False)
    email = db.Column(db.String(64), unique = True, index = True, nullable = False)
    role = db.Column(db.String(32), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    creator_id = Column(Integer, nullable = False)
    last_login_time = Column(DateTime, nullable = False)
    creation_time = Column(DateTime, nullable = False)
    
    address = db.Column(db.String(32), nullable = False)
    
    erp_role = db.Column(db.String(32), nullable = False)
    
    # sim
    company = db.Column(db.String(24), nullable = False)
    qq = db.Column(db.String(12), nullable = False)
    
    wangwang = db.Column(db.String(32), nullable = False)
    
    # imei order
    invoice_company = db.Column(db.String(24), nullable = False)
    bank = db.Column(db.String(32), nullable = False)
    bank_account = db.Column(db.String(32), nullable = False)
    tax_number = db.Column(db.String(32), nullable = False)
    fixed_phone = db.Column(db.String(24), nullable = False)
    shipping_address = db.Column(db.String(32), nullable = False)
    recipient = db.Column(db.String(32), nullable = False)
    recipient_phone = db.Column(db.String(24), nullable = False)
    
    @staticmethod
    def __init__(self, *initial_data, **kwargs): #def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
        
    def is_user(self):
        #return int(self.role[3]) == ROLE_USER
        return True
        
    def is_god(self):
        #return int(self.role[3]) == ROLE_GOD
        #return self.erp_role[0] == '1' or self.id in [701, 14379]
        return self.role[6] == '1'
        
    def is_agent(self):
        #return int(self.role[3]) == ROLE_AGENT
        return self.role[6] == '2'
        
    def is_factory(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[2] == '1'
    
    def is_rd(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[3] == '1'
    
    def is_fae(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[4] == '1'
        
    def is_customer(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[5] == '1'
        
    def is_help(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[6] == '1'
        
    def is_accountant(self):
        #return int(self.role[3]) == ROLE_FACTORY
        return self.erp_role[7] == '1'

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    '''
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    '''

    def generate_reset_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email = new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.name
'''

            