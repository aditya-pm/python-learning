from pydantic import BaseModel, Field, EmailStr, SecretStr, HttpUrl
from typing import Annotated
from uuid import UUID, uuid4


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    # username must have minimum 3 and maximum 20 characters
    username: Annotated[str, Field(min_length=3, max_length=20)]

    # SecretStr hides data in logs (useful for sensitive data)
    # SecretStr will remain masked when printing or serializing
    password: SecretStr
    website: HttpUrl | None = None

    # email validation (requires: pip install "pydantic[email]")
    email: EmailStr

    # age must be greater than or equal to 13, and less than or equal to 130
    age: Annotated[int, Field(ge=13, le=130)]


# valid User
if __name__ == "__main__":
    user = User(
        username="aditya_pm",
        email="aditya@gmail.com",
        age=20,
        password=SecretStr("secret123"),
    )
    print(user)

    # to actually access the password:
    print(user.password.get_secret_value())

# uid=UUID('6e1ed83e-0ebd-47f6-a2d6-8ccecce9bb6a') username='aditya_pm'
# password=SecretStr('**********') website=None email='aditya@gmail.com' age=20
# secret123


# make sure to check the more available pydantic types in the documentation
