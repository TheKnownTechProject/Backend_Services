DRAFT_STATUS_ID = "draft"
PUBLISHED_STATUS_ID = "published"
ARCHIVED_STATUS_ID = "archived"
PENDING_STATUS_ID = "pending"

MASTER_STATUSES: list[dict[str, str | bool]] = [
    {"status_id": DRAFT_STATUS_ID, "status_label": "Draft", "description": "Saved as draft", "is_active": True},
    {
        "status_id": PUBLISHED_STATUS_ID,
        "status_label": "Published",
        "description": "Visible on public site",
        "is_active": True,
    },
    {
        "status_id": ARCHIVED_STATUS_ID,
        "status_label": "Archived",
        "description": "Archived from public listings",
        "is_active": True,
    },
    {
        "status_id": PENDING_STATUS_ID,
        "status_label": "Pending",
        "description": "Waiting for editorial review",
        "is_active": True,
    },
]
