# Pizza semantic artifacts

This directory contains **repository-owned semantic artifacts** derived from or defined against the preserved Pizza Ontology 2.0 semantic model.

They are intentionally separate from the historical editor ontology:

```text
src/ontology/pizza-edit.owl
    preserved Pizza Ontology 2.0 source
            │
            ├── reasoning/
            ├── validation/
            ├── rules/
            ├── decisions/
            ├── calculations/
            ├── mappings/
            └── workflows/
```

## Consumer contract

[`manifest.ttl`](manifest.ttl) is the machine-readable catalog for semantic artifacts intended for downstream consumption. Consumers bind the stable repository-relative artifact paths to an immutable Git commit or preservation release.

The manifest currently publishes **23 distributions**:

| Concern | Published artifacts |
| --- | --- |
| reasoning | coherent OWL module |
| validation | SHACL profile + conforming/non-conforming RDF |
| rule evaluation | SPARQL rule + result vocabulary + RDF input |
| decision evaluation | DMN decision + outcome vocabulary + decision cases |
| calculation | OpenMath formula + calculation vocabulary + numeric cases |
| semantic mapping | SPARQL mapping + Menu target vocabulary + source RDF + expected target RDF |
| workflow execution | BPMN process + workflow vocabulary + valid/invalid inputs + expected target + case contract |

The reasoning module reproduces selected historical Pizza semantic content and retains the upstream CC BY 3.0 boundary. Repository-authored SHACL, rule, decision, calculation, mapping, workflow, vocabulary, and example-data artifacts are MIT-licensed engineering material unless stated otherwise.

`verify_consumer_contract.py` verifies the catalog, metadata, dependencies, licensing, and repository-relative paths.

## Execution semantics

```text
Ontology    → reason
Constraint  → validate
Rule        → evaluate
Decision    → decide
Calculation → calculate
Mapping     → transform
Workflow    → execute
```

### Reasoning

[`reasoning/`](reasoning/) contains the canonical coherent OWL module used to demonstrate representative Pizza entailments.

### Validation

[`validation/`](validation/) contains repository-defined SHACL shapes and explicit RDF data examples.

### Rule evaluation

[`rules/`](rules/) contains the vegetarian-warning SPARQL `CONSTRUCT` rule, result vocabulary, and explicit source graph.

### Decision evaluation

[`decisions/`](decisions/) contains the dietary-suitability DMN 1.5 decision, semantic outcomes, and decision contexts.

### Calculation

[`calculations/`](calculations/) contains the Pizza-area OpenMath formula, unit-grounding vocabulary, and numeric cases.

### Semantic mapping

[`mappings/`](mappings/) contains a SPARQL 1.1 `CONSTRUCT` transformation from Pizza RDF into a distinct Menu projection semantic model.

The mapping differs from the Rule mode:

```text
Rule
    source semantic model
        ↓ derive
    source-domain statement

Mapping
    source semantic model
        ↓ transform through mapping semantics
    target semantic model
```

### Workflow execution

[`workflows/`](workflows/) contains a BPMN 2.0.2 process that composes the existing validation and mapping semantics:

```text
Start
  ↓
Validate Pizza RDF
  ↓
conforms?
  ├── false → Rejected
  └── true
        ↓
Transform Pizza → Menu
        ↓
      Published
```

The BPMN model owns orchestration only. `workflow-vocabulary.ttl` binds semantic workflow operations to existing artifact roles, so the workflow does not duplicate SHACL constraints or SPARQL mapping logic. The valid and invalid cases verify ordered execution, intermediate state, conditional branching, and suppression of the mapping step on rejection.

## Downstream use

```text
pizza-ontology
    owns Pizza semantic artifacts
        ↓ commit/release-pinned contract
ESKA / applications / agents
    consume and operationalize them
```

Downstream consumers should retain applicable provenance and licensing information rather than copy these artifacts into a second semantic source of truth.
