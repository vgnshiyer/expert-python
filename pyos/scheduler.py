# --------------------------------------------------
#    === Scheduler ===
# --------------------------------------------------

from tasks import Task
from collections import deque

# scheduler which alternates between tasks when they yield
class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.id] = newtask
        self.schedule(newtask)
        return newtask.id

    def schedule(self, task):
        self.ready.append(task)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.popleft()
            result = task.run()
            self.schedule(task)