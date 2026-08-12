#!/usr/bin/env python3
"""Verify the reviewed SMO typing boundary for Pizza implementation projections."""

from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
JSON_EVIDENCE = ROOT / "projections/pizza-concepts/profile/evidence.ttl"
OPENAPI_EVIDENCE = ROOT / "projections/pizza-openapi/evidence.ttl"
JSON_PROJECTION = ROOT / "projections/pizza-concepts/pizza-concepts.json"
OPENAPI_PROJECTION = ROOT / "projections/pizza-openapi/pizza-concepts.openapi.json"
OPENAPI_CONFIG = ROOT / "projections/pizza-openapi/openapi-config.json"
HISTORICAL_ONTOLOGY = ROOT / "src/ontology/pizza-edit.owl"
MAPPING_RESULT = ROOT / "artifacts/mappings/data/expected-menu.ttl"
PUBLICATION_METADATA = ROOT / "metadata/publication.ttl"

SOURCE = URIRef("http://www.co-ode.org/ontologies/pizza/2.0.0")
JSON_PROJECTION_ID = URIRef("urn:pizza-ontology:projection:pizza-concepts:v1")

SMO = Namespace("https://w3id.org/smo#")
ESKA = Namespace("https://w3id.org/eska#")
PROV = Namespace("http://www.w3.org/ns/prov#")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_graph(path: Path) -> Graph:
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def implementation_projections(graph: Graph) -> set[URIRef]:
    return {
        subject
        for subject in graph.subjects(RDF.type, SMO.ImplementationProjection)
        if isinstance(subject, URIRef)
    }


def verify_json_projection() -> None:
    evidence = load_graph(JSON_EVIDENCE)
    projection = load_json(JSON_PROJECTION)

    require(projection["projection"]["id"] == str(JSON_PROJECTION_ID), "JSON projection identity changed")
    require(
        projection["sourceSemanticModel"]["versionIri"] == str(SOURCE),
        "JSON projection source semantic-model identity changed",
    )
    require((SOURCE, RDF.type, SMO.SemanticModel) in evidence, "Pizza source lacks smo:SemanticModel in JSON evidence")
    require((SOURCE, RDF.type, ESKA.SemanticModel) in evidence, "existing eska:SemanticModel evidence was lost")
    require((SOURCE, RDF.type, PROV.Entity) in evidence, "existing source PROV entity evidence was lost")
    require(
        (JSON_PROJECTION_ID, RDF.type, SMO.ImplementationProjection) in evidence,
        "JSON catalog lacks smo:ImplementationProjection",
    )
    require((JSON_PROJECTION_ID, RDF.type, ESKA.Result) in evidence, "existing JSON eska:Result evidence was lost")
    require((JSON_PROJECTION_ID, RDF.type, PROV.Entity) in evidence, "existing JSON PROV entity evidence was lost")
    require(
        (JSON_PROJECTION_ID, PROV.wasDerivedFrom, SOURCE) in evidence,
        "JSON implementation projection lost provenance to Pizza Ontology 2.0",
    )
    require(
        implementation_projections(evidence) == {JSON_PROJECTION_ID},
        "JSON evidence broadened smo:ImplementationProjection beyond the reviewed artifact",
    )


def verify_openapi_projection() -> None:
    evidence = load_graph(OPENAPI_EVIDENCE)
    document = load_json(OPENAPI_PROJECTION)
    config = load_json(OPENAPI_CONFIG)
    projection_id = URIRef(config["projectionId"])

    extension = document["x-pizza-projection"]
    require(extension["projection"]["id"] == str(projection_id), "OpenAPI projection identity changed")
    require(
        extension["sourceSemanticModel"]["versionIri"] == str(SOURCE),
        "OpenAPI source semantic-model identity changed",
    )
    require(
        set(extension["projectionPolicy"]) == {"preserved", "transformed", "introduced", "omitted"},
        "OpenAPI projection no longer carries the explicit four-part projection policy",
    )
    require((SOURCE, RDF.type, SMO.SemanticModel) in evidence, "Pizza source lacks smo:SemanticModel in OpenAPI evidence")
    require(
        (projection_id, RDF.type, SMO.ImplementationProjection) in evidence,
        "OpenAPI contract lacks smo:ImplementationProjection",
    )
    require((projection_id, RDF.type, PROV.Entity) in evidence, "OpenAPI projection lacks PROV entity evidence")
    require(
        (projection_id, PROV.wasDerivedFrom, SOURCE) in evidence,
        "OpenAPI implementation projection lacks provenance to Pizza Ontology 2.0",
    )
    require(
        implementation_projections(evidence) == {projection_id},
        "OpenAPI evidence broadened smo:ImplementationProjection beyond the reviewed artifact",
    )


def verify_negative_boundary() -> None:
    historical = HISTORICAL_ONTOLOGY.read_text(encoding="utf-8")
    require(
        "https://w3id.org/smo" not in historical,
        "historical Pizza ontology was modified to carry external SMO architectural typing",
    )

    for path in (MAPPING_RESULT, PUBLICATION_METADATA):
        text = path.read_text(encoding="utf-8")
        require(
            "ImplementationProjection" not in text or "https://w3id.org/smo" not in text,
            f"reviewed negative boundary broadened into {path.relative_to(ROOT)}",
        )


def main() -> None:
    verify_json_projection()
    verify_openapi_projection()
    verify_negative_boundary()
    print("PASS: Pizza SMO alignment is limited to the semantic source and two proven implementation projections")


if __name__ == "__main__":
    main()
