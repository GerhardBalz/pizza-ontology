# OAK access: Pizza vertical slice

This example demonstrates **Track 3 — Access** using the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) against the repository-owned Pizza Ontology 2.0 source.

The goal is deliberately small:

```text
pizza:AmericanHot
    │ lookup / English label
    ▼
American Hot
    │ relationships
    ├── rdfs:subClassOf → pizza:NamedPizza
    └── pizza:hasTopping → pizza:JalapenoPepperTopping
    │
    ▼
is-a ancestry
```

This is ontology **access**, not OWL reasoning. OAK projects common OWL axioms such as named `SubClassOf` axioms and simple existential restrictions into graph relationships. Reasoning remains a separate concern in Track 4.

## Versions

The example pins:

```text
oaklib 0.7.1
pronto 2.7.3
```

The explicit Pronto pin prevents the Python dependency resolver from selecting an old Pronto release that is incompatible with Python 3.12.

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
OAK Functional-Syntax adapter
```

The temporary file is not a new semantic artifact and is never committed.

## Pizza prefix

OAK's common interface uses CURIE-style identifiers. The historical Pizza namespace is therefore registered explicitly:

```text
pizza = http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

This changes only how the OAK client refers to entities. It does **not** change the Pizza ontology IRIs.

## Multilingual labels

Pizza 2.0 contains multilingual labels. The examples explicitly request English (`en`) rather than relying on an arbitrary first label.

That makes the access contract clear:

```text
pizza:AmericanHot
    ├── English → American Hot
    └── other language labels remain in the ontology
```

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
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -l en \
  -i examples/oak/.work/pizza-edit.ofn \
  info pizza:AmericanHot
```

Projected relationships:

```bash
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -l en \
  -i examples/oak/.work/pizza-edit.ofn \
  relationships pizza:AmericanHot
```

Is-a ancestors:

```bash
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -l en \
  -i examples/oak/.work/pizza-edit.ofn \
  ancestors -p i pizza:AmericanHot
```

The global prefix, language, and input options intentionally appear **before** the command.

## Python API

[`access_pizza.py`](access_pizza.py) uses the common OAK interface:

- `get_adapter(...)`
- `prefix_map()`
- `label(...)`
- `relationships(...)`
- `ancestors(...)`

The example verifies that OAK can access the English Pizza entity label, its asserted superclass, the `hasTopping some JalapenoPepperTopping` relationship projection, and is-a ancestry without embedding those domain facts as application rules.

## Adapter capability boundary

OAK defines common interfaces across multiple adapters, but not every backend implements every operation.

For the local Functional-Syntax adapter used by this first slice, ontology enumeration / ontology-metadata access is not implemented. The Python example records this capability boundary explicitly instead of treating it as a Pizza-data failure.

```text
common OAK interface
        │
        ├── labels / relationships / ancestry  ✓ local adapter
        │
        └── ontology metadata                 backend-dependent
```

A later access/distribution example can introduce a metadata-capable backend when that capability has a concrete use case.

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
