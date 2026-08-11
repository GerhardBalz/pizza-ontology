#!/usr/bin/env python3
"""Deterministic reference application for the Pizza OpenAPI projection.

The application deliberately consumes implementation projections rather than the
Pizza OWL source:

- JSON concept projection: runtime application data;
- OpenAPI projection: interface contract verified independently in CI.

No OWL parsing, reasoning, or semantic relationship reconstruction occurs here.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA_PATH = ROOT / "projections" / "pizza-concepts" / "pizza-concepts.json"
OPENAPI_PATH = ROOT / "projections" / "pizza-openapi" / "pizza-concepts.openapi.json"
UX_DIR = ROOT / "examples" / "ux" / "pizza-api-explorer"
SHARED_STYLES = ROOT / "examples" / "ux" / "pizza-explorer" / "styles.css"


class PizzaCatalogApplication:
    """Application behavior over the checked-in JSON implementation projection."""

    def __init__(self, data_path: Path = DATA_PATH) -> None:
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        self.concepts = payload["concepts"]
        self.by_id = {concept["id"]: concept for concept in self.concepts}

    @staticmethod
    def _searchable_text(concept: dict) -> str:
        values = [concept["displayLabel"], concept["id"], concept["iri"]]
        for relation_name in ("directSuperClasses", "requiredToppings"):
            for reference in concept[relation_name]:
                values.extend([reference["id"], reference["iri"]])
        return " ".join(values).casefold()

    def list_concepts(self, query: str = "", required_topping: str = "") -> dict:
        normalized_query = query.strip().casefold()
        items = []

        for concept in self.concepts:
            if normalized_query and normalized_query not in self._searchable_text(concept):
                continue
            if required_topping and not any(
                topping["id"] == required_topping for topping in concept["requiredToppings"]
            ):
                continue
            items.append(concept)

        return {"count": len(items), "items": items}

    def get_concept(self, concept_id: str) -> dict | None:
        return self.by_id.get(concept_id)


APPLICATION = PizzaCatalogApplication()


class PizzaCatalogHandler(BaseHTTPRequestHandler):
    server_version = "PizzaCatalogReference/1.0"

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - stdlib signature
        # Keep the reference application quiet by default. The verifier reports
        # failures explicitly and production logging is outside this example.
        return

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, value: dict) -> None:
        body = (json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _send_file(self, path: Path, content_type: str | None = None) -> None:
        if not path.is_file():
            self._send_json(HTTPStatus.NOT_FOUND, {"message": "Static resource not found"})
            return
        guessed = content_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self._send_bytes(HTTPStatus.OK, path.read_bytes(), f"{guessed}; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        request = urlparse(self.path)
        path = request.path

        if path == "/concepts":
            parameters = parse_qs(request.query, keep_blank_values=False)
            query = parameters.get("q", [""])[0]
            required_topping = parameters.get("requiredTopping", [""])[0]
            self._send_json(
                HTTPStatus.OK,
                APPLICATION.list_concepts(query=query, required_topping=required_topping),
            )
            return

        prefix = "/concepts/"
        if path.startswith(prefix) and len(path) > len(prefix):
            concept_id = unquote(path[len(prefix) :])
            concept = APPLICATION.get_concept(concept_id)
            if concept is None:
                self._send_json(
                    HTTPStatus.NOT_FOUND,
                    {"message": f"Projected Pizza concept not found: {concept_id}"},
                )
            else:
                self._send_json(HTTPStatus.OK, concept)
            return

        # Contract publication is a static application convenience rather than a
        # domain API operation. The checked-in OpenAPI document remains the source.
        if path == "/openapi.json":
            self._send_file(OPENAPI_PATH, "application/json")
            return

        if path in ("/", "/index.html"):
            self._send_file(UX_DIR / "index.html", "text/html")
            return
        if path == "/app.js":
            self._send_file(UX_DIR / "app.js", "text/javascript")
            return
        if path == "/styles.css":
            self._send_file(SHARED_STYLES, "text/css")
            return
        if path == "/api-styles.css":
            self._send_file(UX_DIR / "api-styles.css", "text/css")
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"message": "Resource not found"})


def create_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), PizzaCatalogHandler)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    host, port = server.server_address[:2]
    print(f"Pizza Catalog reference application listening on http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
