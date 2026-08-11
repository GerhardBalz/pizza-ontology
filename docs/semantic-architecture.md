# Cross-Track Pizza Semantic Architecture

## Purpose

This document uses the Pizza project as a concrete architecture case study for separating semantic concerns without disconnecting them.

The project deliberately keeps several layers distinct:

```text
historical ontology
    ↓ engineer / access / reason / validate
source-owned semantic artifacts
    ↓ publish through an explicit consumer contract
semantic capabilities and executions
    ↓ expose through services and agents where useful
applications and user experiences
```

The goal is not to force every concern into one ontology or one meta-model. The goal is to preserve traceability across independently governed layers.

## Architecture principle

The Pizza Ontology is the semantic center of the repository, but it is not the whole system.

```text
Ontology
    semantic meaning and logical commitments

Semantic artifacts
    executable or machine-interpretable knowledge around the domain

Distributions
    concrete published representations of those artifacts

Semantic capabilities
    contracts describing what semantic knowledge can do

Executions
    concrete applications of capabilities that produce results

Services and agents
    optional operational access layers

Applications and UX
    consumer-specific experiences informed by semantic knowledge
```

No layer silently replaces another as the semantic source of truth.

## The nine tracks

### 1. Model — Protégé and OWL

Primary concern: the historical Pizza Ontology 2.0 semantic model.

Responsibilities include:

- classes, properties, restrictions, disjointness, definitions, individuals and annotations;
- ontology/entity identity;
- asserted versus inferred semantics;
- preservation of intentional historical teaching characteristics.

The authoritative preservation editor ontology is `src/ontology/pizza-edit.owl`.

This track does not own release engineering, application projections or runtime service contracts.

### 2. Engineer — ODK

Primary concern: reproducible ontology engineering around the preserved semantic baseline.

Responsibilities include:

- repository source management;
- ROBOT/ODK build and QC automation;
- semantic regression tests;
- release engineering;
- toolchain reproducibility;
- preservation-safe artifact generation.

Engineering may change how the ontology is built, checked or distributed without changing Pizza Ontology 2.0 semantics.

### 3. Access — OAK

Primary concern: programmatic ontology access.

Responsibilities include:

- CURIE and identifier handling;
- label lookup;
- ancestry and relationship traversal;
- graph-oriented projections of OWL structure;
- application-facing ontology access.

OAK is an access layer over semantic sources. It is not a replacement ontology and it does not redefine Pizza semantics.

### 4. Reason and Validate

Primary concern: executable semantic interpretation and conformance checks.

The repository keeps reasoning and validation distinct:

```text
OWL / HermiT
    What follows logically from the semantic model?

SHACL / pySHACL
    Does explicit RDF data satisfy a validation profile?
```

The source-owned reasoning and validation artifacts live under `artifacts/reasoning/` and `artifacts/validation/`.

Validation profiles are additional repository-authored semantic artifacts; they are not presented as automatic translations of OWL semantics.

### 5. Publish and Govern

Primary concern: identity, publication, provenance, versioning, licensing and authority.

The project uses explicit distinctions:

```text
Ontology ≠ file
Ontology ≠ repository
Ontology version ≠ repository release
Release ≠ distribution
Identifier ≠ location
Host ≠ authority
Repository ownership ≠ ontology authority
```

`artifacts/manifest.ttl` provides a machine-readable consumer contract for source-owned semantic artifacts. Immutable Git commits or preservation releases bind that contract to a concrete source state.

The repository does not claim authority over the historical `co-ode.org` identifier space.

### 6. Project — Semantic Projections

Primary concern: implementation-oriented representations derived from semantic knowledge.

Candidate projections include JSON, JSON Schema, OpenAPI schema fragments, graph/search models and other application representations.

A projection must document which semantics are:

- preserved;
- transformed;
- approximated;
- omitted;
- introduced for implementation purposes.

A projection is not the ontology and must not silently become a competing semantic source of truth.

### 7. Experience — Ontology-Informed UX

Primary concern: user experiences that consume semantic knowledge.

Examples include:

- semantic navigation;
- ontology-informed search and filtering;
- guided forms/configuration;
- explanations of classifications or constraints;
- vocabulary-aware validation messages.

UX-specific knowledge can remain outside the ontology while retaining links to semantic entities and projections.

### 8. Execute — Executable Semantic Knowledge

Primary concern: operationalizing source-owned semantic knowledge through ESKA.

The repository boundary is explicit:

```text
pizza-ontology
    owns Pizza semantic artifacts
        ↓ immutable source contract
ESKA
    owns execution architecture
```

Pizza currently publishes semantic artifacts for seven execution modes:

```text
Ontology    → reason
Constraint  → validate
Rule        → evaluate
Decision    → decide
Calculation → calculate
Mapping     → transform
Workflow    → execute
```

ESKA represents these through reusable architecture concepts such as Semantic Capability, Execution, Result, Verification, Service, Agent, Deployment and PROV-O lineage.

Execution architecture must not become the accidental owner of domain semantics.

### 9. Architect — Semantic Modeling

Primary concern: architectural relationships among all tracks.

This track asks which concepts are:

- domain-specific to Pizza;
- specific to executable knowledge architecture;
- already owned by external standards/vocabularies;
- genuinely reusable Semantic Modeling concepts.

It should generalize only from implemented evidence.

## Cross-cutting traceability

Traceability is the connective tissue between otherwise separate layers.

A representative chain is:

```text
historical Pizza ontology/entity
    ↓
repository-owned semantic artifact
    ↓
manifest distribution
    ↓
immutable Git source identity
    ↓
ESKA Semantic Capability
    ↓
Execution
    ↓
Result
    ↓
Verification
    ↓
PROV-O lineage
    ↓
Service / Agent / application consumer
```

The chain permits each layer to evolve under its own responsibility while preserving evidence about where meaning originated and how it was transformed or executed.

## Semantic artifact families

The current source-owned artifact families expose an important architecture finding: implementation technology does not determine semantic role.

For example, both Rule and Mapping use SPARQL `CONSTRUCT`, but their contracts differ:

```text
Rule
    source semantic model
        ↓ derive
    source-domain statement

Mapping
    source semantic model
        ↓ mapping semantic model
    target semantic model
        ↓
    transformed target graph
```

Workflow differs again: BPMN owns orchestration while existing SHACL and Mapping artifacts own the semantics of its steps.

This supports modeling semantic role explicitly rather than inferring it from file format or execution engine.

## Identity and lifecycle layers

The project currently demonstrates several distinct identity/lifecycle concerns:

```text
historical ontology identity
historical ontology version
entity identity
repository release
semantic artifact identity
distribution location
immutable source commit
ESKA capability identity
execution identity
result identity
deployment identity
```

These identities may be related, but they are not interchangeable.

This is especially important for preserved or inherited ontologies where repository stewardship does not imply authority over the original ontology namespace.

## Standards ownership versus project concepts

The project should prefer established vocabularies where they already express the required semantics.

Examples already used or relevant include:

- OWL for ontology semantics;
- RDF/RDFS for graph and schema foundations;
- SHACL for validation;
- PROV-O for provenance and activity/entity/agent lineage;
- Dublin Core Terms for identifiers, sources and relations;
- DCAT where distribution metadata is appropriate;
- SKOS where concept-scheme semantics are appropriate;
- BPMN for workflow orchestration;
- DMN for decisions;
- OpenMath for mathematical expressions.

A future Semantic Modeling ontology should not duplicate these vocabularies merely to create ESKA- or Pizza-prefixed equivalents.

## Concept-harvesting matrix

The implemented work suggests the following initial classification.

| Concept | Current home | Generalization status |
|---|---|---|
| Pizza class/property/entity | Pizza Ontology | Pizza-specific |
| SHACL Pizza validation profile | `pizza-ontology` artifact | Pizza-specific semantic artifact |
| Pizza rule/decision/calculation/mapping/workflow | `pizza-ontology` artifacts | Pizza-specific semantic artifacts |
| Semantic Capability | ESKA | Executable-knowledge architecture |
| Execution / Result / Verification | ESKA + PROV-O | Executable-knowledge architecture with standards reuse |
| Knowledge Service / Agent / Deployment | ESKA extensions | Operational architecture |
| Provenance activity/entity/agent lineage | PROV-O | Standards-owned |
| Identifier/source/relation metadata | Dublin Core Terms | Standards-owned |
| Distribution metadata | DCAT candidate | Standards-owned where applicable |
| Semantic Model | Cross-cutting | Candidate reusable Semantic Modeling concept |
| Semantic Artifact | Cross-cutting | Candidate reusable Semantic Modeling concept |
| Projection | Cross-cutting | Candidate reusable Semantic Modeling concept |
| Source / target semantic-model role | Demonstrated by Mapping | Candidate reusable Semantic Modeling relation |
| Representation / distribution | Cross-cutting | Prefer standards + architecture guidance before new ontology terms |
| Authority / stewardship | Cross-cutting governance | Candidate architecture concepts; model only if executable use requires it |

This matrix is deliberately provisional. A separate Semantic Modeling ontology/repository is justified only when multiple implemented examples require shared machine-readable concepts that are not already adequately represented by existing standards.

## Repository boundaries

The current boundary can be summarized as:

```text
pizza-ontology
    concrete domain semantics
    semantic source artifacts
    preservation engineering
    publication contract

ESKA
    executable semantic capability model
    execution/result/verification architecture
    service/agent/deployment extensions
    execution provenance profile

external standards
    OWL / RDF / RDFS / SHACL / PROV-O / DCTERMS
    DCAT / SKOS where applicable
    BPMN / DMN / OpenMath for specialized semantics

future Semantic Modeling layer
    only concepts demonstrated to be reusable across these boundaries
```

## Architectural decision rule

Before introducing a new generic concept, ask:

1. Is it required by more than one implemented semantic mode or repository boundary?
2. Is the concept already adequately represented by an established standard?
3. Does machine-readable representation provide concrete executable or governance value?
4. Can it remain an architectural/documentation distinction instead of becoming an ontology term?
5. Does introducing it preserve rather than blur ownership and authority boundaries?

If these questions do not provide a strong justification, keep the concept local and provisional.

## Next architectural steps

The near-term sequence is:

1. publish the first `preservation-v0.1.0` repository baseline;
2. use this architecture as the basis for the first semantic projection;
3. define long-term preservation-safe distribution/publication locations;
4. test ontology-informed UX against the access/projection boundary;
5. revisit a separate Semantic Modeling ontology only after these implementations produce additional reusable concepts.

The purpose of the Pizza project is therefore not to build one universal semantic model. It is to provide a small, understandable domain in which semantic architecture boundaries can be made explicit, executable and testable.
