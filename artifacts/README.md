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
        ↓
ESKA / applications / agents
    consume and operationalize them
```

Downstream consumers should pin to a repository commit or preservation release and retain the applicable provenance and licensing information.
