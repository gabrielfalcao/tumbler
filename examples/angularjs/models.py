# -*- coding: utf-8 -*-
#
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from tumbler import Model


class Person(Model):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    date_added = Column(DateTime, default=datetime.utcnow)
