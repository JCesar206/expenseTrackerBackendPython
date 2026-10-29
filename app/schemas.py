from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    kind: Literal["income", "expense"]
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El nombre no puede estar vacío.")
        return value

class CategoryUpdated(CategoryCreate):
    pass
class CategoryResponse(BaseModel):
    id: int
    name: str
    kind: str
    user_id: int | None
    model_config = ConfigDict(form_attributes=True)