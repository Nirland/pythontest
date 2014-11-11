#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test multiprocessing in Python on simple file finder.
In my cases parallel finder owns sequence finder on 50%!
"""
import multiprocessing as mp
import re
import os
import sys
import time


class FileTester(mp.Process):

    def __init__(self, queue, result, pattern):
        super(FileTester, self).__init__()
        self.queue = queue
        self.daemon = True
        self.matcher = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        self.result = result

    def run(self):
        while True:
            signal, filepath = self.queue.get()
            if not signal:
                return

            text = ""
            try:
                f = open(filepath, 'r')
                text = f.read().replace('\n', '')
            except IOError:
                print "File not found"
            finally:
                f.close()

            if (len(text) > 0) and (self.matcher.search(text) is not None):
                self.result.put(filepath)


class FileRunner(object):

    def __init__(self, queue, path=os.getcwd()):
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise Exception("Path not found")

        self.queue = queue

    def run(self, path=None):
        if path is None:
            path = self.path

        for item in os.listdir(path):
            fullpath = os.path.join(path, item)
            if os.path.isdir(fullpath):
                self.run(fullpath)

            if (os.path.isfile(fullpath)):
                self.queue.put((1, fullpath))


class SequenceFileRunner(object):

    def __init__(self, pattern, path=os.getcwd()):
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise Exception("Path not found")
        self.matcher = re.compile(pattern, re.IGNORECASE | re.MULTILINE)

    def run(self, path=None):
        if path is None:
            path = self.path

        for item in os.listdir(path):
            fullpath = os.path.join(path, item)
            if os.path.isdir(fullpath):
                self.run(fullpath)

            if (os.path.isfile(fullpath)):
                text = ""
                try:
                    f = open(fullpath, 'r')
                    text = f.read().replace('\n', '')
                except IOError:
                    print "File not found"
                finally:
                    f.close()

                if (len(text) > 0) and (self.matcher.search(text) is not None):
                    print fullpath


###========================================================================
###========================================================================
###========================================================================


if __name__ == "__main__":
    numcores = 2

    if (len(sys.argv) < 3):
        sys.exit()

    pattern, path = sys.argv[1], sys.argv[2]
    print "Parralel finder starts..."
    start = time.time()
    queue = mp.Queue()
    result = mp.Queue()
    testers = []
    for i in range(numcores):
        testers.append(FileTester(queue, result, pattern))

    for tester in testers:
        tester.start()

    fr = FileRunner(queue, path)
    fr.run()

    for tester in testers:
        queue.put((0, None))

    for tester in testers:
        tester.join()

    while (result.qsize()):
        print result.get()

    end = time.time() - start
    print "Done! Execution time: %.3f" % end
    print "=================================="

    print "Sequence Finder starts..."
    start = time.time()
    fr = SequenceFileRunner(pattern, path)
    fr.run()
    end = time.time() - start
    print "Done! Execution time: %.3f" % end
