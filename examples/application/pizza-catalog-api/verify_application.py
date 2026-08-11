#!/usr/bin/env python3
"""Verify the OpenAPI → Application → UX Pizza reference path."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate_spec

from app import DATA_PATH, HERE, OPENAPI_PATH, ROOT, create_server

UX_DIR = ROOT / "examples" / "ux" / "pizza-api-explorer"
APP_SOURCE = HERE / "app.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validator_for(spec: dict, schema_name: str) -> Draft202012Validator:
    # OpenAPI 3.1 schemas use JSON Schema 2020-12. Keep the OpenAPI components
    # under the same root so existing #/components/... references resolve.
    root_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": f"#/components/schemas/{schema_name}",
        "components": spec["components"],
    }
    return Draft202012Validator(root_schema, format_checker=FormatChecker())


def request_json(url: str) -> tuple[int, dict]:
    try:
        with urlopen(url, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def request_text(url: str) -> tuple[int, str]:
    with urlopen(url, timeout=5) as response:
        return response.status, response.read().decode("utf-8")


def verify_no_semantic_fact_duplication(data: dict) -> None:
    implementation_sources = [
        APP_SOURCE,
        UX_DIR / "index.html",
        UX_DIR / "app.js",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in implementation_sources)

    selected_ids = {concept["id"] for concept in data["concepts"]}
    topping_ids = {
        topping["id"]
        for concept in data["concepts"]
        for topping in concept["requiredToppings"]
    }

    for semantic_id in sorted(selected_ids | topping_ids):
        require(
            semantic_id not in combined,
            f"projected semantic identity must not be hard-coded in application/UX source: {semantic_id}",
        )

    app_source = APP_SOURCE.read_text(encoding="utf-8")
    require("oaklib" not in app_source, "application must not import OAK at runtime")
    require("get_adapter" not in app_source, "application must not access the OWL adapter")

    ux_source = (UX_DIR / "app.js").read_text(encoding="utf-8")
    require(
        "pizza-concepts.json" not in ux_source,
        "API-backed UX must not bypass the application and load the JSON projection directly",
    )
    require("src/ontology" not in ux_source, "API-backed UX must not access ontology source paths")
    require("/concepts" in ux_source, "API-backed UX must call the application contract")


def main() -> None:
    spec = load_json(OPENAPI_PATH)
    data = load_json(DATA_PATH)
    validate_spec(spec)

    require("/concepts" in spec["paths"], "OpenAPI contract must define GET /concepts")
    require(
        "/concepts/{conceptId}" in spec["paths"],
        "OpenAPI contract must define GET /concepts/{conceptId}",
    )

    verify_no_semantic_fact_duplication(data)

    collection_validator = validator_for(spec, "PizzaConceptCollection")
    concept_validator = validator_for(spec, "PizzaConcept")
    error_validator = validator_for(spec, "Error")

    server = create_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    base = f"http://{host}:{port}"

    try:
        status, collection = request_json(f"{base}/concepts")
        require(status == 200, "GET /concepts must return HTTP 200")
        collection_validator.validate(collection)
        require(
            collection["items"] == data["concepts"],
            "unfiltered application collection must expose the checked-in JSON projection content",
        )
        require(collection["count"] == len(data["concepts"]), "collection count must match items")

        sample = data["concepts"][0]
        query = urlencode({"q": sample["id"]})
        status, filtered = request_json(f"{base}/concepts?{query}")
        require(status == 200, "q-filter request must return HTTP 200")
        collection_validator.validate(filtered)
        require(
            filtered["items"] == [sample],
            "q filtering by a projected concept identifier must select the matching concept",
        )

        topping_id = sample["requiredToppings"][0]["id"]
        query = urlencode({"requiredTopping": topping_id})
        status, topping_filtered = request_json(f"{base}/concepts?{query}")
        require(status == 200, "requiredTopping-filter request must return HTTP 200")
        collection_validator.validate(topping_filtered)
        require(topping_filtered["items"], "known projected topping filter must return at least one concept")
        require(
            all(
                any(item["id"] == topping_id for item in concept["requiredToppings"])
                for concept in topping_filtered["items"]
            ),
            "requiredTopping filtering must use projected existential-target identifiers",
        )

        encoded_id = quote(sample["id"], safe="")
        status, detail = request_json(f"{base}/concepts/{encoded_id}")
        require(status == 200, "GET /concepts/{conceptId} must return HTTP 200 for selected concept")
        concept_validator.validate(detail)
        require(detail == sample, "item endpoint must return the corresponding projected concept")

        missing_id = quote("pizza:MissingProjectionConcept", safe="")
        status, error = request_json(f"{base}/concepts/{missing_id}")
        require(status == 404, "unknown concept identifier must return documented HTTP 404")
        error_validator.validate(error)

        status, served_contract = request_json(f"{base}/openapi.json")
        require(status == 200, "application must make the checked-in contract inspectable")
        require(served_contract == spec, "served OpenAPI contract must be byte-semantically identical to checked-in spec")

        status, page = request_text(f"{base}/")
        require(status == 200, "API-backed UX root must be served by the application")
        require("Application-mediated" in page, "API-backed UX must identify its application boundary")

        status, javascript = request_text(f"{base}/app.js")
        require(status == 200 and "fetch" in javascript, "API-backed UX JavaScript must be served")

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    print(
        "SUCCESS: OpenAPI-backed Pizza application implements the checked-in interface contract, "
        "serves source-projected data, and provides an API-backed UX without runtime OWL access."
    )


if __name__ == "__main__":
    main()
