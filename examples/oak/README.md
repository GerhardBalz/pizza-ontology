# OAK access: Pizza vertical slice

This example demonstrates **Track 3 — Access** using the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) against the repository-owned Pizza Ontology 2.0 source.

The goal is deliberately small:

```text
pizza:AmericanHot
    │ lookup / label access
    ▼
multilingual rdfs:label
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

## Multilingual labels and adapter behavior

Pizza 2.0 contains multilingual `rdfs:label` values. For `pizza:AmericanHot`, the preserved ontology contains both:

```text
AmericanHot       @en
AmericanaPicante  @pt
```

The current OAK `FunOwlImplementation` exposes the common `label(curie, lang=...)` signature, but its implementation does not apply the language argument when selecting among multiple `rdfs:label` values. It returns the first value supplied by the underlying OWL representation, and that order is not a stable language-selection contract.

The example therefore verifies **label access without assuming label order**. Either preserved `rdfs:label` is accepted for this backend, while the entity CURIE/IRI and semantic relationships remain deterministic.

```text
common OAK label interface
        │
        └── FunOwl local adapter
              ├── label access       ✓
              └── language filtering not enforced by label()
```

A later example can use a backend with explicit language-aware label selection if that becomes a concrete requirement. The historical multilingual annotations should not be changed merely to make this adapter deterministic.

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
  -i examples/oak/.work/pizza-edit.ofn \
  info pizza:AmericanHot
```

Projected relationships:

```bash
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -i examples/oak/.work/pizza-edit.ofn \
  relationships pizza:AmericanHot
```

Is-a ancestors:

```bash
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -i examples/oak/.work/pizza-edit.ofn \
  ancestors -p i pizza:AmericanHot
```

The global prefix and input options intentionally appear **before** the command.

## Python API

[`access_pizza.py`](access_pizza.py) uses the common OAK interface:

- `get_adapter(...)`
- `prefix_map()`
- `label(...)`
- `relationships(...)`
- `ancestors(...)`

The example verifies that OAK can access a preserved Pizza label, its asserted superclass, the `hasTopping some JalapenoPepperTopping` relationship projection, and is-a ancestry without embedding those domain facts as application rules.

## Adapter capability boundaries

OAK defines common interfaces across multiple adapters, but not every backend implements every operation or every optional behavior.

For the local Functional-Syntax adapter used by this first slice:

- entity labels are accessible, but deterministic language filtering is not implemented by `label()`;
- relationship projection and ancestry are supported for the selected OWL constructs;
- ontology enumeration / ontology-metadata access is not implemented.

The Python example records these capability boundaries explicitly instead of treating them as Pizza-data failures.

```text
common OAK interface
        │
        ├── labels                         ✓ local adapter
        ├── relationships / ancestry       ✓ local adapter
        ├── label language filtering       backend-dependent
        └── ontology metadata              backend-dependent
```

A later access/distribution example can introduce a richer backend when one of those capabilities has a concrete use case.

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
