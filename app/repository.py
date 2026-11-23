from .schemas import Order


class OrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []
        self._next_id: int = 1

    def get_all(self) -> list[Order]:
        return self._orders.copy()

    def get_by_id(self, order_id: int) -> Order | None:
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def add(self, order: Order) -> Order:
        order = order.model_copy(update={"id": self._next_id})
        self._next_id += 1
        self._orders.append(order)
        return order

    def update(self, order_id: int, update_data: dict) -> Order | None:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                updated_order = order.model_copy(update=update_data)
                self._orders[index] = updated_order
                return updated_order
        return None

    def delete(self, order_id: int) -> bool:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                self._orders.pop(index)
                return True
        return False