from pydantic import BaseModel, EmailStr, Field, SecretStr
from datetime import datetime, UTC
from typing import Literal, Annotated
from functools import partial
from uuid import uuid4, UUID


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
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

    # nested fields
    author: User
    comments: list[Comment] = Field(default_factory=list)


post_data = {
    "title": "Understanding Pydantic Models",
    "content": "Pydantic makes data validation easy and intuitive...",
    "slug": "understanding-pydantic",
    "author": {
        "username": "coreyms",
        "email": "CoreyMSchafer@gmail.com",
        "age": 39,
        "password": "secret123",
    },
    "comments": [
        {
            "content": "I think I understand nested models now!",
            "author_email": "student@example.com",
            "likes": 25,
        },
        {
            "content": "Can you cover FastAPI next?",
            "author_email": "viewer@example.com",
            "likes": 15,
        },
    ],
}

# Pydantic automatically validates and constructs nested models recursively
post = BlogPost(**post_data)
# or
post2 = BlogPost.model_validate(post_data)

print(post.model_dump_json(indent=2))
# {
#   "title": "Understanding Pydantic Models",
#   "content": "Pydantic makes data validation easy and intuitive...",
#   "view_count": 0,
#   "is_published": false,
#   "tags": [],
#   "created_at": "2026-01-27T11:10:50.833259Z",
#   "status": "draft",
#   "slug": "understanding-pydantic",
#   "author": {
#     "uid": "a7a9a62c-514e-4ba8-82a6-e863e7f07eca",
#     "username": "coreyms",
#     "email": "CoreyMSchafer@gmail.com",
#     "age": 39,
#     "password": "**********"
#   },
#   "comments": [
#     {
#       "content": "I think I understand nested models now!",
#       "author_email": "student@example.com",
#       "likes": 25
#     },
#     {
#       "content": "Can you cover FastAPI next?",
#       "author_email": "viewer@example.com",
#       "likes": 15
#     }
#   ]
# }
