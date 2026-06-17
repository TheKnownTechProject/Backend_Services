from pydantic import BaseModel, Field


class AssetResponse(BaseModel):
    assetId: str
    assetType: str
    url: str
    fileName: str
    mimeType: str
    altText: str | None = None
    uploadedBy: str
    createdAt: str
    s3Key: str
    fileSize: int


class AssetListResponse(BaseModel):
    items: list[AssetResponse]


class UploadAssetRequest(BaseModel):
    altText: str | None = Field(default=None, max_length=250)
    assetType: str = Field(min_length=2, max_length=50)
