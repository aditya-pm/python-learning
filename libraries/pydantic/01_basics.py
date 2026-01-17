from datetime import datetime
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    # required fields
    uid: int
    username: str
    email: str

    # optional fields
    bio: str = ""
    is_active: bool = True

    # truly optional (field not required, defaults to None)
    # error: full_name type is str, but default value is None type
    # full_name: str = None
    full_name: str | None = None
    verified_at: datetime | None = None


# error: required fields not passed
# user = User()

# optional fields need not be passed
user = User(uid=123, username="Aditya", email="aditya@email.com")

print(user)
# uid=123 username='Aditya' email='aditya@email.com' bio='' is_active=True full_name=None verified_at=None

print(user.username)
# Aditya

user.username = "AdityaPM"
print(user.username)
# AdityaPM

# NOTE:
# by default, model instances are mutable
# by default, there is no re-validation if you change a field
# below code WORKS:
user.bio = 123  # type: ignore
print(user.bio)
# 123

user.bio = "Python Developer"
print(user.bio)
# Python Developer

# convert pydantic model to python dict
model_dict: dict = user.model_dump()
# convert pydantic model to json str
model_json: str = user.model_dump_json(indent=2)
print(model_json)
# {
#   "uid": 123,
#   "username": "AdityaPM",
#   "email": "aditya@email.com",
#   "bio": "Python Developer",
#   "is_active": true,
#   "full_name": null,
#   "verified_at": null
# }

try:
    # all 3 are invalid, but only 2 errors thrown, "123" is converted to 123.
    # pydantic, by default, converts types when it makes sense to do so.
    # it is common to receive integers as strings, hence the conversion, but
    # not as common to receive a None type in place of string and integer type
    # in place of string, hence the errors are thrown.
    # this automatic conversion behaviour is known as type coercion, and can be
    # disabled
    user2 = User(uid="123", username=None, email=123)  # type: ignore
except ValidationError as e:
    print(e)
    # 2 validation errors for User
    # username
    # Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    # email
    # Input should be a valid string [type=string_type, input_value=123, input_type=int]
