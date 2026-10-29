from datetime import datetime
from decimal import Decimal
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

class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    kind: Literal["income", "expemse"]
    transaction_date: datetime
    category_di: int | None = Field(default=None, gt=0)

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("La descripción no puede estar vacía.")
        return value

class TransactionUpdate(TransactionCreate):
    pass
class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: Decimal
    kind: str
    transaction_date: datetime
    user_id: int
    category_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)