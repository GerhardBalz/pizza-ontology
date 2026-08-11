#!/usr/bin/env python3
"""Verify the ontology-informed UX consumes the semantic projection cleanly.

The UX must consume the checked-in projection from Track 6 rather than copying
Pizza concept semantics into HTML or JavaScript. This verifier checks that
boundary and smoke-tests the static paths through a local HTTP server.
"""

from __future__ import annotations

import json
import re
import threading
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROJECTION = ROOT / "projections" / "pizza-concepts" / "pizza-concepts.json"
INDEX = HERE / "index.html"
APP = HERE / "app.js"
STYLES = HERE / "styles.css"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def extract_projection_url(app_js: str) -> str:
    match = re.search(r'const\s+PROJECTION_URL\s*=\s*["\']([^"\']+)["\']\s*;', app_js)
    require(match is not None, "app.js must declare a single PROJECTION_URL consumer boundary")
    return match.group(1)


def semantic_tokens(projection: dict[str, object]) -> set[str]:
    tokens: set[str] = set()
    for concept in projection["concepts"]:
        tokens.add(concept["id"])
        tokens.add(concept["iri"])
        tokens.add(concept["displayLabel"])
        for relation_name in ("directSuperClasses", "requiredToppings"):
            for relation in concept[relation_name]:
                tokens.add(relation["id"])
                tokens.add(relation["iri"])
    return {token for token in tokens if token}


def smoke_test_http() -> None:
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        port = server.server_address[1]
        base = f"http://127.0.0.1:{port}"
        urls = [
            f"{base}/examples/ux/pizza-explorer/",
            f"{base}/examples/ux/pizza-explorer/app.js",
            f"{base}/examples/ux/pizza-explorer/styles.css",
            f"{base}/projections/pizza-concepts/pizza-concepts.json",
        ]
        responses = []
        for url in urls:
            with urllib.request.urlopen(url, timeout=5) as response:
                require(response.status == 200, f"HTTP smoke test failed for {url}")
                responses.append(response.read())

        served_projection = json.loads(responses[-1].decode("utf-8"))
        require(served_projection == json.loads(PROJECTION.read_text()), "served projection differs from repository file")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main() -> None:
    for path in (INDEX, APP, STYLES, PROJECTION):
        require(path.is_file(), f"required UX file missing: {path.relative_to(ROOT)}")

    projection = json.loads(PROJECTION.read_text())
    app_js = APP.read_text()
    index_html = INDEX.read_text()

    projection_url = extract_projection_url(app_js)
    resolved_projection = (HERE / projection_url).resolve()
    require(
        resolved_projection == PROJECTION.resolve(),
        f"PROJECTION_URL must resolve to {PROJECTION.relative_to(ROOT)}",
    )

    # The consumer code may know the projection schema keys, but it must not
    # duplicate the selected Pizza concept instances or topping identities.
    copied_tokens = sorted(
        token
        for token in semantic_tokens(projection)
        if token in app_js or token in index_html
    )
    require(
        not copied_tokens,
        "UX hard-codes projection data instead of consuming it: " + ", ".join(copied_tokens),
    )

    require("requiredToppings" in app_js, "UI must render the projection's requiredToppings contract")
    require("directSuperClasses" in app_js, "UI must render the projection's directSuperClasses contract")
    require("traceability" in app_js, "UI must expose projection traceability")
    require("hasTopping some X" in index_html, "UI must explain the existential topping semantics precisely")
    require("does not parse or reinterpret the OWL ontology" in index_html, "UI must state its semantic boundary")

    smoke_test_http()
    print(
        "SUCCESS: Pizza explorer consumes the checked-in semantic projection, "
        "contains no hard-coded projected concept data, and serves all required assets."
    )


if __name__ == "__main__":
    main()
