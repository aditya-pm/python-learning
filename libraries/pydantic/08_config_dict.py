from pydantic import BaseModel, EmailStr, Field, SecretStr, ConfigDict
from datetime import datetime, UTC
from typing import Literal, Annotated
from functools import partial
from uuid import uuid4, UUID
import json


class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # enable aliases for fields
        strict=True,  # disables most type coercion (UUID-from-str is still allowed)
        extra="allow",  # allows passing of fields not defined by the model (other options = ignore (default), forbid)
        validate_assignment=True,  # validates again if a field is assigned new value (default = False)
        # frozen=True,  # makes model immutable
    )

    uid: UUID = Field(alias="id", default_factory=uuid4)
    username: str
    email: EmailStr
    age: Annotated[int, Field(ge=13, le=130)]
    password: SecretStr


class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0


class BlogPost(BaseModel):
    title: str
    content: str
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]
    author: User
    comments: list[Comment] = Field(default_factory=list)


if __name__ == "__main__":

    # User Dictionary
    # this works because we set uid alias to be id
    user_data = {
        "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
        "username": "Aditya_PM",
        "email": "aditya@email.com",
        "age": 20,
        "password": "secret123",
        "note": "this is an extra field",
    }
    user = User.model_validate(user_data)

    print(user.model_dump_json(indent=2))
    print()
    # {
    #   "uid": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    #   "username": "Aditya_PM",
    #   "email": "aditya@email.com",
    #   "age": 20,
    #   "password": "**********"
    # }

    print(user.model_dump_json(indent=2, by_alias=True))
    print()
    # {
    #   "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    #   "username": "Aditya_PM",
    #   "email": "aditya@email.com",
    #   "age": 20,
    #   "password": "**********"
    # }

    # password is explicitly excluded from serialization here
    print(user.model_dump_json(indent=2, by_alias=True, exclude={"password"}))
    print()
    # {
    #   "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    #   "username": "Aditya_PM",
    #   "email": "aditya@email.com",
    #   "age": 20
    # }

    print(user.model_dump_json(indent=2, by_alias=True, include={"username", "email"}))
    print()
    # {
    #   "username": "Aditya_PM",
    #   "email": "aditya@email.com"
    # }

    # example to demonstrate loading from JSON
    user2 = User.model_validate_json(json.dumps(user_data))
    print(user2.model_dump_json(indent=2, by_alias=True))
    print()
    # {
    #   "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    #   "username": "Aditya_PM",
    #   "email": "aditya@email.com",
    #   "age": 20,
    #   "password": "**********"
    # }
