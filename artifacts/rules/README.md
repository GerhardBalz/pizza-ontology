# Pizza rule evaluation artifact

This directory contains the source-owned Pizza semantic artifacts for a third executable-semantic mode used by the companion ESKA project:

```text
Rule → evaluate
```

The example is deliberately small. It asks:

> **Should a Pizza receive a vegetarian warning when its explicit RDF data references a topping typed as `pizza:MeatTopping`?**

## Rule

[`vegetarian-warning.rq`](vegetarian-warning.rq) is a SPARQL 1.1 `CONSTRUCT` rule:

```sparql
CONSTRUCT {
  ?pizza rule:requiresVegetarianWarning true .
}
WHERE {
  ?pizza a pizza:Pizza ;
         pizza:hasTopping ?topping .
  ?topping a pizza:MeatTopping .
}
```

The output predicate is defined in [`rule-vocabulary.ttl`](rule-vocabulary.ttl).

The rule is intentionally evaluated against **explicit RDF assertions only**. This artifact does not run OWL reasoning and does not perform SHACL validation.

## Input data

[`data/menu-pizzas.ttl`](data/menu-pizzas.ttl) contains two control cases:

```text
meatyPizza
    hasTopping hamTopping
    hamTopping a MeatTopping
        ↓ rule evaluates
requiresVegetarianWarning true

vegetablePizza
    hasTopping tomatoTopping
    tomatoTopping a VegetableTopping
        ↓ rule evaluates
no warning result
```

The rule itself contains neither example identifier, so the expected result is produced from the represented condition rather than a hard-coded test case.

## Execute

Install the pinned dependency:

```bash
python -m pip install -r artifacts/rules/requirements.txt
```

Run:

```bash
python artifacts/rules/evaluate_rule.py
```

The evaluator executes the SPARQL `CONSTRUCT`, requires exactly one warning result, verifies the non-matching control case, and writes the generated RDF graph to `artifacts/rules/results/evaluation.ttl`.

## Execution-mode boundary

This mode is intentionally different from the other Pizza semantic artifacts:

```text
OWL module
    ↓ HermiT
reason / entail

SHACL shapes
    ↓ pySHACL
validate / conform

SPARQL rule
    ↓ rule evaluation
construct / derive
```

The same business-looking outcome could theoretically be represented by another formalism. The architectural purpose here is not to claim SPARQL as a universal rule language; it is to provide one standards-based, deterministic rule artifact whose operational semantics differ from both OWL entailment and SHACL conformance checking.

## Downstream ownership

`pizza-ontology` owns the rule semantics, rule vocabulary, and Pizza input data. ESKA may consume a commit-pinned version of these artifacts and provide the Capability, execution, verification, and provenance architecture around them.

```text
pizza-ontology
    rule + vocabulary + input data
        ↓ immutable commit + artifacts/manifest.ttl
ESKA
    Rule Evaluation Capability
        ↓
Execution → Result → Verification → Provenance
```

The historical Pizza Ontology 2.0 source is unchanged.
