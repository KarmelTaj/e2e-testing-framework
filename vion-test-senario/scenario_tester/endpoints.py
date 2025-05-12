from enum import Enum

class HTTPMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class EndPoint:
    def __init__(self, method: HTTPMethods, url: str):
        self.url = url
        self.method = method