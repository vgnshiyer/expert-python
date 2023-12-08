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