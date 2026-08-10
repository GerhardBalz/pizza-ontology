# Pizza Ontology

[![Build Status](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml/badge.svg)](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml)

A modern **ontology engineering and executable knowledge reference project** based on the classic Pizza OWL ontology.

The Pizza domain is deliberately small and understandable. That makes it a useful common example for exploring the lifecycle of semantic knowledge — from ontology modeling and engineering to programmatic access, publication, reasoning, validation, rules, decisions, semantic projections, APIs, user experience, and executable knowledge.

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

The **ontology is the semantic center** of the project. Tools, derived artifacts, APIs, decisions, and applications are engineering or operational layers around that semantic model.

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
       ┌──────────────┬───────┼──────────┬───────────┐
       ▼              ▼       ▼          ▼           ▼
   Reasoning      Validation  Rules    Decisions   Projections
       │              │       │          │           │
       └──────────────┴───────┴──────────┴─────┬─────┘
                                               ▼
                                    Executable Knowledge
                                               │
                                               ▼
                              Executable Semantic Knowledge Architecture
```

The project evolves across nine complementary tracks.

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

Use the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) to explore programmatic ontology access:

- entity lookup,
- labels,
- ancestors and descendants,
- relationships and graph traversal,
- queries and mappings,
- ontology metadata where supported by the selected adapter,
- use from scripts and applications.

The first executable OAK slice is implemented in [`examples/oak`](examples/oak). Starting from `pizza:AmericanHot`, it demonstrates preserved multilingual label access, explicit Pizza CURIE-prefix registration, projected OWL relationships, and is-a ancestry through both the OAK Python API and CLI.

The example also records backend boundaries rather than hiding them. The local Functional-Syntax `FunOwlImplementation` supports the selected label/relationship/traversal operations, but language filtering and ontology metadata capabilities remain adapter-dependent.

### 4. Reason and Validate

Explore the distinction between **asserted knowledge**, **inferred knowledge**, **logical coherence**, and **data conformance** using ROBOT, HermiT, SPARQL, SHACL, and pySHACL.

The historical Pizza ontology deliberately contains two unsatisfiable teaching classes:

- `CheeseyVegetableTopping`
- `IceCream`

They are preserved and tested as expected historical behavior.

For reusable reasoning, [`artifacts/reasoning`](artifacts/reasoning) contains a canonical coherent module demonstrating that:

```text
AmericanHot SubClassOf SpicyPizza
```

is **not asserted** but is **inferred** by HermiT, verified by SPARQL, and explainable from the selected Pizza axioms.

For explicit RDF data validation, [`artifacts/validation`](artifacts/validation) contains a repository-authored SHACL profile plus conforming and non-conforming examples.

```text
OWL / HermiT
    What follows logically from the semantic model?

SHACL / pySHACL
    Does explicit RDF data satisfy a validation profile?
```

### 5. Publish and Govern

Use Pizza as a concrete case study for ontology identity, publication, provenance, versioning, release, licensing, and governance.

Important distinctions include:

```text
Ontology ≠ OWL file
Ontology ≠ Git repository
Ontology version ≠ Repository release
Release ≠ Distribution
Identifier ≠ Location
Host ≠ Authority
Repository Owner ≠ Ontology Authority
Upstream semantic license ≠ Repository-authored material license
```

See:

- [Ontology Identity and Publication Model](docs/identity-publication-model.md)
- [Pizza Ontology Provenance](docs/pizza-provenance.md)
- [Versioning and Release Model](docs/versioning-release-model.md)
- [Licensing](LICENSE.md)
- [Attribution and Provenance Notice](NOTICE.md)

This repository is the **preservation/stewardship line** for Pizza Ontology 2.0. Repository releases use a separate preservation release series and do not change the historical ontology version merely because engineering artifacts evolve.

### 6. Project — Semantic Projections

Explore structures derived from or informed by the semantic model, for example:

- JSON representations,
- JSON Schema,
- API schemas,
- OpenAPI,
- graph models,
- search indexes,
- validation schemas.

Derived artifacts need not be automatically generated from OWL, but they should remain **traceable to the semantic model** while adding concerns appropriate to their own architectural layer.

### 7. Experience — Ontology-Informed UX

Explore how semantic knowledge can inform user interaction:

- semantic navigation,
- search and filtering,
- ontology-driven forms,
- guided configuration,
- explanations,
- validation messages,
- vocabulary-aware interfaces.

UX contains knowledge that does not naturally belong in the ontology itself, but can remain connected to it.

### 8. Execute — Executable Knowledge

The companion [Executable Semantic Knowledge Architecture (ESKA)](https://github.com/GerhardBalz/executable-semantic-knowledge-architecture) project uses Pizza as its initial semantic reference domain.

The repository boundary is intentional:

```text
pizza-ontology
    owns and engineers Pizza semantic artifacts
        │
        ▼
ESKA
    operationalizes semantic knowledge as executable capabilities,
    executions, services, agents, verification, and provenance
```

[`artifacts/manifest.ttl`](artifacts/manifest.ttl) is the machine-readable consumer contract. It currently publishes **ten** semantic distributions covering four different execution semantics:

```text
Ontology   → reason
Constraint → validate
Rule       → evaluate
Decision   → decide
```

The published artifacts include:

- coherent OWL reasoning module,
- SHACL validation profile,
- conforming and non-conforming RDF validation data,
- SPARQL vegetarian-warning rule,
- rule-result vocabulary,
- rule-evaluation RDF data,
- DMN 1.5 dietary-suitability decision table,
- decision outcome vocabulary,
- canonical decision-input cases.

ESKA currently pins this repository to immutable commit:

```text
983b691d9d2102ffad97a3ec31aa9b1435b3e547
```

and runtime-materializes the declared artifacts instead of maintaining independent Pizza-domain semantic copies.

```text
pizza-ontology
    owns semantic artifacts
        ↓ artifacts/manifest.ttl
    immutable commit 983b691...
        ↓
ESKA
    runtime materializes semantic inputs
        ↓
    Capability / Execution / Service / Agent /
    Verification / Provenance
```

The key principle is:

> **Execution must not sever semantics — and execution architecture should not become the accidental owner of domain semantics.**

### 9. Architect — Semantic Modeling

Use the complete project as a case study for broader Semantic Modeling concepts:

- semantic identity,
- provenance,
- authority and stewardship,
- versioning and lifecycle,
- semantic projections,
- executable semantic artifacts,
- model-driven and knowledge-driven systems,
- relationships between conceptual, semantic, logical, and executable models.

## Current Status

The current baseline is a preservation-oriented migration of **Pizza Ontology 2.0** into an ODK-managed repository.

The migration preserves:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

owl:versionInfo
2.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

The editor ontology is [`src/ontology/pizza-edit.owl`](src/ontology/pizza-edit.owl).

The project intentionally does **not** claim authority over the historical `co-ode.org` identifier space.

### Preservation line and repository releases

The semantic ontology version and repository release version are independent:

```text
Historical semantic version
    Pizza Ontology 2.0

Repository preservation release
    preservation-v0.x.y
```

The planned first repository release is:

```text
preservation-v0.1.0
```

A preservation release may add OAK examples, distributions, SHACL profiles, rules, decisions, semantic projections, UX examples, or ESKA integration while the preserved ontology continues to declare version `2.0`.

See [Versioning and Release Model](docs/versioning-release-model.md). The first preservation release is tracked by [issue #7](https://github.com/GerhardBalz/pizza-ontology/issues/7).

### Possible successor ontology

A future modernized Pizza ontology may coexist with this preservation line. If created, it should be treated as a **separate successor lineage** with an explicit authority model, a new ontology identity and governed namespace, a separate repository, and its own version series.

Unless authority over the historical Pizza identifier space is established, a successor should not silently become `Pizza 2.1`, `Pizza 3.0`, or issue new version IRIs beneath the historical `co-ode.org` ontology IRI.

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

This repository acts as a preservation, migration, engineering, and learning environment derived from that historical artifact. It does not claim to be the original authority or source repository of the Pizza ontology.

For the detailed lineage and authority analysis, see [docs/pizza-provenance.md](docs/pizza-provenance.md).

## Repository Structure

```text
pizza-ontology/
├── .github/
│   └── workflows/
├── artifacts/
│   ├── manifest.ttl
│   ├── verify_consumer_contract.py
│   ├── reasoning/
│   │   └── ...
│   ├── validation/
│   │   └── ...
│   ├── rules/
│   │   └── ...
│   └── decisions/
│       ├── pizza-dietary-suitability.dmn
│       ├── decision-vocabulary.ttl
│       ├── data/
│       └── ...
├── docs/
│   ├── identity-publication-model.md
│   ├── pizza-provenance.md
│   └── versioning-release-model.md
├── examples/
│   └── oak/
├── LICENSES/
│   └── MIT.txt
├── src/
│   └── ontology/
│       ├── pizza-edit.owl
│       ├── pizza-odk.yaml
│       └── pizza.Makefile
├── CONTRIBUTING.md
├── LICENSE.md
├── NOTICE.md
└── README.md
```

## Working with the Ontology

### ODK lifecycle and QC

With [ODK Runner](https://github.com/INCATools/odkrunner) installed:

```bash
cd src/ontology
odkrun make test
```

### OAK access

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

See [`examples/oak/README.md`](examples/oak/README.md).

### OWL reasoning artifact

```bash
bash artifacts/reasoning/run.sh
```

The regression proves that `AmericanHot SubClassOf SpicyPizza` is not asserted, is inferred by HermiT, and can be explained.

### SHACL validation artifact

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/validation/validate_examples.py
```

### SPARQL rule evaluation artifact

```bash
python -m pip install -r artifacts/rules/requirements.txt
python artifacts/rules/evaluate_rule.py
```

The rule derives a vegetarian warning from explicit meat-topping data while leaving the vegetable control unmatched.

### DMN decision artifact

```bash
python artifacts/decisions/evaluate_decision.py
```

The canonical DMN 1.5 `UNIQUE` table maps explicit `containsMeat` / `containsFish` contexts to semantic dietary-suitability outcomes:

```text
meatyPizza       → NotVegetarian
fishPizza        → PescatarianOnly
vegetarianPizza  → Vegetarian
```

The included evaluator is a regression harness for the exact supported DMN subset, not a general-purpose DMN engine.

### Semantic artifact consumer contract

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/verify_consumer_contract.py
```

The verifier requires the manifest to publish exactly the expected **ten** distributions and checks their paths, formats, dependencies, provenance, conformance metadata, and license boundaries.

Consumers should pair the stable artifact role/path contract with an immutable Git commit or preservation release rather than bind to mutable `main` content.

## CI Concerns

The repository currently verifies six independent concerns:

```text
ODK      → preserve / engineer / ontology QC
OAK      → access / navigate
HermiT   → reason / infer
SHACL    → validate / conform
SPARQL   → evaluate rule / derive
DMN      → decide / select outcome
```

Keeping these jobs separate makes the architectural boundaries executable rather than merely descriptive.

## Roadmap

- [x] Establish Pizza 2.0 preservation baseline
- [x] Migrate the ontology into ODK
- [x] Establish semantic regression tests
- [x] Document ontology identity and Pizza provenance
- [x] Establish preservation/repository versioning model
- [x] Establish repository licensing and attribution boundary
- [ ] Cut the first `preservation-v0.1.0` repository release
- [ ] Refine publication and distribution strategy
- [x] Add first OAK access vertical slice
- [x] Add canonical coherent reasoning and SHACL validation artifacts
- [x] Publish the machine-readable semantic artifact consumer contract
- [x] Add source-owned SPARQL rule-evaluation artifacts
- [x] Add source-owned DMN decision artifacts
- [x] Integrate stable Pizza semantic artifacts with ESKA through immutable source bindings
- [ ] Add broader ontology exploration and query examples
- [ ] Add alternative distributions such as Turtle
- [ ] Explore semantic projections into schemas and APIs
- [ ] Explore ontology-informed user experience
- [ ] Relate the case study to broader Semantic Modeling concepts
- [ ] Evaluate a separate successor Pizza ontology when semantic modernization is required

## Acknowledgements

The ontology used by this repository is derived from the classic Pizza ontology and its Manchester / Protégé tutorial tradition.

This engineering repository uses ODK, ROBOT, OAK, HermiT, SHACL/pySHACL, RDFLib/SPARQL, and DMN across their respective tracks.

## License

This repository has an explicit licensing boundary rather than one blanket license:

- historical **Pizza Ontology 2.0 semantic content** and distributions containing it retain **CC BY 3.0** and the upstream attribution;
- newly created **repository software and engineering material** is licensed under the **MIT License** unless stated otherwise;
- newly created original **repository documentation** is licensed under **CC BY 4.0** unless stated otherwise;
- third-party material retains its own license.

See [LICENSE.md](LICENSE.md) for the licensing model and [NOTICE.md](NOTICE.md) for Pizza attribution and provenance.
