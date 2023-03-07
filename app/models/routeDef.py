from fastapi import APIRouter


class RouteDef:
    router: APIRouter
    prefix: str
    tags: list[str]

    def __init__(self, router: APIRouter, prefix: str, tags: list[str]):
        self.router = router
        self.prefix = prefix
        self.tags = tags
