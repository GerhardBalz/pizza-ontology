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
            └── vocabulary / semantic reference
                    ▼
                artifacts/validation/
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

The reasoning module reproduces selected historical Pizza semantic content and therefore retains the upstream CC BY 3.0 boundary. The SHACL profile and RDF validation examples are newly authored semantic-engineering artifacts and fall under the repository's MIT engineering-material license unless a more specific notice is added later.

`verify_consumer_contract.py` parses the catalog, verifies the required metadata, and fails if a published relative path no longer resolves to a repository-owned file.

## Reasoning

[`reasoning/`](reasoning/) contains the canonical coherent OWL module used to demonstrate and verify representative Pizza entailments without changing the full historical teaching ontology.

The selected Pizza semantic content retains the upstream CC BY 3.0 licensing and attribution boundary.

## Validation

[`validation/`](validation/) contains repository-defined SHACL shapes and RDF instance-data examples for explicit data conformance checks.

These are engineering artifacts, not a replacement for OWL semantics and not an automatic translation of the ontology.

## Downstream use

These artifacts establish the source-ownership boundary needed by Track 8:

```text
pizza-ontology
    owns Pizza semantic artifacts
        ↓ commit/release-pinned contract
ESKA / applications / agents
    consume and operationalize them
```

Downstream consumers should retain the applicable provenance and licensing information. They should not copy the semantic artifacts into a second source-of-truth repository merely for convenience.
