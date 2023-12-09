# -----------------------------------------------
#       === Tasks ===
# -----------------------------------------------

# encapsulates a running task
class Task:
    taskid = 0
    def __init__(self, target):
        Task.taskid += 1
        self.id = Task.taskid
        self.target = target # target coroutine
        self.sendval = None  # val to send

    def run(self):
        return self.target.send(self.sendval)

    def __repr__(self):
        return f"Task {self.id}"