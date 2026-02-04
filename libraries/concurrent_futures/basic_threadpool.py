"""
DETAILED EXPLANATION - ThreadPoolExecutor Basics (basic_thread_pool.py)

This script demonstrates the fundamental behavior of `ThreadPoolExecutor` from the
`concurrent.futures` module. It shows how tasks are submitted, how the thread pool
executes them concurrently up to a defined limit (`max_workers`), and how `.result()`
can block execution.

EXECUTION FLOW:
1. We define a `task(n)` function that prints a start message, sleeps for 2 seconds
   (simulating a blocking I/O or CPU-bound operation), then returns a completion string.

2. We record the start time using `time.perf_counter()`.

3. We create a `ThreadPoolExecutor` with `max_workers=3` using a `with` statement.
   - The context manager ensures that once the `with` block exits, the executor is
     gracefully shut down (`executor.shutdown(wait=True)` is called implicitly).
   - `max_workers=3` means at most 3 threads will run tasks at the same time.

4. We submit five tasks (task1-task5) using `executor.submit(task, n)`.
   - **Key concept:** `submit()` is *non-blocking*. It schedules the task and immediately
     returns a `Future` object, even if the task has not started yet.
   - The first three submissions (`task1`, `task2`, `task3`) are picked up by the three
     available threads and start running immediately.
   - The last two submissions (`task4`, `task5`) are placed into the executor's internal
     queue, waiting for a thread to become free.

5. Immediately after all submissions, the line:
       print("\n|| I am executed before task4 and task5 starts executing! ||\n")
   runs in the **main thread**, showing that submitting tasks does *not* block the main
   thread. Even while tasks 1-3 are sleeping, the main thread proceeds.

6. We check the state of `task1` before calling `.result()`:
       task1.running() → True (most likely, because it's one of the first three running)
       task1.done()    → False (it's not finished yet)

7. `task1.result()` is a **blocking call**.
   - The main thread pauses here and waits for task1 to complete.
   - Meanwhile, tasks 2 and 3 continue running in their threads.
   - Tasks 4 and 5 are still queued and cannot start until one of the first three tasks
     finishes and a worker thread becomes free.

8. After ~2 seconds, tasks 1-3 complete. At this point:
   - `task1.result()` returns its value, and we print it.
   - The print after `.result()` shows:
       task1.running() → False
       task1.done()    → True

9. Once the `with` block exits:
   - The executor waits for all remaining tasks (tasks 4 and 5) to finish, because the
     default shutdown is `wait=True`.
   - Tasks 4 and 5 then start running concurrently (up to 3 threads available, so both
     run together) and finish after another ~2 seconds.

10. The total runtime is about 4 seconds:
    - First batch (tasks 1-3) → ~2 seconds
    - Second batch (tasks 4-5) → ~2 seconds

KEY TAKEAWAYS:
- `executor.submit()` is non-blocking: it queues tasks immediately.
- Only `max_workers` tasks run at a time; others wait in the queue.
- `.result()` blocks until the corresponding task completes.
- Main thread execution can continue after submissions, independent of the worker threads.
- Context manager ensures proper cleanup and waiting for all tasks to finish.

"""

from concurrent.futures import ThreadPoolExecutor, Future
import time


def task(n):
    print(f"Starting task {n}")
    time.sleep(2)
    return f"Task {n} completed."


start = time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as executor:
    # submit is non blocking, hence task1 - task5 are queued immediately
    # task1-task3 also begins executing immediately as max_workers = 3
    # tasks: list[Future] = [executor.submit(task, i) for i in range(1, 6)]
    task1: Future = executor.submit(task, 1)
    task2: Future = executor.submit(task, 2)
    task3: Future = executor.submit(task, 3)
    task4: Future = executor.submit(task, 4)
    task5: Future = executor.submit(task, 5)
    print("\n|| I am executed before task4 and task5 starts executing! ||\n")

    # Check the state before waiting
    print("Before .result():", task1.running(), task1.done(), flush=True)

    print(task1.result())  # Blocking call, waits for completion
    print("After .result():", task1.running(), task1.done(), flush=True)

# Takes 4 seconds: 2 seconds for task1 - task3, then 2 seconds for task4 - task5
print(f"Time take: {time.perf_counter() - start:.2f}")
