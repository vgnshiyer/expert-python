from scheduler import Scheduler
from system_call import getTid

if __name__ == '__main__':
    def foo():
        mytid = yield getTid()
        i = 5
        while i > 0:
            print("I am foo")
            yield
            i -= 1

    def bar():
        mytid = yield getTid()
        i = 10
        while i > 0:
            print("I am bar")
            yield
            i -= 1

    scheduler = Scheduler()
    scheduler.new(foo())
    scheduler.new(bar())
    scheduler.mainloop()