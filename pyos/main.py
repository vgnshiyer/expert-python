from scheduler import Scheduler
from system_call import getTid, NewTask, KillTask

if __name__ == '__main__':
    def foo():
        mytid = yield getTid()
        while True:
            print(f"I'm foo, {mytid}")
            yield

    def main():
        child = yield NewTask(foo())
        for i in range(5):
            yield
        yield KillTask(child)
        print("main done")

    scheduler = Scheduler()
    scheduler.new(main())
    scheduler.mainloop()