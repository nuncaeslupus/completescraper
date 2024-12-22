import json
from typing import Optional

from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from requests import Response

from src.http_session.http_session import HTTPMethod, HTTPSession


class TestHTTPSessionRequests:
    host = "postman-echo.com"
    url_get = f"https://{host}/get"
    url_post = f"https://{host}/post"

    def check_response(
        self,
        json_response: dict,
        method: HTTPMethod,
        response: Optional[Response] = None,
    ) -> None:
        assert response is None or response.status_code == 200
        assert isinstance(json_response, dict)
        assert (
            json_response["url"] == self.url_get
            if method == HTTPMethod.GET
            else self.url_post
        )
        assert json_response["args"] == {}
        assert json_response["headers"]["host"] == self.host

    def test_get(self) -> None:
        session = HTTPSession()
        response = session.get(self.url_get)
        json_response = response.json()
        self.check_response(json_response, HTTPMethod.GET, response)

    def test_post(self) -> None:
        session = HTTPSession()
        response = session.post(self.url_post, json={})
        json_response = response.json()
        self.check_response(json_response, HTTPMethod.POST, response)

    def test_get_json(self) -> None:
        session = HTTPSession()
        response = session.get_json(self.url_get)
        json_response = response.json()
        self.check_response(json_response, HTTPMethod.GET, response)

    def test_post_json(self) -> None:
        session = HTTPSession()
        response = session.post_json(self.url_post, json={})
        json_response = response.json()
        self.check_response(json_response, HTTPMethod.POST, response)

    def test_get_soup(self) -> None:
        session = HTTPSession()
        soup = session.get_soup(self.url_get)
        json_response = json.loads(str(soup))
        assert isinstance(soup, BeautifulSoup)
        self.check_response(json_response, HTTPMethod.GET)

    def test_post_soup(self) -> None:
        session = HTTPSession()
        soup = session.post_soup(self.url_post, json={})
        json_response = json.loads(str(soup))
        assert isinstance(soup, BeautifulSoup)
        self.check_response(json_response, HTTPMethod.POST)

    def test_get_pyquery(self) -> None:
        session = HTTPSession()
        p = session.get_pyquery(self.url_get)
        text = p.html()
        assert isinstance(text, str)
        json_response = json.loads(text)
        assert isinstance(p, pq)
        self.check_response(json_response, HTTPMethod.GET)

    def test_post_pyquery(self) -> None:
        session = HTTPSession()
        p = session.post_pyquery(self.url_post, json={})
        text = p.html()
        assert isinstance(text, str)
        json_response = json.loads(text)
        assert isinstance(p, pq)
        self.check_response(json_response, HTTPMethod.POST)


class TestURL:
    def test_build_url_host(self) -> None:
        urls = {
            "http://example.com": "http://example.com",
            "/": "http://example.com/",
            "/get": "http://example.com/get",
            "/post": "http://example.com/post",
            "": "http://example.com",
            "http://example.org": "http://example.org",
        }

        for original, built in urls.items():
            session = HTTPSession("http://example.com")
            assert session.build_url(original) == built

    def test_build_url_no_host(self) -> None:
        urls = {
            "http://example.com": "http://example.com",
            "/": "/",
            "/get": "/get",
            "/post": "/post",
            "": "",
            "http://example.org": "http://example.org",
        }

        for original, built in urls.items():
            session = HTTPSession()
            assert session.build_url(original) == built
