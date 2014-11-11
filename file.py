#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test random and file api
"""

import os
import random
from datetime import datetime
import sys


class Logger(object):

    """
    Class doc
    """

    def __init__(self, frm='log', count=5):
        super(Logger, self).__init__()
        self.format = frm
        self.count = count
        self.alpha = "abcdefghijklmnopqrstuvwxyz0123456789"

    def get_filename(self, num=1):
        date = datetime.now()
        return "log%d_%d_%d_%d-%d_%d.%s" % \
            (num, date.day, date.month, date.year,
                date.hour, date.minute, self.format)

    def get_random_string(self):
        return ''.join(random.choice(self.alpha)
                       for i in xrange(random.randrange(len(self.alpha))))

    def create_files(self):
        for i in range(1, self.count + 1):
            realpath = os.path.join(os.getcwd(), self.get_filename(i))
            if os.path.isfile(realpath):
                continue
            try:
                f = open(realpath, "w")
                f.writelines(self.get_random_string() + '\n'
                             for j in xrange(random.randint(1, 100)))
            except:
                continue
            finally:
                f.close()


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    ext = ''
    count = 5
    if (sys.argv is not None) and (len(sys.argv) > 2):
        try:
            ext = str(sys.argv[1])
            count = int(sys.argv[2])
        except TypeError:
            print "Not correct parameters"
        except:
            print "Not correct parameters"

    log = Logger(ext, count)
    log.create_files()
    raw_input("Done! Press any key...")
