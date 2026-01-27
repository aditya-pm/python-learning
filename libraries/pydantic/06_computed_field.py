from pydantic import (
    BaseModel,
    Field,
    computed_field,
)
from typing import Annotated
from uuid import UUID, uuid4


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]

    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    # computed_field is computed during model/instance creation/instantiation
    # this field will be included when the model is serialized
    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10_000


if __name__ == "__main__":
    # valid User
    user = User(username="Aditya_Pm")
    print(user)
    # uid=UUID('bafc9886-7b90-4070-90d3-e38cec5e3428') username='Aditya_Pm'
    # first_name='' last_name='' follower_count=0 display_name='Aditya_Pm'
    # is_influencer=False

    user2 = User(username="Aditya_Pm", first_name="Aditya", last_name="Menon")
    print(user2)
    # uid=UUID('42e0040d-7df7-4b00-9de0-7452ebef5058') username='Aditya_Pm'
    # first_name='Aditya' last_name='Menon' follower_count=0 display_name='Aditya Menon'
    # is_influencer=False

    # computed_field values are included during serialization (model_dump / JSON)
    print(user2.model_dump_json(indent=2))
    # {
    # "uid": "434bec79-75de-490d-816b-0d4c2a0a2d4f",
    # "username": "Aditya_Pm",
    # "first_name": "Aditya",
    # "last_name": "Menon",
    # "follower_count": 0,
    # "display_name": "Aditya Menon",
    # "is_influencer": false
    # }
