from pydantic import BaseModel, Field, ValidationError
from typing import Annotated


class User(BaseModel):
    # uid here needs to be greater than 0
    uid: Annotated[int, Field(gt=0)]
    # username must have minimum 3 and maximum 20 characters
    username: Annotated[str, Field(min_length=3, max_length=20)]

    # email validation using regex
    email: Annotated[
        str, Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    ]

    # age must be greater than or equal to 13, and less than or equal to 130
    age: Annotated[int, Field(ge=13, le=130)]


if __name__ == "__main__":
    ### Invalid User
    try:
        user = User(
            uid=0,
            username="cs",
            email="aditya@email.com",
            age=12,
        )
    except ValidationError as e:
        print(e)

# 3 validation errors for User
# uid
#   Input should be greater than 0 [type=greater_than, input_value=0, input_type=int]
# username
#   String should have at least 3 characters [type=string_too_short, input_value='cs', input_type=str]
# age
#   Input should be greater than or equal to 13 [type=greater_than_equal, input_value=12, input_type=int]


# apart from adding constraints using Annotated manually,
# pydantic also provides constrained types (e.g. EmailStr, PositiveInt)
