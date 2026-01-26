from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    SecretStr,
    HttpUrl,
    field_validator,
    model_validator,
    ValidationError,
)
from typing import Annotated
from uuid import UUID, uuid4


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: SecretStr
    website: HttpUrl | None = None
    email: EmailStr
    age: Annotated[int, Field(ge=13, le=130)]

    # checks if username is alphanumeric (underscores allowed), if not raise
    # ValueError, otherwise convert username to lowercase.
    # this example does validation (checking if alphanumeric) and normalization
    # (converting to lowercase)
    # NOTE: this validator runs AFTER pydantic runs its own type validators
    # requires to be a classmethod because the class is not instantiated at the
    # time of the validation (self does not exist)
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()

    # NOTE: DOES NOT WORK AS PYDANTIC'S VALIDATOR RUNS BEFORE AND THROWS ERROR
    # because HttpUrl must start with either http:// or https://
    # @field_validator("website")
    # @classmethod
    # def add_https(cls, v: str | None) -> str | None:
    #     if v and not v.startswith(("http://", "https://")):
    #         return f"https://{v}"
    #     return v

    # NOTE: this validator runs BEFORE pydantic's own type validator, which is
    # important here because if the website does not start with http:// or https://
    # pydantic will throw error as it is not a valid HttpUrl, however, we are trying
    # to add https:// by ourselves before that happens so that the result can be
    # validated by pydantic
    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v


# when multiple fields need to be validated, we use model_validator instead
# model validators take the entire model/instance (self) and we can access
# attributes via the instance (e.g.: self.password)
# model_validator runs after all the fields are validated by pydantic
# does not require @classmethod (the instance is already created, hence self exists)
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self) -> UserRegistration:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


if __name__ == "__main__":
    # valid User
    user = User(
        username="Aditya_Pm",
        email="aditya@gmail.com",
        age=20,
        password=SecretStr("secret123"),
        website="aditya.com",  # type: ignore  # raw string, fixed by validator before HttpUrl validation
    )
    print(user)
    # uid=UUID('7f7b10b9-380a-4ed7-af21-9b73e791bedb') username='aditya_pm'
    # password=SecretStr('**********') website=HttpUrl('https://aditya.com/')
    # email='aditya@gmail.com' age=20

    try:
        user_registration = UserRegistration(
            email="aditya@email.com", password="secret123", confirm_password="secret456"
        )
    except ValidationError as e:
        print(e)

    # 1 validation error for UserRegistration
    # Value error, Password do not match [type=value_error,
    #   input_value={'email': 'aditya@email.c..._password': 'secret456'}, input_type=dict]


# good practises for validators:
# - always return the value, even if not modified
# - raise value errors, pydantic will catch it and convert it to validation error
# - either mutate value or throw error, do not do both
