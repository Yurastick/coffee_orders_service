from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Query

from .config import Settings, get_settings
from .repository import OrderRepository
from .service import OrderService

SettingsDep = Annotated[Settings, Depends(get_settings)]


@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()


def get_service(
    repository: Annotated[OrderRepository, Depends(get_repository)],
) -> OrderService:
    return OrderService(repository)


def pagination_params(
    settings: SettingsDep,
    limit: int | None = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
) -> dict:
    page_size = limit if limit is not None else settings.default_page_size
    page_size = min(page_size, settings.max_page_size)
    return {"limit": page_size, "offset": offset}


ServiceDep = Annotated[OrderService, Depends(get_service)]
PaginationDep = Annotated[dict, Depends(pagination_params)]