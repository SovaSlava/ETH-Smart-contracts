# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
from sqlalchemy import *
import sys

script_path = sys.argv[1]
conf = configparser.RawConfigParser()
conf.read(script_path + "config.conf")
db = conf.get("db", "sql")
token_update_time = int(conf.get("token", "update_time"))


engine = create_engine(db, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
import models
meta = MetaData()
meta.reflect(bind=engine)
def init_db():
    import models
    Base.metadata.create_all(bind=engine)