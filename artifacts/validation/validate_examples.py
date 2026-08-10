#!/usr/bin/env python3
"""Validate canonical conforming and non-conforming Pizza instance examples."""

from __future__ import annotations

from pathlib import Path

from pyshacl import validate
from rdflib import Namespace, URIRef

HERE = Path(__file__).resolve().parent
SHAPES = HERE / "pizza-instance-shapes.ttl"
DATA = HERE / "data"
RESULTS = HERE / "results"

SH = Namespace("http://www.w3.org/ns/shacl#")
PIZZA = Namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl#")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_case(filename: str, expected_conforms: bool):
    data_path = DATA / filename
    conforms, report_graph, report_text = validate(
        data_graph=str(data_path),
        shacl_graph=str(SHAPES),
        inference="none",
        meta_shacl=True,
        advanced=False,
        debug=False,
    )

    RESULTS.mkdir(exist_ok=True)
    report_path = RESULTS / f"{data_path.stem}-report.ttl"
    report_graph.serialize(destination=str(report_path), format="turtle")

    require(
        conforms is expected_conforms,
        f"{filename}: expected conforms={expected_conforms}, got {conforms}\n{report_text}",
    )

    return report_graph, report_text


def main() -> None:
    conforming_graph, _ = validate_case("conforming.ttl", True)
    non_conforming_graph, report_text = validate_case("non-conforming.ttl", False)

    require(
        not list(conforming_graph.objects(None, SH.result)),
        "Conforming example unexpectedly contains SHACL validation results",
    )

    result_paths = {
        path
        for path in non_conforming_graph.objects(None, SH.resultPath)
        if isinstance(path, URIRef)
    }
    require(
        PIZZA.hasBase in result_paths,
        f"Expected a hasBase violation; report paths were {sorted(map(str, result_paths))}",
    )
    require(
        PIZZA.hasTopping in result_paths,
        f"Expected a hasTopping violation; report paths were {sorted(map(str, result_paths))}",
    )

    print("SUCCESS: SHACL accepts the conforming Pizza example and rejects the non-conforming example.")
    print("Expected violation paths: pizza:hasBase, pizza:hasTopping")
    print(report_text)


if __name__ == "__main__":
    main()
