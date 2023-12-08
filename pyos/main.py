from scheduler import Scheduler

if __name__ == '__main__':
    def foo():
        while True:
            print("I am foo")
            yield

    def bar():
        while True:
            print("I am bar")
            yield

    scheduler = Scheduler()
    scheduler.new(foo())
    scheduler.new(bar())
    scheduler.mainloop()