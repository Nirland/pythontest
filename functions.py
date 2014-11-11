#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test functional opportunities of Python
"""

from time import strftime


def function(*args, **kwargs):
    for item in args:
        if (isinstance(item, list) or
                isinstance(item, tuple) or isinstance(item, set)):
            function(*item)
        elif (isinstance(item, dict)):
            function(**item)

        if not(isinstance(item, list) or isinstance(item, dict) or
                isinstance(item, tuple) or isinstance(item, set)):
                    print item,

    for key, item in kwargs.items():
        if (isinstance(item, list) or
                isinstance(item, tuple) or isinstance(item, set)):
            function(*item)
        elif (isinstance(item, dict)):
            function(**item)

        if not(isinstance(item, list) or isinstance(item, dict) or
                isinstance(item, tuple) or isinstance(item, set)):
            print "{%s=>%s}" % (key, item),


def decorator(func):
    text = "!"

    def adder(*args, **kwargs):
        print "Decorator starts at " + strftime("%d-%m-%y %H:%M")
        return func(*args, **kwargs) + text
    return adder


class ClassDecor(object):
    funcs = {}

    @classmethod
    def addfunc(cls, func):
        cls.funcs[func.__name__] = func

        def closure(*arg, **kwarg):
            return func(*arg, **kwarg)
        return closure


@decorator
@ClassDecor.addfunc
def hello(name="Nir"):
    return "Hello %s" % name


def gen(start=0, end=10, step=1):
    i = start
    while i < end:
        yield i
        i = i + step


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    n = 7
    print reduce(lambda x, y: x*y, xrange(1, n))

    l = [x for x in xrange(10)]
    print l[::2], l[1::2], l * 3
    print map(lambda x, y, z: x*y*z, l, l, l)
    print filter(lambda x: x % 2 == 0, l)

    l2 = [x for x in gen(1, 11, 2)]
    print l2

    s1, s2 = set(l), set(l2)
    print s1, s2, s1 - s2, s2 - s1, s1 & s2, s1 | s2

    d = dict(zip(l, sorted(l, reverse=True)))
    t = sorted(d.items(), key=lambda item: item[1])
    print d, t

    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print [a[i][j] for i in xrange(len(a)) for j in xrange(len(a[i])) if i < j]

    print hello(), hello() * 2
    print ClassDecor.funcs

    function(1, 2, 3, 4, 5, [10, 15, "test", "azaza"],
             *["nonono", "hi"], name="nir", lvl=80,
             ht=("tup1", "tup2", "tup3"), **{"class": "pal", "ad": 90})
