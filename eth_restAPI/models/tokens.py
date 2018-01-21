from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
import configparser
import sys

script_path = sys.argv[1]
conf = configparser.RawConfigParser()
conf.read(script_path + "config.conf")
token_update_time = int(conf.get("token", "update_time"))




class Token(Base):
    __tablename__ = 'tokens'

    def generate_uuid(self):
        return str(uuid.uuid4())

    id = Column(Integer, primary_key=True)
    user_id = Column(None, ForeignKey("users.id"), unique=True)
    user = relationship("User", uselist=False, backref='tokens')
    token = Column(String, default=generate_uuid)
    exp = Column(DateTime)

    def __init__(self, user_id):
        self.user_id = user_id
        self.exp = datetime.now() + timedelta(minutes=token_update_time)

    def exp_update(self):
        pass

    def __repr__(self):
        return self.token