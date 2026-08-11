# Pizza Ontology

[![Build Status](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml/badge.svg)](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml)

A modern **ontology engineering, semantic projection, and executable knowledge reference project** based on the classic Pizza OWL ontology.

The Pizza domain is deliberately small and understandable. It provides one stable semantic subject for exploring ontology modeling, engineering, access, reasoning, validation, publication, executable semantic artifacts, implementation projections, applications, user experience, and executable semantic knowledge architecture.

## Why Pizza?

The Pizza ontology is a well-known OWL teaching example from the Manchester / Protégé tutorial tradition. It demonstrates non-trivial OWL concepts while remaining immediately understandable:

- classes and class hierarchies;
- object properties and restrictions;
- disjointness and defined classes;
- value partitions and individuals;
- multilingual labels and annotations;
- reasoning;
- intentional unsatisfiable teaching classes.

The historical **Pizza Ontology 2.0** remains the semantic preservation baseline. Repository-authored engineering, executable, projection, application, and UX artifacts are maintained around that baseline without silently changing its historical identity.

## Architecture at a glance

The ontology is the semantic center, but it is not the whole system.

```text
Pizza Ontology 2.0
    authoritative semantic model
        │
        ├── Protégé / OWL        model
        ├── ODK / ROBOT          engineer / preserve
        ├── OAK                  access / query
        ├── HermiT               reason
        └── SHACL etc.           validate / execute semantic artifacts
        │
        ▼
source-owned semantic artifacts
    reasoning / validation / rule / decision /
    calculation / mapping / workflow
        │
        ├──────────────→ ESKA
        │                Capability → Execution → Result → Verification
        │
        ▼
source-verified semantic slice
        │
        ├── JSON ImplementationProjection
        │       concrete projected content
        │       └──→ direct-projection UX
        │
        └── OpenAPI ImplementationProjection
                interface contract
                 │
                 └── + JSON content projection
                          ↓
                     Application
                          ↓ HTTP
                     API-backed UX
```

The guiding rule is:

> **No downstream layer silently becomes a second semantic source of truth.**

## Nine Tracks

### 1. Model — Protégé and OWL

The historical Pizza Ontology 2.0 owns the domain semantics: classes, properties, restrictions, definitions, disjointness, individuals, annotations, and ontology/entity identity.

The preserved editor ontology is [`src/ontology/pizza-edit.owl`](src/ontology/pizza-edit.owl).

See [Pizza OWL Modeling Patterns and Teaching Cases](docs/pizza-owl-modeling-patterns.md).

### 2. Engineer — Ontology Development Kit

The [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit) and ROBOT provide reproducible source management, semantic regression testing, QC, preservation-safe builds, and release engineering.

The historical Pizza 2.0 ontology has been migrated into the ODK editor ontology while preserving its semantic content and identifiers.

### 3. Access — Ontology Access Kit

The [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) provides programmatic access to identifiers, labels, relationships, and ancestry.

The executable reference under [`examples/oak/`](examples/oak/) includes both the original `pizza:AmericanHot` vertical slice and a broader query specimen covering entity identity/labels, direct versus transitive hierarchy, projected `hasTopping` relationships, descendant traversal, and backend-dependent lexical-search capability probing through the OAK Python API and CLI.

OAK is an access layer over the semantic source. It is not a replacement ontology and graph traversal is not a substitute for OWL reasoning.

### 4. Reason and Validate

The repository deliberately keeps OWL reasoning and SHACL validation distinct:

```text
OWL / HermiT     → What follows logically from the ontology?
SHACL / pySHACL  → Does explicit RDF data satisfy a validation profile?
```

The historical ontology contains two intentional unsatisfiable teaching classes:

- `CheeseyVegetableTopping`
- `IceCream`

They are preserved and regression-tested.

[`artifacts/reasoning/`](artifacts/reasoning/) proves that `AmericanHot SubClassOf SpicyPizza` is inferred rather than asserted. [`artifacts/validation/`](artifacts/validation/) provides a repository-authored SHACL profile with conforming and non-conforming examples.

### 5. Publish and Govern

Publication keeps identity, release, distribution, location, authority, and stewardship separate:

```text
Ontology ≠ file
Ontology ≠ repository
Ontology version ≠ repository release
Release ≠ distribution
Identifier ≠ location
Host ≠ authority
Repository ownership ≠ ontology authority
```

See:

- [Ontology Identity and Publication Model](docs/identity-publication-model.md)
- [Pizza Ontology Provenance](docs/pizza-provenance.md)
- [Versioning and Release Model](docs/versioning-release-model.md)
- [Preservation-Safe Distributions](docs/preservation-distributions.md)
- [Publication and Distribution Policy](docs/publication-distribution-policy.md)
- [Machine-Readable Publication Catalog](metadata/publication.ttl)
- [Licensing](LICENSE.md)
- [Attribution and Provenance Notice](NOTICE.md)

This repository is the **preservation/stewardship line** for Pizza Ontology 2.0. It does not claim authority over the historical `co-ode.org` namespace.

### 6. Project — Semantic Projections

The repository now demonstrates two materially different **Implementation Projections** over one shared OAK-verified source slice.

#### JSON content projection

[`projections/pizza-concepts/`](projections/pizza-concepts/) produces a checked-in JSON/JSON-Schema catalog containing selected projected Pizza concepts.

```text
Pizza OWL
    ↓ OAK source extraction
selected semantic slice
    ↓
PizzaConceptCatalog JSON
```

#### OpenAPI interface projection

[`projections/pizza-openapi/`](projections/pizza-openapi/) produces an OpenAPI 3.1 contract for exposing the selected concept projection through an application API.

```text
Pizza OWL
    ↓ OAK source extraction
selected semantic slice
    ↓
OpenAPI 3.1 contract
```

Both projections explicitly document semantics that are preserved, transformed, introduced, and omitted. Both are regression-tested against the preserved Pizza source.

The OpenAPI contract deliberately introduces application-interface concerns such as paths, operations, query parameters, response envelopes, and HTTP statuses. Those are not Pizza ontology facts.

### 7. Experience — Ontology-Informed UX

Two comparable UX architectures are implemented.

#### Direct projection → UX

The [Pizza Semantic Explorer](https://gerhardbalz.github.io/pizza-ontology/examples/ux/pizza-explorer/) is a static GitHub Pages application that consumes the JSON Implementation Projection directly:

```text
Pizza OWL
    ↓
JSON ImplementationProjection
    ↓
UX
```

The browser does not parse OWL or recreate Pizza semantic relationships in JavaScript.

#### Projections → Application → UX

[`examples/application/pizza-catalog-api/`](examples/application/pizza-catalog-api/) implements the checked-in OpenAPI contract using the JSON projection as projected runtime content. [`examples/ux/pizza-api-explorer/`](examples/ux/pizza-api-explorer/) consumes that application over HTTP:

```text
JSON content projection
        +
OpenAPI interface projection
        ↓
Application
        ↓
API-backed UX
```

The application owns runtime filtering, lookup, HTTP envelopes, and `404` behavior. Semantic identity and selected semantic relationships remain upstream in the source-verified projection.

### 8. Execute — Executable Semantic Knowledge

The companion [Executable Semantic Knowledge Architecture (ESKA)](https://github.com/GerhardBalz/executable-semantic-knowledge-architecture) project operationalizes source-owned Pizza semantics.

[`artifacts/manifest.ttl`](artifacts/manifest.ttl) publishes **twenty-three semantic distributions** across seven execution semantics:

```text
Ontology    → reason
Constraint  → validate
Rule        → evaluate
Decision    → decide
Calculation → calculate
Mapping     → transform
Workflow    → execute
```

The ownership boundary is explicit:

```text
pizza-ontology
    owns Pizza semantic artifacts
        ↓ immutable source contract
ESKA
    owns capability / execution / result / verification
    and optional service / agent / deployment architecture
```

> **Execution must not sever semantics — and execution architecture should not become the accidental owner of domain semantics.**

### 9. Architect — Semantic Modeling

The cross-track architecture has now produced two evidence-backed reusable concepts:

```text
SemanticModel
ImplementationProjection
```

`SemanticModel` is the cross-formalism semantic representation concept already exercised by Pizza and the ESKA execution modes.

`ImplementationProjection` is a non-authoritative implementation-oriented representation or contract derived from selected semantics under an explicit preservation/transformation/introduction/omission policy with machine-verifiable source traceability.

The project deliberately keeps this narrower than semantic Mapping / Transformation:

```text
ImplementationProjection
    SemanticModel → narrower application representation / contract

Semantic Mapping / Transformation
    source SemanticModel
        → mapping semantics
        → target SemanticModel
```

See:

- [Cross-Track Pizza Semantic Architecture](docs/semantic-architecture.md)
- [Semantic Modeling Concept Harvest](docs/semantic-modeling-concept-harvest.md)
- [Semantic Modeling Vocabulary Decision](docs/semantic-modeling-vocabulary-decision.md)

The conceptual extraction threshold has passed, but a separate Semantic Modeling namespace/repository is intentionally deferred while ESKA's permanent W3ID namespace activation is still unresolved. ESKA issue #57 will reassess ownership of `SemanticModel` after that governance step.

## Preservation baseline

The preserved semantic identity remains:

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

### Repository releases

Ontology semantic version and repository preservation release are independent:

```text
Historical semantic version
    Pizza Ontology 2.0

Repository preservation release
    preservation-v0.x.y
```

The first repository release, [`preservation-v0.1.0`](https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.1.0), establishes the conservative preservation baseline.

The verified Functional Syntax + Turtle distribution workflow was added after that release, so `preservation-v0.1.0` remains unchanged. A later preservation release can attach the verified multi-format distribution set as immutable assets.

### Possible successor ontology

A future modernized Pizza ontology may coexist with this preservation line only when there is a concrete semantic modernization requirement. It should use an explicit authority model, new governed ontology/entity identity, provenance back to Pizza 2.0, and its own version series.

Issue #4 remains intentionally dormant until such a requirement exists.

## Repository structure

```text
pizza-ontology/
├── .github/workflows/
├── artifacts/
│   ├── manifest.ttl
│   ├── reasoning/
│   ├── validation/
│   ├── rules/
│   ├── decisions/
│   ├── calculations/
│   ├── mappings/
│   └── workflows/
├── docs/
├── examples/
│   ├── oak/
│   ├── application/
│   │   └── pizza-catalog-api/
│   └── ux/
│       ├── pizza-explorer/
│       └── pizza-api-explorer/
├── metadata/
│   ├── publication.ttl
│   └── verify_publication_metadata.py
├── projections/
│   ├── common/
│   ├── pizza-concepts/
│   └── pizza-openapi/
├── src/ontology/
│   ├── pizza-edit.owl
│   ├── pizza-odk.yaml
│   └── pizza.Makefile
├── LICENSES/
├── CONTRIBUTING.md
├── LICENSE.md
├── NOTICE.md
└── README.md
```

## Run key reference paths

### Ontology engineering

```bash
cd src/ontology
odkrun make test
```

### OAK access

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

The runner covers both the minimal access slice and broader entity/hierarchy/relationship/descendant/search-capability queries.

### JSON semantic projection

```bash
python -m pip install -r projections/pizza-concepts/requirements.txt
python projections/pizza-concepts/project.py --check
```

### OpenAPI semantic projection

```bash
python -m pip install -r projections/pizza-openapi/requirements.txt
python projections/pizza-openapi/project.py --check
```

### Direct-projection UX

From the repository root:

```bash
python -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/examples/ux/pizza-explorer/
```

The deployed GitHub Pages version is:

https://gerhardbalz.github.io/pizza-ontology/examples/ux/pizza-explorer/

### OpenAPI-backed application + UX

```bash
python -m pip install -r examples/application/pizza-catalog-api/requirements.txt
python examples/application/pizza-catalog-api/app.py --port 8001
```

Then open:

```text
http://127.0.0.1:8001/
http://127.0.0.1:8001/concepts
http://127.0.0.1:8001/openapi.json
```

Runtime contract verification:

```bash
node --check examples/ux/pizza-api-explorer/app.js
python examples/application/pizza-catalog-api/verify_application.py
```

### Executable semantic artifacts

```bash
bash artifacts/reasoning/run.sh
python artifacts/validation/validate_examples.py
python artifacts/rules/evaluate_rule.py
python artifacts/decisions/evaluate_decision.py
python artifacts/calculations/evaluate_calculation.py
python artifacts/mappings/evaluate_mapping.py
python artifacts/workflows/evaluate_workflow.py
```

## CI architecture

The main `CI` workflow currently contains **13 independent jobs**:

```text
ontology_qc              preserve / engineer / ontology QC
oak_access               access / navigate / query
semantic_projection      JSON Implementation Projection
openapi_projection       OpenAPI Implementation Projection
ontology_informed_ux     direct projection → UX
openapi_application_ux   projections → Application → UX
reasoning_artifact       reason / infer
shacl_validation         validate / contracts / publication metadata
rule_evaluation          evaluate rule / derive
decision_evaluation      decide / select outcome
calculation_evaluation   calculate / numeric result
mapping_evaluation       transform / target graph
workflow_evaluation      execute / conditional composition
```

A separate **Modeling reference** workflow verifies that the OWL teaching guide remains anchored to representative axioms in the preserved source ontology.

## Roadmap

- [x] Establish Pizza 2.0 preservation baseline
- [x] Migrate the ontology into ODK
- [x] Establish semantic regression tests
- [x] Document ontology identity, provenance, modeling patterns, and licensing boundaries
- [x] Establish preservation/repository versioning and publication model
- [x] Cut `preservation-v0.1.0`
- [x] Add preservation-safe Functional Syntax + Turtle distributions
- [x] Add first OAK access vertical slice
- [x] Add broader OAK ontology exploration and query examples — #60
- [x] Add reasoning and SHACL validation references
- [x] Publish the machine-readable semantic artifact consumer contract
- [x] Add Rule, Decision, Calculation, Mapping, and Workflow semantic artifacts
- [x] Integrate stable Pizza semantic artifacts with ESKA through immutable source bindings
- [x] Add JSON/JSON-Schema Implementation Projection
- [x] Add OpenAPI 3.1 Implementation Projection
- [x] Add direct-projection ontology-informed UX
- [x] Add OpenAPI-backed deterministic application and API-backed UX
- [x] Harvest broader Semantic Modeling concepts from implemented evidence
- [x] Adopt `SemanticModel + ImplementationProjection` as the conceptual reusable pair
- [ ] Revisit a separate Semantic Modeling namespace/repository after ESKA W3ID governance stabilizes
- [ ] Evaluate a separate successor Pizza ontology only when semantic modernization is required — #4

## Acknowledgements

The ontology is derived from the classic Pizza ontology and its Manchester / Protégé tutorial tradition. The reference project uses Protégé, ODK, ROBOT, OAK, HermiT, SHACL/pySHACL, RDFLib/SPARQL, DMN, OpenMath, BPMN, JSON Schema, and OpenAPI across their respective architectural roles.

## License

This repository has an explicit licensing boundary:

- historical Pizza Ontology 2.0 semantic content and distributions containing it retain **CC BY 3.0** and upstream attribution;
- newly created repository software and engineering material is **MIT** unless stated otherwise;
- newly created original repository documentation is **CC BY 4.0** unless stated otherwise;
- third-party material retains its own license.

See [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).
