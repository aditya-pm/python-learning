"""
ProcessPoolExecutor + Manager + User-defined class demo using namespaces

Key Concepts:

1. Manager:
   - A Manager creates a server process that holds Python objects
     which can be shared across multiple processes.
   - Shared objects include lists, dicts, Namespace objects, and more.
   - These objects are **proxies**, automatically handling inter-process
     communication and serialization.

2. Namespace for user-defined class attributes:
   - Manager.Namespace() provides a generic shared container.
   - Python objects themselves (like instances of custom classes) cannot
     be directly shared between processes because they are not automatically
     picklable across processes if they have methods or internal state.
   - To share a user-defined class instance, we **map its attributes manually**
     to the Namespace before processing.
   - After all processes finish, we **map the Namespace attributes back** to
     the class instance to sync the updated state.

3. Lock:
   - Shared objects are **not automatically process-safe**.
   - Using a lock ensures that only one process can modify the Namespace at
     a time, preventing race conditions and inconsistent results.

4. ProcessPoolExecutor:
   - Runs functions in separate processes.
   - Functions must receive picklable arguments.
   - Using a Manager's shared objects allows processes to read/write shared
     state safely without needing to pickle the whole class instance.

Flow of Execution:

1. Define a user class `MyData` with attributes x and y.
2. Create a Manager object, then a Namespace object to hold x and y.
   - Creating a Manager first allows us to extend shared resources easily,
     e.g., adding shared lists, dicts, or more Namespace objects.
3. Map the class instance attributes to the Namespace.
4. Create a Lock to ensure process-safe updates.
5. Define a function `modify_data` that takes the Namespace and a delta,
   modifies its attributes under the lock, and returns the updated values.
6. Submit multiple tasks to ProcessPoolExecutor to modify the shared data
   concurrently.
7. After all tasks finish, map the Namespace attributes back to the class
   instance to sync the results.
8. Print the final object state to confirm updates.

Notes:
- Without the lock, concurrent writes may overwrite each other, leading
  to inconsistent results.
- This approach allows safe sharing and modification of user-defined class
  data across multiple processes.
"""

from concurrent.futures import ProcessPoolExecutor
import multiprocessing


class MyData:
    """User-defined class with two numeric attributes."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"MyData(x={self.x}, y={self.y})"


def modify_data(ns, delta, lock):
    """
    Each process safely modifies the shared Namespace.

    Args:
        ns (Namespace): Shared Namespace with attributes x and y.
        delta (int): Value to add to each attribute.
        lock (Lock): Multiprocessing lock for safe updates.

    Returns:
        tuple: Updated values of x and y.
    """
    with lock:  # Ensure only one process modifies the Namespace at a time
        print(f"Process modifying: x={ns.x}, y={ns.y}, delta={delta}")
        ns.x += delta
        ns.y += delta
        return ns.x, ns.y


if __name__ == "__main__":
    # 1. Create a Manager
    manager = multiprocessing.Manager()

    # 2. Create a Namespace object to hold shared attributes
    shared_data = manager.Namespace()

    # 3. Create a common lock to prevent race conditions
    lock = manager.Lock()

    # 4. Initialize Namespace with attributes from a user-defined class
    my_obj = MyData(10, 20)
    shared_data.x = my_obj.x
    shared_data.y = my_obj.y

    print("Before processing:", my_obj)

    # 5. Use ProcessPoolExecutor to modify shared data concurrently
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(modify_data, shared_data, i, lock) for i in range(1, 4)
        ]
        for f in futures:
            result = f.result()
            print("Result from process:", result)

    # 6. Map Namespace attributes back to class instance
    my_obj.x = shared_data.x
    my_obj.y = shared_data.y

    print("After processing:", my_obj)
