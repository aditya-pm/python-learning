"""
ProcessPoolExecutor Picklability Demo

Key Concept: Pickling
---------------------
- Pickling is Python's way of serializing objects into a byte stream so they can
  be sent to other processes or saved to disk.
- ProcessPoolExecutor executes tasks in separate processes. Python needs to
  serialize (pickle) the function and its arguments to send them to worker
  processes.
- Only picklable functions and arguments can be submitted as tasks. Non-picklable
  objects include:
    * Nested functions
    * Lambda functions
    * Local classes or instances defined inside another function
- Attempting to submit non-picklable objects will raise a PicklingError or
  AttributeError.

Flow of Execution Demonstrated in This Script:
----------------------------------------------
1. **Top-level function (works)**:
    - Function defined at module level is picklable.
    - Submitted to ProcessPoolExecutor and executed in separate processes.
    - Results are collected using Future.result().

2. **Nested function (fails)**:
    - Function defined inside `main()` is not picklable.
    - Submitting it to the process pool raises an exception.
    - Demonstrates that local functions cannot be serialized for separate processes.

3. **Lambda function (fails)**:
    - Lambdas are anonymous and local by nature; not picklable.
    - Submitting a lambda also raises a pickling exception.

4. **Picklable object as argument (works)**:
    - Class `Picklable` is defined at the top level (module scope), so its
      instances are picklable.
    - A top-level function `compute(obj)` is used as the task function.
    - Each worker process receives a pickled `Picklable` object, calls
      `compute()`, and returns the result.
    - Demonstrates the correct pattern for passing objects to ProcessPoolExecutor.

Notes:
------
- Always define task functions at the top level of a module.
- Classes passed as arguments should also be top-level.
- Using nested functions or lambdas with ProcessPoolExecutor will fail due
  to pickling limitations.
- Future.result() collects results from each process after execution.
"""

from concurrent.futures import ProcessPoolExecutor
import time


# Top-level function (picklable)
def top_level_task(n: int) -> int:
    return n * n


class Picklable:
    """Example class to demonstrate picklable objects as task arguments."""

    def __init__(self, val):
        self.val = val

    def compute(self):
        return self.val * 2


# Top-level function to operate on picklable object
def compute(obj):
    return obj.compute()


def main():
    print("\n=== Top-level function (works) ===")
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(top_level_task, i) for i in range(5)]
        results = [f.result() for f in futures]
        print(f"Results: {results}")

    print("\n=== Nested function (fails) ===")

    # Nested function inside main (NOT picklable)
    def nested_task(n: int) -> int:
        return n * n

    try:
        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(nested_task, i) for i in range(5)]
            results = [f.result() for f in futures]
            print(f"Results: {results}")
    except Exception as e:
        print(f"Caught exception: {e}")

    print("\n=== Lambda function (fails) ===")
    try:
        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(lambda x: x * x, i) for i in range(5)]
            results = [f.result() for f in futures]
            print(f"Results: {results}")
    except Exception as e:
        print(f"Caught exception: {e}")

    print("\n=== Picklable object as argument (works) ===")
    objects = [Picklable(i) for i in range(5)]
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(compute, obj) for obj in objects]
        results = [f.result() for f in futures]
        print(f"Results: {results}")

    print(
        "\nDemo complete. Always use picklable top-level functions for ProcessPoolExecutor tasks."
    )


if __name__ == "__main__":
    main()
