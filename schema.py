from pydantic import BaseModel, Field, EmailStr, ConfigDict, AliasChoices

class UserBase(BaseModel):
    username: str = Field(
        validation_alias=AliasChoices("username", "user_name", "user"),
        min_length=1,
        max_length=50,
        description="Enter user name",
    )
    name: str | None = Field(default=None, max_length=50)
    email: EmailStr = Field(description="The email address of the user")

class UserCreate(UserBase):
    password: str = Field(min_length=1, max_length=128)
    role: str = Field(default="user")

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    name: str | None = None
    role: str

class UserPrivate(UserPublic):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str