from dataclasses import dataclass, field


@dataclass
class InMemoryDataStore:
    categories: dict[str, dict] = field(default_factory=dict)
    tags: dict[str, dict] = field(default_factory=dict)
    blogs_metadata: dict[str, dict] = field(default_factory=dict)
    blogs_contents: dict[str, dict] = field(default_factory=dict)
    blog_analytics: dict[str, dict] = field(default_factory=dict)
    blog_assets: dict[str, dict] = field(default_factory=dict)
    users: dict[str, dict] = field(default_factory=dict)
    blog_statuses: dict[str, dict] = field(default_factory=dict)


class BaseRepository:
    def __init__(self, store: InMemoryDataStore):
        self.store = store
