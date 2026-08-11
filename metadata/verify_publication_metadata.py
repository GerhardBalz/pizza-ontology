from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "metadata" / "publication.ttl"

DCAT = Namespace("http://www.w3.org/ns/dcat#")
PUB = Namespace("urn:pizza-ontology:publication:")

CATALOG = PUB.PizzaPreservationCatalog
RELEASE_V010 = PUB.PreservationV010
RELEASE_V020 = PUB.PreservationV020
DIST_OFN = PUB.PreservationV020FunctionalSyntax
DIST_TTL = PUB.PreservationV020Turtle
DIST_CHECKSUMS = PUB.PreservationV020Checksums

HISTORICAL_ONTOLOGY = URIRef("http://www.co-ode.org/ontologies/pizza")
HISTORICAL_VERSION = URIRef("http://www.co-ode.org/ontologies/pizza/2.0.0")
UPSTREAM = URIRef("https://protege.stanford.edu/ontologies/pizza/pizza.owl")
REPOSITORY = URIRef("https://github.com/GerhardBalz/pizza-ontology")
CC_BY_3 = URIRef("https://creativecommons.org/licenses/by/3.0/")

RELEASE_V010_PAGE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.1.0"
)
RELEASE_V010_SOURCE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/blob/preservation-v0.1.0/src/ontology/pizza-edit.owl"
)

RELEASE_V020_COMMIT = "3bd6e3817e2cdc44e77899a2e603878a85845e9d"
RELEASE_V020_PAGE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.2.0"
)
RELEASE_V020_TAG_SOURCE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/blob/preservation-v0.2.0/src/ontology/pizza-edit.owl"
)
RELEASE_V020_COMMIT_SOURCE = URIRef(
    f"https://github.com/GerhardBalz/pizza-ontology/blob/{RELEASE_V020_COMMIT}/src/ontology/pizza-edit.owl"
)

DOWNLOAD_OFN = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/download/"
    "preservation-v0.2.0/pizza-2.0-preserved.ofn"
)
DOWNLOAD_TTL = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/download/"
    "preservation-v0.2.0/pizza-2.0-preserved.ttl"
)
DOWNLOAD_CHECKSUMS = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/download/"
    "preservation-v0.2.0/SHA256SUMS"
)


def require(graph: Graph, triple: tuple) -> None:
    if triple not in graph:
        raise AssertionError(f"Missing publication metadata triple: {triple!r}")


def require_exact_objects(graph: Graph, subject, predicate, expected: set) -> None:
    actual = set(graph.objects(subject, predicate))
    if actual != expected:
        raise AssertionError(
            f"Unexpected objects for {subject} {predicate}: expected={expected!r}, actual={actual!r}"
        )


def verify_distribution(
    graph: Graph,
    distribution,
    identifier: str,
    format_value: str,
    download_url: URIRef,
    *,
    semantic_content: bool,
) -> None:
    require(graph, (distribution, RDF.type, DCAT.Distribution))
    require(graph, (distribution, DCTERMS.identifier, Literal(identifier)))
    require(graph, (distribution, DCTERMS.format, Literal(format_value)))
    require(graph, (distribution, DCAT.accessURL, RELEASE_V020_PAGE))
    require_exact_objects(graph, distribution, DCAT.downloadURL, {download_url})

    if semantic_content:
        require(graph, (distribution, DCTERMS.license, CC_BY_3))
        require(graph, (distribution, DCTERMS.relation, HISTORICAL_VERSION))
        require(graph, (distribution, Namespace("http://www.w3.org/ns/prov#").wasDerivedFrom, RELEASE_V020_COMMIT_SOURCE))


def main() -> None:
    graph = Graph()
    graph.parse(CATALOG_PATH, format="turtle")

    require(graph, (CATALOG, RDF.type, DCAT.Catalog))
    require(graph, (CATALOG, DCTERMS.relation, HISTORICAL_ONTOLOGY))
    require(graph, (CATALOG, DCTERMS.source, UPSTREAM))
    require(graph, (CATALOG, DCAT.landingPage, REPOSITORY))
    require_exact_objects(graph, CATALOG, DCAT.dataset, {RELEASE_V010, RELEASE_V020})

    # preservation-v0.1.0 remains an immutable source-snapshot release and must
    # not be retrofitted with the later multi-format distribution assets.
    require(graph, (RELEASE_V010, RDF.type, DCAT.Dataset))
    require(graph, (RELEASE_V010, DCTERMS.identifier, Literal("preservation-v0.1.0")))
    require(graph, (RELEASE_V010, DCTERMS.relation, HISTORICAL_ONTOLOGY))
    require(graph, (RELEASE_V010, DCTERMS.relation, HISTORICAL_VERSION))
    require(graph, (RELEASE_V010, DCTERMS.source, UPSTREAM))
    require(graph, (RELEASE_V010, DCTERMS.source, RELEASE_V010_SOURCE))
    require(graph, (RELEASE_V010, DCAT.landingPage, RELEASE_V010_PAGE))
    require(graph, (RELEASE_V010, DCAT.accessURL, RELEASE_V010_PAGE))
    require_exact_objects(graph, RELEASE_V010, DCAT.downloadURL, set())
    require_exact_objects(graph, RELEASE_V010, DCAT.distribution, set())

    # preservation-v0.2.0 is the first release that actually publishes the
    # governed Functional Syntax + Turtle + checksum bundle.
    require(graph, (RELEASE_V020, RDF.type, DCAT.Dataset))
    require(graph, (RELEASE_V020, DCTERMS.identifier, Literal("preservation-v0.2.0")))
    require(graph, (RELEASE_V020, DCTERMS.relation, HISTORICAL_ONTOLOGY))
    require(graph, (RELEASE_V020, DCTERMS.relation, HISTORICAL_VERSION))
    require(graph, (RELEASE_V020, DCTERMS.source, UPSTREAM))
    require(graph, (RELEASE_V020, DCTERMS.source, RELEASE_V020_TAG_SOURCE))
    require(graph, (RELEASE_V020, DCTERMS.source, RELEASE_V020_COMMIT_SOURCE))
    require(graph, (RELEASE_V020, DCAT.landingPage, RELEASE_V020_PAGE))
    require(graph, (RELEASE_V020, DCAT.accessURL, RELEASE_V020_PAGE))
    require_exact_objects(graph, RELEASE_V020, DCAT.downloadURL, set())
    require_exact_objects(
        graph,
        RELEASE_V020,
        DCAT.distribution,
        {DIST_OFN, DIST_TTL, DIST_CHECKSUMS},
    )

    verify_distribution(
        graph,
        DIST_OFN,
        "pizza-2.0-preserved.ofn",
        "OWL Functional Syntax",
        DOWNLOAD_OFN,
        semantic_content=True,
    )
    verify_distribution(
        graph,
        DIST_TTL,
        "pizza-2.0-preserved.ttl",
        "text/turtle",
        DOWNLOAD_TTL,
        semantic_content=True,
    )
    verify_distribution(
        graph,
        DIST_CHECKSUMS,
        "SHA256SUMS",
        "text/plain",
        DOWNLOAD_CHECKSUMS,
        semantic_content=False,
    )
    require_exact_objects(
        graph,
        DIST_CHECKSUMS,
        DCTERMS.relation,
        {DIST_OFN, DIST_TTL},
    )

    # Historical semantic identifiers remain identifiers. This repository must
    # not attach GitHub publication locations to them as though it controlled
    # the historical co-ode.org namespace.
    for historical_identifier in (HISTORICAL_ONTOLOGY, HISTORICAL_VERSION):
        for predicate in (DCAT.landingPage, DCAT.accessURL, DCAT.downloadURL):
            locations = list(graph.objects(historical_identifier, predicate))
            if locations:
                raise AssertionError(
                    "Historical Pizza semantic identifier is being conflated "
                    f"with repository publication location: {historical_identifier} "
                    f"{predicate} {locations!r}"
                )

    print(
        "Publication metadata contract verified for preservation-v0.1.0 and "
        "published preservation-v0.2.0 distributions."
    )


if __name__ == "__main__":
    main()
