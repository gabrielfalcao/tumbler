#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from collections import OrderedDict
from sqlalchemy import Column
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.sqlalchemy import Model as BaseModel
from flask.ext.sqlalchemy import _BoundDeclarativeMeta


MODELS = OrderedDict()


class ORM(_BoundDeclarativeMeta):
    def __init__(cls, name, bases, attrs):
        super(ORM, cls).__init__(name, bases, attrs)

        if cls.__module__ == __name__ or name == 'Model':
            return

        MODELS[name] = cls


class Model(BaseModel):
    __metaclass__ = ORM
    __abstract__ = True

    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    @classmethod
    def prepare_data_for_query(self, kw):
        data = {}
        columns = dict([(k, v) for k, v in self.__dict__.items() if isinstance(v, Column)])

        for attr in columns.keys():
            if attr in kw:
                data[attr] = kw[attr]

        return data

    @classmethod
    def create(cls, **kw):
        obj = cls.Table(**cls.prepare_data_for_query(kw))
        cls.__session__.add(obj)
        cls.__session__.commit()
        cls.__session__.flush()

        return obj

    @classmethod
    def all(cls):
        objs = cls.__session__.query(cls.Table).order_by('-id')
        return objs

    @classmethod
    def get_by(cls, **kw):
        try:
            obj = cls.__session__.query(cls.Table).filter_by(**cls.prepare_data_for_query(kw)).one()
        except NoResultFound:
            return None

        return obj

    @classmethod
    def get_or_create_by(cls, **kw):
        result = cls.get_by(**kw)
        if not result:
            result = cls.create(**kw)

        return result

    def set(self, **kw):
        kw = self.prepare_data_for_query(kw)

        for key, value in kw.items():
            setattr(self, key, value)

    def save(self):
        result = self.__session__.merge(self)
        return result

    def to_dict(self):
        return self.serialize()

    def serialize(self):
        result = {}

        for attr in self.__columns__.keys():
            col = self.__columns__[attr]
            default = None
            if col.default:
                default = col.default.arg

            result[attr] = getattr(self, attr, default)

        return result
