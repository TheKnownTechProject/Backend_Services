from pydantic import BaseModel


class CursorPaginationMeta(BaseModel):
    cursor: str | None = None
    nextCursor: str | None = None
    limit: int
