"""
ProcessPoolExecutor / ThreadPoolExecutor Shared State & Process Safety Demo

Key Concepts:

1. Memory Model Differences:
   - ThreadPoolExecutor: Threads share memory by default.
     Modifications to shared objects (like lists) are visible across threads.
   - ProcessPoolExecutor: Processes have **isolated memory**.
     Changes to normal Python objects inside a process are **not visible** to the main process or other processes.

2. Shared Objects via multiprocessing.Manager:
   - Manager creates a **server process** that holds shared objects.
   - Supported shared objects include list, dict, Namespace, etc.
   - These objects are **proxies**, allowing multiple processes to safely read/write.
   - Example:
       manager = multiprocessing.Manager()
       shared_list = manager.list()

3. Why create a Manager first:
   - Manager acts as the central coordination point for all shared objects.
   - You can create multiple shared objects (lists, dicts, Namespaces) from the same manager.
   - This avoids creating multiple managers and provides flexibility for scaling.

4. Process Safety:
   - Shared objects are still proxies and may need **Locks** to avoid race conditions
     if multiple processes write to them simultaneously.
   - For this demo, we show simple append operations without locks for clarity.
     (In production, always consider locks for writes.)

Flow of Execution:

1. Demonstrates difference between threads (shared memory) and processes (isolated memory).
2. Shows how a Manager allows safe shared state between processes for built-in types.
3. Each function appends a value to a shared list (thread or manager list) and returns a copy of the current state.
4. ThreadPoolExecutor: all threads see the same list naturally.
5. ProcessPoolExecutor: normal list would be copied per process; using manager.list() allows shared state.
"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import time

# Shared list for demonstration in threads (threads naturally share memory)
shared_list = []


def thread_task(n):
    """Task function for ThreadPoolExecutor: appends to shared memory list."""
    shared_list.append(n)
    time.sleep(0.5)
    return shared_list.copy()


def process_task(n, shared):
    """Task function for ProcessPoolExecutor: appends to a manager list (shared across processes)."""
    shared.append(n)
    time.sleep(0.5)
    return list(shared)


if __name__ == "__main__":
    # -------------------------------
    # ThreadPoolExecutor example
    # -------------------------------
    print("=== ThreadPoolExecutor: shared memory ===")
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(thread_task, range(5))
        for result in results:
            print(result)
    print("Final shared_list:", shared_list)

    # -------------------------------
    # ProcessPoolExecutor example
    # -------------------------------
    print("\n=== ProcessPoolExecutor: shared memory via Manager ===")
    # Manager acts as a shared memory space across processes
    manager = multiprocessing.Manager()
    shared = manager.list()  # create a shared list via manager

    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_task, i, shared) for i in range(5)]
        for f in futures:
            print(f.result())
    print("Final shared list:", list(shared))
