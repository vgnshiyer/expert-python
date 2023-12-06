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

