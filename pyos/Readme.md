# PyOS

### Theory

**Task**
In the context of operating systems and concurrent programming, a task (also known as a process or a thread, depending on the context) is a unit of execution. It's a piece of code that can be run independently of other tasks. Each task has its own state, including things like its current instruction, its register values, and its memory space.

**Scheduler**
A scheduler is a component of the operating system that decides which tasks to run, when to run them, and how long to run them for. The scheduler is responsible for managing all the tasks that are currently being executed by the system.

The scheduler uses an algorithm to decide which task to run next. This could be as simple as round-robin scheduling (where each task gets a turn in order), or it could be a more complex algorithm that takes into account things like task priority, how long the task has been waiting, etc.

**System Call**
A system call is a programmatic way in which a computer program requests a service from the kernel of the operating system it is executed on. This service may include hardware-related services (for example, accessing the hard disk), creating and executing new processes, and communicating with integral kernel services such as process scheduling.