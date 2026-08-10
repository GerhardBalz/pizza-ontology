#!/usr/bin/env python3
"""Verify the machine-readable Pizza semantic artifact consumer contract."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts" / "manifest.ttl"

DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
PROV = Namespace("http://www.w3.org/ns/prov#")
ART = Namespace("urn:pizza-ontology:artifact:")

EXPECTED = {
    "artifacts/reasoning/spicy-pizza.ofn",
    "artifacts/validation/pizza-instance-shapes.ttl",
    "artifacts/validation/data/conforming.ttl",
    "artifacts/validation/data/non-conforming.ttl",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    graph = Graph().parse(MANIFEST, format="turtle")

    distributions = set(graph.objects(ART.PizzaSemanticArtifactSet, DCAT.distribution))
    require(len(distributions) == 4, f"expected four published distributions, got {len(distributions)}")

    paths: set[str] = set()
    for distribution in distributions:
        identifier = graph.value(distribution, DCTERMS.identifier)
        media_type = graph.value(distribution, DCTERMS.format)
        license_iri = graph.value(distribution, DCTERMS.license)

        require(identifier is not None, f"{distribution}: missing dcterms:identifier")
        require(media_type is not None, f"{distribution}: missing dcterms:format")
        require(isinstance(license_iri, URIRef), f"{distribution}: missing URI-valued dcterms:license")

        path = str(identifier)
        require(path.startswith("artifacts/"), f"{distribution}: identifier must be a repository-relative artifacts/ path")
        require((ROOT / path).is_file(), f"{distribution}: published artifact does not exist: {path}")
        paths.add(path)

    require(paths == EXPECTED, f"published artifact set differs from expected contract: {sorted(paths)}")

    reasoning = ART.SpicyPizzaReasoningModule
    require(
        (reasoning, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/3.0/")) in graph,
        "reasoning module must retain CC BY 3.0",
    )
    require(
        any(graph.objects(reasoning, PROV.wasDerivedFrom)),
        "reasoning module must retain explicit derivation provenance",
    )

    for authored in (ART.PizzaInstanceShapes, ART.ConformingPizzaData, ART.NonConformingPizzaData):
        require(
            (authored, DCTERMS.license, URIRef("https://opensource.org/license/mit")) in graph,
            f"{authored}: repository-authored engineering artifact must identify the MIT license",
        )

    print("SUCCESS: Pizza semantic artifact consumer contract is complete and resolves to repository-owned files.")
    for path in sorted(paths):
        print(f"- {path}")


if __name__ == "__main__":
    main()
