# -*- coding: utf-8 -*-
#

from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    DateTime,
    String,
)
from datetime import datetime
from tumbler import Model


def now():
    return datetime.utcnow()


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    email = Column(Unicode(100), nullable=False)
    password = Column(String(128), nullable=False)
    date_added = Column(DateTime, default=now)

    def match_password(self, plain):
        return self.password == bcrypt.hashpw(
            plain, self.password)

    @classmethod
    def secretify_password(cls, plain):
        return bcrypt.hashpw(plain, bcrypt.gensalt(12))
