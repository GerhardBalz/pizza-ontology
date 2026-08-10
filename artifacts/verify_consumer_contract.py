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
    "artifacts/rules/vegetarian-warning.rq",
    "artifacts/rules/rule-vocabulary.ttl",
    "artifacts/rules/data/menu-pizzas.ttl",
    "artifacts/decisions/pizza-dietary-suitability.dmn",
    "artifacts/decisions/decision-vocabulary.ttl",
    "artifacts/decisions/data/cases.json",
    "artifacts/calculations/pizza-area.openmath.xml",
    "artifacts/calculations/calculation-vocabulary.ttl",
    "artifacts/calculations/data/cases.json",
    "artifacts/mappings/pizza-to-menu.rq",
    "artifacts/mappings/menu-vocabulary.ttl",
    "artifacts/mappings/data/source-pizzas.ttl",
    "artifacts/mappings/data/expected-menu.ttl",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    graph = Graph().parse(MANIFEST, format="turtle")

    distributions = set(graph.objects(ART.PizzaSemanticArtifactSet, DCAT["distribution"]))
    require(len(distributions) == 17, f"expected seventeen published distributions, got {len(distributions)}")

    paths: set[str] = set()
    for distribution in distributions:
        identifier = graph.value(distribution, DCTERMS["identifier"])
        media_type = graph.value(distribution, DCTERMS["format"])
        license_iri = graph.value(distribution, DCTERMS["license"])

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
        (reasoning, DCTERMS["license"], URIRef("https://creativecommons.org/licenses/by/3.0/")) in graph,
        "reasoning module must retain CC BY 3.0",
    )
    require(any(graph.objects(reasoning, PROV["wasDerivedFrom"])), "reasoning module must retain explicit derivation provenance")

    for authored in (
        ART.PizzaInstanceShapes,
        ART.ConformingPizzaData,
        ART.NonConformingPizzaData,
        ART.PizzaVegetarianWarningRule,
        ART.PizzaRuleVocabulary,
        ART.PizzaRuleData,
        ART.PizzaDietarySuitabilityDecision,
        ART.PizzaDecisionVocabulary,
        ART.PizzaDecisionCases,
        ART.PizzaAreaCalculationFormula,
        ART.PizzaCalculationVocabulary,
        ART.PizzaCalculationCases,
        ART.PizzaMenuProjectionMapping,
        ART.PizzaMenuVocabulary,
        ART.PizzaMappingSourceData,
        ART.PizzaMappingExpectedOutput,
    ):
        require(
            (authored, DCTERMS["license"], URIRef("https://opensource.org/license/mit")) in graph,
            f"{authored}: repository-authored engineering artifact must identify the MIT license",
        )

    require((ART.PizzaVegetarianWarningRule, DCTERMS["requires"], ART.PizzaRuleVocabulary) in graph, "Pizza rule must require the published rule vocabulary")
    require((ART.PizzaRuleData, DCTERMS["requires"], ART.PizzaRuleVocabulary) in graph, "Pizza rule data must require the published rule vocabulary")

    require(
        (ART.PizzaDietarySuitabilityDecision, DCTERMS["conformsTo"], URIRef("https://www.omg.org/spec/DMN/1.5/")) in graph,
        "Pizza decision model must identify DMN 1.5 conformance",
    )
    require((ART.PizzaDietarySuitabilityDecision, DCTERMS["requires"], ART.PizzaDecisionVocabulary) in graph, "Pizza decision model must require the published decision vocabulary")
    require((ART.PizzaDecisionCases, DCTERMS["requires"], ART.PizzaDietarySuitabilityDecision) in graph, "Pizza decision cases must require the published DMN decision model")
    require((ART.PizzaDecisionCases, DCTERMS["requires"], ART.PizzaDecisionVocabulary) in graph, "Pizza decision cases must require the published decision vocabulary")

    require(
        (ART.PizzaAreaCalculationFormula, DCTERMS["conformsTo"], URIRef("https://openmath.org/standard/om20-2019-07-01/omstd20.html")) in graph,
        "Pizza calculation formula must identify OpenMath 2.0 Revision 2 conformance",
    )
    require((ART.PizzaAreaCalculationFormula, DCTERMS["requires"], ART.PizzaCalculationVocabulary) in graph, "Pizza calculation formula must require the published calculation vocabulary")
    require((ART.PizzaCalculationCases, DCTERMS["requires"], ART.PizzaAreaCalculationFormula) in graph, "Pizza calculation cases must require the published OpenMath formula")
    require((ART.PizzaCalculationCases, DCTERMS["requires"], ART.PizzaCalculationVocabulary) in graph, "Pizza calculation cases must require the published calculation vocabulary")

    require(
        (ART.PizzaMenuProjectionMapping, DCTERMS["conformsTo"], URIRef("https://www.w3.org/TR/sparql11-query/")) in graph,
        "Pizza mapping must identify SPARQL 1.1 Query conformance",
    )
    require((ART.PizzaMenuProjectionMapping, DCTERMS["requires"], ART.PizzaMenuVocabulary) in graph, "Pizza mapping must require the target Menu vocabulary")
    require((ART.PizzaMappingExpectedOutput, DCTERMS["conformsTo"], ART.PizzaMenuVocabulary) in graph, "expected mapping output must conform to the target Menu vocabulary")
    require((ART.PizzaMappingExpectedOutput, DCTERMS["requires"], ART.PizzaMenuProjectionMapping) in graph, "expected mapping output must require the mapping specification")
    require((ART.PizzaMappingExpectedOutput, DCTERMS["requires"], ART.PizzaMappingSourceData) in graph, "expected mapping output must require the canonical source data")

    print("SUCCESS: Pizza semantic artifact consumer contract is complete and resolves to repository-owned files.")
    for path in sorted(paths):
        print(f"- {path}")


if __name__ == "__main__":
    main()
