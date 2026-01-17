# manual validation
def create_user(username: str, email: str, age: int):
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")

    return {"username": username, "email": email, "age": age}


# works
user1 = create_user("Aditya", "aditya@email.com", 20)

# error (expected)
# user2 = create_user("Aditya", None, "old")
"""
issues:
- manual validation does not scale well. For nested structures
  (e.g. list[dict[int, str]]), validation logic becomes verbose
  and error-prone.
- only the first encountered error is reported. Multiple incorrect
  fields require repeated fix-run cycles.
"""
from pydantic import BaseModel


# syntax similar to dataclasses, but dataclasses do not validate data
class User(BaseModel):
    username: str
    email: str
    age: int


# works
user1 = User(username="Aditya", email="aditya@email.com", age=20)

# error (expected)
# user1 = User(username="Aditya", email=None, age="old")
# both errors are highlighted
