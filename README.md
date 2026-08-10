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
- ontology metadata where supported by the selected adapter,
- use from scripts and applications.

The first executable OAK slice is implemented in [`examples/oak`](examples/oak). Starting from `pizza:AmericanHot`, it demonstrates English label lookup, explicit Pizza CURIE-prefix registration, projected OWL relationships, and is-a ancestry through both the OAK Python API and CLI.

The example also makes an important OAK boundary visible: the common interface spans multiple adapters, but individual backends do not necessarily implement every operation. The local Functional-Syntax adapter used by the first slice supports the selected entity/relationship/traversal operations but does not currently implement ontology enumeration/metadata access. That capability is therefore recorded as backend-dependent rather than treated as a Pizza-data defect.

### 4. Reason and Validate

Explore the distinction between **asserted knowledge**, **inferred knowledge**, **logical coherence**, and **data conformance** using ROBOT, HermiT, SPARQL, SHACL, and pySHACL.

The historical Pizza ontology deliberately contains two unsatisfiable classes:

- `CheeseyVegetableTopping`
- `IceCream`

Rather than removing them, this repository preserves them as part of the teaching ontology and explicitly verifies them as expected semantic behavior.

For reusable reasoning, the repository now owns a canonical coherent module in [`artifacts/reasoning`](artifacts/reasoning). It demonstrates that:

```text
AmericanHot SubClassOf SpicyPizza
```

is **not asserted** in the module but is **inferred** by HermiT, verified by SPARQL, and explainable from the selected Pizza axioms. The module is pinned to the preserved Pizza source blob and carries machine-readable provenance.

For explicit RDF instance-data validation, [`artifacts/validation`](artifacts/validation) defines a repository-owned SHACL profile plus conforming and non-conforming examples. The validation profile is deliberately not presented as an automatic translation of OWL semantics:

```text
OWL / HermiT
    What follows logically from the semantic model?

SHACL / pySHACL
    Does explicit RDF data satisfy a validation profile?
```

The two concerns are tested independently in CI.

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

The architecture behind these distinctions is documented in:

- [Ontology Identity and Publication Model](docs/identity-publication-model.md)
- [Pizza Ontology Provenance](docs/pizza-provenance.md)
- [Versioning and Release Model](docs/versioning-release-model.md)
- [Licensing](LICENSE.md)
- [Attribution and Provenance Notice](NOTICE.md)

The current repository is the **preservation/stewardship line** for Pizza Ontology 2.0. Repository releases use a separate preservation release series and do not change the historical ontology version merely because engineering artifacts evolve.

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

The companion [Executable Semantic Knowledge Architecture (ESKA)](https://github.com/GerhardBalz/executable-semantic-knowledge-architecture) project uses Pizza as its initial semantic reference domain. The repository boundary is intentional:

```text
pizza-ontology
    owns and engineers Pizza semantic artifacts
        │
        ▼
ESKA
    operationalizes semantic knowledge as executable capabilities,
    services, agents, verification, and provenance
```

That boundary is now executable rather than merely documented. [`artifacts/manifest.ttl`](artifacts/manifest.ttl) publishes the machine-readable consumer contract for the canonical reasoning module, SHACL profile, and validation data. ESKA pins this repository to immutable commit:

```text
613ff0b6e615cbb2eac7cd92358eca9f885fbc7d
```

and runtime-materializes the declared artifacts instead of maintaining independent Pizza-domain semantic copies.

```text
pizza-ontology
    owns semantic artifacts
        ↓ artifacts/manifest.ttl
    immutable commit 613ff0...
        ↓
ESKA
    runtime materializes semantic inputs
        ↓
    Capability / Execution / Service / Agent /
    Verification / Provenance
```

The ESKA integration was completed in ESKA PR #19, merged as `7dbbdf0a1ae39a7bdb3c9af0fb410d5899acbc5a`. Both repositories verify their side of the contract in CI: this repository verifies the published artifact paths and metadata, while ESKA verifies the immutable source binding, forbids reintroduction of its former semantic copies, and executes reasoning, validation, Service, and Agent behavior over the source-owned artifacts.

Track 8 is therefore complete. The key principle is:

> **Execution must not sever semantics — and execution architecture should not become the accidental owner of domain semantics.**

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

The editor ontology is:

[`src/ontology/pizza-edit.owl`](src/ontology/pizza-edit.owl)

The current project intentionally does **not** claim authority over the historical `co-ode.org` identifier space.

### Preservation line and repository releases

This repository is now explicitly treated as the **preservation, stewardship, engineering, and learning line** for the historical Pizza Ontology 2.0 baseline.

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

A repository release may add OAK examples, alternative distributions, SHACL shapes, semantic projections, UX examples, or ESKA integration while the preserved ontology continues to declare version `2.0`.

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

This repository currently acts as a preservation, migration, engineering, and learning environment derived from that historical artifact. It does not claim to be the original authority or source repository of the Pizza ontology.

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
│   │   ├── spicy-pizza.ofn
│   │   ├── provenance.ttl
│   │   └── ...
│   └── validation/
│       ├── pizza-instance-shapes.ttl
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
│   ├── ontology/
│   │   ├── pizza-edit.owl
│   │   ├── pizza-odk.yaml
│   │   ├── pizza.Makefile
│   │   └── ...
│   ├── scripts/
│   └── sparql/
├── CONTRIBUTING.md
├── LICENSE.md
├── NOTICE.md
└── README.md
```

Additional examples will be introduced as the API/projection, UX, knowledge-graph, and executable-knowledge tracks are developed.

## Working with the Ontology

### ODK lifecycle and QC

The project uses ODK containers. With [ODK Runner](https://github.com/INCATools/odkrunner) installed:

```bash
cd src/ontology
odkrun make test
```

The test suite includes a Pizza-specific semantic regression test that verifies the two intentionally unsatisfiable tutorial classes.

### OAK access

Install the pinned OAK dependencies and run the first access slice:

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

See [`examples/oak/README.md`](examples/oak/README.md) for the CLI, Python API, prefix, language, and adapter-capability details.

### OWL reasoning artifact

Run the canonical coherent reasoning module:

```bash
bash artifacts/reasoning/run.sh
```

The regression proves that `AmericanHot SubClassOf SpicyPizza` is not asserted, is inferred by HermiT, and can be explained. See [`artifacts/reasoning/README.md`](artifacts/reasoning/README.md).

### SHACL validation artifact

Install the pinned validator and test both explicit data cases:

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/validation/validate_examples.py
```

The conforming graph must pass; the non-conforming graph must fail on the expected `hasBase` and `hasTopping` paths. See [`artifacts/validation/README.md`](artifacts/validation/README.md).

### Semantic artifact consumer contract

The same validation dependency set provides `rdflib`, which is used to verify the machine-readable downstream contract:

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/verify_consumer_contract.py
```

The verifier requires the manifest to publish exactly the expected reasoning, SHACL, conforming-data, and non-conforming-data artifacts; checks their formats, provenance, and license metadata; and fails if a declared repository-relative path no longer resolves.

Consumers should pair those stable artifact roles/paths with an immutable Git commit or preservation release rather than bind to mutable `main` content.

## Architecture Documents

### Ontology Identity and Publication Model

[`docs/identity-publication-model.md`](docs/identity-publication-model.md)

Defines the generic concepts used by this project, including ontology and entity identity, versioning, releases, distributions, source repositories, provenance, authority, stewardship, hosting, and rights.

### Pizza Ontology Provenance

[`docs/pizza-provenance.md`](docs/pizza-provenance.md)

Applies the generic model to the historical Pizza ontology and documents its lineage, upstream source, contributors, hosting, authority uncertainty, migration provenance, and preservation-versus-successor analysis.

### Versioning and Release Model

[`docs/versioning-release-model.md`](docs/versioning-release-model.md)

Defines the adopted distinction between the immutable historical Pizza Ontology 2.0 semantic baseline, repository preservation releases, artifact/distribution types, toolchain versions, and a possible separate successor ontology lineage.

## Roadmap

The repository will evolve incrementally rather than attempting to demonstrate every concept at once.

- [x] Establish Pizza 2.0 preservation baseline
- [x] Migrate the ontology into ODK
- [x] Establish semantic regression tests
- [x] Document ontology identity and publication concepts
- [x] Document Pizza provenance
- [x] Establish preservation/repository versioning model
- [x] Establish repository licensing and attribution boundary
- [ ] Cut the first `preservation-v0.1.0` repository release
- [ ] Refine publication and distribution strategy
- [x] Add first OAK access vertical slice
- [x] Add canonical coherent reasoning and SHACL validation artifacts
- [x] Publish the machine-readable semantic artifact consumer contract
- [x] Integrate stable Pizza semantic artifacts with ESKA through an immutable source binding
- [ ] Add broader ontology exploration and query examples
- [ ] Add alternative distributions such as Turtle
- [ ] Explore semantic projections into schemas and APIs
- [ ] Explore ontology-informed user experience
- [ ] Relate the case study to broader Semantic Modeling concepts
- [ ] Evaluate a separate successor Pizza ontology when semantic modernization is required

## Acknowledgements

The ontology used by this repository is derived from the classic Pizza ontology and its Manchester / Protégé tutorial tradition.

This engineering repository uses the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit), [ROBOT](https://robot.obolibrary.org/), [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/), HermiT, SHACL, and pySHACL across their respective tracks.

## License

This repository has an explicit licensing boundary rather than one blanket license:

- historical **Pizza Ontology 2.0 semantic content** and distributions containing it retain **CC BY 3.0** and the upstream attribution;
- newly created **repository software and engineering material** is licensed under the **MIT License** unless stated otherwise;
- newly created original **repository documentation** is licensed under **CC BY 4.0** unless stated otherwise;
- third-party material retains its own license.

See [LICENSE.md](LICENSE.md) for the licensing model and [NOTICE.md](NOTICE.md) for Pizza attribution and provenance.