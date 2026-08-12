#!/usr/bin/env python3
"""Verify the Pizza concept projection/preservation profile end to end."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS

HERE = Path(__file__).resolve().parent
PROJECTION_DIR = HERE.parent
ROOT = HERE.parents[2]
BUILD = HERE / "build"

sys.path.insert(0, str(PROJECTION_DIR))
import project as projection_project  # noqa: E402

PROFILE_PATH = HERE / "profile.ttl"
CONTRACT_PATH = HERE / "preservation-contract.json"
SHAPES_PATH = HERE / "shapes.ttl"
EVIDENCE_PATH = HERE / "evidence.ttl"
REPORT_PATH = BUILD / "shacl-report.ttl"
SUMMARY_PATH = BUILD / "evidence.json"

PROFILE_ID = URIRef("urn:pizza-ontology:profile:pizza-concepts-preservation:v1")
PROJECTION_ID = URIRef("urn:pizza-ontology:projection:pizza-concepts:v1")
SOURCE_ID = URIRef("http://www.co-ode.org/ontologies/pizza/2.0.0")
VERIFICATION_ID = URIRef("urn:pizza-ontology:verification:pizza-concepts-profile:v1")

PROF = Namespace("http://www.w3.org/ns/dx/prof/")
ROLE = Namespace("http://www.w3.org/ns/dx/prof/role/")
SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
ESKA = Namespace("https://w3id.org/eska#")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_projection_and_contract() -> dict:
    projection = projection_project.build_projection()
    projection_project.validate_projection(projection)
    projection_project.check_golden(projection)

    contract = load_json(CONTRACT_PATH)
    require(contract["profileId"] == str(PROFILE_ID), "profileId does not match profile identity")
    require(contract["projectionId"] == projection["projection"]["id"], "projectionId does not match generated projection")
    require(
        contract["sourceVersionIri"] == projection["sourceSemanticModel"]["versionIri"] == str(SOURCE_ID),
        "sourceVersionIri does not match authoritative Pizza source identity",
    )

    policy_mapping = {
        "mustPreserve": "preserved",
        "mayTransform": "transformed",
        "mayIntroduce": "introduced",
        "mayOmit": "omitted",
    }
    for contract_key, projection_key in policy_mapping.items():
        contract_policy = [item["projectionPolicyText"] for item in contract[contract_key]]
        actual_policy = projection["projectionPolicy"][projection_key]
        require(
            contract_policy == actual_policy,
            f"{contract_key} no longer exactly matches projectionPolicy.{projection_key}",
        )

    selected = contract["selectedConcepts"]
    actual_ids = [concept["id"] for concept in projection["concepts"]]
    require(selected == actual_ids, "profile selectedConcepts no longer match generated projection concepts")

    for concept in projection["concepts"]:
        require(concept["iri"], f"{concept['id']} lost historical IRI preservation")
        require(
            concept["traceability"]["sourceEntityIri"] == concept["iri"],
            f"{concept['id']} traceability no longer points to the projected historical IRI",
        )
        require(isinstance(concept["directSuperClasses"], list), f"{concept['id']} directSuperClasses is not projected")
        require(isinstance(concept["requiredToppings"], list), f"{concept['id']} requiredToppings is not projected")

    return projection


def load_data_graph() -> Graph:
    graph = Graph()
    graph.parse(PROFILE_PATH, format="turtle")
    graph.parse(EVIDENCE_PATH, format="turtle")
    return graph


def verify_profile_structure(graph: Graph) -> None:
    require((PROFILE_ID, RDF.type, PROF.Profile) in graph, "profile is not typed prof:Profile")
    require(
        not list(graph.objects(PROFILE_ID, PROF.isProfileOf)),
        "root profile must not use prof:isProfileOf for the historical Pizza ontology",
    )
    require(
        (PROJECTION_ID, DCTERMS.conformsTo, PROFILE_ID) in graph,
        "projection does not claim conformance to the explicit profile",
    )
    require(
        (PROJECTION_ID, PROV.wasDerivedFrom, SOURCE_ID) in graph,
        "projection lacks PROV lineage to Pizza Ontology 2.0",
    )

    required_roles = {ROLE.specification, ROLE.constraints, ROLE.schema, ROLE.validation}
    observed_roles = set()
    for descriptor in graph.objects(PROFILE_ID, PROF.hasResource):
        observed_roles.update(graph.objects(descriptor, PROF.hasRole))
    require(required_roles <= observed_roles, "profile does not expose all required PROF resource roles")


def run_shacl(data_graph: Graph) -> tuple[bool, Graph, str]:
    shapes_graph = Graph().parse(SHAPES_PATH, format="turtle")
    conforms, report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
    )
    require(isinstance(report_graph, Graph), "pySHACL did not return an RDF report graph")
    return bool(conforms), report_graph, str(report_text)


def enrich_and_write_report(report_graph: Graph) -> None:
    reports = list(report_graph.subjects(RDF.type, SH.ValidationReport))
    require(len(reports) == 1, "expected exactly one sh:ValidationReport")
    report = reports[0]
    require((report, SH.conforms, Literal(True)) in report_graph, "positive SHACL report does not contain sh:conforms true")
    report_graph.add((report, RDF.type, ESKA.Result))
    report_graph.add((report, RDF.type, PROV.Entity))
    report_graph.add((report, PROV.wasGeneratedBy, VERIFICATION_ID))
    report_graph.serialize(destination=REPORT_PATH, format="turtle")


def verify_negative_control(data_graph: Graph) -> None:
    negative = Graph()
    for triple in data_graph:
        negative.add(triple)
    negative.remove((PROJECTION_ID, DCTERMS.conformsTo, PROFILE_ID))

    conforms, report_graph, report_text = run_shacl(negative)
    if conforms:
        raise AssertionError("negative control unexpectedly conformed after removing dcterms:conformsTo")

    reports = list(report_graph.subjects(RDF.type, SH.ValidationReport))
    require(reports, "negative control did not produce a SHACL validation report")
    require(
        any((report, SH.conforms, Literal(False)) in report_graph for report in reports),
        "negative control report does not state sh:conforms false",
    )
    require("conforms" in report_text.lower(), "negative control failure was not reported as a conformance violation")


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)

    projection = verify_projection_and_contract()
    data_graph = load_data_graph()
    verify_profile_structure(data_graph)

    conforms, report_graph, report_text = run_shacl(data_graph)
    if not conforms:
        raise AssertionError("positive projection evidence graph failed SHACL validation:\n" + report_text)
    enrich_and_write_report(report_graph)

    verify_negative_control(data_graph)

    summary = {
        "profile": str(PROFILE_ID),
        "projection": projection["projection"]["id"],
        "sourceSemanticModel": projection["sourceSemanticModel"]["versionIri"],
        "projectionRegeneration": "passed",
        "jsonSchemaValidation": "passed",
        "selectedSemanticPreservation": "passed",
        "profileContractAlignment": "passed",
        "shaclConforms": True,
        "negativeControlConforms": False,
        "verification": str(VERIFICATION_ID),
        "shaclReport": str(REPORT_PATH.relative_to(ROOT)),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print("PASS: Pizza projection satisfies its explicit projection/preservation profile")


if __name__ == "__main__":
    main()
