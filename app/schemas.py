from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OrderSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class OrderCreate(BaseModel):
    drink: str = Field(
        min_length=1,
        description="Название напитка из меню",
        examples=["Латте"]
    )
    size: OrderSize = Field(
        description="Размер напитка",
        examples=["medium"]
    )
    quantity: int = Field(
        gt=0,
        description="Количество напитков",
        examples=[2]
    )
    customer_name: str | None = Field(
        default=None,
        description="Имя клиента",
        examples=["Ирина"]
    )


class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1)
    size: OrderSize | None = None
    quantity: int | None = Field(default=None, gt=0)
    customer_name: str | None = None
    status: OrderStatus | None = None


class Order(BaseModel):
    id: int
    drink: str
    size: OrderSize
    quantity: int
    customer_name: str | None = None
    status: OrderStatus
    created_at: datetime