# completescraper

[![PyPI](https://img.shields.io/pypi/v/completescraper)](https://pypi.org/project/completescraper/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/nuncaeslupus/completescraper/blob/main/LICENSE)

**A small Python library for scraping HTML sites with `requests`, BeautifulSoup and PyQuery.**

`HTTPSession` is a `requests.Session` with a base URL, a browser User-Agent, request logging and helpers that return parsed pages. The `Html*` containers turn a `<form>`, `<select>`, `<ul>` or `<ol>` into a name plus a dict of its children, which is what you need to replay a login form or read a list of options.

## Quick start

```bash
pip install completescraper
```

```python
from completescraper import HTTPSession

s = HTTPSession("https://example.com")
soup = s.get_soup("/")          # GET https://example.com/ -> BeautifulSoup
print(soup.title.string)
```

Each request is logged as `[INFO] [time] GET      [200] https://example.com/`.

## Example

Parse a form and a select without any network access:

```python
from completescraper import HtmlForm, HtmlSelect, HTTPSession

html = """
<form name="login" action="/session">
  <input name="csrf" value="a1b2c3" type="hidden">
  <input name="user" value="">
  <select name="lang">
    <option name="en" value="en-GB">English</option>
    <option name="es" value="es-ES">Espanol</option>
  </select>
</form>
"""
form = HtmlForm(html, "login")
print(form.name, form.children)
print(HtmlSelect(html, "lang").children)

s = HTTPSession("https://example.com/")
print(s.build_url("/search"), s.build_url("https://other.org/x"))
```

Output:

```text
login {'csrf': 'a1b2c3', 'user': ''}
{'en': 'en-GB', 'es': 'es-ES'}
https://example.com/search https://other.org/x
```

`form.children` is ready to post back: `s.post("/session", data={**form.children, "user": "me"})`.

## Reference

### `HTTPSession(base_url="")`

A `requests.Session`. Relative URLs are joined to `base_url`; absolute URLs (containing `//`) pass through. Extra keyword arguments go to `requests`.

| Method | Returns |
|---|---|
| `get`, `post`, `put`, `delete` | `requests.Response` (sends `Accept: text/html`) |
| `get_json`, `post_json` | `requests.Response` (sends `Accept: application/json`) |
| `get_soup`, `post_soup` | `BeautifulSoup` (`parser="html.parser"` by default) |
| `get_pyquery`, `post_pyquery` | `PyQuery` |
| `fetch(method, url, accept=...)` | `requests.Response` for an `HTTPMethod` and any `Accept` value |

`HTTPMethod` and `HTTPAccept` live in `completescraper.http_session.enums`.

### Containers

`HtmlForm`, `HtmlSelect`, `HtmlUl` (exported) and `HtmlOl` (in `completescraper.parser.html_containers`) are pydantic models with `name` and `children`. Each takes `html` (a string or `BeautifulSoup`), an optional id to pick the container, a position when several match (default `0`), and the attributes used as the child key and value:

| Class | Children | Key / value by default |
|---|---|---|
| `HtmlForm` | `<input>` | `name` / `value` |
| `HtmlSelect` | `<option>` | `name` / `value` |
| `HtmlUl`, `HtmlOl` | `<li>` | `name` / element text |

Containers are matched by their `name` attribute unless you pass another (for example `form_id_attr="id"`). An empty or unmatched container is falsy.

## From an agent

There is no CLI or MCP server. An agent uses it as a library: build an `HTTPSession`, fetch with `get_soup` or `get_pyquery`, and read forms with `HtmlForm` to get the field dict to post back.

## Development

```bash
pip install -e .
python -m pytest            # run from the repository root
```

`tests/test_http_session.py` calls `postman-echo.com` and needs network access; the container tests run offline.

## Related projects

- [claude-arsenal](https://github.com/nuncaeslupus/claude-arsenal) — spec-driven Claude Code workflow and gated task queue.
- [drawspec](https://github.com/nuncaeslupus/drawspec) — declarative diagram spec → clean SVG/PNG/text, writable by LLMs; MCP server included.
- [doc-control](https://github.com/nuncaeslupus/doc-control) — lets AI agents edit Word documents as tracked changes.
- [literary-critic](https://github.com/nuncaeslupus/literary-critic) — LLM manuscript analysis the way a professional editor would.
- [integral-job-search](https://github.com/nuncaeslupus/integral-job-search) — candidate-centred job search run in Claude Code.

## License

MIT — see [LICENSE](https://github.com/nuncaeslupus/completescraper/blob/main/LICENSE).
