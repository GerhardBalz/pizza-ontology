# Pizza semantic artifacts

This directory contains **repository-owned semantic artifacts** derived from or defined against the preserved Pizza Ontology 2.0 semantic model.

They are intentionally separate from the historical editor ontology:

```text
src/ontology/pizza-edit.owl
    preserved Pizza Ontology 2.0 source
            │
            ├── selected / derived semantic knowledge
            │       ▼
            │   artifacts/reasoning/
            │
            ├── vocabulary / semantic reference
            │       ▼
            │   artifacts/validation/
            │
            ├── explicit rule semantics + input data
            │       ▼
            │   artifacts/rules/
            │
            ├── explicit decision semantics + input cases
            │       ▼
            │   artifacts/decisions/
            │
            └── mathematical formula + domain grounding + cases
                    ▼
                artifacts/calculations/
```

## Consumer contract

[`manifest.ttl`](manifest.ttl) is the machine-readable catalog for semantic artifacts intended for downstream consumption.

The catalog deliberately uses **stable repository-relative paths** rather than mutable `main` URLs:

```text
artifact catalog
    + repository commit / preservation release
                ↓
      immutable artifact binding
```

A consumer therefore pins this repository to a Git commit or preservation release and resolves the catalog identifiers within that revision. This separates the stable artifact role/path contract from the consumer's chosen immutable version binding.

The currently published semantic artifact set is:

| Role | Repository path | License |
| --- | --- | --- |
| coherent OWL reasoning module | `artifacts/reasoning/spicy-pizza.ofn` | CC BY 3.0 |
| Pizza instance SHACL profile | `artifacts/validation/pizza-instance-shapes.ttl` | MIT |
| conforming validation data | `artifacts/validation/data/conforming.ttl` | MIT |
| non-conforming validation data | `artifacts/validation/data/non-conforming.ttl` | MIT |
| vegetarian-warning SPARQL rule | `artifacts/rules/vegetarian-warning.rq` | MIT |
| rule result vocabulary | `artifacts/rules/rule-vocabulary.ttl` | MIT |
| rule evaluation data | `artifacts/rules/data/menu-pizzas.ttl` | MIT |
| dietary-suitability DMN decision | `artifacts/decisions/pizza-dietary-suitability.dmn` | MIT |
| decision outcome vocabulary | `artifacts/decisions/decision-vocabulary.ttl` | MIT |
| canonical decision input cases | `artifacts/decisions/data/cases.json` | MIT |
| Pizza circular-area OpenMath formula | `artifacts/calculations/pizza-area.openmath.xml` | MIT |
| calculation vocabulary | `artifacts/calculations/calculation-vocabulary.ttl` | MIT |
| canonical calculation cases | `artifacts/calculations/data/cases.json` | MIT |

The reasoning module reproduces selected historical Pizza semantic content and therefore retains the upstream CC BY 3.0 boundary. The SHACL, rule, decision, calculation, vocabulary, and example-data artifacts are newly authored semantic-engineering material and fall under the repository's MIT engineering-material license unless a more specific notice is added later.

`verify_consumer_contract.py` parses the catalog, verifies the required metadata, and fails if a published relative path no longer resolves to a repository-owned file.

## Reasoning

[`reasoning/`](reasoning/) contains the canonical coherent OWL module used to demonstrate and verify representative Pizza entailments without changing the full historical teaching ontology.

The selected Pizza semantic content retains the upstream CC BY 3.0 licensing and attribution boundary.

## Validation

[`validation/`](validation/) contains repository-defined SHACL shapes and RDF instance-data examples for explicit data conformance checks.

These are engineering artifacts, not a replacement for OWL semantics and not an automatic translation of the ontology.

## Rule evaluation

[`rules/`](rules/) contains a SPARQL 1.1 `CONSTRUCT` rule, its result vocabulary, and explicit Pizza RDF input data.

The first rule derives:

```text
requiresVegetarianWarning true
```

for a Pizza whose explicit input graph references a topping typed as `pizza:MeatTopping`. It deliberately performs neither OWL reasoning nor SHACL validation.

## Decision evaluation

[`decisions/`](decisions/) contains a DMN 1.5 `UNIQUE` decision table, its semantic outcome vocabulary, and explicit decision-input cases.

The decision selects one of three semantic outcomes:

```text
NotVegetarian
PescatarianOnly
Vegetarian
```

from the explicit boolean inputs `containsMeat` and `containsFish`. It is intentionally distinct from rule evaluation: the decision chooses one outcome from an explicit decision context rather than constructing RDF from a matched graph pattern.

## Calculation

[`calculations/`](calculations/) contains an OpenMath formula, a small Pizza calculation vocabulary, and canonical numeric cases.

The first calculation evaluates:

```text
areaSquareCentimetres = π × (diameterCm / 2)²
```

The OpenMath artifact carries the mathematical structure; the RDF vocabulary grounds the input and output in centimetres and square centimetres. The regression evaluator executes only the small OpenMath subset used by this formula and verifies all published cases.

## Downstream use

These artifacts establish the source-ownership boundary needed by ESKA and other consumers:

```text
pizza-ontology
    owns Pizza semantic artifacts
        ↓ commit/release-pinned contract
ESKA / applications / agents
    consume and operationalize them
```

Downstream consumers should retain the applicable provenance and licensing information. They should not copy the semantic artifacts into a second source-of-truth repository merely for convenience.
