# Pizza SHACL validation profile

This directory is the repository-owned **Track 4 — Validate** artifact for explicit Pizza instance data.

It is intentionally separate from OWL reasoning.

## Validation question

For an RDF node explicitly typed as `pizza:Pizza`, does the data satisfy this repository-defined profile?

```text
Pizza instance
    ├── exactly one explicit hasBase value
    │       └── typed PizzaBase
    │
    └── at least one explicit hasTopping value
            └── typed PizzaTopping
```

The profile is defined in [`pizza-instance-shapes.ttl`](pizza-instance-shapes.ttl).

## OWL coherence is not SHACL conformance

These are different questions:

```text
OWL / HermiT
    What follows logically from the ontology?

SHACL / pySHACL
    Does this explicit RDF data satisfy a validation profile?
```

OWL uses open-world semantic reasoning. This SHACL profile checks explicit graph data against operational constraints. The SHACL shape is therefore **not presented as a translation of Pizza Ontology 2.0** and does not change the ontology.

That distinction matters for this repository because the historical Pizza ontology intentionally contains unsatisfiable tutorial classes, while an instance-data graph can independently conform or fail to conform to a SHACL profile.

## Examples

[`data/conforming.ttl`](data/conforming.ttl) contains a Pizza instance with one base and one topping and is expected to conform.

[`data/non-conforming.ttl`](data/non-conforming.ttl) intentionally:

- omits `pizza:hasBase`;
- points `pizza:hasTopping` to a resource that is not typed `pizza:PizzaTopping`.

The regression therefore expects violations on both paths:

```text
pizza:hasBase
pizza:hasTopping
```

## Run

From the repository root:

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/validation/validate_examples.py
```

The validation dependency is pinned to pySHACL 0.40.1.

Generated validation reports are written to `artifacts/validation/results/` and are not committed.

## Ownership and licensing

The SHACL profile and example instance data are repository-authored engineering artifacts and follow the repository's MIT licensing boundary unless stated otherwise.

The Pizza class and property IRIs referenced by the profile remain identifiers from the historical Pizza Ontology 2.0 semantic model.

## Architectural boundary

```text
Pizza Ontology 2.0
        │ supplies vocabulary / semantics
        ▼
Pizza SHACL validation profile
        │ repository-defined data contract
        ▼
explicit RDF instance data
        │
        ▼
conforms / does not conform
```

This validation artifact is owned by `pizza-ontology` so downstream consumers can reuse the same domain validation contract without ESKA or application repositories redefining Pizza-specific constraints.
