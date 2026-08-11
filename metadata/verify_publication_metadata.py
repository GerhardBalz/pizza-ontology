from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "metadata" / "publication.ttl"

DCAT = Namespace("http://www.w3.org/ns/dcat#")
PUB = Namespace("urn:pizza-ontology:publication:")

CATALOG = PUB.PizzaPreservationCatalog
RELEASE = PUB.PreservationV010

HISTORICAL_ONTOLOGY = URIRef("http://www.co-ode.org/ontologies/pizza")
HISTORICAL_VERSION = URIRef("http://www.co-ode.org/ontologies/pizza/2.0.0")
UPSTREAM = URIRef("https://protege.stanford.edu/ontologies/pizza/pizza.owl")
REPOSITORY = URIRef("https://github.com/GerhardBalz/pizza-ontology")
RELEASE_PAGE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.1.0"
)
RELEASE_SOURCE = URIRef(
    "https://github.com/GerhardBalz/pizza-ontology/blob/preservation-v0.1.0/src/ontology/pizza-edit.owl"
)


def require(graph: Graph, triple: tuple) -> None:
    if triple not in graph:
        raise AssertionError(f"Missing publication metadata triple: {triple!r}")


def main() -> None:
    graph = Graph()
    graph.parse(CATALOG_PATH, format="turtle")

    require(graph, (CATALOG, RDF.type, DCAT.Catalog))
    require(graph, (CATALOG, DCTERMS.relation, HISTORICAL_ONTOLOGY))
    require(graph, (CATALOG, DCTERMS.source, UPSTREAM))
    require(graph, (CATALOG, DCAT.landingPage, REPOSITORY))
    require(graph, (CATALOG, DCAT.dataset, RELEASE))

    require(graph, (RELEASE, RDF.type, DCAT.Dataset))
    require(graph, (RELEASE, DCTERMS.identifier, Literal("preservation-v0.1.0")))
    require(graph, (RELEASE, DCTERMS.relation, HISTORICAL_ONTOLOGY))
    require(graph, (RELEASE, DCTERMS.relation, HISTORICAL_VERSION))
    require(graph, (RELEASE, DCTERMS.source, UPSTREAM))
    require(graph, (RELEASE, DCTERMS.source, RELEASE_SOURCE))
    require(graph, (RELEASE, DCAT.landingPage, RELEASE_PAGE))
    require(graph, (RELEASE, DCAT.accessURL, RELEASE_PAGE))

    # preservation-v0.1.0 predates the repository's multi-format preservation
    # distribution workflow. Do not invent or retrofit ontology release-asset
    # URLs into its publication metadata.
    download_urls = list(graph.objects(RELEASE, DCAT.downloadURL))
    if download_urls:
        raise AssertionError(
            "preservation-v0.1.0 must not claim ontology release-asset "
            f"downloadURL values: {download_urls!r}"
        )

    # Historical semantic identifiers remain identifiers. This repository must
    # not attach its own GitHub publication locations to them as though it
    # controlled the historical co-ode.org namespace.
    for historical_identifier in (HISTORICAL_ONTOLOGY, HISTORICAL_VERSION):
        for predicate in (DCAT.landingPage, DCAT.accessURL, DCAT.downloadURL):
            locations = list(graph.objects(historical_identifier, predicate))
            if locations:
                raise AssertionError(
                    "Historical Pizza semantic identifier is being conflated "
                    f"with repository publication location: {historical_identifier} "
                    f"{predicate} {locations!r}"
                )

    print("Publication metadata contract verified.")


if __name__ == "__main__":
    main()
