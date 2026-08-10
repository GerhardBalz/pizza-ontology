#!/usr/bin/env python3
"""Evaluate and verify the canonical Pizza SPARQL CONSTRUCT rule."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Literal, Namespace

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RULE = Namespace("urn:pizza-ontology:rule:")
EX = Namespace("urn:pizza-ontology:rule:example:")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    query_text = (HERE / "vegetarian-warning.rq").read_text(encoding="utf-8")
    require("meatyPizza" not in query_text, "rule must not hard-code the positive example")
    require("vegetablePizza" not in query_text, "rule must not hard-code the control example")

    data = Graph().parse(HERE / "data" / "menu-pizzas.ttl", format="turtle")
    Graph().parse(HERE / "rule-vocabulary.ttl", format="turtle")

    query_result = data.query(query_text)
    result_graph = query_result.graph
    require(result_graph is not None, "SPARQL CONSTRUCT did not return an RDF graph")

    expected = (EX.meatyPizza, RULE.requiresVegetarianWarning, Literal(True))
    control = (EX.vegetablePizza, RULE.requiresVegetarianWarning, Literal(True))

    require(expected in result_graph, "meatyPizza must require a vegetarian warning")
    require(control not in result_graph, "vegetablePizza must not require a vegetarian warning")

    warning_results = list(result_graph.triples((None, RULE.requiresVegetarianWarning, None)))
    require(len(warning_results) == 1, f"expected exactly one warning result, got {len(warning_results)}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    result_graph.serialize(destination=RESULTS / "evaluation.ttl", format="turtle")

    print("SUCCESS: SPARQL rule evaluation derives the warning only for the Pizza with an explicit MeatTopping.")
    print("Rule:       artifacts/rules/vegetarian-warning.rq")
    print("Input:      artifacts/rules/data/menu-pizzas.ttl")
    print("Derived:    meatyPizza requiresVegetarianWarning true")
    print("Control:    vegetablePizza has no warning result")
    print(f"Result:     {RESULTS / 'evaluation.ttl'}")


if __name__ == "__main__":
    main()
