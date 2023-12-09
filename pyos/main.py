from scheduler import Scheduler
from system_call import getTid, NewTask, KillTask, WaitTask

if __name__ == '__main__':
    def foo():
        mytid = yield getTid()
        i = 5
        while i:
            print(f"I'm foo, {mytid}")
            yield
            i -= 1

    def main():
        child = yield NewTask(foo())
        print("waiting for child")
        yield WaitTask(child)
        
        print("main process")
        mid = yield getTid()
        for i in range(5):
            print("I'm main")
            yield

    scheduler = Scheduler()
    scheduler.new(main())
    scheduler.mainloop()