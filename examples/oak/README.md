# OAK access: Pizza exploration and query reference

This example demonstrates **Track 3 — Access** using the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) against the repository-owned Pizza Ontology 2.0 source.

The access reference now has two layers:

```text
minimal vertical slice
    pizza:AmericanHot
        ↓
    label / relationships / ancestors

broader exploration/query slice
    selected Pizza entities
        ↓
    identity + labels
    direct vs transitive hierarchy
    projected hasTopping relationships
    descendant traversal
    backend-dependent lexical search capability
```

This is ontology **access**, not OWL reasoning. OAK projects common OWL structures into graph-oriented relationships and provides traversal over that graph. Formal classification remains a separate concern in Track 4.

## Architecture boundary

```text
Pizza Ontology 2.0
    authoritative semantic source
        ↓ accessed through
OAK adapter
        ↓
lookup / relationship projection / graph traversal / optional search
        ↓
engineering / projection / application consumers
```

OAK does not replace the semantic model. Query results are views over the preserved source, not new Pizza assertions or a second ontology.

The repository deliberately keeps three responsibilities separate:

```text
OAK access
    lookup / traversal / relationship projection

OWL reasoning
    logical inference / classification

Implementation Projection
    explicit application-facing representation or contract
```

## Versions

The example pins:

```text
oaklib 0.7.1
pronto 2.7.3
```

The explicit Pronto pin prevents the Python dependency resolver from selecting an older Pronto release incompatible with the Python runtime used by CI.

## Why the temporary `.ofn` file?

`src/ontology/pizza-edit.owl` preserves the historical ODK editor filename, but its content is OWL Functional Syntax. OAK's local-file selector uses the resource descriptor/extension to select an adapter.

`run.sh` therefore creates a **byte-identical temporary copy** named `pizza-edit.ofn` solely as a syntax hint:

```text
src/ontology/pizza-edit.owl
        │ exact bytes
        ▼
examples/oak/.work/pizza-edit.ofn
        │ runtime only
        ▼
OAK Functional-Syntax adapter
```

The temporary file is not a semantic distribution and is never committed.

## Pizza prefix

The historical Pizza entity namespace is registered explicitly for OAK CURIE access:

```text
pizza = http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

This changes only client-side identifier compacting. It does not change Pizza IRIs.

## Example 1 — minimal vertical slice

[`access_pizza.py`](access_pizza.py) keeps the original `pizza:AmericanHot` example deliberately small.

It verifies:

- CURIE → historical IRI expansion;
- access to one of the preserved multilingual `rdfs:label` values;
- asserted `rdfs:subClassOf` graph projection;
- a projected `hasTopping some ...` relationship;
- transitive is-a ancestry;
- label-language and ontology-metadata capability boundaries of the selected adapter.

### Multilingual labels

Pizza 2.0 contains both English and Portuguese labels for `pizza:AmericanHot`:

```text
AmericanHot       @en
AmericanaPicante  @pt
```

The current local Functional-Syntax adapter exposes the common OAK `label(..., lang=...)` signature but does not provide a deterministic language-selection contract for this example. The regression therefore verifies label access without depending on which preserved multilingual label is returned first.

Semantic identity remains the CURIE / full IRI, not the selected display label.

## Example 2 — broader exploration/query slice

[`query_pizza.py`](query_pizza.py) asks five distinct access questions without turning them into application rules.

### 1. Entity identity and labels

The example resolves a small selected set including:

```text
pizza:NamedPizza
pizza:PizzaTopping
pizza:hasTopping
pizza:AmericanHot
pizza:Margherita
```

For each entity it records:

- CURIE;
- full historical IRI;
- adapter-provided label where available.

The regression requires projected Pizza entities to remain in the preserved historical entity namespace.

### 2. Direct versus transitive hierarchy

For selected pizzas the example compares:

```text
relationships(...)
    asserted named rdfs:subClassOf parents

ancestors(..., predicates=[rdfs:subClassOf])
    transitive is-a graph closure
```

It verifies that every asserted direct superclass occurs in the corresponding ancestor closure.

This is graph traversal over the selected adapter. It is **not** a HermiT classification result.

### 3. Projected `hasTopping` relationships

The example reads selected relationship targets through:

```text
relationships([entity])
```

and groups targets for:

```text
pizza:hasTopping
```

These relationship edges are OAK's graph-oriented view of selected OWL restrictions. For example, the regression keeps the established `AmericanHot → JalapenoPepperTopping` access case tied to the source ontology.

The access view must not be interpreted as a closed Pizza recipe.

### 4. Descendant traversal

The example exercises downward graph traversal as a different query from ancestry:

```text
descendants(pizza:NamedPizza, predicates=[rdfs:subClassOf])
descendants(pizza:PizzaTopping, predicates=[rdfs:subClassOf])
```

It verifies representative source-backed relationships such as selected named pizzas descending from `NamedPizza` and the jalapeño topping descending from `PizzaTopping`.

It also derives asserted direct children of `NamedPizza` by checking the direct `rdfs:subClassOf` parents of the bounded descendant set. This keeps **direct** and **transitive** hierarchy semantics explicit.

### 5. Lexical search capability

OAK defines lexical search through its Search Interface, but support depends on the selected backend.

The broader example therefore treats:

```text
basic_search("Margherita")
```

as a **capability probe**:

- if the adapter implements it, the example reports a bounded result set;
- if it raises `NotImplementedError` or does not expose the method, the example records search as unsupported for that backend;
- either outcome leaves the Pizza semantic source unchanged.

Search ranking/matching is not promoted into a Pizza semantic contract.

## Run

From the repository root:

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

The runner exercises both Python examples and four CLI access operations.

Generated runtime output is written under:

```text
examples/oak/results/
```

and the byte-identical syntax-hint copy under:

```text
examples/oak/.work/
```

Both are runtime-only.

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

Is-a descendants:

```bash
runoak \
  --prefix 'pizza=http://www.co-ode.org/ontologies/pizza/pizza.owl#' \
  -i examples/oak/.work/pizza-edit.ofn \
  descendants -p i pizza:NamedPizza
```

The global prefix/input options intentionally appear before the command.

## Adapter capability boundaries

OAK exposes common interfaces over multiple backends, but a given adapter does not necessarily implement every operation or optional behavior.

The examples make those boundaries visible rather than turning unsupported behavior into a false Pizza-data failure.

```text
common OAK concern
        │
        ├── CURIE / IRI identity               verified
        ├── labels                             verified
        ├── relationships                      verified
        ├── ancestor graph traversal           verified
        ├── descendant graph traversal         verified by broader slice
        ├── deterministic label-language choice backend-dependent
        ├── lexical basic_search               capability-probed
        └── ontology metadata                  capability-probed
```

A different backend should be introduced only when a concrete requirement needs capabilities the local Functional-Syntax adapter does not provide.

## Relationship to downstream architecture

The broader access reference complements rather than replaces the projection/application path:

```text
Pizza OWL
    ↓ OAK access
source-verified semantic slice
    ├── JSON ImplementationProjection
    └── OpenAPI ImplementationProjection
            ↓
        Application / UX
```

Projection policy decides what semantics cross into an implementation contract. OAK merely provides one controlled access mechanism to the source.

## Verification contract

`run.sh` fails if the selected source-backed access expectations drift, including:

- the established `AmericanHot` relationship slice;
- direct/transitive hierarchy consistency;
- representative `NamedPizza` descendant membership;
- representative `PizzaTopping` descendant membership;
- CLI ancestor and descendant traversal.

This keeps the examples educational and executable without treating the example code as the semantic authority.
