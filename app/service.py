from datetime import datetime

from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .repository import OrderRepository
from .schemas import Order, OrderCreate, OrderStatus, OrderUpdate


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def list_orders(
        self, status: OrderStatus | None, limit: int, offset: int
    ) -> list[Order]:
        result = self.repository.get_all()
        if status is not None:
            result = [order for order in result if order.status == status]
        return result[offset : offset + limit]

    def count_orders(self) -> int:
        return len(self.repository.get_all())

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def create_order(self, data: OrderCreate) -> Order:
        new_order = Order(
            id=0,  # настоящий id выдаст репозиторий в add()
            status=OrderStatus.pending,
            created_at=datetime.now(),
            **data.model_dump(),
        )
        return self.repository.add(new_order)

    def update_order(self, order_id: int, data: OrderUpdate) -> Order:
        order = self.get_order(order_id)
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)
        return self.repository.update(order_id, data.model_dump(exclude_unset=True))

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)
        self.repository.delete(order_id)