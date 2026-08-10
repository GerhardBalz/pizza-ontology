#!/usr/bin/env python3
"""Evaluate and verify the canonical Pizza OpenMath calculation artifact."""

from __future__ import annotations

import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
FORMULA = HERE / "pizza-area.openmath.xml"
VOCABULARY = HERE / "calculation-vocabulary.ttl"
CASES = HERE / "data" / "cases.json"
RESULTS = HERE / "results"

OM_NS = "http://www.openmath.org/OpenMath"
OM = f"{{{OM_NS}}}"
EXPECTED_SYMBOLS = {
    ("arith1", "times"),
    ("arith1", "divide"),
    ("arith1", "power"),
    ("nums1", "pi"),
}
EXPECTED_VARIABLES = {"diameterCm"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def local_name(element: ET.Element) -> str:
    return element.tag.removeprefix(OM)


def evaluate(element: ET.Element, variables: dict[str, float]) -> float:
    tag = local_name(element)

    if tag == "OMI":
        return float(int((element.text or "").strip()))

    if tag == "OMV":
        name = element.attrib["name"]
        require(name in variables, f"unbound OpenMath variable: {name}")
        return float(variables[name])

    if tag == "OMS":
        cd = element.attrib.get("cd")
        name = element.attrib.get("name")
        if (cd, name) == ("nums1", "pi"):
            return math.pi
        raise AssertionError(f"unsupported standalone OpenMath symbol: {cd}:{name}")

    if tag == "OMA":
        children = list(element)
        require(len(children) >= 2, "OpenMath application must contain an operator and arguments")
        operator = children[0]
        require(local_name(operator) == "OMS", "OpenMath application operator must be OMS")
        cd = operator.attrib.get("cd")
        name = operator.attrib.get("name")
        args = [evaluate(child, variables) for child in children[1:]]

        if (cd, name) == ("arith1", "times"):
            return math.prod(args)
        if (cd, name) == ("arith1", "divide"):
            require(len(args) == 2, "arith1:divide requires exactly two arguments")
            return args[0] / args[1]
        if (cd, name) == ("arith1", "power"):
            require(len(args) == 2, "arith1:power requires exactly two arguments")
            return args[0] ** args[1]
        raise AssertionError(f"unsupported OpenMath operator: {cd}:{name}")

    raise AssertionError(f"unsupported OpenMath element: {tag}")


def parse_formula() -> ET.Element:
    root = ET.parse(FORMULA).getroot()
    require(local_name(root) == "OMOBJ", "formula root must be OMOBJ")
    require(root.attrib.get("version") == "2.0", "formula must declare OpenMath version 2.0")
    require(root.attrib.get("cdbase") == "http://www.openmath.org/cd", "formula must use the canonical OpenMath content-dictionary base")

    expressions = list(root)
    require(len(expressions) == 1, "formula OMOBJ must contain exactly one expression")

    symbols = {
        (element.attrib.get("cd"), element.attrib.get("name"))
        for element in root.iter(f"{OM}OMS")
    }
    variables = {
        element.attrib.get("name")
        for element in root.iter(f"{OM}OMV")
    }
    require(symbols == EXPECTED_SYMBOLS, f"unexpected OpenMath symbol set: {sorted(symbols)}")
    require(variables == EXPECTED_VARIABLES, f"unexpected OpenMath variable set: {sorted(variables)}")
    return expressions[0]


def verify_vocabulary() -> None:
    text = VOCABULARY.read_text(encoding="utf-8")
    require("calc:PizzaAreaCalculation" in text, "calculation vocabulary must define PizzaAreaCalculation")
    require("calc:diameterCentimetres" in text, "calculation vocabulary must define diameterCentimetres")
    require("calc:areaSquareCentimetres" in text, "calculation vocabulary must define areaSquareCentimetres")
    require("xsd:decimal" in text, "calculation vocabulary must identify decimal numeric values")


def main() -> None:
    expression = parse_formula()
    verify_vocabulary()
    suite = json.loads(CASES.read_text(encoding="utf-8"))

    require(suite.get("calculation") == "urn:pizza-ontology:calculation:PizzaAreaCalculation", "unexpected calculation identifier")
    require(suite.get("inputRelation") == "urn:pizza-ontology:calculation:diameterCentimetres", "unexpected input relation")
    require(suite.get("outputRelation") == "urn:pizza-ontology:calculation:areaSquareCentimetres", "unexpected output relation")

    cases = suite.get("cases")
    require(isinstance(cases, list) and len(cases) == 3, "expected exactly three canonical calculation cases")

    outputs = []
    for case in cases:
        diameter = float(case["diameterCm"])
        expected = float(case["expectedAreaSquareCentimetres"])
        require(math.isfinite(diameter) and diameter > 0, f"diameter must be positive and finite: {diameter}")

        actual = evaluate(expression, {"diameterCm": diameter})
        rounded = round(actual, 6)
        require(
            math.isclose(rounded, expected, rel_tol=0.0, abs_tol=1e-6),
            f"{case['id']}: expected area {expected}, got {rounded}",
        )
        outputs.append(
            {
                "id": case["id"],
                "diameterCm": diameter,
                "areaSquareCentimetres": rounded,
            }
        )

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "results.json").write_text(
        json.dumps({"results": outputs}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("SUCCESS: OpenMath Pizza area formula produced all expected canonical results.")
    for output in outputs:
        print(f"- {output['id']}: {output['diameterCm']:g} cm -> {output['areaSquareCentimetres']:.6f} cm^2")


if __name__ == "__main__":
    main()
