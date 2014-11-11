#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test meta programming
"""


class TableNotDefinedError(Exception):
    pass


class ModelMeta(type):
    """docstring for ModelMeta"""
    def __new__(cls, name, bases, args):
        if not("__table__" in args):
            raise TableNotDefinedError
        return super(ModelMeta, cls).__new__(cls, name, bases, args)

    def __call__(cls, **kwarg):
        obj = type.__call__(cls)

        if cls.__dict__["__table__"] is None:
            raise NotImplementedError

        sql = "CREATE TABLE %s(\n" % cls.__dict__["__table__"]

        for key, value in dict(cls.__dict__).items():
            if isinstance(value, Field):
                setattr(obj, key, kwarg.get(key, None))

                sql += str(value) + ",\n"

        sql = sql[0: len(sql)-2] + "\n);"
        cls.__sql__ = sql
        return obj


class Model(object):
    __metaclass__ = ModelMeta
    __table__ = None

    @classmethod
    def to_sql(cls):
        return cls.__dict__.get("__sql__", "")

    def __repr__(self):
        text = self.__class__.__name__ + "{"
        for key, value in self.__dict__.items():
            text += "%s => %s," % (key, value)
        return text[0: len(text)-1] + "}"


class Field(object):
    def __init__(self, fieldName):
        self.fieldName = fieldName
        self.value = None

    def __get__(self, obj, type=None):
        return obj.__dict__[self.fieldName]

    def __set__(self, obj, value):
        obj.__dict__[self.fieldName] = value

    def __del__(self, obj):
        del obj.__dict__[self.fieldName]
        del self.fieldName


class StringField(Field):
    def __init__(self, fieldName, fieldLen=255):
        super(StringField, self).__init__(fieldName)
        self.fieldLen = fieldLen

    def __set__(self, obj, value):
        if not(isinstance(value, str)):
            raise TypeError
        obj.__dict__[self.fieldName] = value[0:self.fieldLen]

    def __del__(self, obj):
        super(StringField, self).__del__(obj)
        del self.fieldLen

    def __repr__(self):
        return "%s VARCHAR(%d)" % (self.fieldName, self.fieldLen)


class IntegerField(StringField):
    def __init__(self, fieldName, fieldLen=11):
        super(StringField, self).__init__(fieldName)
        if (fieldLen > 11):
            self.fieldLen = 11
        else:
            self.fieldLen = fieldLen

    def __set__(self, obj, value):
        try:
            obj.__dict__[self.fieldName] = int(value)
        except ValueError:
            pass

    def __repr__(self):
        return "%s INT(%d)" % (self.fieldName, self.fieldLen)


class TextField(Field):
    def __get__(self, obj, type=None):
        return unicode(obj.__dict__[self.fieldName])

    def __repr__(self):
        return "%s TEXT" % self.fieldName


class Entry(Model):
    __table__ = "post"

    title = StringField("title", 150)
    description = TextField("description")
    comments = IntegerField("comments")


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    e = Entry(title="Test", description="TEXT TEXT TEXT", comments=10)
    e2 = Entry(title="Hello", description="Hello world!", comments=100)
    print e
    print e2
    print e.to_sql()
