def prime_it(func):
    def wrapper(*a, **kw):
        f = func(*a, **kw)
        f.send(None)
        return f
    return wrapper

# 1] cofollow -> hooking a coroutine with another
import time
def follow(thefile, target):
    thefile.seek(0, 2) # go the EOF
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(.1)
            continue
        target.send(line) # sink

@prime_it
def printer():
    while True:
        line = (yield)
        print(line)

f = open("access-log")
follow(f, printer())

# 2] copipe

import time
def follow(thefile, target):
    thefile.seek(0, 2) # go the EOF
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(.1)
            continue
        target.send(line) # sink

@prime_it
def grep(pattern, target):
    while True:
        line = (yield) # receive a line
        if pattern in line:
            target.send(line) # send to next stage

@prime_it
def printer():
    while True:
        line = (yield)
        print(line)

f = open("access-log")
follow(f,
        grep("python", printer()))

# 3] benchmark -- coroutine vs objects

def GrepHandler(object):
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target
    def send(self, line):
        if self.pattern in line:
            self.target.send(line)

@prime_it
def grep(pattern, target):
    while True:
        line = (yield) # receive a line
        if pattern in line:
            target.send(line) # send to next stage

@prime_it
def null():
    while True:
        item = (yield)

from timeit import timeit
line = 'python is nice'
p1 = grep('python', null())
p2 = GrepHandler("python", null())

print("coroutine:", timeit("p1.send(line)", "from __main__ import line, p1"))
print("object:", timeit("p2.send(line)", "from __main__ import line, p2"))