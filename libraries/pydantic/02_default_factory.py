from pydantic import BaseModel, Field
from datetime import datetime, UTC
from functools import partial
from typing import Literal


class BlogPost(BaseModel):
    title: str
    content: str
    # union type
    author_id: str | int

    view_count: int = 0
    is_published: bool = False

    # default_factory is simply a function that gets called to create a new
    # default value each time you create an instance
    tags: list[str] = Field(default_factory=list)
    # NOTE: just assigning empty list is BAD practise, using a mutable default
    # like an empty list causes that list to be shared among all instances.
    # tags: list[str] = []  # BAD
    # see concepts/mutable_default_arguments.py for more information

    # similarly, below code does not work as expected as datetime.now is called
    # once when the class is created, not when each instance is created.
    # so, every BlogPost would then have the same create_at time
    # created_at: datetime = datetime.now(tz=UTC)

    # below is also incorrect, as we are passing in an executed function
    # created_at: datetime = Field(default_factory=datetime.now(tz=UTC))

    # this works
    created_at_lambda: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    # alternatively, use partial (returns unexecuted function with specified parameters)
    # partial is useful when you want to avoid lambdas and keep things reusable/testable
    created_at_partial: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    # status can be either draft, published or archived only, defaults to draft
    status: Literal["draft", "published", "archived"] = "draft"


post = BlogPost(
    title="Getting Started with Python",
    content="Here's how to begin...",
    author_id="12345",
)

if __name__ == "__main__":
    print(post)

# title='Getting Started with Python' content="Here's how to begin..." author_id='12345'
# view_count=0 is_published=False tags=[]
# created_at_lambda=datetime.datetime(2026, 1, 25, 14, 57, 38, 259026, tzinfo=datetime.timezone.utc)
# created_at_partial=datetime.datetime(2026, 1, 25, 14, 57, 38, 259214, tzinfo=datetime.timezone.utc)
# status='draft'
