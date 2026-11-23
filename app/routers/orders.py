from fastapi import APIRouter, Query, status

from ..dependencies import PaginationDep, ServiceDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый заказ",
)
def create_order(order_data: OrderCreate, service: ServiceDep):
    return service.create_order(order_data)


@router.get(
    "",
    response_model=list[Order],
    summary="Получить список заказов",
)
def get_orders(
    service: ServiceDep,
    pagination: PaginationDep,
    order_status: OrderStatus | None = Query(
        default=None,
        alias="status",
        description="Фильтр по статусу заказа",
    ),
):
    return service.list_orders(
        order_status, pagination["limit"], pagination["offset"]
    )


@router.get(
    "/{order_id}",
    response_model=Order,
    summary="Получить заказ по ID",
)
def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)


@router.patch(
    "/{order_id}",
    response_model=Order,
    summary="Изменить заказ",
)
def update_order(order_id: int, order_data: OrderUpdate, service: ServiceDep):
    return service.update_order(order_id, order_data)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отменить заказ",
)
def delete_order(order_id: int, service: ServiceDep):
    service.delete_order(order_id)