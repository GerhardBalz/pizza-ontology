#!/usr/bin/env python3
"""Execute and verify the canonical Pizza semantic mapping artifact."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from rdflib.compare import isomorphic

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "data" / "source-pizzas.ttl"
EXPECTED = HERE / "data" / "expected-menu.ttl"
TARGET_MODEL = HERE / "menu-vocabulary.ttl"
MAPPING = HERE / "pizza-to-menu.rq"
RESULTS = HERE / "results"

PIZZA = Namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl#")
MENU = Namespace("urn:pizza-ontology:menu:")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    source = Graph().parse(SOURCE, format="turtle")
    target_model = Graph().parse(TARGET_MODEL, format="turtle")
    expected = Graph().parse(EXPECTED, format="turtle")
    mapping_text = MAPPING.read_text(encoding="utf-8")

    require((MENU.MenuItem, RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")) in target_model, "target semantic model must define menu:MenuItem")
    require((MENU.displayName, RDF.type, URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")) in target_model, "target semantic model must define menu:displayName")
    require((MENU.ingredientName, RDF.type, URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")) in target_model, "target semantic model must define menu:ingredientName")

    result = source.query(mapping_text)
    transformed = result.graph
    require(transformed is not None, "SPARQL CONSTRUCT mapping did not produce an RDF graph")
    require(isomorphic(transformed, expected), "transformed target graph differs from the canonical expected menu projection")

    allowed_predicates = {RDF.type, MENU.displayName, MENU.ingredientName}
    for subject, predicate, obj in transformed:
        require(predicate in allowed_predicates, f"unexpected target predicate: {predicate}")
        require(not str(predicate).startswith(str(PIZZA)), f"source Pizza predicate leaked into target graph: {predicate}")
        if predicate == RDF.type:
            require(obj == MENU.MenuItem, f"target rdf:type must be menu:MenuItem, got {obj}")
        require(not (isinstance(obj, URIRef) and str(obj).startswith(str(PIZZA))), f"source Pizza class/entity leaked into target graph: {obj}")

    require(len(transformed) == 6, f"expected six target triples, got {len(transformed)}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    transformed.serialize(destination=RESULTS / "menu-projection.ttl", format="turtle")

    print("SUCCESS: Pizza semantic mapping produced the canonical target graph.")
    print("Source model: Pizza RDF vocabulary")
    print("Target model: urn:pizza-ontology:menu:")
    print(f"Triples: {len(transformed)}")
    print(f"Result: {RESULTS / 'menu-projection.ttl'}")


if __name__ == "__main__":
    main()
