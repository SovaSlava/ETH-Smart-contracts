#from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(120), unique=True)
    password = Column(String(120))
    secret = Column(String(120))
    nonce = Column(Integer)
    nonce2 = Column(Integer)

    def __init__(self, login=None, password=None, secret=None, nonce=None):
        self.login = login
        self.password = password
        self.secret = secret
        self.nonce = 1
        
    def __repr__(self):
        return '<User %r>' % (self.login)