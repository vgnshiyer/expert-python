# --------------------------------------------------
#    === Scheduler ===
# --------------------------------------------------

from tasks import Task
from collections import deque, defaultdict
from system_call import SystemCall

# scheduler which alternates between tasks when they yield
class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.taskmap = {}

        # tasks waiting for other tasks to exit
        self.exit_waiting = defaultdict(list)

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.id] = newtask
        self.schedule(newtask)
        return newtask.id

    def exit(self, task):
        print("Task %d terminated" % task.id)
        del self.taskmap[task.id]

        # notify other tasks waiting
        while self.exit_waiting[task.id]:
            print(f"Task {task.id} was waiting for {self.exit_waiting[task.id]}")
            waiting = self.exit_waiting[task.id].pop()
            self.schedule(waiting)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting[waittid].append(task)
            return True
        return False

    def schedule(self, task):
        self.ready.append(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.popleft()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)