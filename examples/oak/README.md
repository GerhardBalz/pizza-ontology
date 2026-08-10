# OAK access: Pizza vertical slice

This example demonstrates **Track 3 — Access** using the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) against the repository-owned Pizza Ontology 2.0 source.

The goal is deliberately small:

```text
AmericanHot
    │ lookup / label
    ▼
American Hot
    │ relationships
    ├── rdfs:subClassOf → NamedPizza
    └── hasTopping → JalapenoPepperTopping
    │
    ▼
is-a ancestry + ontology metadata
```

This is ontology **access**, not OWL reasoning. OAK projects common OWL axioms such as named `SubClassOf` axioms and simple existential restrictions into graph relationships. Reasoning remains a separate concern in Track 4.

## Version

The example pins:

```text
oaklib 0.7.1
```

## Why the temporary `.ofn` file?

`src/ontology/pizza-edit.owl` preserves the historical ODK editor filename, but its content is OWL Functional Syntax. OAK's local-file selector uses the file descriptor/extension to select an adapter.

`run.sh` therefore makes a **byte-identical temporary copy** named `pizza-edit.ofn` solely as an explicit syntax hint for OAK:

```text
src/ontology/pizza-edit.owl
        │ exact bytes
        ▼
examples/oak/.work/pizza-edit.ofn
        │ runtime only
        ▼
OAK horned-OWL-backed adapter
```

The temporary file is not a new semantic artifact and is never committed.

## Run

From the repository root:

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

The runner exercises both the Python API and CLI.

## CLI examples

Entity lookup:

```bash
runoak -i examples/oak/.work/pizza-edit.ofn info "American Hot"
```

Projected relationships:

```bash
runoak -i examples/oak/.work/pizza-edit.ofn relationships "American Hot"
```

Is-a ancestors:

```bash
runoak -i examples/oak/.work/pizza-edit.ofn ancestors -p i "American Hot"
```

The global `-i` / `--input` option intentionally appears **before** the command, following OAK's CLI contract.

## Python API

[`access_pizza.py`](access_pizza.py) uses the common OAK interface:

- `get_adapter(...)`
- `label(...)`
- `relationships(...)`
- `ancestors(...)`
- `ontology_metadata_map()`

The example verifies that OAK can access the Pizza entity label, its asserted superclass, the `hasTopping some JalapenoPepperTopping` relationship projection, is-a ancestry, and ontology metadata without embedding those domain facts as application rules.

## Architectural boundary

```text
Pizza Ontology 2.0
        │
        │ accessed through
        ▼
OAK
        │
        ▼
lookup / traversal / relationship projection
```

OAK does not replace the semantic model, and this example does not move Pizza semantics into Python code. The ontology remains the source of the relationships being accessed.
