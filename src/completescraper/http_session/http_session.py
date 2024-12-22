import logging

from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from requests import Response, Session

from .enums import HTTPAccept, HTTPMethod

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0"

LOGGING_FORMAT = "[%(levelname)s] [%(asctime)s] %(message)s"
logging.basicConfig(
    format=LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S.%f", level=logging.INFO
)


class HTTPSession(Session):
    def __init__(self, base_url: str = "") -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.base_url = base_url.rstrip("/") if base_url else ""
        self.headers.update({"User-Agent": USER_AGENT})

    def build_url(self, url: str) -> str:
        if "//" not in url:
            return f"{self.base_url}/{url.lstrip('/')}" if url else self.base_url
        return url

    def fetch(
        self, method: HTTPMethod, url: str, accept: str = HTTPAccept.HTML.value, **kwargs
    ) -> Response:
        url = self.build_url(url)
        self.headers.update({"Accept": accept})
        method_map = {
            HTTPMethod.GET: super().get,
            HTTPMethod.POST: super().post,
            HTTPMethod.PUT: super().put,
            HTTPMethod.DELETE: super().delete,
        }
        if method in method_map:
            response = method_map[method](url, **kwargs)
            self.logger.info(f"{method.name.ljust(8)} [{response.status_code}] {url}")
            return response
        else:
            raise ValueError("Invalid HTTP method.")

    def get(self, url, **kwargs) -> Response:
        return self.fetch(HTTPMethod.GET, url, **kwargs)

    def post(self, url, **kwargs) -> Response:
        return self.fetch(HTTPMethod.POST, url, **kwargs)

    def put(self, url, **kwargs) -> Response:
        return self.fetch(HTTPMethod.PUT, url, **kwargs)

    def delete(self, url, **kwargs) -> Response:
        return self.fetch(HTTPMethod.DELETE, url, **kwargs)

    def get_json(self, url: str, **kwargs) -> Response:
        return self.get(url, accept=HTTPAccept.JSON.value, **kwargs)

    def post_json(self, url: str, **kwargs) -> Response:
        return self.post(url, accept=HTTPAccept.JSON.value, **kwargs)

    def get_soup(self, url: str, parser: str = "html.parser", **kwargs) -> BeautifulSoup:
        return BeautifulSoup(self.get(url, **kwargs).content, parser)

    def post_soup(
        self, url: str, parser: str = "html.parser", **kwargs
    ) -> BeautifulSoup:
        return BeautifulSoup(self.post(url, **kwargs).content, parser)

    def get_pyquery(self, url: str, **kwargs) -> pq:
        return pq(self.get(url, **kwargs).content)

    def post_pyquery(self, url: str, **kwargs) -> pq:
        return pq(self.post(url, **kwargs).content)
