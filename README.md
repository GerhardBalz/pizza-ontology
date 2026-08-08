# Pizza Ontology

[![Build Status](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml/badge.svg)](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml)

A modern **ontology engineering and executable knowledge reference project** based on the classic Pizza OWL ontology.

The Pizza domain is deliberately small and understandable. That makes it a useful common example for exploring the lifecycle of semantic knowledge — from ontology modeling and engineering to programmatic access, publication, semantic projections, APIs, user experience, and executable knowledge.

## Why Pizza?

The Pizza ontology is a well-known OWL teaching example from the Manchester / Protégé ontology tutorial tradition.

Its domain is simple enough to understand immediately, while the ontology demonstrates non-trivial OWL concepts such as:

- classes and class hierarchies,
- object properties and property characteristics,
- existential and universal restrictions,
- disjointness and defined classes,
- value partitions and individuals,
- multilingual labels and annotations,
- reasoning,
- and intentionally unsatisfiable classes used as teaching examples.

This repository uses Pizza as a stable semantic subject around which different ontology and knowledge-engineering technologies can be explored.

## Project Direction

The **ontology is the semantic center** of the project. Tools, representations, APIs, and applications are engineering or operational layers around that semantic model.

```text
                         Pizza Ontology
                              │
                      semantic model
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
    Protégé                  ODK                    OAK
 model / author       engineer / manage       access / query
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
                              ▼
                    Semantic Knowledge
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
     Reasoning          Semantic Projections     Knowledge Graph
    Validation             / Schemas
        │                     │
        │              ┌──────┴──────┐
        │              ▼             ▼
        │             APIs           UX
        │
        └─────────────────────┬─────────────────────
                              ▼
                    Executable Knowledge
                              │
                    rules / decisions /
                    agents / actions
                              │
                              ▼
               Executable Knowledge Architecture
```

The project is intended to evolve across complementary tracks.

### 1. Model — Protégé and OWL

Use the Pizza ontology to explore ontology modeling with [Protégé](https://protege.stanford.edu/) and OWL:

- ontology structure,
- classes and properties,
- restrictions and definitions,
- annotations,
- reasoning,
- ontology metadata,
- identity and versioning.

### 2. Engineer — Ontology Development Kit

Use the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit) to demonstrate how an existing standalone ontology can be migrated into and managed as a modern ontology-engineering project:

- Git-based source management,
- reproducible builds,
- ROBOT tooling,
- automated validation,
- semantic regression tests,
- CI workflows,
- release engineering,
- provenance and governance.

The historical Pizza 2.0 ontology has been migrated into the ODK editor ontology while preserving its original semantic content and identifiers.

### 3. Access — Ontology Access Kit

Use the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) to explore programmatic ontology access, including:

- entity lookup,
- labels and definitions,
- ancestors and descendants,
- relationships and graph traversal,
- queries and mappings,
- ontology metadata,
- use from scripts and applications.

### 4. Reason and Validate

Explore the distinction between asserted knowledge, inferred knowledge, and validation using tools such as ROBOT, HermiT, SPARQL, and OWL profile validation.

The historical Pizza ontology deliberately contains two unsatisfiable classes:

- `CheeseyVegetableTopping`
- `IceCream`

Rather than removing them, this repository preserves them as part of the teaching ontology and explicitly verifies them as expected semantic behavior.

### 5. Publish and Govern

Use Pizza as a concrete case study for ontology identity, publication, provenance, and governance.

Important distinctions include:

```text
Ontology ≠ OWL file
Ontology ≠ Git repository
Version ≠ Release
Release ≠ Distribution
Identifier ≠ Location
Host ≠ Authority
Repository Owner ≠ Ontology Authority
```

The architecture behind these distinctions is documented in:

- [Ontology Identity and Publication Model](docs/identity-publication-model.md)
- [Pizza Ontology Provenance](docs/pizza-provenance.md)

### 6. Project — Semantic Projections

Explore how selected structures can be derived from or informed by the semantic model, for example:

- JSON representations,
- JSON Schema,
- API schemas,
- OpenAPI,
- graph models,
- search indexes,
- validation schemas.

The goal is not to assume that every implementation artifact should be generated automatically from OWL. Derived artifacts should remain **traceable to the semantic model** while adding concerns appropriate to their own architectural layer.

### 7. Experience — Ontology-Informed UX

Explore how semantic knowledge can inform user interaction, including:

- semantic navigation,
- search and filtering,
- ontology-driven forms,
- guided configuration,
- explanations,
- validation messages,
- vocabulary-aware interfaces.

User experience contains additional knowledge that does not naturally belong in the ontology itself, but can remain connected to it.

### 8. Execute — Executable Knowledge

Explore the progression from representing knowledge to using knowledge operationally:

```text
Ontology
   ↓
Reasoning
   ↓
Queries
   ↓
Validation
   ↓
Semantic projections
   ↓
APIs / UX
   ↓
Rules / decisions
   ↓
Agents / actions
```

This provides a small reference domain for exploring **Executable Knowledge** and **Executable Knowledge Architecture**.

### 9. Architect — Semantic Modeling

Use the complete project as a case study for broader Semantic Modeling concepts:

- semantic identity,
- provenance,
- authority and stewardship,
- versioning and lifecycle,
- semantic projections,
- model-driven and knowledge-driven systems,
- relationships between conceptual, semantic, logical, and executable models.

## Current Status

The current baseline is a preservation-oriented migration of **Pizza 2.0** into an ODK-managed repository.

The migration preserves:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

The editor ontology is:

[`src/ontology/pizza-edit.owl`](src/ontology/pizza-edit.owl)

The current project intentionally does **not** claim authority over the historical `co-ode.org` identifier space.

Whether future work remains a preservation/stewardship environment or establishes a new successor ontology is an explicit architectural decision that remains open. See [Pizza Ontology Provenance](docs/pizza-provenance.md).

## Provenance

The migration baseline is based on the Pizza 2.0 ontology distributed by the Stanford Protégé site:

https://protege.stanford.edu/ontologies/pizza/pizza.owl

The ontology belongs to the historical Manchester / Protégé OWL tutorial tradition and explicitly credits:

- Alan Rector
- Chris Wroe
- Matthew Horridge
- Nick Drummond
- Robert Stevens

The upstream ontology declares **Creative Commons Attribution 3.0 (CC BY 3.0)**.

This repository currently acts as a preservation, migration, engineering, and learning environment derived from that historical artifact. It does not claim to be the original authority or source repository of the Pizza ontology.

For the detailed lineage and authority analysis, see [docs/pizza-provenance.md](docs/pizza-provenance.md).

## Repository Structure

```text
pizza-ontology/
├── .github/
│   └── workflows/
├── docs/
│   ├── identity-publication-model.md
│   └── pizza-provenance.md
├── src/
│   ├── ontology/
│   │   ├── pizza-edit.owl
│   │   ├── pizza-odk.yaml
│   │   ├── pizza.Makefile
│   │   └── ...
│   ├── scripts/
│   └── sparql/
├── CONTRIBUTING.md
└── README.md
```

Additional examples will be introduced as the OAK, API, UX, knowledge-graph, and executable-knowledge tracks are developed.

## Working with the Ontology

The project uses ODK containers. With [ODK Runner](https://github.com/INCATools/odkrunner) installed:

```bash
cd src/ontology
odkrun make test
```

The test suite includes a Pizza-specific semantic regression test that verifies the two intentionally unsatisfiable tutorial classes.

## Architecture Documents

### Ontology Identity and Publication Model

[`docs/identity-publication-model.md`](docs/identity-publication-model.md)

Defines the generic concepts used by this project, including ontology and entity identity, versioning, releases, distributions, source repositories, provenance, authority, stewardship, hosting, and rights.

### Pizza Ontology Provenance

[`docs/pizza-provenance.md`](docs/pizza-provenance.md)

Applies the generic model to the historical Pizza ontology and documents its lineage, upstream source, contributors, hosting, authority uncertainty, migration provenance, and preservation-versus-successor options.

## Roadmap

The repository will evolve incrementally rather than attempting to demonstrate every concept at once.

- [x] Establish Pizza 2.0 preservation baseline
- [x] Migrate the ontology into ODK
- [x] Establish semantic regression tests
- [x] Document ontology identity and publication concepts
- [x] Document Pizza provenance
- [ ] Refine publication and release strategy
- [ ] Add OAK access examples
- [ ] Add ontology exploration and query examples
- [ ] Add alternative distributions such as Turtle
- [ ] Explore semantic projections into schemas and APIs
- [ ] Explore ontology-informed user experience
- [ ] Explore executable knowledge examples
- [ ] Relate the case study to broader Semantic Modeling and Executable Knowledge Architecture concepts

## Acknowledgements

The ontology used by this repository is derived from the classic Pizza ontology and its Manchester / Protégé tutorial tradition.

This engineering repository uses the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit), [ROBOT](https://robot.obolibrary.org/), and related ontology tooling. It also intends to explore [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) as a programmatic access layer.

## License

The upstream Pizza 2.0 ontology declares **CC BY 3.0**.

Licensing of newly created documentation, code, examples, and other repository artifacts will be specified separately so that the provenance and licensing of the historical ontology are not silently conflated with the licensing of new work.
