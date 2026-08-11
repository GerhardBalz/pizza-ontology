# Pizza Ontology

[![Build Status](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml/badge.svg)](https://github.com/GerhardBalz/pizza-ontology/actions/workflows/qc.yml)

A modern **ontology engineering and executable knowledge reference project** based on the classic Pizza OWL ontology.

The Pizza domain is deliberately small and understandable. It provides one stable semantic subject for exploring ontology modeling, engineering, access, reasoning, validation, publication, rules, decisions, calculations, mappings, workflows, projections, user experience, and executable semantic knowledge.

## Why Pizza?

The Pizza ontology is a well-known OWL teaching example from the Manchester / Protégé ontology tutorial tradition. It demonstrates non-trivial OWL concepts while remaining immediately understandable:

- classes and class hierarchies;
- object properties and restrictions;
- disjointness and defined classes;
- value partitions and individuals;
- multilingual labels and annotations;
- reasoning;
- intentional unsatisfiable teaching classes.

The historical Pizza Ontology 2.0 remains the semantic preservation baseline. Repository-authored engineering artifacts are maintained around that baseline without silently changing its historical identity.

## Project Direction

The **ontology is the semantic center**. Tools and executable artifacts remain separate engineering or operational layers.

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
 ┌─────────┬─────────┬──────┬─┼──────┬──────────┬────────┬───────────┐
 ▼         ▼         ▼      ▼        ▼          ▼        ▼           ▼
Reasoning Validation Rules Decisions Calculations Mappings Workflows Projections
 │         │         │      │        │          │        │           │
 └─────────┴─────────┴──────┴────────┴──────────┴────────┴─────┬─────┘
                                                               ▼
                                                    Executable Knowledge
                                                               │
                                                               ▼
                                          Executable Semantic Knowledge Architecture
```

## Nine Tracks

### 1. Model — Protégé and OWL

Explore ontology structure, classes and properties, restrictions and definitions, annotations, reasoning, metadata, identity, and versioning with [Protégé](https://protege.stanford.edu/) and OWL.

### 2. Engineer — Ontology Development Kit

Use the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit) for Git-based source management, reproducible builds, ROBOT tooling, automated validation, semantic regression tests, CI, release engineering, provenance, and governance.

The historical Pizza 2.0 ontology has been migrated into the ODK editor ontology while preserving its semantic content and identifiers.

### 3. Access — Ontology Access Kit

Use the [Ontology Access Kit (OAK)](https://incatools.github.io/ontology-access-kit/) for entity lookup, labels, ancestry, relationship traversal, queries, and application access.

The first executable slice in [`examples/oak`](examples/oak) starts at `pizza:AmericanHot` and demonstrates CURIE-prefix registration, preserved multilingual label access, projected OWL relationships, and is-a ancestry through the OAK Python API and CLI.

The example records adapter capabilities explicitly: the local Functional-Syntax adapter supports the selected access operations, while language filtering and ontology metadata behavior remain backend-dependent.

### 4. Reason and Validate

The historical ontology deliberately contains two unsatisfiable teaching classes:

- `CheeseyVegetableTopping`
- `IceCream`

They are preserved and regression-tested as historical behavior.

[`artifacts/reasoning`](artifacts/reasoning) contains a coherent reasoning module proving that:

```text
AmericanHot SubClassOf SpicyPizza
```

is not asserted but is inferred by HermiT and verifiable with SPARQL.

[`artifacts/validation`](artifacts/validation) contains a repository-authored SHACL profile and explicit conforming/non-conforming RDF examples.

```text
OWL / HermiT     → What follows logically?
SHACL / pySHACL  → Does explicit RDF satisfy the profile?
```

### 5. Publish and Govern

Use Pizza as a case study for semantic identity, publication, provenance, versioning, release, licensing, and governance.

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
- [Preservation-Safe Distributions](docs/preservation-distributions.md)
- [Publication and Distribution Policy](docs/publication-distribution-policy.md)
- [Machine-Readable Publication Catalog](metadata/publication.ttl)
- [Licensing](LICENSE.md)
- [Attribution and Provenance Notice](NOTICE.md)

This repository is the **preservation/stewardship line** for Pizza Ontology 2.0.

### 6. Project — Semantic Projections

Explore JSON, JSON Schema, API schemas, OpenAPI, graph models, search indexes, and other projections. Derived artifacts need not be mechanically generated from OWL, but they should remain traceable to the semantic model.

### 7. Experience — Ontology-Informed UX

Explore semantic navigation, search/filtering, ontology-informed forms, guided configuration, explanations, validation messages, and vocabulary-aware interfaces. UX-specific knowledge can remain outside the ontology while retaining semantic links.

### 8. Execute — Executable Knowledge

The companion [Executable Semantic Knowledge Architecture (ESKA)](https://github.com/GerhardBalz/executable-semantic-knowledge-architecture) project operationalizes source-owned Pizza semantics.

```text
pizza-ontology
    owns and engineers Pizza semantic artifacts
        │
        ▼
ESKA
    operationalizes them as Capabilities, Executions,
    Results, Verification, provenance, Services and Agents
```

[`artifacts/manifest.ttl`](artifacts/manifest.ttl) is the machine-readable consumer contract. It currently publishes **twenty-three semantic distributions** covering seven execution semantics:

```text
Ontology    → reason
Constraint  → validate
Rule        → evaluate
Decision    → decide
Calculation → calculate
Mapping     → transform
Workflow    → execute
```

The published set contains:

- one coherent OWL reasoning module;
- one SHACL validation profile and two RDF validation cases;
- one SPARQL rule, rule-result vocabulary, and RDF rule data;
- one DMN 1.5 decision table, decision vocabulary, and decision cases;
- one OpenMath area formula, calculation vocabulary, and calculation cases;
- one SPARQL semantic mapping, target Menu vocabulary, source RDF graph, and expected target RDF graph;
- one BPMN 2.0.2 workflow, workflow semantic vocabulary, valid/invalid workflow inputs, expected valid Menu graph, and workflow case contract.

The Mapping artifact is deliberately different from the Rule artifact even though both use SPARQL `CONSTRUCT`:

```text
Rule
    Pizza source semantic model
        ↓ derive
    Pizza-domain statement

Mapping
    Pizza source semantic model
        ↓ mapping semantics
    Menu target semantic model
        ↓
    transformed target graph
```

The Workflow artifact is different again: it owns orchestration rather than the semantics of its steps.

```text
Start
  ↓
Validate Pizza RDF                 existing SHACL semantics
  ↓
conforms?
  ├── false → Rejected
  └── true
        ↓
Transform Pizza → Menu             existing Mapping semantics
        ↓
      Published
```

The valid case executes both semantic steps; the invalid case stops after validation and never executes Mapping.

ESKA pins the semantic artifact contract to the corrected immutable source commit:

```text
715f0460a43abacb5258eedd3d722da219a25a43
```

and materializes declared artifacts at runtime rather than maintaining independent Pizza-domain semantic copies. This corrected commit also resolves the workflow Mapping-artifact identifier mismatch detected by independent ESKA consumption.

> **Execution must not sever semantics — and execution architecture should not become the accidental owner of domain semantics.**

### 9. Architect — Semantic Modeling

Use the project as a case study for semantic identity, provenance, authority/stewardship, lifecycle, semantic projections, executable artifacts, source/target semantic roles, composite semantic execution, knowledge-driven systems, and the relationship between conceptual, semantic, logical, and executable models.

## Preservation Baseline

The current baseline preserves:

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

The editor ontology is [`src/ontology/pizza-edit.owl`](src/ontology/pizza-edit.owl). This project intentionally does **not** claim authority over the historical `co-ode.org` identifier space.

### Repository releases

Ontology version and repository release version are independent:

```text
Historical semantic version
    Pizza Ontology 2.0

Repository preservation release
    preservation-v0.x.y
```

The first repository release, [`preservation-v0.1.0`](https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.1.0), establishes the conservative preservation baseline.

The verified multi-format Functional Syntax and Turtle distribution workflow was added after that release. `preservation-v0.1.0` remains unchanged; a subsequent preservation release can publish the verified distribution set as immutable release assets.

A preservation release can add engineering, access, validation, rule, decision, calculation, mapping, workflow, projection, UX, or integration artifacts while the preserved ontology continues to declare version `2.0`.

### Possible successor ontology

A future modernized Pizza ontology may coexist with this preservation line. If created, it should be a **separate successor lineage** with explicit authority, a new ontology identity/governed namespace, a separate repository, and its own version series. It should not silently become Pizza 2.1/3.0 without legitimate authority over the historical identity.

## Provenance

The migration baseline is derived from the Pizza 2.0 ontology distributed by the Stanford Protégé site:

`https://protege.stanford.edu/ontologies/pizza/pizza.owl`

The historical ontology credits Alan Rector, Chris Wroe, Matthew Horridge, Nick Drummond, and Robert Stevens and declares **CC BY 3.0**. This repository acts as a preservation, migration, engineering, and learning environment; it does not claim to be the original ontology authority.

See [docs/pizza-provenance.md](docs/pizza-provenance.md).

## Repository Structure

```text
pizza-ontology/
├── .github/workflows/
├── artifacts/
│   ├── manifest.ttl
│   ├── verify_consumer_contract.py
│   ├── reasoning/
│   ├── validation/
│   ├── rules/
│   ├── decisions/
│   ├── calculations/
│   ├── mappings/
│   └── workflows/
├── docs/
├── examples/oak/
├── metadata/
│   ├── publication.ttl
│   └── verify_publication_metadata.py
├── LICENSES/
├── src/ontology/
│   ├── pizza-edit.owl
│   ├── pizza-odk.yaml
│   └── pizza.Makefile
├── CONTRIBUTING.md
├── LICENSE.md
├── NOTICE.md
└── README.md
```

## Run the Executable Artifacts

ODK lifecycle/QC:

```bash
cd src/ontology
odkrun make test
```

OAK access:

```bash
python -m pip install -r examples/oak/requirements.txt
bash examples/oak/run.sh
```

OWL reasoning:

```bash
bash artifacts/reasoning/run.sh
```

SHACL validation:

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/validation/validate_examples.py
```

SPARQL rule evaluation:

```bash
python -m pip install -r artifacts/rules/requirements.txt
python artifacts/rules/evaluate_rule.py
```

DMN decision evaluation:

```bash
python artifacts/decisions/evaluate_decision.py
```

OpenMath calculation evaluation:

```bash
python artifacts/calculations/evaluate_calculation.py
```

Semantic mapping evaluation:

```bash
python -m pip install -r artifacts/mappings/requirements.txt
python artifacts/mappings/evaluate_mapping.py
```

BPMN workflow evaluation:

```bash
python -m pip install -r artifacts/workflows/requirements.txt
python artifacts/workflows/evaluate_workflow.py
```

The workflow regression proves both execution paths:

```text
valid-publication   → validation → mapping → Published
invalid-rejection   → validation → Rejected
```

Semantic artifact consumer contract:

```bash
python -m pip install -r artifacts/validation/requirements.txt
python artifacts/verify_consumer_contract.py
```

Publication metadata contract:

```bash
python metadata/verify_publication_metadata.py
```

The semantic-artifact verifier requires exactly the expected **twenty-three** distributions and checks their paths, formats, dependencies, provenance/conformance metadata, and licensing boundaries. The publication verifier independently checks that release locations remain distinct from historical semantic identifiers and that `preservation-v0.1.0` does not claim later distribution assets.

## CI Concerns

Nine independent concerns remain intentionally separate:

```text
ODK        → preserve / engineer / ontology QC
OAK        → access / navigate
HermiT     → reason / infer
SHACL      → validate / conform
SPARQL     → evaluate rule / derive
DMN        → decide / select outcome
OpenMath   → calculate / numeric result
Mapping    → transform / target graph
BPMN       → execute / conditional composition
```

## Roadmap

- [x] Establish Pizza 2.0 preservation baseline
- [x] Migrate the ontology into ODK
- [x] Establish semantic regression tests
- [x] Document ontology identity and Pizza provenance
- [x] Establish preservation/repository versioning model
- [x] Establish repository licensing and attribution boundary
- [x] Cut the first `preservation-v0.1.0` repository release
- [x] Refine publication and distribution strategy
- [x] Add first OAK access vertical slice
- [x] Add canonical coherent reasoning and SHACL validation artifacts
- [x] Publish the machine-readable semantic artifact consumer contract
- [x] Add source-owned SPARQL rule-evaluation artifacts
- [x] Add source-owned DMN decision artifacts
- [x] Add source-owned OpenMath calculation artifacts
- [x] Add source-owned semantic Mapping artifacts
- [x] Add source-owned BPMN Workflow artifacts
- [x] Integrate stable Pizza semantic artifacts with ESKA through immutable source bindings
- [ ] Add broader ontology exploration and query examples
- [x] Add alternative distributions such as Turtle
- [ ] Explore semantic projections into schemas and APIs
- [ ] Explore ontology-informed user experience
- [ ] Relate the case study to broader Semantic Modeling concepts
- [ ] Evaluate a separate successor Pizza ontology when semantic modernization is required

## Acknowledgements

The ontology is derived from the classic Pizza ontology and its Manchester / Protégé tutorial tradition. This engineering repository uses ODK, ROBOT, OAK, HermiT, SHACL/pySHACL, RDFLib/SPARQL, DMN, OpenMath, SPARQL-based semantic transformation, and BPMN across their respective tracks.

## License

This repository has an explicit licensing boundary:

- historical Pizza Ontology 2.0 semantic content and distributions containing it retain **CC BY 3.0** and upstream attribution;
- newly created repository software and engineering material is **MIT** unless stated otherwise;
- newly created original repository documentation is **CC BY 4.0** unless stated otherwise;
- third-party material retains its own license.

See [LICENSE.md](LICENSE.md) and [NOTICE.md](NOTICE.md).