#!/usr/bin/env python3
"""Execute and verify the canonical Pizza BPMN workflow artifact."""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

from pyshacl import validate
from rdflib import Graph, Namespace, URIRef
from rdflib.compare import isomorphic

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = HERE / "results"

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
WF_NS = "urn:pizza-ontology:workflow:"
BPMN = {"bpmn": BPMN_NS, "wf": WF_NS}

DCTERMS = Namespace("http://purl.org/dc/terms/")
ART = Namespace("urn:pizza-ontology:artifact:")
WF = Namespace(WF_NS)

WORKFLOW = HERE / "pizza-menu-publication.bpmn"
VOCAB = HERE / "workflow-vocabulary.ttl"
CASES = HERE / "data" / "cases.json"
SHAPES = ROOT / "artifacts" / "validation" / "pizza-instance-shapes.ttl"
MAPPING = ROOT / "artifacts" / "mappings" / "pizza-to-menu.rq"
MENU_VOCAB = ROOT / "artifacts" / "mappings" / "menu-vocabulary.ttl"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_workflow() -> dict[str, object]:
    root = ET.parse(WORKFLOW).getroot()
    require(root.tag == f"{{{BPMN_NS}}}definitions", "workflow must use the BPMN 2.0 MODEL namespace")

    process = root.find("bpmn:process", BPMN)
    require(process is not None, "workflow must contain one BPMN process")
    require(process.get("id") == "PizzaMenuPublicationProcess", "unexpected workflow process id")
    require(process.get("isExecutable") == "true", "workflow process must be executable")

    tasks: dict[str, str] = {}
    for task in process.findall("bpmn:serviceTask", BPMN):
        task_id = task.get("id")
        implementation = task.get("implementation")
        binding = task.find("bpmn:extensionElements/wf:semanticOperation", BPMN)
        require(task_id is not None and implementation is not None, "workflow service task missing id or implementation")
        require(binding is not None and binding.get("ref") == implementation, f"{task_id}: semantic operation binding must match implementation")
        tasks[task_id] = implementation

    require(tasks == {
        "ValidatePizzaData": str(WF.ValidatePizzaData),
        "TransformPizzaToMenu": str(WF.TransformPizzaToMenu),
    }, f"unexpected workflow task bindings: {tasks}")

    gateway = process.find("bpmn:exclusiveGateway[@id='ValidationGateway']", BPMN)
    require(gateway is not None, "workflow must contain ValidationGateway")
    require(gateway.get("default") == "FlowRejected", "validation gateway default path must reject")

    flows: dict[str, tuple[str, str, str | None]] = {}
    for flow in process.findall("bpmn:sequenceFlow", BPMN):
        condition = flow.find("bpmn:conditionExpression", BPMN)
        flows[str(flow.get("id"))] = (
            str(flow.get("sourceRef")),
            str(flow.get("targetRef")),
            (condition.text or "").strip() if condition is not None else None,
        )

    require(flows.get("FlowStartValidate") == ("Start", "ValidatePizzaData", None), "workflow must start with validation")
    require(flows.get("FlowValidateGateway") == ("ValidatePizzaData", "ValidationGateway", None), "validation must feed the gateway")
    require(flows.get("FlowPublished") == ("ValidationGateway", "TransformPizzaToMenu", "validationConforms"), "conforming path must execute mapping")
    require(flows.get("FlowRejected") == ("ValidationGateway", "Rejected", None), "default path must end Rejected")
    require(flows.get("FlowTransformPublished") == ("TransformPizzaToMenu", "Published", None), "mapping must end Published")

    outcomes: dict[str, str] = {}
    for end in process.findall("bpmn:endEvent", BPMN):
        binding = end.find("bpmn:extensionElements/wf:workflowOutcome", BPMN)
        if binding is not None:
            outcomes[str(end.get("id"))] = str(binding.get("ref"))
    require(outcomes == {"Published": str(WF.Published), "Rejected": str(WF.Rejected)}, f"unexpected workflow outcomes: {outcomes}")

    return {"process": process.get("id"), "tasks": tasks, "outcomes": outcomes}


def verify_operation_bindings() -> None:
    graph = Graph().parse(VOCAB, format="turtle")
    require((WF.ValidatePizzaData, DCTERMS.requires, ART.PizzaInstanceShapes) in graph, "validation workflow operation must require PizzaInstanceShapes")
    require((WF.TransformPizzaToMenu, DCTERMS.requires, ART.PizzaMenuMapping) in graph, "mapping workflow operation must require PizzaMenuMapping")
    require((WF.TransformPizzaToMenu, DCTERMS.requires, ART.PizzaMenuVocabulary) in graph, "mapping workflow operation must require PizzaMenuVocabulary")
    require((WF.Published, None, None) in graph and (WF.Rejected, None, None) in graph, "workflow outcomes must be defined in the source vocabulary")


def validate_graph(data: Graph) -> bool:
    shapes = Graph().parse(SHAPES, format="turtle")
    conforms, _, _ = validate(data_graph=data, shacl_graph=shapes, inference="none", abort_on_first=False)
    return bool(conforms)


def transform_graph(data: Graph) -> Graph:
    query = MAPPING.read_text(encoding="utf-8")
    result = data.query(query)
    graph = Graph()
    for triple in result.graph:
        graph.add(triple)
    return graph


def run_cases() -> list[dict[str, object]]:
    document = json.loads(CASES.read_text(encoding="utf-8"))
    require(document.get("workflow") == "PizzaMenuPublicationProcess", "workflow cases target a different process")
    cases = document.get("cases")
    require(isinstance(cases, list) and len(cases) == 2, "expected exactly two workflow cases")

    results: list[dict[str, object]] = []
    for case in cases:
        require(isinstance(case, dict), "workflow case must be a JSON object")
        identifier = str(case["id"])
        data_path = ROOT / str(case["input"])
        data = Graph().parse(data_path, format="turtle")

        steps = [str(WF.ValidatePizzaData)]
        conforms = validate_graph(data)
        target_graph: Graph | None = None

        if conforms:
            steps.append(str(WF.TransformPizzaToMenu))
            target_graph = transform_graph(data)
            outcome = str(WF.Published)
        else:
            outcome = str(WF.Rejected)

        require(outcome == case.get("expectedOutcome"), f"{identifier}: expected outcome {case.get('expectedOutcome')}, got {outcome}")
        require(steps == case.get("expectedSteps"), f"{identifier}: expected steps {case.get('expectedSteps')}, got {steps}")

        if outcome == str(WF.Published):
            expected_path = ROOT / str(case.get("expectedTarget"))
            expected = Graph().parse(expected_path, format="turtle")
            require(target_graph is not None and isomorphic(target_graph, expected), f"{identifier}: transformed graph differs from expected target")
        else:
            require(target_graph is None, f"{identifier}: mapping must not execute for rejected workflow")
            require("expectedTarget" not in case, f"{identifier}: rejected workflow must not declare a target graph")

        results.append({
            "id": identifier,
            "validationConforms": conforms,
            "steps": steps,
            "outcome": outcome,
            "targetTripleCount": len(target_graph) if target_graph is not None else 0,
        })

    return results


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    workflow = parse_workflow()
    verify_operation_bindings()
    results = run_cases()

    payload = {"workflow": workflow["process"], "results": results}
    (RESULTS / "workflow-results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("SUCCESS: canonical Pizza BPMN workflow executed with conditional semantic steps.")
    for result in results:
        print(f"- {result['id']}: conforms={result['validationConforms']} steps={len(result['steps'])} outcome={result['outcome']}")


if __name__ == "__main__":
    main()
