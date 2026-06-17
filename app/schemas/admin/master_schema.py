from pydantic import BaseModel


class BlogStatusResponse(BaseModel):
    statusId: str
    statusLabel: str
    description: str
    isActive: bool


class MasterListResponse(BaseModel):
    items: list[dict]
