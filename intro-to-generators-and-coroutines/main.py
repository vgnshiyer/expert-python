# 1]
def countdown(n):
    print(f"counting down from {n}")
    while n > 0:
        yield n
        n -= 1
    print("done counting")

for i in countdown(10):
    print(i)

# 2] follow.py : `tail -f` implementation
import time

def follow(thefile):
    thefile.seek(0, 2) # go to the end of file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # sleep briefly
            continue
        yield line

logfile = open('access-log')
for line in follow(logfile):
    print(line)

# 3] pipeline.py

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

logfile = open("access-log")
loglines = follow(logfile) # loglines is a generator of all log lines
plines = grep("python", loglines) # plines is a generator of all log lines with pattern python

for line in plines:
    print(line)

# 4] simple coroutine

def grep(pattern):
    print(f"Looking for {pattern}")
    while True:
        line = (yield)
        if pattern in line:
            print(line)

g = grep("python")
g.send(None) # priming it -> so that it goes through the first yield
g.send("Ayy.. Here to learn about generators!")
g.send("python comes now")

# 5] A decorator to prime a coroutine

