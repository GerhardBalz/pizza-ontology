#!/usr/bin/env python3
"""Evaluate and verify the canonical Pizza DMN decision-table artifact.

This runner intentionally supports only the small DMN 1.5 subset exercised by
`pizza-dietary-suitability.dmn`: a UNIQUE decision table with boolean unary
input tests (`true`, `false`, `-`) and one string output.
"""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
MODEL = HERE / "pizza-dietary-suitability.dmn"
CASES = HERE / "data" / "cases.json"
RESULTS = HERE / "results"
OUTPUT = RESULTS / "decision-results.json"

DMN_NS = "https://www.omg.org/spec/DMN/20230324/MODEL/"
NS = {"dmn": DMN_NS}
EXPECTED_INPUTS = ["containsMeat", "containsFish"]
EXPECTED_OUTCOMES = {
    "urn:pizza-ontology:decision:NotVegetarian",
    "urn:pizza-ontology:decision:PescatarianOnly",
    "urn:pizza-ontology:decision:Vegetarian",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text_of(element: ET.Element | None) -> str:
    require(element is not None, "required DMN text element is missing")
    return (element.text or "").strip()


def parse_model() -> tuple[str, list[str], list[tuple[list[str], str]]]:
    root = ET.parse(MODEL).getroot()
    require(root.tag == f"{{{DMN_NS}}}definitions", "decision model must use the DMN 1.5 MODEL namespace")

    decision = root.find("dmn:decision[@id='pizzaDietarySuitabilityDecision']", NS)
    require(decision is not None, "expected Pizza dietary-suitability decision is missing")

    table = decision.find("dmn:decisionTable", NS)
    require(table is not None, "decision must contain a DMN decisionTable")
    require(table.get("hitPolicy") == "UNIQUE", "decision table must use UNIQUE hit policy")

    inputs = [
        text_of(clause.find("dmn:inputExpression/dmn:text", NS))
        for clause in table.findall("dmn:input", NS)
    ]
    require(inputs == EXPECTED_INPUTS, f"unexpected decision inputs: {inputs}")

    outputs = table.findall("dmn:output", NS)
    require(len(outputs) == 1, "decision table must define exactly one output clause")
    require(outputs[0].get("name") == "dietarySuitability", "unexpected decision output name")

    rules: list[tuple[list[str], str]] = []
    for rule in table.findall("dmn:rule", NS):
        tests = [text_of(entry.find("dmn:text", NS)) for entry in rule.findall("dmn:inputEntry", NS)]
        require(len(tests) == len(inputs), f"rule {rule.get('id')} has wrong input-entry count")
        output_entries = rule.findall("dmn:outputEntry", NS)
        require(len(output_entries) == 1, f"rule {rule.get('id')} must have exactly one output entry")
        raw_output = text_of(output_entries[0].find("dmn:text", NS))
        require(raw_output.startswith('"') and raw_output.endswith('"'), f"rule {rule.get('id')} output must be a quoted string")
        outcome = raw_output[1:-1]
        require(outcome in EXPECTED_OUTCOMES, f"unexpected decision outcome: {outcome}")
        rules.append((tests, outcome))

    require(len(rules) == 3, f"expected three decision rules, got {len(rules)}")
    return str(decision.get("id")), inputs, rules


def unary_test_matches(test: str, value: bool) -> bool:
    if test == "-":
        return True
    if test == "true":
        return value is True
    if test == "false":
        return value is False
    raise AssertionError(f"unsupported DMN unary test in canonical decision: {test!r}")


def decide(inputs: list[str], rules: list[tuple[list[str], str]], context: dict[str, object]) -> str:
    require(set(context) == set(inputs), f"decision context fields differ from model inputs: {sorted(context)}")
    require(all(isinstance(context[name], bool) for name in inputs), "decision inputs must be booleans")

    matches: list[str] = []
    for tests, outcome in rules:
        if all(unary_test_matches(test, bool(context[name])) for test, name in zip(tests, inputs)):
            matches.append(outcome)

    require(len(matches) == 1, f"UNIQUE decision table expected exactly one matching rule, got {matches}")
    return matches[0]


def main() -> None:
    decision_id, inputs, rules = parse_model()
    cases_document = json.loads(CASES.read_text(encoding="utf-8"))
    require(cases_document.get("decision") == decision_id, "decision test cases target a different DMN decision")

    cases = cases_document.get("cases")
    require(isinstance(cases, list) and len(cases) == 3, "expected exactly three canonical decision cases")

    results: list[dict[str, object]] = []
    seen_outcomes: set[str] = set()
    for case in cases:
        require(isinstance(case, dict), "decision case must be an object")
        identifier = case.get("id")
        context = case.get("inputs")
        expected = case.get("expected")
        require(isinstance(identifier, str) and identifier.startswith("urn:pizza-ontology:decision:data:"), "decision case must have a semantic Pizza case identifier")
        require(isinstance(context, dict), f"{identifier}: inputs must be an object")
        require(isinstance(expected, str) and expected in EXPECTED_OUTCOMES, f"{identifier}: invalid expected outcome")

        actual = decide(inputs, rules, context)
        require(actual == expected, f"{identifier}: expected {expected}, got {actual}")
        seen_outcomes.add(actual)
        results.append({"id": identifier, "inputs": context, "outcome": actual})

    require(seen_outcomes == EXPECTED_OUTCOMES, "canonical cases must exercise all three decision outcomes")

    RESULTS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "decision": decision_id,
                "model": MODEL.name,
                "hitPolicy": "UNIQUE",
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("SUCCESS: DMN 1.5 Pizza dietary-suitability decision selected exactly one expected outcome for every canonical case.")
    for result in results:
        print(f"- {result['id']} -> {result['outcome']}")
    print(f"Results: {OUTPUT}")


if __name__ == "__main__":
    main()
