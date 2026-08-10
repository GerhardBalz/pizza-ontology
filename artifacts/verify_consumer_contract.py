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
    "artifacts/workflows/pizza-menu-publication.bpmn",
    "artifacts/workflows/workflow-vocabulary.ttl",
    "artifacts/workflows/data/valid-pizza.ttl",
    "artifacts/workflows/data/invalid-pizza.ttl",
    "artifacts/workflows/data/expected-valid-menu.ttl",
    "artifacts/workflows/data/cases.json",
}

AUTHORED = (
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
    ART.PizzaMenuPublicationWorkflow,
    ART.PizzaWorkflowVocabulary,
    ART.PizzaWorkflowValidData,
    ART.PizzaWorkflowInvalidData,
    ART.PizzaWorkflowExpectedTarget,
    ART.PizzaWorkflowCases,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def requires(graph: Graph, subject, *objects) -> None:
    for obj in objects:
        require((subject, DCTERMS["requires"], obj) in graph, f"{subject} must require {obj}")


def main() -> None:
    graph = Graph().parse(MANIFEST, format="turtle")
    distributions = set(graph.objects(ART.PizzaSemanticArtifactSet, DCAT["distribution"]))
    require(len(distributions) == 23, f"expected twenty-three published distributions, got {len(distributions)}")

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
    require((reasoning, DCTERMS["license"], URIRef("https://creativecommons.org/licenses/by/3.0/")) in graph, "reasoning module must retain CC BY 3.0")
    require(any(graph.objects(reasoning, PROV["wasDerivedFrom"])), "reasoning module must retain explicit derivation provenance")

    for authored in AUTHORED:
        require((authored, DCTERMS["license"], URIRef("https://opensource.org/license/mit")) in graph, f"{authored}: repository-authored engineering artifact must identify the MIT license")

    requires(graph, ART.PizzaVegetarianWarningRule, ART.PizzaRuleVocabulary)
    requires(graph, ART.PizzaRuleData, ART.PizzaRuleVocabulary)

    require((ART.PizzaDietarySuitabilityDecision, DCTERMS["conformsTo"], URIRef("https://www.omg.org/spec/DMN/1.5/")) in graph, "Pizza decision model must identify DMN 1.5 conformance")
    requires(graph, ART.PizzaDietarySuitabilityDecision, ART.PizzaDecisionVocabulary)
    requires(graph, ART.PizzaDecisionCases, ART.PizzaDietarySuitabilityDecision, ART.PizzaDecisionVocabulary)

    require((ART.PizzaAreaCalculationFormula, DCTERMS["conformsTo"], URIRef("https://openmath.org/standard/om20-2019-07-01/omstd20.html")) in graph, "Pizza calculation formula must identify OpenMath 2.0 Revision 2 conformance")
    requires(graph, ART.PizzaAreaCalculationFormula, ART.PizzaCalculationVocabulary)
    requires(graph, ART.PizzaCalculationCases, ART.PizzaAreaCalculationFormula, ART.PizzaCalculationVocabulary)

    require((ART.PizzaMenuProjectionMapping, DCTERMS["conformsTo"], URIRef("https://www.w3.org/TR/sparql11-query/")) in graph, "Pizza mapping must identify SPARQL 1.1 Query conformance")
    requires(graph, ART.PizzaMenuProjectionMapping, ART.PizzaMenuVocabulary)
    require((ART.PizzaMappingExpectedOutput, DCTERMS["conformsTo"], ART.PizzaMenuVocabulary) in graph, "expected mapping output must conform to target Menu vocabulary")
    requires(graph, ART.PizzaMappingExpectedOutput, ART.PizzaMenuProjectionMapping, ART.PizzaMappingSourceData)

    require((ART.PizzaMenuPublicationWorkflow, DCTERMS["conformsTo"], URIRef("https://www.omg.org/spec/BPMN/2.0.2/")) in graph, "Pizza workflow must identify BPMN 2.0.2 conformance")
    requires(graph, ART.PizzaMenuPublicationWorkflow, ART.PizzaWorkflowVocabulary, ART.PizzaInstanceShapes, ART.PizzaMenuProjectionMapping, ART.PizzaMenuVocabulary)
    requires(graph, ART.PizzaWorkflowVocabulary, ART.PizzaInstanceShapes, ART.PizzaMenuProjectionMapping, ART.PizzaMenuVocabulary)
    require((ART.PizzaWorkflowExpectedTarget, DCTERMS["conformsTo"], ART.PizzaMenuVocabulary) in graph, "workflow expected target must conform to target Menu vocabulary")
    requires(graph, ART.PizzaWorkflowExpectedTarget, ART.PizzaMenuProjectionMapping, ART.PizzaWorkflowValidData)
    requires(graph, ART.PizzaWorkflowCases, ART.PizzaMenuPublicationWorkflow, ART.PizzaWorkflowVocabulary, ART.PizzaWorkflowValidData, ART.PizzaWorkflowInvalidData, ART.PizzaWorkflowExpectedTarget)

    print("SUCCESS: Pizza semantic artifact consumer contract is complete and resolves to repository-owned files.")
    for path in sorted(paths):
        print(f"- {path}")


if __name__ == "__main__":
    main()
