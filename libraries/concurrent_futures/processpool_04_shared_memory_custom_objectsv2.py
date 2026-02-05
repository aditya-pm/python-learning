# processpool_03_shared_memory_custom_objects uses namespaces for custom objects.
# here (processpool_04_shared_memory_custom_objectsv2.py) we use another approach,
# without using namespaces

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager


class MyData:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def get_values(self):
        return {"x": self.x, "y": self.y}

    def modify_values(self, values_dict):
        self.x = values_dict["x"]
        self.y = values_dict["y"]


def modify(shared_dict, delta, lock):
    """Each process modifies the shared dict safely."""
    with lock:
        shared_dict["x"] += delta
        shared_dict["y"] += delta
        return shared_dict["x"], shared_dict["y"]


if __name__ == "__main__":
    my_data = MyData(10, 20)

    # Create a manager
    manager = Manager()

    # Create a lock
    lock = manager.Lock()

    # shared dict
    shared_dict = manager.dict(my_data.get_values())

    # Use ProcessPoolExecutor to modify shared_dict concurrently
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(modify, shared_dict, i, lock) for i in range(1, 4)]
        for f in futures:
            print("Result from process:", f.result())

    my_data.modify_values(shared_dict)

    print("Final shared_dict:", dict(shared_dict))
