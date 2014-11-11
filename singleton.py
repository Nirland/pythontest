#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Two basic ways of implementation singleton
"""


class Singleton(type):
    """Singleton meta"""

    instance = None

    def __call__(cls, *arg, **kwarg):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*arg, **kwarg)
        return cls.instance


class Test(object):
    """docstring for Test"""

    __metaclass__ = Singleton

    def __new__(cls, *arg, **kwarg):
        print "class created!"
        return super(Test, cls).__new__(cls, *arg, **kwarg)

    def __init__(self, arg):
        self.arg = arg


class TestMeta(object):
    __metaclass__ = Singleton


def singleton(klass):
    instances = {}

    def get_instance(*arg, **kwarg):
        if (instances.get(klass, None) is None):
            instances[klass] = klass(*arg, **kwarg)
        return instances[klass]

    return get_instance


@singleton
class KlassDecor(object):
    def __init__(self, arg):
        self.arg = arg


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    t = Test(2)
    t2 = Test(5)
    print t, t2
    print t.arg, t2.arg
    print "======================="
    kd = KlassDecor(7)
    kd2 = KlassDecor(10)
    print kd, kd2
