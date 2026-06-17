class MasterService:
    def __init__(self, blog_status_repository):
        self.blog_status_repository = blog_status_repository

    def list_blog_statuses(self) -> list[dict]:
        return self.blog_status_repository.list_all()
