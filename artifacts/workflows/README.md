# Pizza BPMN workflow artifact

This directory contains the source-owned semantic workflow used by ESKA's `Workflow → execute` mode.

The workflow uses **BPMN 2.0.2** for control flow and keeps the semantics of its individual steps in already published Pizza artifacts.

```text
Start
  ↓
Validate Pizza RDF
  ↓
validationConforms?
  ├── false → Rejected
  └── true
        ↓
Transform Pizza → Menu
        ↓
      Published
```

## Separation of concerns

The BPMN model does not contain SHACL constraints or SPARQL mapping logic.

```text
BPMN process
    ordering / gateway / end outcome
        │
        ├── ValidatePizzaData
        │       ↓ workflow-vocabulary.ttl
        │   PizzaInstanceShapes
        │
        └── TransformPizzaToMenu
                ↓ workflow-vocabulary.ttl
            PizzaMenuMapping + PizzaMenuVocabulary
```

`workflow-vocabulary.ttl` defines the semantic workflow operations, their required artifact roles, and the `Published` / `Rejected` outcomes. The BPMN service tasks bind to those operation IRIs through `wf:semanticOperation` extension elements.

## Canonical cases

`data/cases.json` defines two cases:

- **valid-publication** — the Pizza graph conforms to the SHACL profile, so validation is followed by Mapping and the workflow ends `Published`;
- **invalid-rejection** — the Pizza graph is missing a required base, so the workflow ends `Rejected` after validation and Mapping must not execute.

The valid case is also checked against `data/expected-valid-menu.ttl`.

## Run

```bash
python -m pip install -r artifacts/workflows/requirements.txt
python artifacts/workflows/evaluate_workflow.py
```

The regression verifies:

- BPMN 2.0 process structure, service-task bindings, exclusive gateway, conditional/default paths, and end outcomes;
- workflow vocabulary bindings to the existing SHACL and Mapping artifact roles;
- the valid and invalid SHACL outcomes;
- conditional execution/suppression of the Mapping step;
- isomorphic equality of the valid transformed graph with the expected Menu graph.

This is a deliberately small executable BPMN subset for architectural testing, not a general-purpose BPMN engine.
