from typing import TypeVar, Generic, List
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int

class TimestampMixin:
    created_at: datetime
    updated_at: datetime

def paginate(items: List[T], skip: int, limit: int) -> PaginatedResponse[T]:
    return PaginatedResponse(
        items=items[skip:skip + limit],
        total=len(items),
        skip=skip,
        limit=limit
    )

def format_error(code: str, message: str, details: dict = None):
    error = {"code": code, "message": message}
    if details:
        error["details"] = details
    return {"error": error}
