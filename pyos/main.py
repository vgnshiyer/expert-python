from scheduler import Scheduler

if __name__ == '__main__':
    def foo():
        i = 5
        while i > 0:
            print("I am foo")
            yield
            i -= 1

    def bar():
        i = 10
        while i > 0:
            print("I am bar")
            yield
            i -= 1

    scheduler = Scheduler()
    scheduler.new(foo())
    scheduler.new(bar())
    scheduler.mainloop()