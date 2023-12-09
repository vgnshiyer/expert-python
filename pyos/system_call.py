# -------------------------------------------------------------
#                   === System Call ===
# -------------------------------------------------------------

class SystemCall:
    def handle(self):
        pass

class getTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.id
        self.sched.schedule(self.task)

class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target
    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)

class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid
    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)