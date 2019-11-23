# Everything is a Process

`fork()` is the primary method for creating processes on Unix.
It creates a child process with a separate address space.
The child inherits the parent's set of open file descriptors,
which is often used for interprocess communication, e.g. using `pipe()`.

On success of `fork()`, the PID of the child process is returned to the parent
and `0` is returned to the child.

Process state in Linux is represented usign `struct task_struct`. It stores
process state (is running?), pid, uid, gid, pointers to parent process,
opened files, signal handlers.

The basic unit of execution is a light-weight process (LWP), created using `clone()`.
Multiple LWPs may share resources. Each LWP has a unique stack and set of registers.

Both `fork()` and pthreads use `clone()` under the hood.
The difference lies in the flags passed to it.

`pthread_create()` shares the virtual memory (`CLONE_VM`),
file descriptors (`CLONE_FILES`), signal handlers (`CLONE_SIGNAL`), ...

> What are pthreads, anyway? POSIX Threads is an API specification
> that defines functions for thread management, synchronization, thread-local storage,
> and so on. It is available on many platforms besides Linux, like BSD and Mac OS X.

`fork()` creates a separate memory space for the program. However, there's
an important optimization in Linux: the data is not immediately copied, rather,
the pages point to the same physical addresses and marked as read-only. When
the child process attempts to write to them, a page fault is generated
and it is at this point that the kernel copies the data.

`fork()` only copies the calling thread. This may cause problems in
a multithreaded environment, because the effect is essentially that all the
other threads die at the fork point (the locks may be left unreleased,
the shared data may be left in a corrupted state, etc.)
