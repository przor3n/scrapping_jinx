#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wykoppl.env import DB_CONNECTION

# this has to be only one
# engine = create_engine('sqlite:///file.db')
engine = create_engine(DB_CONNECTION)

assert engine, 'Engine not set'

Session = sessionmaker(bind=engine)
session = Session() # use session object

assert session, 'Session not set'
